#-----------------------------------------------------------------------------
# qwiic_adxl313.py
#
# Python library for the SparkFun Triple Axis Accelerometer Breakout - ADXL313 (QWIIC).
#
# https://www.sparkfun.com/products/17241
#
#------------------------------------------------------------------------
#
# Written by SparkFun Electronics, October 2020
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:# www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2020 SparkFun Electronics
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
qwiic_adxl313
============
Python module for the [SparkFun Triple Axis Accelerometer Breakout - ADXL313 (QWIIC)](https://www.sparkfun.com/products/17241)

This python package is a port of the existing [SparkFun ADXL313 Arduino Library](https://github.com/sparkfun/SparkFun_ADXL313_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""
#-----------------------------------------------------------------------------

import qwiic_i2c

__version__ = "3.0.0"

# Define the device name and I2C addresses. These are set in the class defintion 
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at 
# runtine
#
# The name of this device 
_DEFAULT_NAME = "Qwiic ADXL313"

# Some devices have multiple availabele addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the 
# device.
_AVAILABLE_I2C_ADDRESS = [0x1D, 0x53]

# define our valid chip IDs
_VALID_CHIP_IDS = [0xCB]

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported 
# from this module.

class QwiicADXL313(object):
	"""
	QwiicADXL313

		:param address: The I2C address to use for the device. 
						If not provided, the default address is used.
		:param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.
		:return: The ADXL313 device object.
		:rtype: Object
	"""
	# Constructor
	device_name = _DEFAULT_NAME
	available_addresses = _AVAILABLE_I2C_ADDRESS

	ADXL313_TO_READ = 6      # Number of Bytes Read - Two Bytes Per Axis

	#/////////////////////////////////////////
	## ADXL313 Registers //
    #/////////////////////////////////////////
	ADXL313_DEVID_0 = 0x00
	ADXL313_DEVID_1 = 0x01
	ADXL313_PARTID = 0x02
	ADXL313_REVID = 0x03
	ADXL313_XID = 0x04
	ADXL313_SOFT_RESET = 0x18
	ADXL313_OFSX = 0x1E
	ADXL313_OFSY = 0x1F
	ADXL313_OFSZ = 0x20
	ADXL313_THRESH_ACT = 0x24
	ADXL313_THRESH_INACT = 0x25
	ADXL313_TIME_INACT = 0x26
	ADXL313_ACT_INACT_CTL = 0x27
	ADXL313_BW_RATE = 0x2C
	ADXL313_POWER_CTL = 0x2D
	ADXL313_INT_ENABLE = 0x2E
	ADXL313_INT_MAP = 0x2F
	ADXL313_INT_SOURCE = 0x30
	ADXL313_DATA_FORMAT = 0x31
	ADXL313_DATA_X0 = 0x32
	ADXL313_DATA_X1 = 0x33
	ADXL313_DATA_Y0 = 0x34
	ADXL313_DATA_Y1 = 0x35
	ADXL313_DATA_Z0 = 0x36
	ADXL313_DATA_Z1 = 0x37
	ADXL313_FIFO_CTL = 0x38
	ADXL313_FIFO_STATUS = 0x39

	#////////////////////////////////
	## ADXL313 Responses //
	#////////////////////////////////
	ADXL313_DEVID_0_RSP_EXPECTED = 0xAD
	ADXL313_DEVID_1_RSP_EXPECTED = 0x1D
	ADXL313_PARTID_RSP_EXPECTED = 0xCB

	ADXL313_I2C_ADDRESS_DEFAULT = 0x1D
	ADXL313_I2C_ADDRESS_ALT = 0x53
	ADXL313_CS_PIN_DEFAULT = 10

 	#/************************** INTERRUPT PINS **************************/
	ADXL313_INT1_PIN = 0x00		# INT1: 0
	ADXL313_INT2_PIN = 0x01		# INT2: 1


 	#/********************** INTERRUPT BIT POSITION **********************/
	ADXL313_INT_DATA_READY_BIT = 0x07
	ADXL313_INT_ACTIVITY_BIT = 0x04
	ADXL313_INT_INACTIVITY_BIT = 0x03
	ADXL313_INT_WATERMARK_BIT = 0x01
	ADXL313_INT_OVERRUN_BIT = 0x00

	ADXL313_DATA_READY = 0x07
	ADXL313_ACTIVITY = 0x04
	ADXL313_INACTIVITY = 0x03
	ADXL313_WATERMARK = 0x01
	ADXL313_OVERRUN	= 0x00

 	#/********************** RANGE SETTINGS OPTIONS **********************/
	ADXL313_RANGE_05_G = 0x00 # 0-0.5G
	ADXL313_RANGE_1_G = 0x01 # 0-1G
	ADXL313_RANGE_2_G = 0x02 # 0-2G
	ADXL313_RANGE_4_G = 0x03 # 0-4G

 	#/********************** POWER_CTL BIT POSITION **********************/
	ADXL313_I2C_DISABLE_BIT = 0x06
	ADXL313_LINK_BIT = 0x05
	ADXL313_AUTOSLEEP_BIT = 0x04
	ADXL313_MEASURE_BIT = 0x03
	ADXL313_SLEEP_BIT = 0x02

 	#/********************** BANDWIDTH RATE CODES (HZ) *******************/
	ADXL313_BW_1600 = 0xF			# 1111		IDD = 170uA
	ADXL313_BW_800 = 0xE			# 1110		IDD = 115uA
	ADXL313_BW_400 = 0xD			# 1101		IDD = 170uA
	ADXL313_BW_200 = 0xC			# 1100		IDD = 170uA (115 low power)
	ADXL313_BW_100 = 0xB			# 1011		IDD = 170uA (82 low power)
	ADXL313_BW_50 = 0xA			# 1010		IDD = 170uA (64 in low power)
	ADXL313_BW_25 = 0x9			# 1001		IDD = 115uA (57 in low power)
	ADXL313_BW_12_5 = 0x8			# 1000		IDD = 82uA (50 in low power)
	ADXL313_BW_6_25 = 0x7			# 0111		IDD = 65uA (43 in low power)
	ADXL313_BW_3_125 = 0x6			# 0110		IDD = 57uA

 	#/********************** FIFO MODE OPTIONS ***************************/
	ADXL313_FIFO_MODE_BYPASS = 0x00
	ADXL313_FIFO_MODE_FIFO = 0x01
	ADXL313_FIFO_MODE_STREAM = 0x02
	ADXL313_FIFO_MODE_TRIGGER = 0x03

 	#/****************************** ERRORS ******************************/
	ADXL313_OK = 1		# No Error
	ADXL313_ERROR = 0		# Error Exists

	ADXL313_NO_ERROR = 0		# Initial State
	ADXL313_READ_ERROR = 1		# Accelerometer Reading Error
	ADXL313_BAD_ARG = 2		# Bad Argument

 	#/********************** INTERRUPT STATUSES **************************/
	ADXL313_INTSOURCE_DATAREADY = 0
	ADXL313_INTSOURCE_ACTIVITY = 0
	ADXL313_INTSOURCE_INACTIVITY = 0
	ADXL313_INTSOURCE_WATERMARK = 0
	ADXL313_INTSOURCE_OVERRUN = 0

	#/***************** x,y,z variables (raw values) *********************/
	x = 0
	y = 0
	z = 0

	# Constructor
	def __init__(self, address=None, i2c_bus=None):

		# The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
		address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
		# Did the user specify an I2C address?
		self.address = address if address != None else self.available_addresses[0]

		# Use the given I2C bus, or the platform's default bus
		self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

	# ----------------------------------
	# is_connected()
	#
	# Is an actual board connected to our system?

	def is_connected(self):
		""" 
			Determine if a device is connected to the system.

			:return: True if the device is connected, otherwise False.
			:rtype: bool
		"""
		return self._i2c.is_device_connected(self.address)

	# ----------------------------------
	# begin()
	#
	# Initialize the system/validate the board. 
	def begin(self):
		""" 
			Initialize the operation of the module

			:return: Returns true of the initializtion was successful, otherwise False.
			:rtype: bool
		"""
		# No device at this address
		if not self.is_connected():
			return False

		# are we who we need to be?
		chip_id = self._i2c.read_byte(self.address, self.ADXL313_PARTID)
		if not chip_id in _VALID_CHIP_IDS:
			return False

		return True

	# ----------------------------------
	# standby()
	#
	# clears the measure bit, putting decive in standby mode, ready for configuration
	def standby(self):
		""" 
			clears the measure bit, putting decive in standby mode, ready for configuration

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_POWER_CTL, self.ADXL313_MEASURE_BIT, False)

	# ----------------------------------
	# measure_mode_on()
	#
	# sets the measure bit, putting decive in measure mode, ready for reading data
	def measure_mode_on(self):
		""" 
			sets the measure bit, putting decive in measure mode, ready for reading data

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_POWER_CTL, self.ADXL313_MEASURE_BIT, True)

	# ----------------------------------
	# data_ready()
	#
	# Reads INT Source register, returns dataready bit status (0 or 1)
	def data_ready(self):
		""" 
			Reads INT Source register, returns dataready bit status (0 or 1)

			:return: Status of dataready bit within the int source register
			:rtype: bool
		"""
		return self.get_register_bit(self.ADXL313_INT_SOURCE, self.ADXL313_INT_DATA_READY_BIT)

	# ----------------------------------
	# set_register_bit()
	#
	# Sets or clears bit of specified register
	def set_register_bit(self, reg_address, bit_pos, state):
		""" 
			Sets or clears bit of specified register

            :param reg_address: The address of the register you'd like to affect.
            :param bit_pos: The specific bit of the register you'd like to affect.
            :param state: The condition of the bit you'd like to set/clear (0 or 1).

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		_register = self._i2c.read_byte(self.address, reg_address)
		if(state):
			_register |= (1 << bit_pos) # Forces nth Bit of _register to 1. Other Bits Unchanged.
		else:
			_register &= ~(1 << bit_pos) # Forces nth Bit of _register to 0. Other Bits Unchanged.
		self._i2c.write_byte(self.address, reg_address, _register)
		return True        

	# ----------------------------------
	# get_register_bit()
	#
	# gets the bit status of specified register
	def get_register_bit(self, reg_address, bit_pos):
		""" 
			Gets the bit status of specified register

            :param reg_address: The address of the register you'd like to read
            :param bit_pos: The specific bit of the register you'd like to read

			:return: Status of bit spcified within the register (0 or 1)
			:rtype: bool
		"""
		_register = self._i2c.read_byte(self.address, reg_address)
		return ((_register >> bit_pos) & 1)  

	# ----------------------------------
	# read_accel()
	#
	# Reads Acceleration into Three Class Variables:  x, y and z
	def read_accel(self):
		""" 
			Reads Acceleration into Three Class Variables:  x, y and z

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		buff = self._i2c.read_block(self.address, self.ADXL313_DATA_X0, self.ADXL313_TO_READ)
		self.x = ((buff[1] << 8) | buff[0])
		self.y = ((buff[3] << 8) | buff[2])
		self.z = ((buff[5] << 8) | buff[4])

		# device datatype is SIGNED 16 bit int (twos compliment)
		# python receives this as simply 16 bits of data and stores it in a 32 byte data type
		# we need to modify each incoming data value to be more useful and allow negative values
		if self.x > 32767:
			self.x -= 65536
		if self.y > 32767:
			self.y -= 65536
		if self.z > 32767:
			self.z -= 65536			
		return True    

	# ----------------------------------
	# get_range()
	#
	# Reads the current range setting on the device
	def get_range(self):
		""" 
			Reads the current range setting on the device

			:return: range setting of the device (from in DATA_FORMAT register)
			:rtype: float
		"""
		_register = self._i2c.read_byte(self.address, self.ADXL313_DATA_FORMAT)
		_range = (_register & 0b00000011)
		range_val = 0.1 # float, so we can handle the 0.5 range value

		# device datatype is SIGNED 16 bit int (twos compliment)
		# python receives this as simply 16 bits of data and stores it in a 32 byte data type
		# we need to modify each incoming data value to be more useful and allow negative values
		if _range == self.ADXL313_RANGE_05_G:
			range_val = 0.5
		elif _range == self.ADXL313_RANGE_1_G:
			range_val = 1.0
		elif _range == self.ADXL313_RANGE_2_G:
			range_val = 2.0
		elif _range == self.ADXL313_RANGE_4_G:
			range_val = 4.0		
		return range_val

	# ----------------------------------
	# set_range()
	#
	# Sets the range setting on the device
	def set_range(self, new_range):
		""" 
			Sets the range setting on the device

			:param range: range value desired (ADXL313_RANGE_05_G, ADXL313_RANGE_1_G, etc)

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		_register = self._i2c.read_byte(self.address, self.ADXL313_DATA_FORMAT)
		to_write = new_range
		to_write |= (_register & 0b11101100)
		self._i2c.write_byte(self.address, self.ADXL313_DATA_FORMAT, to_write)
		return True

	# ----------------------------------
	# autosleep_on()
	#
	# Turns Autosleep on.
	# note, prior to calling this, 
	# you will need to set THRESH_INACT and TIME_INACT.
	# set the link bit, to "link" activity and inactivity sensing
	def autosleep_on(self):
		""" 
			Turns Autosleep on.

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		# set the link bit, to "link" activity and inactivity sensing
		self.set_register_bit(self.ADXL313_POWER_CTL, self.ADXL313_LINK_BIT, True)

		# set the autosleep
		self.set_register_bit(self.ADXL313_POWER_CTL, self.ADXL313_AUTOSLEEP_BIT, True)
		return True

	# ----------------------------------
	# autosleep_off()
	#
	# Turns Autosleep off
	def autosleep_off(self):
		""" 
			Turns Autosleep off.

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		# clear the autosleep bit
		self.set_register_bit(self.ADXL313_POWER_CTL, self.ADXL313_AUTOSLEEP_BIT, False)
		return True		

	# ----------------------------------
	# set_activity_x()
	#
	# Enalbes or disables X axis participattion in activity detection
	def set_activity_x(self, state):
		""" 
			Enalbes or disables X axis participattion in activity detection
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_ACT_INACT_CTL, 6, state)
	
	# ----------------------------------
	# set_activity_y()
	#
	# Enalbes or disables Y axis participattion in activity detection
	def set_activity_y(self, state):
		""" 
			Enalbes or disables Y axis participattion in activity detection
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_ACT_INACT_CTL, 5, state)

	# ----------------------------------
	# set_activity_z()
	#
	# Enalbes or disables Z axis participattion in activity detection
	def set_activity_z(self, state):
		""" 
			Enalbes or disables Z axis participattion in activity detection
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_ACT_INACT_CTL, 4, state)		

	# ----------------------------------
	# set_inactivity_x()
	#
	# Enalbes or disables X axis participattion in inactivity detection
	def set_inactivity_x(self, state):
		""" 
			Enalbes or disables X axis participattion in inactivity detection
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_ACT_INACT_CTL, 2, state)
	
	# ----------------------------------
	# set_inactivity_y()
	#
	# Enalbes or disables Y axis participattion in inactivity detection
	def set_inactivity_y(self, state):
		""" 
			Enalbes or disables Y axis participattion in inactivity detection
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_ACT_INACT_CTL, 1, state)

	# ----------------------------------
	# set_inactivity_z()
	#
	# Enalbes or disables Z axis participattion in inactivity detection
	def set_inactivity_z(self, state):
		""" 
			Enalbes or disables Z axis participattion in inactivity detection
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_ACT_INACT_CTL, 0, state)		

	# ----------------------------------
	# set_activity_threshold()
	#
	# Sets the Threshold Value for Detecting Activity.
	# Data Format is Unsigned, so the Magnitude of the Activity Event is Compared
	# with the Value in the THRESH_ACT Register.
	# The Scale Factor is 62.5mg/LSB.
	# Value of 0 may Result in Undesirable Behavior if the Activity Interrupt Enabled.
	# It Accepts a Maximum Value of 255.
	def set_activity_threshold(self, activity_threshold):
		""" 
			Sets the Threshold Value for Detecting Activity.
			:param activity_threshold: 0-255

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		activity_threshold = self.limit(activity_threshold)
		self._i2c.write_byte(self.address, self.ADXL313_THRESH_ACT, activity_threshold)
		return True		

	# ----------------------------------
	# get_activity_threshold()
	#
	# Gets the Threshold Value for Detecting Activity.
	def get_activity_threshold(self):
		""" 
			Gets the Threshold Value for Detecting Activity.

			:return: activity detection theshold
			:rtype: byte
		"""
		return self._i2c.read_byte(self.address, self.ADXL313_THRESH_ACT)			

	# ----------------------------------
	# set_inactivity_threshold()
	#
	# Sets the Threshold Value for Detecting Inactivity.
	# Data Format is Unsigned, so the Magnitude of the Inactivity Event is Compared
	# with the Value in the THRESH_ACT Register.
	# The Scale Factor is 62.5mg/LSB.
	# Value of 0 may Result in Undesirable Behavior if the Inactivity Interrupt Enabled.
	# It Accepts a Maximum Value of 255.
	def set_inactivity_threshold(self, inactivity_threshold):
		""" 
			Sets the Threshold Value for Detecting Inactivity.
			:param inactivity_threshold: 0-255

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		inactivity_threshold = self.limit(inactivity_threshold)
		self._i2c.write_byte(self.address, self.ADXL313_THRESH_INACT, inactivity_threshold)
		return True		

	# ----------------------------------
	# get_inactivity_threshold()
	#
	# Gets the Threshold Value for Detecting Inactivity.
	def get_inactivity_threshold(self):
		""" 
			Gets the Threshold Value for Detecting Inactivity.

			:return: inactivity detection theshold
			:rtype: byte
		"""
		return self._i2c.read_byte(self.address, self.ADXL313_THRESH_INACT)			

	# ----------------------------------
	# set_time_inactivity()
	#
	# Sets time requirement below inactivity threshold to detect inactivity
	# Contains an Unsigned Time Value Representing the Amount of Time that
	# Acceleration must be Less Than the Value in the THRESH_INACT Register
	# for Inactivity to be Declared.
	# Uses Filtered Output Data* unlike other Interrupt Functions
	# Scale Factor is 1sec/LSB.
	# Value Must Be Between 0 and 255.
	def set_time_inactivity(self, time_inactivity):
		""" 
			Sets time requirement below inactivity threshold to detect inactivity
			:param time_inactivity: 0-255

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		time_inactivity = self.limit(time_inactivity)
		self._i2c.write_byte(self.address, self.ADXL313_TIME_INACT, time_inactivity)
		return True		

	# ----------------------------------
	# get_time_inactivity()
	#
	# Gets time requirement below inactivity threshold to detect inactivity
	def get_time_inactivity(self):
		""" 
			Gets time requirement below inactivity threshold to detect inactivity

			:return: inactivity detection time requirement
			:rtype: byte
		"""
		return self._i2c.read_byte(self.address, self.ADXL313_TIME_INACT)			

	def limit(self, num, minimum=1, maximum=255):
		"""
			Limits input 'num' between minimum and maximum values.
			Default minimum value is 1 and maximum value is 255.

			:param num: the number you'l like to limit
			:param minimum: the min (default 1)
			:param maximum: the max (default 255)

			:return: your new limited number within min and max
			:rtype: int
		"""
		if num > maximum:
			return maximum
		elif num < minimum:
			return minimum
		return num		

	# ----------------------------------
	# set_interrupt_mapping()
	#
	# Maps the desired interrupt bit (from intsource) to the desired hardware interrupt pin
	def set_interrupt_mapping(self, interrupt_bit, interrupt_pin):
		""" 
			Maps the desired interrupt bit (from intsource) to the desired hardware interrupt pin
			:param interrupt_bit: the desired int bit you'd like to map
			:param interrupt_pin: ADXL313_INT1_PIN or ADXL313_INT2_PIN

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_INT_MAP, interrupt_bit, interrupt_pin)	


	# ----------------------------------
	# is_interrupt_enabled()
	#
	# Get status of whether an interrupt is enabled or disabled.
	def is_interrupt_enabled(self, interrupt_bit):
		""" 
			Get status of whether an interrupt is enabled or disabled.
			:param interrupt_bit: the desired int bit you'd like to read

			:return: Returns true if the interrupt bit is enabled, otherwise false
			:rtype: bool
		"""
		return self.get_register_bit(self.ADXL313_INT_ENABLE, interrupt_bit)			

	# ----------------------------------
	# set_interrupt()
	#
	# Sets the enable bit (0 or 1) for one desired int inside the ADXL313_INT_ENABLE register
	def set_interrupt(self, interrupt_bit, state):
		""" 
			Sets the enable bit (0 or 1) for one desired int inside the ADXL313_INT_ENABLE register
			:param interrupt_bit: the desired int bit you'd like to change
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		return self.set_register_bit(self.ADXL313_INT_ENABLE, interrupt_bit, state)	

	# ----------------------------------
	# activity_int()
	#
	# Enables or disables the activity interrupt
	def activity_int(self, state):
		""" 
			Enables or disables the activity interrupt
			
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		if state:
			return self.set_interrupt(self.ADXL313_INT_ACTIVITY_BIT, 1)
		else:
			return self.set_interrupt(self.ADXL313_INT_ACTIVITY_BIT, 0)

	# ----------------------------------
	# inactivity_int()
	#
	# Enables or disables the inactivity interrupt
	def inactivity_int(self, state):
		""" 
			Enables or disables the inactivity interrupt
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		if state:
			return self.set_interrupt(self.ADXL313_INT_INACTIVITY_BIT, 1)
		else:
			return self.set_interrupt(self.ADXL313_INT_INACTIVITY_BIT, 0)		

	# ----------------------------------
	# data_ready_int()
	#
	# Enables or disables the dataready interrupt
	def data_ready_int(self, state):
		""" 
			Enables or disables the dataready interrupt
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		if state:
			return self.set_interrupt(self.ADXL313_INT_DATA_READY_BIT, 1)
		else:
			return self.set_interrupt(self.ADXL313_INT_DATA_READY_BIT, 0)				

	# ----------------------------------
	# watermark_int()
	#
	# Enables or disables the watermark interrupt
	def watermark_int(self, state):
		""" 
			Enables or disables the watermark interrupt
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		if state:
			return self.set_interrupt(self.ADXL313_INT_WATERMARK_BIT, 1)
		else:
			return self.set_interrupt(self.ADXL313_INT_WATERMARK_BIT, 0)					

	# ----------------------------------
	# overrun_int()
	#
	# Enables or disables the overrun interrupt
	def overrun_int(self, state):
		""" 
			Enables or disables the overrun interrupt
			:param state: 1 = enabled, 0 = disabled

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		if state:
			return self.set_interrupt(self.ADXL313_INT_OVERRUN_BIT, 1)
		else:
			return self.set_interrupt(self.ADXL313_INT_OVERRUN_BIT, 0)								


	# ----------------------------------
	# get_fifo_mode()
	#
	# Get the current FIFO mode (0=bypass,1=fifo,2=stream,3=trigger)
	def get_fifo_mode(self):
		""" 
			Get the current FIFO mode (0=bypass,1=fifo,2=stream,3=trigger)

			:return: FIFO mode (0=bypass,1=fifo,2=stream,3=trigger)
			:rtype: byte
		"""
		_register = self._i2c.read_byte(self.address, self.ADXL313_FIFO_CTL)
		mode = (_register & 0b11000000) # mask all the other bits [0:5]
		mode = (mode >> 6)
		return mode

	# ----------------------------------
	# set_fifo_mode(self, mode)
	#
	# Set FIFO mode (0=bypass,1=fifo,2=stream,3=trigger)
	def set_fifo_mode(self, mode):
		""" 
			Set FIFO mode

			:param mode: FIFO mode (ADXL313_FIFO_MODE_BYPASS, ADXL313_FIFO_MODE_FIFO, ADXL313_FIFO_MODE_STREAM, ADXL313_FIFO_MODE_TRIGGER)

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		_register = self._i2c.read_byte(self.address, self.ADXL313_FIFO_CTL) # read entire FIFO_CTRL reg
		_register &= 0b00111111 # clear current mode bits
		_register |= (mode << 6) # set the desired mode bits into our "write regiter variable"
		self._i2c.write_byte(self.address, self.ADXL313_FIFO_CTL, _register) # write it!
		return True

	# ----------------------------------
	# get_fifo_samples_threshold()
	#
	# Get FIFO samples threshold (0-32)
	def get_fifo_samples_threshold(self):
		""" 
			Get FIFO samples threshold (0-32)

			:return: FIFO samples threshold (0-32)
			:rtype: byte
		"""
		_register = self._i2c.read_byte(self.address, self.ADXL313_FIFO_CTL)
		samples = (_register & 0b00011111) # mask all the other bits we don't need [5:7]
		return samples

	# ----------------------------------
	# set_fifo_samples_threshold()
	#
	# Set FIFO samples threshold (0-32)
	def set_fifo_samples_threshold(self, samples):
		""" 
			Set FIFO samples threshold (0-32)

			:param mode: FIFO samples threshold (0-32)

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		_register = self._i2c.read_byte(self.address, self.ADXL313_FIFO_CTL) # read entire FIFO_CTRL reg
		_register &= 0b11100000 # clear current sample threshhold bits [0:4]
		_register |= samples # set the desired sample threshhold bits into our "write regiter variable"
		self._i2c.write_byte(self.address, self.ADXL313_FIFO_CTL, _register) # write it!
		return True

	# ----------------------------------
	# get_fifo_entries_amount()
	#
	# Get FIFO entries amount (0-32)
	def get_fifo_entries_amount(self):
		""" 
			Get FIFO entries amount (0-32)

			:return: FIFO entries amount (0-32)
			:rtype: byte
		"""
		_register = self._i2c.read_byte(self.address, self.ADXL313_FIFO_STATUS) 
		entries = (_register & 0b00111111) # mask all the other bits we don't need [6:7]
		return entries

	# ----------------------------------
	# clear_fifo()
	#
	# Clears all FIFO data by bypassing FIFO and re-entering previous mode
	def clear_fifo(self):
		""" 
			Clears all FIFO data by bypassing FIFO and re-entering previous mode

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		mode = self.get_fifo_mode() # get current mode, so we can return it here later
		self.set_fifo_mode(self.ADXL313_FIFO_MODE_BYPASS) # sets mode to bypass temporarily to clear contents
		self.set_fifo_mode(mode) # return mode to previous selection
		return True

	# ----------------------------------
	# update_int_source_statuses()
	#
	# Reads int Source Register once and updates all individual calss statuses
	def update_int_source_statuses(self):
		""" 
			Reads int Source Register once and updates all individual calss statuses

			:return: Returns true of the function was completed, otherwise False.
			:rtype: bool
		"""
		_register = self._i2c.read_byte(self.address, self.ADXL313_INT_SOURCE)
		self.ADXL313_INTSOURCE_DATAREADY = ((_register >> self.ADXL313_INT_DATA_READY_BIT) & 1)
		self.ADXL313_INTSOURCE_ACTIVITY = ((_register >> self.ADXL313_INT_ACTIVITY_BIT) & 1)
		self.ADXL313_INTSOURCE_INACTIVITY = ((_register >> self.ADXL313_INT_INACTIVITY_BIT) & 1)
		self.ADXL313_INTSOURCE_WATERMARK = ((_register >> self.ADXL313_INT_WATERMARK_BIT) & 1)
		self.ADXL313_INTSOURCE_OVERRUN = ((_register >> self.ADXL313_INT_OVERRUN_BIT) & 1)
		return True

	# ----------------------------------
	# Lower Power definitions
	# 
	def is_low_power(self):
		return self.get_register_bit(self.ADXL313_BW_RATE, 4)

	def low_power_on(self):
		return self.set_register_bit(self.ADXL313_BW_RATE, 4, True)

	def low_power_off(self):
		return self.set_register_bit(self.ADXL313_BW_RATE, 4, False)

	def set_low_power(self, state):
		if(state):
			self.low_power_on()
		else:
			self.low_power_off()


	# ----------------------------------
	# Bandwidth definitions
	# 
	def set_bandwidth(self, bw):
		self._i2c.write_byte(self.address, self.ADXL313_BW_RATE, bw)

	def get_bandwidth(self):
		return self._i2c.read_byte(self.address, self.ADXL313_BW_RATE)
