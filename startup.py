# /*******************************************************
#  * 
#  * Copyright (C) 2015-2016 Kyriakos Naziris <kyriakos@naziris.co.uk>
#  * This is a thesis project of University of Portsmouth.
#  *
#  * This file is part of HomeSecPi.
#  * 
#  * Feel free to use and modify the source code as long as
#  * as you give credits to the original author of the
#  * project (Kyriakos Naziris - kyriakos@naziris.co.uk).
#  *
#  *******************************************************/

from functions import status
from functions import interact 
from functions import database
from functions import keypad
from Adafruit_MCP230xx import Adafruit_MCP230XX
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from multiprocessing import Process
import MCP230xx
import os
import time
import datetime
import subprocess

mcp2 = Adafruit_MCP230XX(address = 0x20, num_gpios = 16) # MCP23017

lcd = Adafruit_CharLCDPlate()
lcd.begin(16,1)

#Initialize the output pins
sensorPin = 7
mcp2.pullup(sensorPin, 1) 
led_yellow = 1
led_green = 2
led_red = 0
buzzer = 3

#The use types the passcode, the passcode will be veriffied 
#and if its correct will disarm/arm the system
def keypads():
  last_digit = None
  while True:
    list1 = [] #Initialize an empty list
    digit = None
    while len(list1) < 4: #The length of the passcode will be 4 digits
      while digit == last_digit or digit is None: #With this loop I prevent multiple press of a number
        digit = keypad().getKey()
        if digit is None:
          last_digit = None
      list1.append(digit)
      interact().button_Pressed()
      attempt = "".join(map(str,list1))
      lcd.clear()
      lcd.message("Please type your\nPasscode: " + "*"*len(attempt))
      last_digit = digit
    print "Given Passcode:",attempt

#Verrification of the passcode
    if (attempt == passcode):
      sys_status = (database().getState())
      print "Status:", sys_status
      if (sys_status == "True"):
            #systatusem was armed, disarm it
        status().disarm()
      else:
        status().arm()
    else:
      lcd.clear()
      lcd.message("Wrong Passcode!")
      os.system('mpg321 -q /home/pi/HomeSecPi/Speech/wrongpass.mp3 &')
      database().writeLogs("Wrong passcode has been given on the keypad")
      interact().indication()
      interact().askPass()
  time.sleep(0.5)

#This function is setting the Motion Sensor's state at 0, 
#if the sensor sense movemnt, the state will change to 128 and it will trigger the alarm.
#It will give some time for the user to type the 4 digit passcode to diarm the system.
#After 10 Seconds if the password is not correct or non is given then the user will receive
#an email and a SMS to inform him about the intrudion
def pir():
  prevState = 0
  while True:
  	status = database().getState()
  	while (status == 'True'):
	    currState=mcp2.input(sensorPin)
	    if prevState==0 and currState==128:
	      image_name = interact().grabPicture()
	      print "Motion detected, armed status: " + status
	      os.system('mpg321 -q /home/pi/HomeSecPi/Speech/motiondetect.mp3 &')
	      time.sleep(30) #Time to enter the passcode 1min
	      status = database().getState()

	      if (status == 'True'):
	        print "Correct passcode not entered, emailing picture and sounding alarm."
	        #interact().takePicture(image_name)
		Process(target=interact().takePicture(image_name)).start()
	        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/alarm.mp3 &')
	        time.sleep(5)
	        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/surrender.mp3 &')
	        time.sleep(5)
	        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/alarm.mp3 &')
	        time.sleep(5)
	      # else:
	      #       if os.path.exists('/home/pi/HomeSecPi/pictures/'+image_name):
	      #         os.remove('/home/pi/HomeSecPi/pictures/'+image_name) #Deletes the taken picture in case of False-Alarm
	      #         print 'File', image_name, 'has beeen deleted'
	        
	    prevState = currState
	    time.sleep(1)

def power():
  prevMode = status().pwr_mode()
  while True:
    currMode = status().pwr_mode()
    if prevMode != currMode:
      if currMode == "External Cable Powering (EPR)":
        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/epr.mp3 &')
        lcd.clear()
        lcd.message("External Cable\nPowering (EPR)")
        time.sleep(3)
      elif currMode == "USB Cable Powering":
        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/usb.mp3 &')
        lcd.clear()
        lcd.message("USB Cable\nPowering")
        time.sleep(3)
      elif currMode == "Raspberry Pi Powering":
        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/pi.mp3 &')
        lcd.clear()
        lcd.message("Raspberry Pi\nPowering")
        time.sleep(3)
      elif currMode == "Battery Powering":
        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/battery.mp3 &')
        lcd.clear()
        lcd.message("Battery\nPowering")
        time.sleep(3)
      elif currMode == "Battery Low Powering":
        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/battery_low.mp3 &')
        lcd.clear()
        lcd.message("Battery Low\nPowering")
        time.sleep(3)
      elif currMode == "CPR Mode":
        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/cpr.mp3 &')
        lcd.clear()
        lcd.message("Running on\nCPR Mode")
        time.sleep(3)
      elif currMode == "BPR Mode":
        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/bpr.mp3 &')
        lcd.clear()
        lcd.message("Running on\nBPR Mode")
        time.sleep(3)
      else:
        os.system('mpg321 -q /home/pi/HomeSecPi/Speech/error.mp3 &')
        lcd.clear()
        lcd.message("Power Reading\nError!")
        time.sleep(3)
      print "Power source has been changed"
      database().writeLogs("Power source has been changed to " + currMode)
      interact().askPass()
    prevMode = currMode
    time.sleep(1)


try:
  #Initialize the hardware system
  attempt = ""
  passcode = database().getFourDigit()
  database().switchOff()
  interact().initialize_Output()
  mcp2.output(buzzer, 1)
  time.sleep(0.3)
  mcp2.output(buzzer, 0)
  mcp2.output(led_green, 1) # Set Green LED as High
  lcd.clear()
  ip=interact().GetInIP()
  lcd.message("IP:\n" + ip)
  time.sleep(5)
  lcd.clear()
  lcd.message("System Ready!")
  print "System Ready audio file playing!"
  os.system('mpg321 -q /home/pi/HomeSecPi/Speech/ready.mp3 &')
  time.sleep(3)
  interact().askPass()
  print "System has been initialized and its ready to use!"
  #Start the above functions simultanously, in process/threads
  Process(target=keypads).start()
  Process(target=pir).start()
  Process(target=power).start()
except KeyboardInterrupt:
    interact().clean()
    print "HomeSecPi App ended safe!"
