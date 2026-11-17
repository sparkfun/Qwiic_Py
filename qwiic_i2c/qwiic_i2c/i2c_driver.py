#
#-----------------------------------------------------------------------------
# i2c_driver.py
#
# Base class used to define the interface for the platform classes. 
#
# A platform class performs the following:
#
#   - Determines if the object is executing on it's desired platform
#		- Platforms are strucutre into broad classifications. For example
#			- Linux systems
#			- CircuitPython 
#
#	- Implements platform specific logic to support a given operation (I2C for now)
#
# This specific class does very little besides define the base interface  
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
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
i2c_driver
============
This is an abstract class used to define the common I2C interface for the qwiic I2C 
implementation. Platform specific drivers sub-class this object and implement the 
neccessary methods.

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""

#-----------------------------------------------------------------------------
# Platform
#
# Base class to define the interface for our platform I2C driver
#
#
class I2CDriver(object):
	"""
	I2CDriver

		Implements the interface for the I2C bus for the qwiic ecosystem.

		:return: The I2C Driver interface for the qwiic system.
		:rtype: Object
	"""

	# stubs
	name = 'qwiic I2C abstract base class'

	def __init__(self, *args, **argk):
		pass


	# A class method is used to determine if the system is executing on the desired platform

	@classmethod
	def isPlatform(cls):
		""" 
			Called to determine if the specific driver supports the current platorm

			:return: True if this platform is supported, otherwise False
			:rtype: bool

		"""
		pass

	@classmethod
	def is_platform(cls):
		""" 
			Called to determine if the specific driver supports the current platorm

			:return: True if this platform is supported, otherwise False
			:rtype: bool

		"""
		pass

	@classmethod
	def is_native_bus(cls, obj):
		"""
			Called to determine if an object is an I2C bus object native to
			this platform (eg. machine.I2C on MicroPython, busio.I2C on
			CircuitPython, smbus2.SMBus on Linux) that this driver can wrap.

			:param obj: The object to check

			:return: True if this driver can wrap the object, otherwise False
			:rtype: bool

		"""
		return False

	@classmethod
	def isNativeBus(cls, obj):
		return cls.is_native_bus(obj)

	#-------------------------------------------------------------------------
	# stubs to support Python with statements.
	#
	# Helpful for I2C interactions that require a mutex.

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		pass


	#-------------------------------------------------------------------------		
	# read Data Command

	def readWord(self, address, commandCode):
		""" 
			Called to read a word (16 bits) from a specific device.

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from, or `None` for no command

			:return: Returns the read data
			:rtype: integer - first 16 bits contain the read data. 

		"""
		return None

	def read_word(self, address, commandCode):
		""" 
			Called to read a word (16 bits) from a specific device.

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from, or `None` for no command

			:return: Returns the read data
			:rtype: integer - first 16 bits contain the read data. 

		"""
		return None

	def readByte(self, address, commandCode):
		""" 
			Called to read a byte (8 bits) from a specific device.

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from, or `None` for no command

			:return: Returns the read data
			:rtype: integer - first 8 bits contain the read data. 

		"""
		return None

	def read_byte(self, address, commandCode):
		""" 
			Called to read a byte (8 bits) from a specific device.

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from, or `None` for no command

			:return: Returns the read data
			:rtype: integer - first 8 bits contain the read data. 

		"""
		return None

	def readBlock(self, address, commandCode, nBytes):
		""" 
			Called to read a block of bytesfrom a specific device.

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from, or `None` for no command
			:param nBytes: The number of bytes to read from the device

			:return: Returns the read data as a list of integers.
			:rtype: list 

		"""
		return None
	
	def read_block(self, address, commandCode, nBytes):
		""" 
			Called to read a block of bytesfrom a specific device.

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from, or `None` for no command
			:param nBytes: The number of bytes to read from the device

			:return: Returns the read data as a list of integers.
			:rtype: list 

		"""
		return None
	
	#--------------------------------------------------------------------------	
	# write Data Commands 
	#
	# Send a command to the I2C bus for this device. 
	#
	# value = 16 bits of valid data..
	#

	def writeCommand(self, address, commandCode):
		""" 
			Called to write a command to a device. No actual data is written

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from 

			:return: None

		"""
		return None

	def write_command(self, address, commandCode):
		""" 
			Called to write a command to a device. No actual data is written

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from 

			:return: None

		"""
		return None

	def writeWord(self, address, commandCode, value):
		""" 
			Called to write a word (16 bits) to a device. 

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param value: The word (16 bits) to write to the I2C bus

			:return: None

		"""

		return None

	def write_word(self, address, commandCode, value):
		""" 
			Called to write a word (16 bits) to a device. 

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param value: The word (16 bits) to write to the I2C bus

			:return: None

		"""
		return None

	def writeByte(self, address, commandCode, value):
		""" 
			Called to write a byte (8 bits) to a device. 

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param value: The byte (8 bits) to write to the I2C bus

			:return: None

		"""

		return None

	def write_byte(self, address, commandCode, value):
		""" 
			Called to write a byte (8 bits) to a device. 

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param value: The byte (8 bits) to write to the I2C bus

			:return: None

		"""
		return None

	def writeBlock(self, address, commandCode, value):
		""" 
			Called to write a block of bytes to a device. 

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param value: A list of bytes (ints) to write on the I2C bus.

			:return: None

		"""
		pass

	def write_block(self, address, commandCode, value):
		""" 
			Called to write a block of bytes to a device. 

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param value: A list of bytes (ints) to write on the I2C bus.

			:return: None

		"""
		return None
	
	def writeReadBlock(self, address, writeBytes, readNBytes):
		""" 
			Called to write a block of bytes to a device, send no stop bit, and then read a block of bytes.

			:param address: The I2C address of the device to read from
			:param writeBytes: A list of bytes (ints) to write on the I2C bus.
			:param readNBytes: The number of bytes to read from the device

			:return: A list of bytes read from the device.
			:rtype: list

		"""
		return None
	
	def write_read_block(self, address, writeBytes, readNBytes):
		""" 
			Called to write a block of bytes to a device, send no stop bit, and then read a block of bytes.

			:param address: The I2C address of the device to read from
			:param writeBytes: A list of bytes (ints) to write on the I2C bus.
			:param readNBytes: The number of bytes to read from the device

			:return: A list of bytes read from the device.
			:rtype: list

		"""
		return None


	def isDeviceConnected(self, devAddress):
		"""
			Determines if a particular device (at the provided address)
			is connected to the bus.

			:param devAddress: The I2C address of the device to check

			:return: True if the device is connected, otherwise False.
			:rtype: bool

		"""
		return None

	def is_device_connected(self, devAddress):
		"""
			Determines if a particular device (at the provided address)
			is connected to the bus.

			:param devAddress: The I2C address of the device to check

			:return: True if the device is connected, otherwise False.
			:rtype: bool

		"""
		return None

	def ping(self, devAddress):
		"""
			Determines if a particular device (at the provided address)
			is connected to the bus.

			:param devAddress: The I2C address of the device to check

			:return: True if the device is connected, otherwise False.
			:rtype: bool

		"""
		return None

	def scan(self):
		"""
			Used to scan the I2C bus, returning a list of I2C address attached to the computer.

			:return: A list of I2C addresses. If no devices are attached, an empty list is returned.
			:rtype: list

		"""
		return None
