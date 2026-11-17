#-----------------------------------------------------------------------------
# linux_i2c.py
#
# Encapsulate the Linux Plaform bus interface
#------------------------------------------------------------------------
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

from .i2c_driver import I2CDriver

import sys


_PLATFORM_NAME = "Linux"

_retry_count = 3

# Supported Boards Mappings from Device Base Model Name (Or name fragment) to bus id.
_kSupportedBoards = {
	"Raspberry Pi": 1,
	"Jetson Orin Nano": 7
}

_kDefaultBoard = "Raspberry Pi"

#-----------------------------------------------------------------------------
# Internal function to identify the linux board we are running on. Returns empty string on error
def _get_board_name():
	try:
		with open('/proc/device-tree/model') as f:
			return f.read()
	except:
		#TODO: We could also have this raise/error out here if we'd prefer
		return ""

#-----------------------------------------------------------------------------
# Internal function to identify the i2c Bus ID based on platform
def _get_i2c_bus_id():
	foundBoardName = _get_board_name()

	for board in _kSupportedBoards.keys():
		if board in foundBoardName:
			return _kSupportedBoards[board]

	# TODO: we could also have this raise/error out here if we'd prefer...
	print(f"Unable to automatically detect Linux board in i2c driver. Assuming {_kDefaultBoard}...")
	return _kSupportedBoards[_kDefaultBoard]

#-----------------------------------------------------------------------------
# Internal function to connect to the systems I2C bus.
#
# Attempts to fail elegantly - often an issue with permissions with the I2C 
# bus. Users of this system should be added to the system i2c group
#
def _connectToI2CBus(iBus=1, *args, **argk):

	try:
		import smbus2
	except Exception as ee:
		print("Error: Unable to load smbus module. Unable to continue", file=sys.stderr)
		return None

	daBus = None

	error=False

	# Connect - catch errors 

	try:
		daBus =  smbus2.SMBus(iBus)
	except Exception as ee:
		if(type(ee) is IOError and ee.errno == 13):
			print("Error:\tUnable to connect to I2C bus %d: Permission denied.\n\tVerify you have permissoin to access the I2C bus" % (iBus), file=sys.stderr)
		else:
			print("Error:\tFailed to connect to I2C bus %d. Error: %s" % (iBus, str(ee)), file=sys.stderr)

		# We had an error.... 
		error=True

	# below is probably not needed, but ...
	if(not error and daBus == None):
		print("Error: Failed to connect to I2C bus %d" % (iBus), file=sys.stderr)

	return daBus

def _connect_to_i2c_bus(*args, **argk):
	return _connectToI2CBus(*args, **argk)

# notes on determining Linux platform
#
# - sys.platform == 'linux' or 'linux2', os.uname ->> res.sysname or res[0]=='Linux'
#	## Means it's a linux system - and we support it
#
# To find out a particular system:
#
# 	- Need to start looking at particular hardware classes in /proc/cpuinfo
# 
class LinuxI2C(I2CDriver):
	global _i2c_msg

	# Constructor
	name = _PLATFORM_NAME

	_i2cbus = None
	_i2c_msg = None

	def __init__(self, iBus=1, i2c_bus=None, *args, **argk):

		# Call the super class. The super calss will use default values if not
		# proviced
		I2CDriver.__init__(self)

		# Use the provided smbus2.SMBus (or compatible) object if given,
		# otherwise create one
		if i2c_bus is not None:
			self._iBus = None
			self._i2cbus = i2c_bus
		else:
			self._iBus = _get_i2c_bus_id()
			self._i2cbus = _connectToI2CBus(self._iBus)

	# Okay, are we running on a Linux system?
	@classmethod
	def isPlatform(cls):

		return sys.platform in ('linux', 'linux2')

	@classmethod
	def is_platform(cls):
		return cls.isPlatform()

	@classmethod
	def is_native_bus(cls, obj):
		# Duck typed so that smbus2.SMBus and any other object with the same
		# interface are accepted. i2c_rdwr is required for reads without a
		# command code, so the original smbus module is not supported
		for method in ("read_byte", "read_byte_data", "write_byte_data", "read_i2c_block_data", "write_i2c_block_data", "i2c_rdwr"):
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

#-------------------------------------------------------------------------	
	# read Data Command

	# Performs a general read of <nBytes> from the device at <address> without a command/register code
	def _read_no_command(self, address, nBytes):
		from smbus2 import i2c_msg

		full_read_msg = i2c_msg.read(address, nBytes)
		self._i2cbus.i2c_rdwr(full_read_msg)

		return list(full_read_msg)

	def readWord(self, address, commandCode):

		data = 0

		# add some error handling and recovery....
		for i in range(_retry_count):
			try:
				if commandCode == None:
					data = self._read_no_command(address, 2) # TODO: Check this, we may need to switch endianess
				else:
					data = self._i2cbus.read_word_data(address, commandCode)
			
				break # break if try succeeds

			except IOError as ioErr:
				# we had an error - let's try again
				if i == _retry_count-1:
					raise ioErr
				pass

		return data

	def read_word(self, address, commandCode):
		return self.readWord(address, commandCode)

	def readByte(self, address, commandCode = None):
		data = 0
		for i in range(_retry_count):
			try:
				if commandCode == None:
					data = self._i2cbus.read_byte(address)
				elif commandCode != None:
					data = self._i2cbus.read_byte_data(address, commandCode)
			
				break # break if try succeeds

			except IOError as ioErr:
				# we had an error - let's try again
				if i == _retry_count-1:
					raise ioErr
				pass

		return data

	def read_byte(self, address, commandCode = None):
		return self.readByte(address, commandCode)

	def readBlock(self, address, commandCode, nBytes):
		data = 0
		for i in range(_retry_count):
			try:
				if commandCode == None:
					data = self._read_no_command(address, nBytes)
				else:
					data = self._i2cbus.read_i2c_block_data(address, commandCode, nBytes)
			
				break # break if try succeeds

			except IOError as ioErr:
				# we had an error - let's try again
				if i == _retry_count-1:
					raise ioErr
				pass

		return data

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

		return self._i2cbus.write_byte(address, commandCode)

	def write_command(self, address, commandCode):
		return self.writeCommand(address, commandCode)

	def writeWord(self, address, commandCode, value):

		return self._i2cbus.write_word_data(address, commandCode, value)

	def write_word(self, address, commandCode, value):
		return self.writeWord(address, commandCode, value)

	def writeByte(self, address, commandCode, value):

		return self._i2cbus.write_byte_data(address, commandCode, value)

	def write_byte(self, address, commandCode, value):
		return self.writeByte(address, commandCode, value)

	def writeBlock(self, address, commandCode, value):

		# if value is a bytearray - convert to list of ints (it's what 
		# required by this call)
		tmpVal = list(value) if type(value) == bytearray else value
		self._i2cbus.write_i2c_block_data(address, commandCode, tmpVal)

	def write_block(self, address, commandCode, value):
		return self.writeBlock(address, commandCode, value)

	def writeReadBlock(self, address, writeBytes, readNBytes):
		return self.__i2c_rdwr__(address, writeBytes, readNBytes)
	
	def write_read_block(self, address, writeBytes, readNBytes):
		return self.writeReadBlock(address, writeBytes, readNBytes)

	def isDeviceConnected(self, devAddress):
		isConnected = False
		try:
			# Try to write nothing to the device
			# If it throws an I/O error - the device isn't connected

			if "Jetson Orin Nano" in _get_board_name():
				self._i2cbus.read_byte(devAddress)
			else:
				self._i2cbus.write_quick(devAddress)

			isConnected = True
		except:
			pass
		
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
		foundDevices = []
		# Loop over the list of legal addresses (0x08 - 0x77)
		for currAddress in range(0x08, 0x78):
			if self.ping(currAddress) == True:
				foundDevices.append(currAddress)
		return foundDevices

	#-----------------------------------------------------------------------
	# Custom method for reading +8-bit register using `i2c_msg` from `smbus2`
	#
	def __i2c_rdwr__(self, address, write_message, read_nbytes):
		"""
		Custom method used for 16-bit (or greater) register reads
		:param address: 7-bit address
		:param write_message: list with register(s) to read
		:param read_nbytes: number of bytes to be read

		:return: response of read transaction
		:rtype: list
		"""
		global _i2c_msg
		
		# Loads i2c_msg if not previously loaded
		if _i2c_msg == None:
			from smbus2 import i2c_msg
			_i2c_msg = i2c_msg
        
		# Sets up write and read transactions for reading a register
		write = _i2c_msg.write(address, write_message)
		read = _i2c_msg.read(address, read_nbytes)

		# Read Register
		for i in range(_retry_count):
			try:
				self._i2cbus.i2c_rdwr(write, read)
			
				break # break if try succeeds

			except IOError as ioErr:
				# we had an error - let's try again
				if i == _retry_count-1:
					raise ioErr
				pass
		
		# Return read transaction (list)
		# Note - To retreive values, list the return: list(read)
		return read
