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
from .i2c_driver import I2CDriver

# All supported platform module and class names
_supported_platforms = {
	"linux_i2c": "LinuxI2C",
	"circuitpython_i2c": "CircuitPythonI2C",
	"micropython_i2c": "MicroPythonI2C"
}

# List of platform drivers found on this system
_drivers = []

# Loop through all supported platform drivers, see if they're included, and
# append them to the driver list if so
for module_name, class_name in _supported_platforms.items():
	try:
		sub_module = __import__("qwiic_i2c." + module_name, None, None, [None])
		_drivers.append(getattr(sub_module, class_name))
	except:
		pass

_default_driver = None

#-------------------------------------------------
# Exported method to get the I2C driver for the execution plaform. 
#
# If no driver is found, a None value is returned
def getI2CDriver(*args, **argk):
	"""
	.. function:: getI2CDriver()

		Returns the qwiic I2C driver object for current platform.

		The first argument can be any of the following:

		- Nothing or None: returns the default I2C driver for this platform
		- A qwiic I2C driver object: returned unchanged
		- A native I2C bus object for this platform (machine.I2C or
		  machine.SoftI2C on MicroPython, busio.I2C on CircuitPython,
		  smbus2.SMBus on Linux): returns a qwiic I2C driver that uses it
		- Otherwise, all arguments are passed to the platform driver to create
		  a new bus (eg. sda and scl pins, or iBus on Linux)

		This means device drivers can pass their i2c_driver argument straight
		through, whether the user provided nothing, a qwiic I2C driver, or a
		native I2C bus object.

		:return: A qwiic I2C driver object for the current platform.
		:rtype: object

		:example:

		>>> import qwiic_i2c
		>>> i2cDriver = qwiic_i2c.getI2CDriver()
		>>> myData = i2cDriver.readByte(0x73, 0x34)

		>>> import machine
		>>> i2cDriver = qwiic_i2c.getI2CDriver(machine.SoftI2C(sda=machine.Pin(0), scl=machine.Pin(1)))
	"""
	global _default_driver

	# Treat a single None argument the same as no arguments, so device drivers
	# can pass their i2c_driver argument straight through
	if len(args) == 1 and args[0] is None and len(argk) == 0:
		args = ()

	# If a qwiic I2C driver is provided, there's nothing to do
	if len(args) == 1 and isinstance(args[0], I2CDriver) and len(argk) == 0:
		return args[0]

	# If no parameters are provided, return the default driver if we have it
	no_params = len(args) == 0 and len(argk) == 0
	if no_params and _default_driver != None:
		return _default_driver

	# Loop through all the drivers to find the one for this platform
	for driverClass in _drivers:
		if driverClass.isPlatform():
			# Found it! If a native I2C bus object was provided, wrap it,
			# otherwise create a new bus with the provided parameters
			if len(args) > 0 and driverClass.is_native_bus(args[0]):
				driver = driverClass(*args[1:], i2c_bus=args[0], **argk)
			else:
				driver = driverClass(*args, **argk)

			# If no parameters are provided, set this as the default driver
			if no_params:
				_default_driver = driver

			# And return it
			return driver

	# If we get here, we didn't find a driver for this platform
	return None

def get_i2c_driver(*args, **argk):
	"""
	.. function:: get_i2c_driver()

		Returns the qwiic I2C driver object for current platform.

		:return: A qwiic I2C driver object for the current platform.
		:rtype: object

		:example:

		>>> import qwiic_i2c
		>>> i2cDriver = qwiic_i2c.get_i2c_driver()
		>>> myData = i2cDriver.readByte(0x73, 0x34)
	"""
	return getI2CDriver(*args, **argk)

#-------------------------------------------------
# Method to determine if a particular device (at the provided address)
# is connected to the bus.
def isDeviceConnected(devAddress, *args, **argk):
	"""
	.. function:: isDeviceConnected()

		Function to determine if a particular device (at the provided address)
		is connected to the bus.

		:param devAddress: The I2C address of the device to check

		:return: True if the device is connected, otherwise False.
		:rtype: bool

	"""
	i2c = getI2CDriver(*args, **argk)

	if not i2c:
		print("Unable to load the I2C driver for this device")
		return False
	
	return i2c.isDeviceConnected(devAddress)

def is_device_connected(devAddress, *args, **argk):
	"""
	.. function:: is_device_connected()

		Function to determine if a particular device (at the provided address)
		is connected to the bus.

		:param devAddress: The I2C address of the device to check

		:return: True if the device is connected, otherwise False.
		:rtype: bool

	"""
	return isDeviceConnected(devAddress, *args, **argk)

#-------------------------------------------------
# Method to determine if a particular device (at the provided address)
# is connected to the bus.
def ping(devAddress, *args, **argk):
	"""
	.. function:: ping()

		Function to determine if a particular device (at the provided address)
		is connected to the bus.

		:param devAddress: The I2C address of the device to check

		:return: True if the device is connected, otherwise False.
		:rtype: bool

	"""
	return isDeviceConnected(devAddress, *args, **argk)
