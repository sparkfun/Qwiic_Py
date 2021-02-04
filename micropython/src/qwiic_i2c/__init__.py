# this file replaces Qwiic_Py/qwiic_i2c/qwiic_i2c/__init__.py
# so that only the pure micropython driver is included.
# this is to avoid possible issues with certain binary file transfers
# https://github.com/dhylands/rshell/issues/144

#-----------------------------------------------------------------------------
# __init__.py
#
#-----------------------------------------------------------------------------
#
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================

"""
qwiic_i2c
=========

A package to abstract the interface to the platform specific I2C bus calls. 
This package is part of the python package for SparkFun qwiic ecosystem. 

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

:example:

	>>> import qwiic_i2c
	>>> connectedDevices = i2cDriver.scan()
	>>> if myDeviceAddress in connectedDevices:
		with qwiic_i2c.getI2CDriver() as i2c:
			i2c.writeByte(myDeviceAddress, register, 0x3F)

:example:
	>>> import qwiic_i2c
	>>> if qwiic_i2c.isDeviceConnected(myDeviceAddress):
		with qwiic_i2c.getI2CDriver() as i2c:
			i2c.writeByte(myDeviceAddress, register, 0x3F)
"""
# Package to abstract the interace to the execution platforms I2C bus for QWIIC.
#
#-----------------------------------------------------------------------------
# Drivers and driver baseclass
from .i2c_driver 	import I2CDriver
from .micropython_rp2040_i2c  import MicroPythonRP2040I2C

_drivers = [MicroPythonRP2040I2C]

_theDriver = None

#-------------------------------------------------
# Exported method to get the I2C driver for the execution plaform. 
#
# If no driver is found, a None value is returned

def getI2CDriver():
	"""
	.. function:: getI2CDriver()

		Returns the qwiic I2C driver object for current platform.

		:return: A qwiic I2C driver object for the current platform.
		:rtype: object

		:example:

		>>> import qwiic_i2c
		>>> i2cDriver = qwiic_i2c.getI2CDriver()
		>>> myData = i2cDriver.readByte(0x73, 0x34)
	"""

	global _theDriver

	if _theDriver != None:
		return _theDriver

	

	for driverClass in _drivers:

		# Does this class/driverd support this platform?
		if driverClass.isPlatform():

			_theDriver = driverClass()
			# Yes - return the driver object
			return _theDriver

	return None

#-------------------------------------------------
# Method to determine if a particular device (at the provided address)
# is connected to the bus.
def isDeviceConnected(devAddress):
	"""
	.. function:: isDeviceConnected()

		Function to determine if a particular device (at the provided address)
		is connected to the bus.

		:param devAddress: The I2C address of the device to check

		:return: True if the device is connected, otherwise False.
		:rtype: bool

	"""
	i2c = getI2CDriver()

	if not i2c:
		print("Unable to load the I2C driver for this device")
		return False
	
	isConnected = False
	try:
		# Try to write a byte to the device, command 0x0
		# If it throws an I/O error - the device isn't connected
		with i2c as i2cDriver:
			i2cDriver.writeCommand(devAddress, 0x0)

			isConnected = True
	except Exception as ee:
		print("Error connecting to Device: %X, %s" % (devAddress, ee))
		pass

	return isConnected
