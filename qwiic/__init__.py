#-----------------------------------------------------------------------------
# __init__.py
#
#------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------
# Usage
#
# The package provides a wrapper/overview of classes that encapsulate a specific 
# object that represnets a qwiic enabled device.
#
# Use of the pacakge is as follows:
#
# Option 1 - import the package, create the specific class
#
#	import qwiic
#   myDevice = qwiic.MyDevice()
#
# Option 2 - Create the device object using the device address, classname or 
#			 human readable name
#
#	import qwiic
#	myDevice = qwiic.create_device("My Device Name")
#
#
#
"""
qwiic
========

The SparkFun qwiic python package aggregates all python qwiic drivers/modules to provide a single entity for qwiic within a python environment. The qwiic package delivers the high-level functionality needed to dynamically discover connected qwiic devices and construct their associated driver object.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""
#-----------------------------------------------------------------------------
from __future__ import print_function
	
import qwiic_i2c
import sys

#-----------------------------------------------------------------------------
# Objects exported from this package. 
#
# For each device imported, add it's device object is imported below
# and added to the internal device list. This is a simple method and 
# not very scalable, but works for now.  
#
# Note - we maintain a list of our driver classes. These are used in
#        some of higher level services this package provides.

_qwiic_devices = []
#
# While a basic system to manage our devices, it works for now. 

from qwiic_bme280 			import QwiicBme280
_qwiic_devices.append(QwiicBme280)

from qwiic_ccs811 			import QwiicCcs811
_qwiic_devices.append(QwiicCcs811)

from qwiic_micro_oled 		import QwiicMicroOled
_qwiic_devices.append(QwiicMicroOled)

from qwiic_proximity  		import QwiicProximity
_qwiic_devices.append(QwiicProximity)

from qwiic_scmd				import QwiicScmd
_qwiic_devices.append(QwiicScmd)

# Create a list of 
#-----------------------------------------------------------------------
# The I2C Device driver
_i2cDriver = None

def _getI2CDriver():

	global _i2cDriver

	if _i2cDriver != None:
		return _i2cDriver

	_i2cDriver = qwiic_i2c.getI2CDriver()

	if _i2cDriver == None:
		print("Unable to get the plaform I2C driver for QWIIC.")

	return _i2cDriver

#-----------------------------------------------------------------------
# I2C Bus / Device methods
#-----------------------------------------------------------------------
# 
# Cache for QWIIC device classes - determined at runtime
#
# The qwiic device classe defs are stored in a dictionary indexed by I2C 
# addresse(s) for the specific device. 

__availableDevices = {}

#-----------------------------------------------------------------------
# _getAvailableDevices()
#
# Return a dictionary that defines the available qwiic devices in the 
# package. The key is the I2C address. 
#
# Devices with multiple possible addresses have mulitple entries.
#
#

def _getAvailableDevices():

	global __availableDevices

	# do we already have these 
	if len(__availableDevices) > 0:  
		return __availableDevices

	# Loop through the device lists and add the class to the dict - address is the key.

	for deviceClass in _qwiic_devices:

		# loop over the device addresses - add name/address 
		for addr in deviceClass.available_addresses:

			__availableDevices[addr] = deviceClass


	return __availableDevices
#-----------------------------------------------------------------------
# scan()
#
# Scans the I2C bus and returns a list of addresses that have a devices connected
#
def scan():
	"""
		Used to scan the I2C bus, returning a list of I2C address attached to the computer.

		:return: A list of I2C addresses. If no devices are attached, an empty list is returned.
		:rtype: list

		:example:

		>>> import qwiic
		>>> [2]: qwiic.scan()
		[61, 91, 96, 119]
	"""

	i2cDriver = _getI2CDriver()

	if i2cDriver == None:
		return []
	
	return i2cDriver.scan()


#-----------------------------------------------------------------------
# list_devices()
#
#	Return a list of tubles that define the qwiic devices connected to the 
#   I2C bus.
#
def list_devices():
	""" 
		Returns a list of known qwiic devices connected to the I2C bus.

		:return: A list of known attached qwiic devices. If no devices are attached, 
			an empty list is returned. 
			Each element of the list a tuple that contains the following values
			(Device I2C Address, Device Name, Device Driver Class Name)
		:rtype: list

		:example:

		>>> import qwiic
		>>> qwiic.list_devices()
		[(61, 'Qwiic Micro OLED', 'QwiicMicroOled'),
 		(91, 'Qwiic CCS811', 'QwiicCcs811'),
 		(96, 'Qwiic Proximity Sensor', 'QwiicProximity'),
 		(119, 'Qwiic BME280', 'QwiicBme280')]
	"""

	# Scan the bus
	foundDevices = scan()
	if len(foundDevices) == 0:
		return []

	# What QWIIC devices do we know about -- what's defined in the package
	qwiicDefs = _getAvailableDevices()
	if len(qwiicDefs) == 0:
		return []

	foundQwiic = []
	# match scan, with definition
	for currAddress in foundDevices:

		if currAddress in qwiicDefs.keys():

			foundQwiic.append((currAddress, qwiicDefs[currAddress].device_name, qwiicDefs[currAddress].__name__))


	return foundQwiic


#-------------------
# get_devices()
#
# 	Returns a list of objects that define the qwiic devices attached to the 
#   I2C bus.
#
def get_devices():
	""" 
		Used to create device objects for all qwiic devices attached to the computer.

		:return: A list of qwiic device objects. 
		         If no qwiic devices are an empty list is returned.
		:rtype: list

		:example:

		>>> import qwiic

		>>> qwiic.get_devices()
		[<qwiic_micro_oled.qwiic_micro_oled.QwiicMicroOled at 0x76081ef0>,
 		<qwiic_ccs811.QwiicCcs811 at 0x752b78b0>,
 		<qwiic_proximity.QwiicProximity at 0x752b0e10>,
 		<qwiic_bme280.QwiicBme280 at 0x752b0a30>]

	"""

	# Scan the bus
	foundDevices = scan()
	if len(foundDevices) == 0:
		return []

	# What QWIIC devices do we know about -- what's defined in the package
	qwiicDefs = _getAvailableDevices()
	if len(qwiicDefs) == 0:
		return []

	foundQwiic = []
	# match scan, with definition
	for currAddress in foundDevices:

		if currAddress in qwiicDefs.keys():
			# Create an object and append to our found list
			# note: class defs are stored in the defs dictionary..
			foundQwiic.append(qwiicDefs[currAddress]())


	return foundQwiic

#-------------------
# create_device()
#
# 	Given the Address, Name or Clasname of a qwiic device, create the 
#	assocaited device object and return it to the caller.
#
#   The intent is for the user to call list_devices(), find a device they like AND 
# 	use this method to create the device
#
def create_device(device=None):
	""" 
		Used to create a device object for a specific qwiic device

		:param device: The I2C address, Name or Class name of the device to created.
		:return: A qwiic device object for the specified qwiic device.
		         If the specified device isn't found, None is returned. 
		:rtype: Object

		:example:

		>>> import qwiic
		>>> results = qwiic.list_devices()
		>>> print(results)
		[(61, 'Qwiic Micro OLED', 'QwiicMicroOled'), (91, 'Qwiic CCS811', 'QwiicCcs811'), 
		(96, 'Qwiic Proximity Sensor', 'QwiicProximity'), (119, 'Qwiic BME280', 'QwiicBme280')]
		
		>>> mydevice = qwiic.create_device(results[0][0])
		>>> print(mydevice)
		<qwiic_micro_oled.qwiic_micro_oled.QwiicMicroOled object at 0x751fdab0>

	"""
	if device == None:
		print("No device provided.")
		return None

	connDevices = list_devices()

	for currDev in connDevices:
		# the entries in the connDevices list are tuples, with the following values
		#   (I2C address, Device Name, Class Name)
		#
		# If the provided value is in the current device tuple, we're done
		if device in currDev:
			# we need the class definition 
			qwiicDefs = _getAvailableDevices()

			# Index using the I2C address (entry 0 of currDev)
			return qwiicDefs[currDev[0]]()

	# if we are here, we have an issue 
	print("Unabled to create requested device - is the device connected?")

	return None


