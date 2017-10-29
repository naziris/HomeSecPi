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


#!/usr/bin/python 
from Adafruit_MCP230xx import Adafruit_MCP230XX
import os
import urllib      # URL functions
import urllib2     # URL functions
import ftplib      #FTP Library
from urllib import urlopen
from time import sleep, strftime
import datetime
import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import RPi.GPIO as GPIO

import subprocess
from subprocess import check_output
import datetime
import time
import sqlite3
import random
import string
import hashlib #For hashed passwords
from multiprocessing import Process, Queue

#e-Mail imports
from smtplib import SMTP
from smtplib import SMTPException
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import sys
import smbus

GPIO.setwarnings(False)
#Initialization of database
db = sqlite3.connect('homesecpidb', check_same_thread=False)
cursor = db.cursor()
queue = Queue()
mcp2 = Adafruit_MCP230XX(address = 0x20, num_gpios = 16) # MCP23017
    
lcd = Adafruit_CharLCDPlate()
lcd.begin(16,1)

led_yellow = 1
led_green = 2
led_red = 0
buzzer = 3


def button_Pressed(self):
  mcp2.output(led_yellow, 1)
  mcp2.output(buzzer, 1)
  sleep(0.3)
  mcp2.output(led_yellow, 0)
  mcp2.output(buzzer, 0)

class keypad():
    # CONSTANTS   
    KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
    ]
     
    ROW         = [4,17,10,22]
    COLUMN      = [14,23,18]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
     
    def getKey(self):
         
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
         
        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                 
        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal < 0 or rowVal > 3:
            self.exit()
            return
         
        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
         
        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
 
        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                 
        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal < 0 or colVal > 2:
            self.exit()
            return
 
        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]
    
    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
   
class interact():

    def clean(self):
        GPIO.cleanup()
        exit()
             
    def initialize_Output(self):
      for k in range (4):
        mcp2.config(k, mcp2.OUTPUT) 

#Beeper beeps twice and LED flashes
    def indication(self):
      mcp2.output(buzzer, 1)
      mcp2.output(led_yellow, 1)
      sleep(0.2)
      mcp2.output(buzzer, 0)
      mcp2.output(led_yellow, 0)
      sleep(0.2)
      mcp2.output(buzzer, 1)
      mcp2.output(led_yellow, 1)
      sleep(0.2)
      mcp2.output(buzzer, 0)
      mcp2.output(led_yellow, 0)

#When a button on the keypad is pressed,
#the beeper sounds and LED flushes
    def button_Pressed(self):
      mcp2.output(buzzer, 1)
      mcp2.output(led_yellow, 1)
      sleep(0.3)
      mcp2.output(buzzer, 0)
      mcp2.output(led_yellow, 0)

    def GetInIP(self):
      output = check_output(["ip","addr","show","eth0"])
      inIP = output.split('\n')[2].strip().split(' ')[1].split('/')[0]
      return inIP

#Write on the screen
    def askPass(self):
    	lcd.clear()
    	lcd.message("Please type your\nPasscode:")

#Sends sms to the user's phone number(fetched from Database),
#using the txtlocal's API
    def sendSms(self, q, message):
      username = 'your@emailaccount.com'
      sender = 'HomeSecPi'
      hash = 'your provided hash'
      numbers = ("'{0}'".format(database().getmNumber()))
      print numbers
      test_flag = 1

      values = {'test'    : test_flag,
              'uname'   : username,
              'hash'    : hash,
              'message' : message,
              'from'    : sender,
              'selectednums' : numbers }
      url = 'http://www.txtlocal.com/sendsmspost.php'
      postdata = urllib.urlencode(values)
      req = urllib2.Request(url, postdata)

      print 'Attempt to send SMS ...'
      while True:
        try:
          urlopen('https://www.google.com')
          break
        except:
          print 'No active internet connection in order to send the SMS. Retry in 30 sec'
        time.sleep(30)
      print "Connection to TXTLocal established"
      try:
        response = urllib2.urlopen(req)
        response_url = response.geturl()
        if response_url==url:
          print 'SMS has been sent!'
      except urllib2.URLError, e:
        print 'Send failed!'
        print e.reason

#Uploading the captured image on the FTP Server
#and then returns a live link of the image
    def ftpSession(self, q, image_path, image_name):
      while True:
        try:
          urlopen('https://www.google.com')
          break
        except:
          print 'No active internet connection in order to upload the picture. Retry in 30 sec FTP'
        time.sleep(30)
      session = ftplib.FTP('ftp.yourdomain.com','username','passowrd') # Here you need to provide your ftp Host, Username and password
      session.cwd('images')                         #Give the correct folder where to store the image
      print "FTP Connection established"
      file = open(image_path,'rb')                  # file to send
      session.storbinary('STOR ' + image_name, file)     # send the file
      file.close()                                    # close file and FTP
      session.quit()
      link = 'http://www.yourdomain.com/your_directory/images_directory/' + image_name # This line here generates a link of the uploaded picture based on your webserver
      print "File has been uploaded!"
      return link

#Sends email using the google's SMTP Server.
    def sendEmail(self, q, Subject, textBody, attachment, receiver):
      """This method sends an email"""
      EMAIL_SUBJECT = Subject
      EMAIL_USERNAME = 'youremail@gmail.com' # Here you need to fill your email address, in my case it was a gmail
      EMAIL_FROM = 'HomeSecPi Project'
      EMAIL_RECEIVER = receiver
      GMAIL_SMTP = "smtp.gmail.com"
      GMAIL_SMTP_PORT = 587
      GMAIL_PASS = 'your_email_password' # And your email password
      TEXT_SUBTYPE = "plain"
         
      #Create the email.
      msg = MIMEMultipart()
      msg["Subject"] = EMAIL_SUBJECT
      msg["From"] = EMAIL_FROM
      msg["To"] = EMAIL_RECEIVER
      body = MIMEMultipart('alternative')
      body.attach(MIMEText(textBody, TEXT_SUBTYPE ))
      #Attach the message
      msg.attach(body)
      #Attach a picuture.
      if attachment != "NO":
        msg.attach(MIMEImage(file(attachment).read()))

      while True:
        try:
          urlopen('https://www.google.com')
          break
        except:
          print 'No active internet connection in order to send the e-Mail. Retry in 30 sec'
        time.sleep(30) 
      print "Connection to e-Mail server established"
      try:
        smtpObj = SMTP(GMAIL_SMTP, GMAIL_SMTP_PORT)
        #Identify yourself to GMAIL ESMTP server.
        smtpObj.ehlo()
        #Put SMTP connection in TLS mode and call ehlo again.
        smtpObj.starttls()
        smtpObj.ehlo()
        #Login to service
        smtpObj.login(user=EMAIL_USERNAME, password=GMAIL_PASS)
        #Send email
        smtpObj.sendmail(EMAIL_FROM, EMAIL_RECEIVER, msg.as_string())
        #close connection and session.
        smtpObj.quit()
        print 'e-Mail has been sent!'
      except SMTPException as error:
        print "Error: unable to send email :  {err}".format(err=error)

#Capture image using the USB PS3 Camera. The picture is captured 
#using the fswebcam and watermaked the actual date and time on it
    def grabPicture(self):
      grab_cam = subprocess.Popen("sudo fswebcam --timestamp '%d-%m-%Y %H:%M:%S (%Z)' -r 640x480 -d /dev/v4l/by-id/usb-OmniVision_Technologies__Inc._USB_Camera-B4.09.24.1-video-index0 -q /home/pi/HomeSecPi/pictures/%m-%d-%y-%H%M.jpg", shell=True)
      grab_cam.wait()
      todays_date = datetime.datetime.today()
      image_name = todays_date.strftime('%m-%d-%y-%H%M') + '.jpg'
      return image_name

#Calls the required functions to upload the captured image on the server, 
#send email and SMS to the user, to alert about the intrudion
    def takePicture(self, image_name):
      image_path = '/home/pi/HomeSecPi/pictures/' + image_name
      #interact().ftpSession(image_path, image_name)
      Process(target=interact().ftpSession, args=(queue, image_path, image_name)).start()
      rLink = 'http://www.yourdomain.com/your_directory/images_directory/' + image_name
      #interact().sendEmail("Intruder Detected", "Here is your intruder:", image_path, database().getEmail()) #Dynamic get receiver
      Process(target=interact().sendEmail, args=(queue, "Intruder Detected", "Here is your intruder:", image_path, database().getEmail())).start()
      print rLink
      #interact().sendSms("Here is your intruder: " + rLink)
      Process(target=interact().sendSms, args=(queue, "Here is your intruder: " + rLink)).start()

#These functions arm and disarm the system accordinly, 
#indicate the right indications on the LCD Screen, LEDs, 
#beeper and Voices, and at the end the ask again for the passcode
class status():

  def disarm(self):
    database().switchOff()
    lcd.clear()
    lcd.message("System Disarmed!")
    ir.indication()
    mcp2.output(led_red, 0)
    database().writeLogs("System has been Disarmed")
    os.system('mpg321 -q /home/pi/HomeSecPi/Speech/disarmed.mp3 &')
    sleep(3)
    attempt = ""
    ir.askPass()

  def arm(self):
    lcd.clear()
    lcd.message("Initializing\nSystem...")
    attempt = ""
    sleep(2)
    os.system('mpg321 -q /home/pi/HomeSecPi/Speech/systemset.mp3 &')
    sleep(5)
    lcd.clear()
    lcd.message('Please Exit Now!')
    finish_time = datetime.datetime.now() + datetime.timedelta(seconds=20)
    while datetime.datetime.now() < finish_time:
      sleep(5)
      ir.indication()

    database().switchOn()
    database().writeLogs("System has been Armed")
    lcd.clear()
    lcd.message("System Armed!")
    ir.indication()
    os.system('mpg321 -q /home/pi/HomeSecPi/Speech/armed.mp3 &')
    mcp2.output(led_red, 1)
    ir.askPass()

  #Reurns the mode of the UPiS power
  def pwr_mode(self):
    i2c = smbus.SMBus(1)
    row = i2c.read_word_data(0x6a, 0x00)
    row = "%02x "%(row,)
    output = (row[-2:]).strip()
    if (output == '1'):
      return "External Cable Powering (EPR)"
    elif (output == '2'):
      return "USB Cable Powering"
    elif (output == '3'):
      return "Raspberry Pi Powering"
    elif (output == '4'):
      return "Battery Powering"
    elif (output == '5'):
      return "Battery Low Powering"
    elif (output == '6'):
      return "CPR Mode"
    elif (output =='7'):
      return "BPR Mode"
    else:
      return "Reading Error"

class database():

#Change the password with the given one
  def changePass(self, password):
    cursor.execute('''UPDATE users SET password = ? WHERE id = 1 ''', (password,))
    db.commit()
    database().writeLogs("User's password has been changed")

#Change the 4 digit passcode with the given one
  def changeFdigit(self, digit):
    cursor.execute('''UPDATE users SET fdigit = ? WHERE id = 1 ''', (digit,))
    database().writeLogs("Four-Digit password has been changed")
    db.commit()

#Generating a random password
  def generatePass(self):
    passwd = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])
    return passwd

#Calles the generatePass function to generate a random password, 
#encrypt it and then store it into the database
  def resetPass(self):
    randomPass = database().generatePass()
    hashedPass = database().getHashed(randomPass)
    database().changePass(hashedPass)
    return randomPass

#Encrypt the password using the hash method    
  def getHashed(self, password):
    return hashlib.sha256(password).hexdigest()

#Transform the given password into hash and check
#if its the same password as the password in the database
  def checkHashedPass(self, password, digest):
    return database().getHashed(password) == digest

#Change email with the given one
  def changeEmail(self, email):
    cursor.execute('''UPDATE users SET email = ? WHERE id = 1 ''', (email,))
    db.commit()
    database().writeLogs("e-Mail has been changed")

#Change username with the given one
  def changeUsername(self, newUsername):
    cursor.execute('''UPDATE users SET Username = ? WHERE id = 1 ''', (newUsername,))
    db.commit()
    database().writeLogs("Username has been changed")

#Change Phone Number with the given one
  def changePhoneNumber(self, newPhonenumber):
    cursor.execute('''UPDATE users SET mNumber = ? WHERE id = 1 ''', (newPhonenumber,))
    db.commit()
    database().writeLogs("Phone number has been changed")

#Returns the actual state of the system (Armed or Disarmed)
  def getState(self):
    cursor.execute('''SELECT enabled FROM functions''')
    output = cursor.fetchone()
    state = output[0]
    return state

#set the enabled field in the database as True,
#Which means the system is armed
  def switchOn(self):
    cursor.execute('''UPDATE functions SET enabled = ? ''', ('True',))
    db.commit()

#set the enabled field in the database as False,
#Which means the system is disarmed
  def switchOff(self):
    cursor.execute('''UPDATE functions SET enabled = ? ''', ('False',))
    db.commit()

#Returns the user's email
  def getEmail(self):
    cursor.execute('''SELECT email FROM users WHERE id = 1''')
    userEmail = cursor.fetchone()
    return userEmail[0]

#Returns the user's phone number
  def getmNumber(self):
    cursor.execute('''SELECT mNumber FROM users WHERE id = 1''')
    mNumber = cursor.fetchone()
    return mNumber[0]

#Returns the user's email
  def getUsername(self):
    cursor.execute('''SELECT username FROM users WHERE id = 1''')
    output = cursor.fetchone()
    currentUsername = str(output[0])
    return currentUsername

#Returns the users encrypted password
  def getPassword(self):
    cursor.execute('''SELECT password FROM users WHERE id = 1''')
    output = cursor.fetchone()
    currentPassword = str(output[0])
    return currentPassword

#Returns the list of users, which for now is just one user
  def getUsers(self):
    users = {}
    cursor.execute('''SELECT username, password FROM users ''')
    all_userDetails = cursor.fetchall()
    for userDetails in all_userDetails:
       users.update({str(userDetails[0]):str(userDetails[1])})
    return users
    db.close()

#Returns the four digit passcode of the user
  def getFourDigit(self):
    cursor.execute('''SELECT fdigit FROM users WHERE id = 1''')
    output = cursor.fetchone()
    fdigit = str(output[0])
    return fdigit

  def getLogs(self):
    cursor.execute('''SELECT * FROM logs ORDER BY dateTime DESC
    LIMIT 15''')
    output = [dict(dateTime=row[0], message=row[1]) for row in cursor.fetchall()]
    return output

  def writeLogs(self, cMessage):
    DateTime = datetime.datetime.now()
    cDateTime = DateTime.strftime('%d/%m/%Y %H:%M:%S')
    cursor.execute('''INSERT INTO logs(dateTime, message) VALUES(?, ?)''',(cDateTime, cMessage))
    db.commit()


#Initialization of the classes
kp = keypad()
ir = interact()
st = status()
