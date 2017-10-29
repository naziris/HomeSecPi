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

import smbus
i2c = smbus.SMBus(1)

#Reurns the mode of the UPiS power
def pwr_mode():
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

#Returns the battary voltage 
def bat_level():
	row = i2c.read_word_data(0x6a, 0x01)
	row = "%02x "%(row,)
	return (float(row) / 100)

#Returns the RPi voltage 
def rpi_level():
	row = i2c.read_word_data(0x6a, 0x03)
	row = "%02x "%(row,)
	return (float(row) / 100)

#Returns the USB voltage 
def usb_level():
	row = i2c.read_word_data(0x6a, 0x05)
	row = "%02x "%(row,)
	return (float(row) / 100)

#Returns the external EPR voltage 
def epr_level():
	row = i2c.read_word_data(0x6a, 0x07)
	row = "%02x "%(row,)
	return (float(row) / 100)

#Returns the UPiS currnet in mA 
def crn_level():
	row = i2c.read_word_data(0x6a, 0x09)
	row = "%02x "%(row,)
	return row

#Reurns the current version of the UPiS
def version():
	row = i2c.read_word_data(0x6b, 0x00)
	row = "%02x "%(row,)
	return float(int(row, 16)) / 100 # int(row,16) is converting the hex string into an integer
