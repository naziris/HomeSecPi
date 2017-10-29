# /*******************************************************
#  * 
#  * Copyright (C) 2015-2016 Kyriakos Naziris <kyriakos@naziris.co.uk>
#  * This is a thesis project of University of Portsmouth.
#  *
#  * This file is part of HomeSecPi.
#  * 
#  * Feel free to use and modify the source code as long as
#  * as you give credit to the original author of the
#  * project (Kyriakos Naziris - kyriakos@naziris.co.uk).
#  *
#  *******************************************************/

import flask, flask.views
from flask import jsonify, request, Response
from werkzeug.contrib.fixers import ProxyFix
from camera_pi import Camera
import functools
from subprocess import check_output
import os
from functions import status, interact, database
import urllib
import re
from time import sleep

app = flask.Flask(__name__)
app.secret_key = 'YourSecurityKey'
users = database().getUsers()


class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('welcome.html')

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("A login is required to see the page!")
            return flask.redirect(flask.url_for('login'))
    return wrapper

class Tongles(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('tongles.html', status=getStatus(), temp=GetTemp(), 
            inIP=GetInIP(), exIP=GetExIP(), pmode=status().pwr_mode())
    def post(self):
        formType = flask.request.form.get('formType')
        digitPass = ""
        if formType == "digitPassword" or "shutdown":
            required = ['firstdigit', 'seconddigit', 'thirddigit', 'fourthdigit']
            for r in required:
                    digitPass += flask.request.form.get(r)
            if str(digitPass) == str(database().getFourDigit()):
                state = database().getState()
                if formType == "shutdown":
                    if state == "True":
                        flask.flash("Disarm system before shutting down!")
                        return flask.redirect(flask.url_for('tongles'))
                    else:
                        print "Shutting Down..."
                        database().writeLogs("System has been shutted down")
                        shutdown()
                elif formType == "digitPassword":
                    if state == "True":
                        status().disarm()
                    else:
                        status().arm()
                else:
                    flask.flash("Something went totally wrong here, please try again!")
                    return flask.redirect(flask.url_for('tongles'))
            else:
                flask.flash("Incorect Password, please try again!")
            return flask.redirect(flask.url_for('tongles'))

class Gallery(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('gallery.html')

class Logs(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('logs.html', records=database().getLogs())

class Stream(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('stream.html')

class Admin(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('admin.html')
    def post(self):
        global users
        formType = flask.request.form.get('formType')

        if formType == "changePassword":
            if 'password' not in flask.request.form:
                flask.flash("Something went totally wrong here. Please try to change your password again!")
                return flask.redirect(flask.url_for('admin'))
            newPassword = database().getHashed(flask.request.form.get('password'))
            currentPassword = database().getPassword()
            if newPassword == currentPassword:
                flask.flash("The password you entered is the same as the current one. Please use a different password and try again!")
                return flask.redirect(flask.url_for('admin'))
            else:
                database().changePass(newPassword)
        elif formType == "editUsername":
            if 'username' not in flask.request.form:
                flask.flash("Something went totally wrong here. Please try to change your password again!")
                return flask.redirect(flask.url_for('admin'))
            newUsername = flask.request.form.get('username')
            currentUsername = database().getUsername()
            if newUsername == currentUsername:
                flask.flash("The username you entered is the same as the current one. Please use a different username and try again!")
                return flask.redirect(flask.url_for('admin'))
            else:
                database().changeUsername(newUsername)
        elif formType == "editemail":
            if 'email' not in flask.request.form:
                flask.flash("Something went totally wrong here. Please try to change your e-Mail address again!")
                return flask.redirect(flask.url_for('admin'))
            newemail = flask.request.form.get('email')
            currentemail = database().getEmail()
            if newemail == currentemail:
                flask.flash("The e-Mail address you entered is the same as the current one. Please use a different one and try again!")
                return flask.redirect(flask.url_for('admin'))
            else:
                database().changeEmail(newemail)
        elif formType == "editphoneNumber":
            if 'phoneNumber' not in flask.request.form:
                flask.flash("Something went totally wrong here. Please try to change your phone number again!")
                return flask.redirect(flask.url_for('admin'))
            getPhonenumber = flask.request.form.get('phoneNumber')
            country = flask.request.form.get('countrySelectBox')
            if country == 'GB':
                newPhonenumber = '44{}'.format(getPhonenumber[1:] if getPhonenumber.startswith('0') else getPhonenumber)
            elif country == 'US':
                newPhonenumber = '1{}'.format(getPhonenumber)
            currentPhonenumber = database().getmNumber()
            if newPhonenumber == currentPhonenumber:
                flask.flash("The phone number you entered is the same as the current one. Please use a different one and try again!")
                return flask.redirect(flask.url_for('admin'))
            database().changePhoneNumber(newPhonenumber)
        elif formType == "editDigitPassword":
            if 'currentPassword' not in flask.request.form:
                flask.flash("Something went totally wrong here. Please try to change your four-digit password again!")
                return flask.redirect(flask.url_for('admin'))
            newPassword = flask.request.form.get('newPassword')
            currentPassword = database().getFourDigit()
            if currentPassword != flask.request.form.get('currentPassword'):
                flask.flash("incorrect current four-digit password, please try again")
                return flask.redirect(flask.url_for('admin'))
            elif newPassword == currentPassword:
                flask.flash("The password you entered is the same as the current one. Please use a different password and try again!")
                return flask.redirect(flask.url_for('admin'))
            else:
                database().changeFdigit(newPassword)
        else:
            flask.flash("Something went totally wrong here. Please try to change the preffered details again")
            return flask.render_template('admin.html')
        flask.flash("Your settings have been  modified succsessfuly. In order your changes to be effectful, you will be logged out in a few seconds!")
        users = database().getUsers()
        flask.session.pop('username', None)
        sleep (1)
        flask.flash("You've been succsessfuly logged out!")
        return flask.redirect(flask.url_for('index'))

class Login(flask.views.MethodView):
    def get(self):
        return flask.render_template('login.html')

    def post(self):
        global users
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            database().writeLogs("User has been succsessfuly logged out!")
            flask.flash("You've been succsessfuly logged out!")
            return flask.redirect(flask.url_for('login'))
        if 'reset' in flask.request.form:
            Username = flask.request.form.get('username')
            if 'username' not in flask.request.form or (database().getUsername() != Username ): #Check That one
                flask.flash("Something went totally wrong here. Please to check your username and try again!")
                return flask.redirect(flask.url_for('login'))
            newPassword = database().resetPass()
            emailBody = "You recently asked to reset your password, your new password is: " + newPassword
            interact().sendEmail("Your new Password!", emailBody, "NO", database().getEmail())
            users = database().getUsers()
            flask.flash("Your password has been reset. You'll receive an email shortly with your new password")
            # users = database().getUsers()
            return flask.redirect(flask.url_for('login'))
        required = ['username', 'passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('login'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        print database().checkHashedPass(passwd, database().getPassword()) 
        if username in users and (database().checkHashedPass(passwd, database().getPassword())) == True :
            flask.session['username'] = username
            database().writeLogs("User has been succsessfuly logged in!")
            flask.flash("Login Succsessful!")
            flask.session['userEmail'] = database().getEmail()
            flask.session['mNumber'] = database().getmNumber()
            return flask.redirect(flask.url_for('admin'))
        else:
            flask.flash("Username doesn't exist or incorrect password")
        return flask.redirect(flask.url_for('login'))

app.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=["GET", "POST"])

app.add_url_rule('/tongles/',
                 view_func=Tongles.as_view('tongles'),
                 methods=['GET', 'POST'])

app.add_url_rule('/gallery/',
                 view_func=Gallery.as_view('gallery'),
                 methods=['GET', 'POST'])

app.add_url_rule('/login/',
                 view_func=Login.as_view('login'),
                 methods=['GET', 'POST'])

app.add_url_rule('/stream/',
                 view_func=Stream.as_view('stream'),
                 methods=['GET', 'POST'])

app.add_url_rule('/logs/',
                 view_func=Logs.as_view('logs'),
                 methods=['GET', 'POST'])

app.add_url_rule('/admin/',
                 view_func=Admin.as_view('admin'),
                 methods=['GET', 'POST'])
    
@app.route("/syStatus")
def getStatus():
    state = database().getState()
    if state == "True":
        status = "Armed"
    else:
        status = "Disarmed"
    return status

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/picture")
def picture():
    link = interact().ftpSession(None, '/home/pi/HomeSecPi/pictures/' + interact().grabPicture(), interact().grabPicture())
    return  jsonify(pictureLink=link)

def shutdown():
    os.system("sudo shutdown -h now")
    return ""

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#System details functions start here -->

def GetTemp():
    #from subprocess import check_output
    output = check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
    temp = float(output.split('=')[1][:-3])
    return temp

def GetInIP():
    output = check_output(["ip","addr","show","eth0"])
    inIP = output.split('\n')[2].strip().split(' ')[1].split('/')[0]
    return inIP

def GetExIP():
    dyndnsRespond = urllib.urlopen("http://checkip.dyndns.org/").read()
    grabIP = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', dyndnsRespond)
    exIP = grabIP[0]
    return exIP

#System details functions ends here <--

# run the webserver on port 68, requires sudo
app.wsgi_app = ProxyFix(app.wsgi_app)
try:
    if __name__ == "__main__":
        app.debug = True
        app.run(host='0.0.0.0', port=8068)
except KeyboardInterrupt:
    interact().clean()
    print "Flask App ended safe!"


