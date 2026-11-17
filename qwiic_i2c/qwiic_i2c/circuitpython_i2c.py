#-----------------------------------------------------------------------------
# cirucitpy_i2c.py
#
# Encapsulate CircuitPython I2C interface
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

# Import items from __future__ ? 
#  NO: There is no future with cicuit py

from .i2c_driver import I2CDriver

import sys
import os

_PLATFORM_NAME = "CircuitPython"

#-----------------------------------------------------------------------------
# Internal function to connect to the systems I2C bus.
#
# Attempts to fail elegantly. Put this in a central place to support 
# error handling  -- especially on non-circuitpy platforms
#
def _connectToI2CBus(sda=None, scl=None, freq=100000, *args, **argk):

	try:
		import board
		import busio
	except Exception as ee:
		print("Error: Unable to load the I2C subsystem modules")
		return None

	daBus = None

	error=False

	# Connect - catch errors 

	try:
		if sda != None and scl != None:
			daBus = busio.I2C(scl, sda, frequency=freq)
		elif hasattr(board, "STEMMA_I2C"):
			daBus = board.STEMMA_I2C()
		else:
			daBus = busio.I2C(board.SCL, board.SDA, frequency=freq)
	except Exception as ee:
		if type(ee) is RuntimeError:
			print("Error:\tUnable to connect to I2C bus. %s" % (ee))
			print("\t\tEnsure a board is connected to the %s board." % (os.uname().machine))			
		else:
			print("Error:\tFailed to connect to I2C bus. Error: %s" % (ee))

		# We had an error.... 
		error=True

	# below is probably not needed, but ...
	if(not error and daBus == None):
		print("Error: Failed to connect to I2C bus. Unable to continue")

	return daBus

def _connect_to_i2c_bus(*args, **argk):
	return _connectToI2CBus(*args, **argk)

# notes on determining CirPy platform
#
# - os.uname().sysname == samd*
#
# 
class CircuitPythonI2C(I2CDriver):

	# Constructor
	name = _PLATFORM_NAME

	_i2cbus = None

	def __init__(self, sda=None, scl=None, freq=100000, i2c_bus=None, *args, **argk):

		# Call the super class. The super calss will use default values if not
		# proviced
		I2CDriver.__init__(self)

		self._sda = sda
		self._scl = scl
		self._freq = freq

		# Use the provided busio.I2C (or compatible) object if given, otherwise
		# create one
		if i2c_bus is not None:
			self._i2cbus = i2c_bus
		else:
			self._i2cbus = _connectToI2CBus(sda=self._sda, scl=self._scl, freq=self._freq)

	# Okay, are we running on a circuit py system?
	@classmethod
	def isPlatform(cls):
		try:
			return 'circuitpython' in sys.implementation
		except:
			return False

	@classmethod
	def is_platform(cls):
		return cls.isPlatform()

	@classmethod
	def is_native_bus(cls, obj):
		# Duck typed so that busio.I2C, bitbangio.I2C, board.I2C(), and any other
		# object with the same interface are all accepted. Checking methods also
		# keeps board pins (eg. board.SDA) from being mistaken for a bus
		for method in ("try_lock", "unlock", "scan", "writeto", "readfrom_into", "writeto_then_readfrom"):
			if not hasattr(obj, method):
				return False
		return True

#-------------------------------------------------------------------------		
	# General get attribute method
	#
	# Used to intercept getting the I2C bus object - so we can perform a lazy
	# connect ....
	#
	def __getattr__(self, name):

		if(name == "i2cbus"):
			return self._i2cbus

		else:
			# Note - we call __getattribute__ to the super class (object).
			return super(I2CDriver, self).__getattribute__(name)

	#-------------------------------------------------------------------------
	# General set attribute method
	#
	# Basically implemented to make the i2cbus attribute readonly to users 
	# of this class. 
	#
	def __setattr__(self, name, value):

		if(name != "i2cbus"):
			super(I2CDriver, self).__setattr__(name, value)

	#----------------------------------------------------------
	# read Data Command

	def readWord(self, address, commandCode):
		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")

		buffer = bytearray(2)

		try:
			if (commandCode == None):
				self._i2cbus.readfrom_into(address, buffer)
			else:
				self._i2cbus.writeto_then_readfrom(address, bytes([commandCode]), buffer)
		except Exception as e:
			self._i2cbus.unlock()
			raise e
		else:
			self._i2cbus.unlock()

		# build and return a word
		return (buffer[1] << 8 ) | buffer[0]

	def read_word(self, address, commandCode):
		return self.readWord(address, commandCode)

	#----------------------------------------------------------
	def readByte(self, address, commandCode = None):
		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")

		buffer = bytearray(1)

		try:
			if (commandCode == None):
				self._i2cbus.readfrom_into(address, buffer)
			else:
				self._i2cbus.writeto_then_readfrom(address, bytes([commandCode]), buffer)
		except Exception as e:
			self._i2cbus.unlock()
			raise e
		else:
			self._i2cbus.unlock()

		return buffer[0]

	def read_byte(self, address, commandCode = None):
		return self.readByte(address, commandCode)

	#----------------------------------------------------------
	def readBlock(self, address, commandCode, nBytes):
		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")

		buffer = bytearray(nBytes)

		try:
			if (commandCode == None):
				self._i2cbus.readfrom_into(address, buffer)
			else:
				self._i2cbus.writeto_then_readfrom(address, bytes([commandCode]), buffer)
		except Exception as e:
			self._i2cbus.unlock()
			raise e
		else:
			self._i2cbus.unlock()

		return list(buffer)

	def read_block(self, address, commandCode, nBytes):
		return self.readBlock(address, commandCode, nBytes)

	#--------------------------------------------------------------------------	
	# write Data Commands 
	#
	# Send a command to the I2C bus for this device. 
	#
	# value = 16 bits of valid data..
	#

	def writeCommand(self, address, commandCode):
		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")
		
		try:
			self._i2cbus.writeto(address, bytes([commandCode]))
		except Exception as e:
			self._i2cbus.unlock()
			raise e
		else:
			self._i2cbus.unlock()

	def write_command(self, address, commandCode):
		return self.writeCommand(address, commandCode)

	#----------------------------------------------------------
	def writeWord(self, address, commandCode, value):
		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")

		buffer = [0, 0]
		buffer[0] = value & 0xFF
		buffer[1] = (value >> 8) & 0xFF

		try:
			self._i2cbus.writeto(address, bytes([commandCode] + buffer))
		except Exception as e:
			self._i2cbus.unlock()
			raise e
		else:
			self._i2cbus.unlock()

	def write_word(self, address, commandCode, value):
		return self.writeWord(address, commandCode, value)

	#----------------------------------------------------------
	def writeByte(self, address, commandCode, value):
		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")
		
		try:
			self._i2cbus.writeto(address, bytes([commandCode] + [value]))
		except Exception as e:
			self._i2cbus.unlock()
			raise e
		else:
			self._i2cbus.unlock()

	def write_byte(self, address, commandCode, value):
		return self.writeByte(address, commandCode, value)

	#----------------------------------------------------------
	def writeBlock(self, address, commandCode, value):
		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")
		
		try:
			self._i2cbus.writeto(address, bytes([commandCode] + value))
		except Exception as e:
			self._i2cbus.unlock()
			raise e
		else:
			self._i2cbus.unlock()

	def write_block(self, address, commandCode, value):
		return self.writeBlock(address, commandCode, value)

	def writeReadBlock(self, address, writeBytes, readNBytes):
		read_buffer = bytearray(readNBytes)

		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")
		
		try:
			self._i2cbus.writeto_then_readfrom(address, bytes(writeBytes), read_buffer)
		except Exception as e:
			self._i2cbus.unlock()
			raise e
		else:
			self._i2cbus.unlock()

		return list(read_buffer)
		
	
	def write_read_block(self, address, writeBytes, readNBytes):
		return self.writeReadBlock(address, writeBytes, readNBytes)

	def isDeviceConnected(self, devAddress):
		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")
		
		isConnected = False
		try:
			# Try to write nothing to the device
			# If it throws an I/O error - the device isn't connected
			self._i2cbus.writeto(devAddress, bytearray())
			isConnected = True
		except:
				try:
					# Some platforms (e.g. ESP32) don't like writing an empty bytearray
					# So we will try another connection test as well:
					buff = bytearray(1)
					self._i2cbus.readfrom_into(devAddress, buff)
					isConnected = True
				except:
					pass
		finally:
			self._i2cbus.unlock()

		return isConnected

	def is_device_connected(self, devAddress):
		return self.isDeviceConnected(devAddress)

	def ping(self, devAddress):
		return self.isDeviceConnected(devAddress)

	#-----------------------------------------------------------------------
	# scan()
	#
	# Scans the I2C bus and returns a list of addresses that have a devices connected
	#
	def scan(self):
		""" Returns a list of addresses for the devices connected to the I2C bus."""
		if not self._i2cbus.try_lock():
			raise Exception("Unable to lock I2C bus")
		
		try:
			devices = self._i2cbus.scan()
		except Exception as e:
			self._i2cbus.unlock()
			raise e
		else:
			self._i2cbus.unlock()
		
		return devices
	