#-----------------------------------------------------------------------------
# qwiic_icm20948.py
#
# Python library for the SparkFun 9DoF IMU Breakout - ICM-20948 (Qwiic).
#
# https://www.sparkfun.com/products/15335
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, March 2020
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
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

"""!
qwiic_icm20948
============
Python module for the [SparkFun 9DoF IMU Breakout - ICM-20948 (Qwiic)](https://www.sparkfun.com/products/15335)

This python package is a port of the existing [SparkFun ICM-20948 Arduino Library](https://github.com/sparkfun/SparkFun_ICM-20948_ArduinoLibrary)

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
_DEFAULT_NAME = "Qwiic ICM20948"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the 
# device.
_AVAILABLE_I2C_ADDRESS = [0x69, 0x68]

# define our valid chip IDs
_VALID_CHIP_IDS = [0xEA]

# Internal Sensor IDs, used in various functions as arguments to know who to affect
ICM_20948_INTERNAL_ACC = (1 << 0)
ICM_20948_INTERNAL_GYR = (1 << 1)
ICM_20948_INTERNAL_MAG = (1 << 2)
ICM_20948_INTERNAL_TMP = (1 << 3)
ICM_20948_INTERNAL_MST = (1 << 4) # I2C Master Ineternal

# Sample mode options
ICM_20948_SAMPLE_MODE_CONTINUOUS = 0x00
ICM_20948_SAMPLE_MODE_CYCLED = 0x01

# Accel full scale range options [AGB2_REG_ACCEL_CONFIG]
GPM2 = 0x00 # G forces Plus or Minus (aka "gpm")
GPM4 = 0x01
GPM8 = 0x02
GPM16 = 0x03

# Gyro full scale range options [AGB2_REG_GYRO_CONFIG_1]
DPS250 = 0x00 #degrees per second (aka "dps")
DPS500 = 0x01
DPS1000 = 0x02
DPS2000 = 0x03

# Accelerometer low pass filter configuration options
# Format is dAbwB_nXbwZ - A is integer part of 3db BW, B is fraction. X is integer part of nyquist bandwidth, Y is fraction
ACC_D246BW_N265BW = 0x00
ACC_D246BW_N265BW_1 = 0x01
ACC_D111BW4_N136BW = 0x02
ACC_D50BW4_N68BW8 = 0x03
ACC_D23BW9_N34BW4 = 0x04
ACC_D11BW5_N17BW = 0x05
ACC_D5BW7_N8BW3 = 0x06
ACC_D473BW_N499BW = 0x07

# Gyro low pass filter configuration options
# Format is dAbwB_nXbwZ - A is integer part of 3db BW, B is fraction. X is integer part of nyquist bandwidth, Y is fraction
GYR_D196BW6_N229BW8 = 0x00
GYR_D151BW8_N187BW6 = 0x01
GYR_D119BW5_N154BW3 = 0x02
GYR_D51BW2_N73BW3 = 0x03
GYR_D23BW9_N35BW9 = 0x04
GYR_D11BW6_N17BW8 = 0x05
GYR_D5BW7_N8BW9 = 0x06
GYR_D361BW4_N376BW5 = 0x07

# Magnetometer specific stuff
MAG_AK09916_I2C_ADDR = 0x0C
MAG_AK09916_WHO_AM_I = 0x4809
MAG_REG_WHO_AM_I = 0x00
AK09916_MODE_POWER_DOWN = 0x00
AK09916_MODE_SINGLE 	= (0x01 << 0)
AK09916_MODE_CONT_10HZ 	= (0x01 << 1)
AK09916_MODE_CONT_20HZ 	= (0x02 << 1)
AK09916_MODE_CONT_50HZ 	= (0x03 << 1)
AK09916_MODE_CONT_100HZ = (0x04 << 1)
AK09916_MODE_SELF_TEST 	= (0x01 << 4)

#Magnetometer Registers (aka sub-addresses when reading as I2C Master)
AK09916_REG_WIA1 = 0x00
AK09916_REG_WIA2 = 0x01
AK09916_REG_ST1 = 0x10
AK09916_REG_HXL = 0x11
AK09916_REG_HXH = 0x12
AK09916_REG_HYL = 0x13
AK09916_REG_HYH = 0x14
AK09916_REG_HZL = 0x15
AK09916_REG_HZH = 0x16
AK09916_REG_ST2 = 0x18
AK09916_REG_CNTL2 = 0x31
AK09916_REG_CNTL3 = 0x32


# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported 
# from this module.

class QwiicICM20948(object):
	"""!
	QwiicICM20948

	@param address: The I2C address to use for the device. 
					If not provided, the default address is used.
	@param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.

	@return **Object** The ICM20948 device object.
	"""
	# Constructor
	device_name			= _DEFAULT_NAME
	available_addresses	= _AVAILABLE_I2C_ADDRESS

 	# Generalized
	REG_BANK_SEL = 						0x7F 

	# Gyroscope and Accelerometer
	# User Bank 0
	AGB0_REG_WHO_AM_I = 				0x00 
	AGB0_REG_USER_CTRL = 				0x03 
	AGB0_REG_LP_CONFIG = 				0x05 
	AGB0_REG_PWR_MGMT_1 = 				0x06
	AGB0_REG_PWR_MGMT_2 = 				0x07
	AGB0_REG_INT_PIN_CONFIG = 			0x0F 
	AGB0_REG_INT_ENABLE = 				0x10
	AGB0_REG_INT_ENABLE_1 = 			0x11
	AGB0_REG_INT_ENABLE_2 = 			0x12
	AGB0_REG_INT_ENABLE_3 = 			0x13
	AGB0_REG_I2C_MST_STATUS = 			0x17 
	AGB0_REG_INT_STATUS = 				0x19 
	AGB0_REG_INT_STATUS_1 = 			0x1A
	AGB0_REG_INT_STATUS_2 = 			0x1B
	AGB0_REG_INT_STATUS_3 = 			0x1C
	AGB0_REG_DELAY_TIMEH = 				0x28 
	AGB0_REG_DELAY_TIMEL = 				0x29
	AGB0_REG_ACCEL_XOUT_H = 			0x2D 
	AGB0_REG_ACCEL_XOUT_L = 			0x2E
	AGB0_REG_ACCEL_YOUT_H = 			0x2F
	AGB0_REG_ACCEL_YOUT_L = 			0x30
	AGB0_REG_ACCEL_ZOUT_H = 			0x31
	AGB0_REG_ACCEL_ZOUT_L = 			0x32
	AGB0_REG_GYRO_XOUT_H = 				0x33
	AGB0_REG_GYRO_XOUT_L = 				0x34
	AGB0_REG_GYRO_YOUT_H = 				0x35
	AGB0_REG_GYRO_YOUT_L = 				0x36
	AGB0_REG_GYRO_ZOUT_H = 				0x37
	AGB0_REG_GYRO_ZOUT_L = 				0x38
	AGB0_REG_TEMP_OUT_H  = 				0x39
	AGB0_REG_TEMP_OUT_L = 				0x3A
	AGB0_REG_EXT_SLV_SENS_DATA_00 =		0x3B
	AGB0_REG_EXT_SLV_SENS_DATA_01 = 	0x3C
	AGB0_REG_EXT_SLV_SENS_DATA_02 = 	0x3D
	AGB0_REG_EXT_SLV_SENS_DATA_03 = 	0x3E
	AGB0_REG_EXT_SLV_SENS_DATA_04 = 	0x3F
	AGB0_REG_EXT_SLV_SENS_DATA_05 = 	0x40
	AGB0_REG_EXT_SLV_SENS_DATA_06 = 	0x41
	AGB0_REG_EXT_SLV_SENS_DATA_07 = 	0x42
	AGB0_REG_EXT_SLV_SENS_DATA_08 = 	0x43
	AGB0_REG_EXT_SLV_SENS_DATA_09 = 	0x44
	AGB0_REG_EXT_SLV_SENS_DATA_10 = 	0x45
	AGB0_REG_EXT_SLV_SENS_DATA_11 = 	0x46
	AGB0_REG_EXT_SLV_SENS_DATA_12 = 	0x47
	AGB0_REG_EXT_SLV_SENS_DATA_13 = 	0x48
	AGB0_REG_EXT_SLV_SENS_DATA_14 = 	0x49
	AGB0_REG_EXT_SLV_SENS_DATA_15 = 	0x4A
	AGB0_REG_EXT_SLV_SENS_DATA_16 = 	0x4B
	AGB0_REG_EXT_SLV_SENS_DATA_17 = 	0x4C
	AGB0_REG_EXT_SLV_SENS_DATA_18 = 	0x4D
	AGB0_REG_EXT_SLV_SENS_DATA_19 = 	0x4E
	AGB0_REG_EXT_SLV_SENS_DATA_20 = 	0x4F
	AGB0_REG_EXT_SLV_SENS_DATA_21 = 	0x50
	AGB0_REG_EXT_SLV_SENS_DATA_22 = 	0x51
	AGB0_REG_EXT_SLV_SENS_DATA_23 = 	0x52
	AGB0_REG_FIFO_EN_1 = 				0x66 
	AGB0_REG_FIFO_EN_2 = 				0x67
	AGB0_REG_FIFO_MODE = 				0x69
	AGB0_REG_FIFO_COUNT_H = 			0x70 
	AGB0_REG_FIFO_COUNT_L = 			0x71
	AGB0_REG_FIFO_R_W = 				0x72
	AGB0_REG_DATA_RDY_STATUS = 			0x74 
	AGB0_REG_FIFO_CFG = 				0x76 
	AGB0_REG_MEM_START_ADDR = 			0x7C # Hmm  Invensense thought they were sneaky not listing these locations on the datasheet...
	AGB0_REG_MEM_R_W = 					0x7D # These three locations seem to be able to access some memory within the device
	AGB0_REG_MEM_BANK_SEL = 			0x7E # And that location is also where the DMP image gets loaded
	AGB0_REG_REG_BANK_SEL = 			0x7F 
	# Bank 1
	AGB1_REG_SELF_TEST_X_GYRO = 		0x02 
	AGB1_REG_SELF_TEST_Y_GYRO = 		0x03
	AGB1_REG_SELF_TEST_Z_GYRO = 		0x04
	AGB1_REG_SELF_TEST_X_ACCEL = 		0x0E 
	AGB1_REG_SELF_TEST_Y_ACCEL = 		0x0F
	AGB1_REG_SELF_TEST_Z_ACCEL = 		0x10
	AGB1_REG_XA_OFFS_H = 				0x14 
	AGB1_REG_XA_OFFS_L = 				0x15
	AGB1_REG_YA_OFFS_H = 				0x17 
	AGB1_REG_YA_OFFS_L = 				0x18
	AGB1_REG_ZA_OFFS_H = 				0x1A 
	AGB1_REG_ZA_OFFS_L = 				0x1B
	AGB1_REG_TIMEBASE_CORRECTION_PLL = 	0x28 
	AGB1_REG_REG_BANK_SEL = 			0x7F 
	# Bank 2
	AGB2_REG_GYRO_SMPLRT_DIV = 			0x00 
	AGB2_REG_GYRO_CONFIG_1 = 			0x01
	AGB2_REG_GYRO_CONFIG_2 = 			0x02
	AGB2_REG_XG_OFFS_USRH = 			0x03
	AGB2_REG_XG_OFFS_USRL = 			0x04
	AGB2_REG_YG_OFFS_USRH = 			0x05
	AGB2_REG_YG_OFFS_USRL = 			0x06
	AGB2_REG_ZG_OFFS_USRH = 			0x07
	AGB2_REG_ZG_OFFS_USRL = 			0x08
	AGB2_REG_ODR_ALIGN_EN = 			0x09
	AGB2_REG_ACCEL_SMPLRT_DIV_1 = 		0x10 
	AGB2_REG_ACCEL_SMPLRT_DIV_2 = 		0x11
	AGB2_REG_ACCEL_INTEL_CTRL = 		0x12
	AGB2_REG_ACCEL_WOM_THR = 			0x13
	AGB2_REG_ACCEL_CONFIG_1 = 			0x14
	AGB2_REG_ACCEL_CONFIG_2 = 			0x15
	AGB2_REG_FSYNC_CONFIG = 			0x52 
	AGB2_REG_TEMP_CONFIG = 				0x53
	AGB2_REG_MOD_CTRL_USR = 			0x54
	AGB2_REG_REG_BANK_SEL = 			0x7F 
	# Bank 3
	AGB3_REG_I2C_MST_ODR_CONFIG = 		0x00 
	AGB3_REG_I2C_MST_CTRL = 			0x01
	AGB3_REG_I2C_MST_DELAY_CTRL = 		0x02
	AGB3_REG_I2C_SLV0_ADDR = 			0x03
	AGB3_REG_I2C_SLV0_REG = 			0x04
	AGB3_REG_I2C_SLV0_CTRL = 			0x05
	AGB3_REG_I2C_SLV0_DO = 				0x06
	AGB3_REG_I2C_SLV1_ADDR = 			0x07
	AGB3_REG_I2C_SLV1_REG = 			0x08
	AGB3_REG_I2C_SLV1_CTRL = 			0x09
	AGB3_REG_I2C_SLV1_DO = 				0x0A
	AGB3_REG_I2C_SLV2_ADDR = 			0x0B
	AGB3_REG_I2C_SLV2_REG = 			0x0C
	AGB3_REG_I2C_SLV2_CTRL = 			0x0D
	AGB3_REG_I2C_SLV2_DO = 				0x0E
	AGB3_REG_I2C_SLV3_ADDR = 			0x0F
	AGB3_REG_I2C_SLV3_REG = 			0x10
	AGB3_REG_I2C_SLV3_CTRL = 			0x11
	AGB3_REG_I2C_SLV3_DO = 				0x12
	AGB3_REG_I2C_SLV4_ADDR = 			0x13
	AGB3_REG_I2C_SLV4_REG = 			0x14
	AGB3_REG_I2C_SLV4_CTRL = 			0x15
	AGB3_REG_I2C_SLV4_DO = 				0x16
	AGB3_REG_I2C_SLV4_DI = 				0x17
	AGB3_REG_REG_BANK_SEL = 			0x7F 
	
	# Magnetometer
	M_REG_WIA2 = 						0x01 
	M_REG_ST1 = 						0x10 
	M_REG_HXL = 						0x11
	M_REG_HXH = 						0x12
	M_REG_HYL = 						0x13
	M_REG_HYH = 						0x14
	M_REG_HZL = 						0x15
	M_REG_HZH = 						0x16
	M_REG_ST2 = 						0x18
	M_REG_CNTL2 = 						0x31 
	M_REG_CNTL3 = 						0x32
	M_REG_TS1 = 						0x33
	M_REG_TS2 = 						0x34

	# Constructor
	def __init__(self, address=None, i2c_bus=None):

		# The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
		address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
		# Did the user specify an I2C address?
		self.address = address if address is not None else self.available_addresses[0]

		# Use the given I2C bus, or the platform's default bus
		self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

	# ----------------------------------
	# is_connected()
	#
	# Is an actual board connected to our system?

	def is_connected(self):
		"""!
		Determine if a ICM20948 device is connected to the system.

		@return **bool** True if the device is connected, otherwise False.
		"""
		return self._i2c.is_device_connected(self.address)

	# ----------------------------------
	# set_bank()
	#
	# Sets the bank register of the ICM20948 module
	def set_bank(self, bank):
		"""!
		Sets the bank register of the ICM20948 module

		@return **bool** Returns true if the bank was a valid value and it was set, otherwise False.
		"""
		if bank > 3:	# Only 4 possible banks
			return False
		bank = ((bank << 4) & 0x30) # bits 5:4 of REG_BANK_SEL
		#return ICM_20948_execute_w(pdev, REG_BANK_SEL, &bank, 1)
		return self._i2c.write_byte(self.address, self.REG_BANK_SEL, bank)

	# ----------------------------------
	# sw_reset()
	#
	# Performs a software reset on the ICM20948 module
	def sw_reset(self):
		"""!
		Performs a software reset on the ICM20948 module

		@return **bool** Returns true if the software reset was successful, otherwise False.
		"""
		# Read the Power Management Register, store in local variable "register"
		self.set_bank(0)
		register = self._i2c.read_byte(self.address, self.AGB0_REG_PWR_MGMT_1)

		# Set the device reset bit [7]
		register |= (1<<7)

		# Write register
		self.set_bank(0)
		return self._i2c.write_byte(self.address, self.AGB0_REG_PWR_MGMT_1, register)		

	# ----------------------------------
	# sleep()
	#
	# Sets the ICM20948 module in or out of sleep mode
	def sleep(self, on):
		"""!
		Sets the ICM20948 module in or out of sleep mode

		@return **bool** Returns true if the sleep setting write was successful, otherwise False.
		"""
		# Read the Power Management Register, store in local variable "register"
		self.set_bank(0)
		register = self._i2c.read_byte(self.address, self.AGB0_REG_PWR_MGMT_1)

		# Set/clear the sleep bit [6] as needed
		if on:
			register |= (1<<6) # set bit
		else:
			register &= ~(1<<6) # clear bit

		# Write register
		self.set_bank(0)
		return self._i2c.write_byte(self.address, self.AGB0_REG_PWR_MGMT_1, register)			

	# ----------------------------------
	# low_power()
	#
	# Sets the ICM20948 module in or out of low power mode
	def low_power(self, on):
		"""!
		Sets the ICM20948 module in or out of low power mode

		@return **bool** Returns true if the power mode setting write was successful, otherwise False.
		"""
		# Read the Power Management Register, store in local variable "register"
		self.set_bank(0)
		register = self._i2c.read_byte(self.address, self.AGB0_REG_PWR_MGMT_1)

		# Set/clear the low power mode bit [5] as needed
		if on:
			register |= (1<<5) # set bit
		else:
			register &= ~(1<<5) # clear bit

		# Write register
		self.set_bank(0)
		return self._i2c.write_byte(self.address, self.AGB0_REG_PWR_MGMT_1, register)	

	# ----------------------------------
	# set_sample_mode()
	#
	# Sets the sample mode of the ICM90248 module
	def set_sample_mode(self, sensors, mode):
		"""!
		Sets the sample mode of the ICM90248 module

		@return **bool** Returns true if the sample mode setting write was successful, otherwise False.
		"""
		# check for valid sensor ID from user of this function
		if not (sensors & (ICM_20948_INTERNAL_ACC | ICM_20948_INTERNAL_GYR | ICM_20948_INTERNAL_MST)):
			return False

		# Read the LP CONFIG Register, store in local variable "register"
		self.set_bank(0)
		register = self._i2c.read_byte(self.address, self.AGB0_REG_LP_CONFIG)

		if (sensors & ICM_20948_INTERNAL_ACC):
			# Set/clear the sensor specific sample mode bit as needed
			if mode == ICM_20948_SAMPLE_MODE_CYCLED:
				register |= (1<<5) # set bit
			elif mode == ICM_20948_SAMPLE_MODE_CONTINUOUS:
				register &= ~(1<<5) # clear bit

		if (sensors & ICM_20948_INTERNAL_GYR):
			# Set/clear the sensor specific sample mode bit as needed
			if mode == ICM_20948_SAMPLE_MODE_CYCLED:
				register |= (1<<4) # set bit
			elif mode == ICM_20948_SAMPLE_MODE_CONTINUOUS:
				register &= ~(1<<4) # clear bit

		if (sensors & ICM_20948_INTERNAL_MST):
			# Set/clear the sensor specific sample mode bit as needed
			if mode == ICM_20948_SAMPLE_MODE_CYCLED:
				register |= (1<<6) # set bit
			elif mode == ICM_20948_SAMPLE_MODE_CONTINUOUS:
				register &= ~(1<<6) # clear bit

		# Write register
		self.set_bank(0)
		return self._i2c.write_byte(self.address, self.AGB0_REG_LP_CONFIG, register)		

	# ----------------------------------
	# set_full_scale_range_accel()
	#
	# Sets the full scale range for the accel in the ICM20948 module
	def set_full_scale_range_accel(self, mode):
		"""!
		Sets the full scale range for the accel in the ICM20948 module

		@return **bool** Returns true if the full scale range setting write was successful, otherwise False.
		"""
		# Read the Accel Config Register, store in local variable "register"
		self.set_bank(2)
		register = self._i2c.read_byte(self.address, self.AGB2_REG_ACCEL_CONFIG_1)

		register &= ~(0b00000110) # clear bits 2:1 (0b0000.0XX0)

		register |= (mode << 1) # place mode select into bits 2:1 of AGB2_REG_ACCEL_CONFIG			

		# Write register
		self.set_bank(2)
		return self._i2c.write_byte(self.address, self.AGB2_REG_ACCEL_CONFIG_1, register)	

	# ----------------------------------
	# set_full_scale_range_gyro()
	#
	# Sets the full scale range for the gyro in the ICM20948 module
	def set_full_scale_range_gyro(self, mode):
		"""!
		Sets the full scale range for the gyro in the ICM20948 module

		@return **bool** Returns true if the full scale range setting write was successful, otherwise False.
		"""
		# Read the Gyro Config Register, store in local variable "register"
		self.set_bank(2)
		register = self._i2c.read_byte(self.address, self.AGB2_REG_GYRO_CONFIG_1)

		register &= ~(0b00000110) # clear bits 2:1 (0b0000.0XX0)

		register |= (mode << 1) # place mode select into bits 2:1 of AGB2_REG_GYRO_CONFIG_1			

		# Write register
		self.set_bank(2)
		return self._i2c.write_byte(self.address, self.AGB2_REG_GYRO_CONFIG_1, register)			

	# ----------------------------------
	# set_dlpf_cfg_accel()
	#
	# Sets the digital low pass filter for the accel in the ICM20948 module
	def set_dlpf_cfg_accel(self, dlpcfg):
		"""!
		Sets the digital low pass filter for the accel in the ICM20948 module

		@return **bool** Returns true if the dlp setting write was successful, otherwise False.
		"""
		# Read the Accel Config Register, store in local variable "register"
		self.set_bank(2)
		register = self._i2c.read_byte(self.address, self.AGB2_REG_ACCEL_CONFIG_1)

		register &= ~(0b00111000) # clear bits 5:3 (0b00XX.X000)

		register |= (dlpcfg << 3) # place dlpcfg select into bits 5:3 of AGB2_REG_ACCEL_CONFIG_1			

		# Write register
		self.set_bank(2)
		return self._i2c.write_byte(self.address, self.AGB2_REG_ACCEL_CONFIG_1, register)	

	# ----------------------------------
	# set_dlpf_cfg_gyro()
	#
	# Sets the digital low pass filter for the gyro in the ICM20948 module
	def set_dlpf_cfg_gyro(self, dlpcfg):
		"""!
		Sets the digital low pass filter for the gyro in the ICM20948 module

		@return **bool** Returns true if the dlp setting write was successful, otherwise False.
		"""
		# Read the gyro Config Register, store in local variable "register"
		self.set_bank(2)
		register = self._i2c.read_byte(self.address, self.AGB2_REG_GYRO_CONFIG_1)

		register &= ~(0b00111000) # clear bits 5:3 (0b00XX.X000)

		register |= (dlpcfg << 3) # place dlpcfg select into bits 5:3 of AGB2_REG_GYRO_CONFIG_1			

		# Write register
		self.set_bank(2)
		return self._i2c.write_byte(self.address, self.AGB2_REG_GYRO_CONFIG_1, register)

	# ----------------------------------
	# enable_dlpf_accel()
	#
	# Enables or disables the accelerometer DLPF of the ICM90248 module
	def enable_dlpf_accel(self, on):
		"""!
		Enables or disables the accelerometer DLPF of the ICM90248 module

		@return **bool** Returns true if the DLPF mode setting write was successful, otherwise False.
		"""

		# Read the AGB2_REG_ACCEL_CONFIG_1, store in local variable "register"
		self.set_bank(2)
		register = self._i2c.read_byte(self.address, self.AGB2_REG_ACCEL_CONFIG_1)

		# Set/clear the ACCEL_FCHOICE bit [0] as needed
		if on:
			register |= (1<<0) # set bit
		else:
			register &= ~(1<<0) # clear bit

		# Write register
		self.set_bank(2)
		return self._i2c.write_byte(self.address, self.AGB2_REG_ACCEL_CONFIG_1, register)	

	# ----------------------------------
	# enable_dlpf_gyro()
	#
	# Enables or disables the Gyro DLPF of the ICM90248 module
	def enable_dlpf_gyro(self, on):
		"""!
		Enables or disables the Gyro DLPF of the ICM90248 module

		@return **bool** Returns true if the DLPF mode setting write was successful, otherwise False.
		"""

		# Read the AGB2_REG_GYRO_CONFIG_1, store in local variable "register"
		self.set_bank(2)
		register = self._i2c.read_byte(self.address, self.AGB2_REG_GYRO_CONFIG_1)

		# Set/clear the GYRO_FCHOICE bit [0] as needed
		if on:
			register |= (1<<0) # set bit
		else:
			register &= ~(1<<0) # clear bit

		# Write register
		self.set_bank(2)
		return self._i2c.write_byte(self.address, self.AGB2_REG_GYRO_CONFIG_1, register)			

	# ----------------------------------
	# data_ready()
	#
	# Returns status of RAW_DATA_0_RDY_INT the ICM90248 module
	def data_ready(self):
		"""!
		Returns status of RAW_DATA_0_RDY_INT the ICM90248 module

		@return **bool** Returns true if raw data is ready, otherwise False.
		"""

		# Read the AGB0_REG_INT_STATUS_1, store in local variable "register"
		self.set_bank(0)
		register = self._i2c.read_byte(self.address, self.AGB0_REG_INT_STATUS_1)

		# check bit [0]
		if (register & (1<<0)):
			return True
		else:
			return False

	# ----------------------------------
	# to_signed_int()
	#
	# Takes an input data of 16 bits, and returns the signed 32 bit int version of this data
	def to_signed_int(self, input):
		"""!
		Takes an input data of 16 bits, and returns the signed 32 bit int version of this data

		@return **int** Signed 32 bit integer
		"""
		if input > 32767:
			input -= 65536
		return input

	# ----------------------------------
	# get_agmt()
	#
	# Reads and updates raw values from accel, gyro, mag and temp of the ICM90248 module
	def get_agmt(self):
		"""!
		Reads and updates raw values from accel, gyro, mag and temp of the ICM90248 module

		@return **bool** Returns True if I2C read_block was successful, otherwise False.
		"""

		# Read all of the readings starting at AGB0_REG_ACCEL_XOUT_H
		numbytes = 14 + 9 # Read Accel, gyro, temp, and 9 bytes of mag
		self.set_bank(0)
		buff = self._i2c.read_block(self.address, self.AGB0_REG_ACCEL_XOUT_H, numbytes)

		self.ax_raw = ((buff[0] << 8) | (buff[1] & 0xFF))
		self.ay_raw = ((buff[2] << 8) | (buff[3] & 0xFF))
		self.az_raw = ((buff[4] << 8) | (buff[5] & 0xFF))

		self.gx_raw = ((buff[6] << 8) | (buff[7] & 0xFF))
		self.gy_raw = ((buff[8] << 8) | (buff[9] & 0xFF))
		self.gz_raw = ((buff[10] << 8) | (buff[11] & 0xFF))

		self.tmp_raw = ((buff[12] << 8) | (buff[13] & 0xFF))

		self.mag_stat1 = buff[14]
		self.mx_raw = ((buff[16] << 8) | (buff[15] & 0xFF)) # Mag data is read little endian
		self.my_raw = ((buff[18] << 8) | (buff[17] & 0xFF))
		self.mz_raw = ((buff[20] << 8) | (buff[19] & 0xFF))
		self.mag_stat2 = buff[22]

		# Convert all values to signed (because python treats all ints as 32 bit ints 
		# and does not see the MSB as the sign of our 16 bit int raw value)
		self.ax_raw = self.to_signed_int(self.ax_raw)
		self.ay_raw = self.to_signed_int(self.ay_raw)
		self.az_raw = self.to_signed_int(self.az_raw)

		self.gx_raw = self.to_signed_int(self.gx_raw)
		self.gy_raw = self.to_signed_int(self.gy_raw)
		self.gz_raw = self.to_signed_int(self.gz_raw)

		self.mx_raw = self.to_signed_int(self.mx_raw)
		self.my_raw = self.to_signed_int(self.my_raw)
		self.mz_raw = self.to_signed_int(self.mz_raw)

		# check for data read error
		if buff:
			return True
		else:
			return False


	# ----------------------------------
	# i2c_master_passthrough()
	#
	# Enables or disables I2C Master Passthrough
	def i2c_master_passthrough(self, passthrough):
		"""!
		Enables or disables I2C Master Passthrough

		@return **bool** Returns true if the setting write was successful, otherwise False.
		"""

		# Read the AGB0_REG_INT_PIN_CONFIG, store in local variable "register"
		self.set_bank(0)
		register = self._i2c.read_byte(self.address, self.AGB0_REG_INT_PIN_CONFIG)

		# Set/clear the BYPASS_EN bit [1] as needed
		if passthrough:
			register |= (1<<1) # set bit
		else:
			register &= ~(1<<1) # clear bit

		# Write register
		self.set_bank(0)
		return self._i2c.write_byte(self.address, self.AGB0_REG_INT_PIN_CONFIG, register)	

	# ----------------------------------
	# i2c_master_enable()
	#
	# Enables or disables I2C Master
	def i2c_master_enable(self, enable):
		"""!
		Enables or disables I2C Master

		@return **bool** Returns true if the setting write was successful, otherwise False.
		"""
		
		self.i2c_master_passthrough(False) # Disable BYPASS_EN

		# Setup Master Clock speed as 345.6 kHz, and NSP (aka next slave read) to "stop between reads"
		# Read the AGB3_REG_I2C_MST_CTRL, store in local variable "register"
		self.set_bank(3)
		register = self._i2c.read_byte(self.address, self.AGB3_REG_I2C_MST_CTRL)

		register &= ~(0x0F) # clear bits for master clock [3:0]
		register |= (0x07) # set bits for master clock [3:0], 0x07 corresponds to 345.6 kHz, good for up to 400 kHz
		register |= (1<<4) # set bit [4] for NSR (next slave read). 0 = restart between reads. 1 = stop between reads.

		# Write register
		self.set_bank(3)
		self._i2c.write_byte(self.address, self.AGB3_REG_I2C_MST_CTRL, register)

		# enable/disable Master I2C
		# Read the AGB0_REG_USER_CTRL, store in local variable "register"
		self.set_bank(0)
		register = self._i2c.read_byte(self.address, self.AGB0_REG_USER_CTRL)

		# Set/clear the I2C_MST_EN bit [5] as needed
		if enable:
			register |= (1<<5) # set bit
		else:
			register &= ~(1<<5) # clear bit

		# Write register
		self.set_bank(0)
		return self._i2c.write_byte(self.address, self.AGB0_REG_USER_CTRL, register)

	# Transact directly with an I2C device, one byte at a time
	# Used to configure a device before it is setup into a normal 0-3 slave slot
	def i2c_master_slv4_txn(self, addr, reg, data, rw, send_reg_addr):
		# Thanks MikeFair! // https://github.com/kriswiner/MPU9250/issues/86

		if rw:
			addr |= 0x80

		self.set_bank(3)
		self._i2c.write_byte(self.address, self.AGB3_REG_I2C_SLV4_ADDR, addr)

		self.set_bank(3)
		self._i2c.write_byte(self.address, self.AGB3_REG_I2C_SLV4_REG, reg)

		ctrl_register_slv4 = 0x00
		ctrl_register_slv4 |= (1<<7) # EN bit [7] (set)
		ctrl_register_slv4 &= ~(1<<6) # INT_EN bit [6] (cleared)
		ctrl_register_slv4 &= ~(0x0F) # DLY bits [4:0] (cleared = 0)
		if(send_reg_addr):
			ctrl_register_slv4 &= ~(1<<5) # REG_DIS bit [5] (cleared)
		else:
			ctrl_register_slv4 |= (1<<5) # REG_DIS bit [5] (set)

		txn_failed = False

		if (rw == False):
			self.set_bank(3)
			self._i2c.write_byte(self.address, self.AGB3_REG_I2C_SLV4_DO, data)

		# Kick off txn
		self.set_bank(3)
		self._i2c.write_byte(self.address, self.AGB3_REG_I2C_SLV4_CTRL, ctrl_register_slv4)

		max_cycles = 1000
		count = 0
		slave4_done = False
		while (slave4_done == False):
			self.set_bank(0)
			i2c_mst_status = self._i2c.read_byte(self.address, self.AGB0_REG_I2C_MST_STATUS)
			if i2c_mst_status & (1<<6): # Check I2C_SLAVE_DONE bit [6]
				slave4_done = True
			if  count > max_cycles:
				slave4_done = True
			count += 1

		if i2c_mst_status & (1<<4): # Check I2C_SLV4_NACK bit [4]
			txn_failed = True

		if count > max_cycles:
			txn_failed = True

		if txn_failed:
			return False

		if rw:
			self.set_bank(3)
			return self._i2c.read_byte(self.address, self.AGB3_REG_I2C_SLV4_DI)
		
		return True # if we get here, then it was a successful write

	def i2c_master_single_w(self, addr, reg, data):
		data1 = self.i2c_master_slv4_txn(addr, reg, data, False, True)
		return data1

	def write_mag(self, reg, data):
		data = self.i2c_master_single_w(MAG_AK09916_I2C_ADDR, reg, data)
		return data

	def i2c_master_single_r(self, addr, reg):
		data = self.i2c_master_slv4_txn(addr, reg, 0, True, True)
		return data

	def read_mag(self, reg):
		data = self.i2c_master_single_r(MAG_AK09916_I2C_ADDR, reg)
		return data

	# ----------------------------------
	# mag_who_i_am()
	#
	# Checks to see that the Magnetometer returns the correct ID value
	def mag_who_i_am(self):
		"""!
		Checks to see that the Magnatometer returns the correct ID value

		@return **bool** Returns true if the check was successful, otherwise False.
		"""

		whoiam1 = self.read_mag(AK09916_REG_WIA1)
		whoiam2 = self.read_mag(AK09916_REG_WIA2)

		if ((whoiam1 == (MAG_AK09916_WHO_AM_I >> 8)) and (whoiam2 == (MAG_AK09916_WHO_AM_I & 0xFF))):
			return True
		else:
			return False

	# ----------------------------------
	# i2c_master_reset()
	#
	# Resets I2C Master Module
	def i2c_master_reset(self):
		"""!
		Resets I2C Master Module

		@return **bool** Returns true if the i2c write was successful, otherwise False.
		"""

		# Read the AGB0_REG_USER_CTRL, store in local variable "register"
		self.set_bank(0)
		register = self._i2c.read_byte(self.address, self.AGB0_REG_USER_CTRL)

		# Set the I2C_MST_RST bit [1]
		register |= (1<<1) # set bit

		# Write register
		self.set_bank(0)
		return self._i2c.write_byte(self.address, self.AGB0_REG_USER_CTRL, register)	

	# ----------------------------------
	# i2c_master_configure_slave()
	#
	# Configures Master/slave settings for the ICM20948 as master, and slave in slots 0-3
	def i2c_master_configure_slave(self, slave, addr, reg, len, rw, enable, data_only, grp, swap):
		"""!
		Configures Master/slave settings for the ICM20948 as master, and slave in slots 0-3

		@return **bool** Returns true if the configuration was successful, otherwise False.
		"""
		# Adjust slave address, reg (aka sub-address), and control as needed for each slave slot (0-3)
		slv_addr_reg = 0x00
		slv_reg_reg = 0x00
		slv_ctrl_reg = 0x00
		if slave == 0:
			slv_addr_reg = self.AGB3_REG_I2C_SLV0_ADDR
			slv_reg_reg = self.AGB3_REG_I2C_SLV0_REG
			slv_ctrl_reg = self.AGB3_REG_I2C_SLV0_CTRL
		elif slave == 1:
			slv_addr_reg = self.AGB3_REG_I2C_SLV1_ADDR
			slv_reg_reg = self.AGB3_REG_I2C_SLV1_REG
			slv_ctrl_reg = self.AGB3_REG_I2C_SLV1_CTRL
		elif slave == 2:
			slv_addr_reg = self.AGB3_REG_I2C_SLV2_ADDR
			slv_reg_reg = self.AGB3_REG_I2C_SLV2_REG
			slv_ctrl_reg = self.AGB3_REG_I2C_SLV2_CTRL
		elif slave == 3:
			slv_addr_reg = self.AGB3_REG_I2C_SLV3_ADDR
			slv_reg_reg = self.AGB3_REG_I2C_SLV3_REG
			slv_ctrl_reg = self.AGB3_REG_I2C_SLV3_CTRL
		else:
			return False

		self.set_bank(3)

		# Set the slave address and the rw flag
		address = addr
		if rw:
			address |= (1<<7) # set bit# set RNW bit [7]
		
		self._i2c.write_byte(self.address, slv_addr_reg, address)

		# Set the slave sub-address (reg)
		sub_address = reg
		self._i2c.write_byte(self.address, slv_reg_reg, sub_address)

		# Set up the control info
		ctrl_reg_slv_x = 0x00
		ctrl_reg_slv_x |= len
		ctrl_reg_slv_x |= (enable << 7)
		ctrl_reg_slv_x |= (swap << 6)
		ctrl_reg_slv_x |= (data_only << 5)
		ctrl_reg_slv_x |= (grp << 4)
		return self._i2c.write_byte(self.address, slv_ctrl_reg, ctrl_reg_slv_x)

	# ----------------------------------
	# startup_magnetometer()
	#
	# Initialize the magnotometer with default values
	def startup_magnetometer(self):
		"""!
		Initialize the magnotometer with default values

		@return **bool** Returns true of the initializtion was successful, otherwise False.
		"""
		self.i2c_master_passthrough(False) #Do not connect the SDA/SCL pins to AUX_DA/AUX_CL
		self.i2c_master_enable(True)
		
		# After a ICM reset the Mag sensor may stop responding over the I2C master
		# Reset the Master I2C until it responds
		tries = 0
		max_tries = 5
		while (tries < max_tries):
			# See if we can read the WhoIAm register correctly
			if (self.mag_who_i_am()):
				break # WIA matched!
			self.i2c_master_reset() # Otherwise, reset the master I2C and try again
			tries += 1

		if (tries == max_tries):
			return False

		#Set up magnetometer
		mag_reg_ctrl2 = 0x00
		mag_reg_ctrl2 |= AK09916_MODE_CONT_100HZ
		self.write_mag(AK09916_REG_CNTL2, mag_reg_ctrl2)

		return self.i2c_master_configure_slave(0, MAG_AK09916_I2C_ADDR, AK09916_REG_ST1, 9, True, True, False, False, False)

	# ----------------------------------
	# begin()
	#
	# Initialize the system/validate the board. 
	def begin(self):
		"""!
		Initialize the operation of the ICM20948 module

		@return **bool** Returns true of the initializtion was successful, otherwise False.
		"""
		# are we who we need to be?
		self.set_bank(0)
		chip_id = self._i2c.read_byte(self.address, self.AGB0_REG_WHO_AM_I)
		if chip_id not in _VALID_CHIP_IDS:
			return False
		
		# software reset
		self.sw_reset()
		self._i2c.delay_ms(50)

		# set sleep mode off
		self.sleep(False)

		# set lower power mode off
		self.low_power(False)

		# set sample mode to continuous for both accel and gyro
		self.set_sample_mode((ICM_20948_INTERNAL_ACC | ICM_20948_INTERNAL_GYR), ICM_20948_SAMPLE_MODE_CONTINUOUS)

		# set full scale range for both accel and gyro (separate functions)
		self.set_full_scale_range_accel(GPM2)
		self.set_full_scale_range_gyro(DPS250)

		# set low pass filter for both accel and gyro (separate functions)
		self.set_dlpf_cfg_accel(ACC_D473BW_N499BW)
		self.set_dlpf_cfg_gyro(GYR_D361BW4_N376BW5)

		# disable digital low pass filters on both accel and gyro
		self.enable_dlpf_accel(False)
		self.enable_dlpf_gyro(False)

		self.startup_magnetometer()

		return True
