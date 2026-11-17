#-----------------------------------------------------------------------
# SparkFun Qwiic VL53L1X Library
#-----------------------------------------------------------------------
#
# Ported by SparkFun Electronics, October 2019
# Author: Wes Furuya
#
# Compatibility:
#     * Original: https://www.sparkfun.com/products/14722
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on Qwiic Distance Sensor, check out the product
# page linked above.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:www.gnu.org/licenses/>.
#
#=======================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#=======================================================================
#
# pylint: disable=line-too-long, bad-whitespace, invalid-name

###############################################################################
###############################################################################
#
# Original License:
# COPYRIGHT(c) 2017 STMicroelectronics International N.V. All rights reserved.
#
# This file is part of VL53L1 Core and is dual licensed,
# either 'STMicroelectronics Proprietary license'
# or 'BSD 3-clause "New" or "Revised" License' , at your option.
#=======================================================================
#
# 'STMicroelectronics Proprietary license'
#=======================================================================
#
# License terms: STMicroelectronics Proprietary in accordance with licensing
# terms at www.st.com/sla0081
#
# STMicroelectronics confidential
# Reproduction and Communication of this document is strictly prohibited unless
# specifically authorized in writing by STMicroelectronics.
#
#=======================================================================
#
# Alternatively, VL53L1 Core may be distributed under the terms of
# 'BSD 3-clause "New" or "Revised" License', in which case the following
# provisions apply instead of the ones mentioned above :
#=======================================================================
#
# License terms: BSD 3-clause "New" or "Revised" License.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#=======================================================================

# Load Necessary Modules:
#----------------------------------------------
import time							# Time access and conversion package
import math							# Basic math package
import qwiic_i2c					# I2C bus driver package

# From vL53l1x_class.h Header File
SOFT_RESET =															0x0000
VL53L1_I2C_SLAVE__DEVICE_ADDRESS =										0x0001
VL53L1_VHV_CONFIG__TIMEOUT_MACROP_LOOP_BOUND =							0x0008
ALGO__CROSSTALK_COMPENSATION_PLANE_OFFSET_KCPS =						0x0016
ALGO__CROSSTALK_COMPENSATION_X_PLANE_GRADIENT_KCPS =					0x0018
ALGO__CROSSTALK_COMPENSATION_Y_PLANE_GRADIENT_KCPS =					0x001A
ALGO__PART_TO_PART_RANGE_OFFSET_MM =									0x001E
MM_CONFIG__INNER_OFFSET_MM =											0x0020
MM_CONFIG__OUTER_OFFSET_MM =											0x0022
GPIO_HV_MUX__CTRL =														0x0030
GPIO__TIO_HV_STATUS =													0x0031
SYSTEM__INTERRUPT_CONFIG_GPIO =											0x0046
PHASECAL_CONFIG__TIMEOUT_MACROP =										0x004B
RANGE_CONFIG__TIMEOUT_MACROP_A_HI =										0x005E
RANGE_CONFIG__VCSEL_PERIOD_A =											0x0060
RANGE_CONFIG__VCSEL_PERIOD_B =											0x0063
RANGE_CONFIG__TIMEOUT_MACROP_B_HI =										0x0061
RANGE_CONFIG__TIMEOUT_MACROP_B_LO =										0x0062
RANGE_CONFIG__SIGMA_THRESH =											0x0064
RANGE_CONFIG__MIN_COUNT_RATE_RTN_LIMIT_MCPS =							0x0066
RANGE_CONFIG__VALID_PHASE_HIGH =										0x0069
VL53L1_SYSTEM__INTERMEASUREMENT_PERIOD =								0x006C
SYSTEM__THRESH_HIGH =													0x0072
SYSTEM__THRESH_LOW =													0x0074
SD_CONFIG__WOI_SD0 =													0x0078
SD_CONFIG__INITIAL_PHASE_SD0 =											0x007A
ROI_CONFIG__USER_ROI_CENTRE_SPAD =										0x007F
ROI_CONFIG__USER_ROI_REQUESTED_GLOBAL_XY_SIZE =							0x0080
SYSTEM__SEQUENCE_CONFIG =												0x0081
VL53L1_SYSTEM__GROUPED_PARAMETER_HOLD =									0x0082
SYSTEM__INTERRUPT_CLEAR =												0x0086
SYSTEM__MODE_START =													0x0087
VL53L1_RESULT__RANGE_STATUS =											0x0089
VL53L1_RESULT__DSS_ACTUAL_EFFECTIVE_SPADS_SD0 =							0x008C
RESULT__AMBIENT_COUNT_RATE_MCPS_SD =									0x0090
VL53L1_RESULT__FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0 =					0x0096
VL53L1_RESULT__PEAK_SIGNAL_COUNT_RATE_CROSSTALK_CORRECTED_MCPS_SD0 =	0x0098
VL53L1_RESULT__OSC_CALIBRATE_VAL =										0x00DE
VL53L1_FIRMWARE__SYSTEM_STATUS =										0x00E5
VL53L1_IDENTIFICATION__MODEL_ID =										0x010F
VL53L1_ROI_CONFIG__MODE_ROI_CENTRE_SPAD =								0x013E

_VL53L1X_DEFAULT_DEVICE_ADDRESS =										0x52

_DEFAULT_NAME = "Qwiic 4m Distance Sensor (ToF)"

_FULL_ADDRESS_LIST = list(range(0x08,0x77+1))					# Full I2C Address List (excluding resrved addresses)
_FULL_ADDRESS_LIST.remove(_VL53L1X_DEFAULT_DEVICE_ADDRESS >> 1) # Remove Default Address of VL53L1X from list
_AVAILABLE_I2C_ADDRESS = [_VL53L1X_DEFAULT_DEVICE_ADDRESS >> 1]	# Initialize with Default Address of VL53L1X
_AVAILABLE_I2C_ADDRESS.extend(_FULL_ADDRESS_LIST)				# Add Full Range of I2C Addresses


# From vL53l1x_class.cpp C++ File

ALGO__PART_TO_PART_RANGE_OFFSET_MM =									0x001E
MM_CONFIG__INNER_OFFSET_MM =											0x0020
MM_CONFIG__OUTER_OFFSET_MM = 											0x0022

# DEBUG_MODE

VL51L1X_DEFAULT_CONFIGURATION = [
0x00,	# 0x2d
0x01,	# 0x2e
0x01,	# 0x2f
0x01,	# 0x30
0x02,	# 0x31
0x00,	# 0x32
0x02,	# 0x33
0x08,	# 0x34
0x00,	# 0x35
0x08,	# 0x36
0x10,	# 0x37
0x01,	# 0x38
0x01,	# 0x39
0x00,	# 0x3a
0x00,	# 0x3b
0x00,	# 0x3c
0x00,	# 0x3d
0xff,	# 0x3e
0x00,	# 0x3f
0x0F,	# 0x40
0x00,	# 0x41
0x00,	# 0x42
0x00,	# 0x43
0x00,	# 0x44
0x00,	# 0x45
0x20,	# 0x46
0x0b,	# 0x47
0x00,	# 0x48
0x00,	# 0x49
0x02,	# 0x4a
0x0a,	# 0x4b
0x21,	# 0x4c
0x00,	# 0x4d
0x00,	# 0x4e
0x05,	# 0x4f
0x00,	# 0x50
0x00,	# 0x51
0x00,	# 0x52
0x00,	# 0x53
0xc8,	# 0x54
0x00,	# 0x55
0x00,	# 0x56
0x38,	# 0x57
0xff,	# 0x58
0x01,	# 0x59
0x00,	# 0x5a
0x08,	# 0x5b
0x00,	# 0x5c
0x00,	# 0x5d
0x01,	# 0x5e
0xdb,	# 0x5f
0x0f,	# 0x60
0x01,	# 0x61
0xf1,	# 0x62
0x0d,	# 0x63
0x01,	# 0x64
0x68,	# 0x65
0x00,	# 0x66
0x80,	# 0x67
0x08,	# 0x68
0xb8,	# 0x69
0x00,	# 0x6a
0x00,	# 0x6b
0x00,	# 0x6c
0x00,	# 0x6d
0x0f,	# 0x6e
0x89,	# 0x6f
0x00,	# 0x70
0x00,	# 0x71
0x00,	# 0x72
0x00,	# 0x73
0x00,	# 0x74
0x00,	# 0x75
0x00,	# 0x76
0x01,	# 0x77
0x0f,	# 0x78
0x0d,	# 0x79
0x0e,	# 0x7a
0x0e,	# 0x7b
0x00,	# 0x7c
0x00,	# 0x7d
0x02,	# 0x7e
0xc7,	# 0x7f
0xff,	# 0x80
0x9B,	# 0x81
0x00,	# 0x82
0x00,	# 0x83
0x00,	# 0x84
0x01,	# 0x85
0x00,	# 0x86
0x00	# 0x87
]

# From vL53l1_error_codes.h Header File
###############################################################################
###############################################################################
# Error Code definitions for VL53L1 API.
#=======================================================================
# PRIVATE define do not edit
#=======================================================================

# VL53L1_define_Error_group Error and Warning code returned by API
# The following DEFINE are used to identify the PAL ERROR

VL53L1_ERROR_NONE =															  0
VL53L1_ERROR_CALIBRATION_WARNING =											 -1
# """Warning invalid calibration data may be in used
# 	\a VL53L1_InitData()
# 	\a VL53L1_GetOffsetCalibrationData
# 	\a VL53L1_SetOffsetCalibrationData"""
VL53L1_ERROR_MIN_CLIPPED =													 -2
# """Warning parameter passed was clipped to min before to be applied"""

VL53L1_ERROR_UNDEFINED =													 -3
# """Unqualified error"""
VL53L1_ERROR_INVALID_PARAMS =												 -4
# """Parameter passed is invalid or out of range"""
VL53L1_ERROR_NOT_SUPPORTED =												 -5
# """Function is not supported in current mode or configuration"""
VL53L1_ERROR_RANGE_ERROR =													 -6
# """Device report a ranging error interrupt status"""
VL53L1_ERROR_TIME_OUT =														 -7
# """Aborted due to time out"""
VL53L1_ERROR_MODE_NOT_SUPPORTED =											 -8
# """Asked mode is not supported by the device"""
VL53L1_ERROR_BUFFER_TOO_SMALL =												 -9
# """..."""
VL53L1_ERROR_COMMS_BUFFER_TOO_SMALL =										-10
# """Supplied buffer is larger than I2C supports"""
VL53L1_ERROR_GPIO_NOT_EXISTING =											-11
# """User tried to setup a non-existing GPIO pin"""
VL53L1_ERROR_GPIO_FUNCTIONALITY_NOT_SUPPORTED =								-12
# """unsupported GPIO functionality"""
VL53L1_ERROR_CONTROL_INTERFACE =											-13
# """error reported from IO functions"""
VL53L1_ERROR_INVALID_COMMAND =												-14
# """The command is not allowed in the current device state (power down)"""
VL53L1_ERROR_DIVISION_BY_ZERO =												-15
# """In the function a division by zero occurs"""
VL53L1_ERROR_REF_SPAD_INIT =												-16
# """Error during reference SPAD initialization"""
VL53L1_ERROR_GPH_SYNC_CHECK_FAIL =											-17
# """GPH sync interrupt check fail - API out of sync with device"""
VL53L1_ERROR_STREAM_COUNT_CHECK_FAIL =										-18
# """Stream count check fail - API out of sync with device"""
VL53L1_ERROR_GPH_ID_CHECK_FAIL =											-19
# """GPH ID check fail - API out of sync with device"""
VL53L1_ERROR_ZONE_STREAM_COUNT_CHECK_FAIL =									-20
# """Zone dynamic config stream count check failed - API out of sync"""
VL53L1_ERROR_ZONE_GPH_ID_CHECK_FAIL =										-21
# """Zone dynamic config GPH ID check failed - API out of sync"""

VL53L1_ERROR_XTALK_EXTRACTION_NO_SAMPLE_FAI =								-22
# """Thrown when run_xtalk_extraction fn has 0 succesful samples when using
# the full array to sample the xtalk. In this case there is not enough
# information to generate new Xtalk parm info. The function will exit and
# leave the current xtalk parameters unaltered"""
VL53L1_ERROR_XTALK_EXTRACTION_SIGMA_LIMIT_FAIL =							-23
# """Thrown when run_xtalk_extraction fn has found that the avg sigma
# estimate of the full array xtalk sample is > than the maximal limit
# allowed. In this case the xtalk sample is too noisy for measurement.
# The function will exit and leave the current xtalk parameters unaltered."""


VL53L1_ERROR_OFFSET_CAL_NO_SAMPLE_FAIL =									-24
# """Thrown if there one of stages has no valid offset calibration
# samples. A fatal error calibration not valid"""
VL53L1_ERROR_OFFSET_CAL_NO_SPADS_ENABLED_FAIL =								-25
# """Thrown if there one of stages has zero effective SPADS Traps the case
# when MM1 SPADs is zero. A fatal error calibration not valid"""
VL53L1_ERROR_ZONE_CAL_NO_SAMPLE_FAIL =										-26
# """Thrown if then some of the zones have no valid samples. A fatal error
# calibration not valid"""
VL53L1_ERROR_TUNING_PARM_KEY_MISMATCH =										-27
# """Thrown if the tuning file key table version does not match with
# expected value. The driver expects the key table version to match the 
# compiled default version number in the define
# #VL53L1_TUNINGPARM_KEY_TABLE_VERSION_DEFAULT*"""
VL53L1_WARNING_REF_SPAD_CHAR_NOT_ENOUGH_SPADS =								-28
# """Thrown if there are less than 5 good SPADs are available."""
VL53L1_WARNING_REF_SPAD_CHAR_RATE_TOO_HIGH =								-29
# """Thrown if the final reference rate is greater than the upper reference
# rate limit - default is 40 Mcps. Implies a minimum Q3 (x10) SPAD (5)
# selected"""
VL53L1_WARNING_REF_SPAD_CHAR_RATE_TOO_LOW =									-30
# """Thrown if the final reference rate is less than the lower reference
# rate limit - default is 10 Mcps. Implies maximum Q1 (x1) SPADs selected"""


VL53L1_WARNING_OFFSET_CAL_MISSING_SAMPLES =									-31
# """Thrown if there is less than the requested number of valid samples."""
VL53L1_WARNING_OFFSET_CAL_SIGMA_TOO_HIGH =									-32
# """Thrown if the offset calibration range sigma estimate is greater than
# 8.0 mm. This is the recommended min value to yield a stable offset
# measurement"""
VL53L1_WARNING_OFFSET_CAL_RATE_TOO_HIGH =									-33
# """Thrown when VL53L1_run_offset_calibration() peak rate is greater than
# that 50.0Mcps. This is the recommended max rate to avoid pile-up
# influencing the offset measurement"""
VL53L1_WARNING_OFFSET_CAL_SPAD_COUNT_TOO_LOW =								-34
# """Thrown when VL53L1_run_offset_calibration() when one of stages range
# has less that 5.0 effective SPADS. This is the recommended min value to
# yield a stable offset"""


VL53L1_WARNING_ZONE_CAL_MISSING_SAMPLES =									-35
# """Thrown if one of more of the zones have less than the requested number
# of valid samples"""
VL53L1_WARNING_ZONE_CAL_SIGMA_TOO_HIGH =									-36
# """Thrown if one or more zones have sigma estimate value greater than
# 8.0 mm. This is the recommended min value to yield a stable offset
# measurement"""
VL53L1_WARNING_ZONE_CAL_RATE_TOO_HIGH =										-37
# """Thrown if one of more zones have peak rate higher than that 50.0Mcps.
# This is the recommended max rate to avoid pile-up influencing the offset
# measurement"""


VL53L1_WARNING_XTALK_MISSING_SAMPLES =										-38
# """Thrown to notify that some of the xtalk samples did not yield valid
# ranging pulse data while attempting to measure the xtalk signal in
# vl53l1_run_xtalk_extract(). This can signify any of the zones are missing
# samples, for further debug information the xtalk_results struct should be
# referred to. This warning is for notification only, the xtalk pulse and
# shape have still been generated"""
VL53L1_WARNING_XTALK_NO_SAMPLES_FOR_GRADIENT =								-39
# """Thrown to notify that some of teh xtalk samples used for gradient
# generation did not yield valid ranging pulse data while attempting to
# measure the xtalk signal in vl53l1_run_xtalk_extract(). This can signify
# that any one of the zones 0-3 yielded no successful samples. The
# xtalk_results struct should be referred to for further debug info. This
# warning is for notification only, the xtalk pulse and shape have still
# been generated."""
VL53L1_WARNING_XTALK_SIGMA_LIMIT_FOR_GRADIENT =								-40
# """Thrown to notify that some of the xtalk samples used for gradient
# generation did not pass the sigma limit check while attempting to
# measure the xtalk signal in vl53l1_run_xtalk_extract(). This can signify
# that any one of the zones 0-3 yielded an avg sigma_mm value > the limit.
# The xtalk_results struct should be referred to for further debug info.
# This warning is for notification only, the xtalk pulse and shape have
# still been generated."""
VL53L1_ERROR_NOT_IMPLEMENTED =												-41
# """Tells requested functionality has not been implemented yet or not
# compatible with the device"""
VL53L1_ERROR_PLATFORM_SPECIFIC_START =										-60
# """Tells the starting code for platform

# _VL53L1_ERROR_CODES_H_

# 	Class representing a VL53L1 sensor component
class QwiicVL53L1X(object):
	# Software Version Information
	VL53L1X_IMPLEMENTATION_VER_MAJOR=		1
	VL53L1X_IMPLEMENTATION_VER_MINOR=		0
	VL53L1X_IMPLEMENTATION_VER_SUB=			1
	VL53L1X_IMPLEMENTATION_VER_REVISION=	0000

	#----------------------------------------------
	# Device Name:
	device_name = _DEFAULT_NAME

	#----------------------------------------------
	# Available Addresses:
	available_addresses = _AVAILABLE_I2C_ADDRESS

	#----------------------------------------------
	# Constructor
	def __init__(self, address = None, debug = None, i2c_driver = None):
		"""!
		This method initializes the class object. If no 'address' or
		'i2c_driver' are inputed or 'None' is specified, the method will
		use the defaults.

		@param address: The I2C address to use for the device.
							If not provided, the method will default to
							the first address in the
							'available_addresses' list.
								Default = 0x29
		@param debug: Designated whether or not to print debug
							statements.
							0-	Don't print debug statements
							1-	Print debug statements
		@param i2c_driver: An existing i2c driver object. If not
							provided a driver object is created from the
							'qwiic_i2c' I2C driver of the SparkFun Qwiic
							library.
		"""

		# Did the user specify an I2C address?
		# Defaults to 0x52 if unspecified.
		self.address = address if address != None else self.available_addresses[0]

		# Load the I2C driver if one isn't provided
		if i2c_driver == None:
			self._i2c = qwiic_i2c.getI2CDriver()
	
			if self._i2c == None:
				print("Unable to load I2C driver for this platform.")
				return
		else:
			self._i2c = i2c_driver


		# Do you want debug statements?
		if debug == None:
			self.debug = 0	# Debug Statements Disabled
		else:
			self.debug = debug	# Debug Statements Enabled (1)


	def _begin(self):
		"""!
		One time device initialization

		@return 	0 on success
					#CALIBRATION_WARNING if failed
		
		"""
		return self.sensor_init()


	def _read_id(self):
		"""!
		Read function of the ID device. (Verifies id ID matches factory number).

		@return 	 0- Correct
					-1- Failure
		
		"""
		if (self.get_sensor_id() == 0xEEAC):
			return 0
		return -1


	def get_distance(self):
		"""!
		This function returns the distance measured by the sensor in mm

		@return **Integer** Distance measured by the sensor in mm
		"""
		self.status = 0
		distance = self.__i2cRead(self.address,
				VL53L1_RESULT__FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0, 2)

		return distance


	def init_sensor(self, address):
		"""!
		Initialize the sensor with default values

		@param address: Device address

		@return 	0 on Success
		
		"""
		self.status = 0
		sensorState = 0
		# VL53L1_Off()
		# VL53L1_On()
		self.status = self.set_i2c_address(address)
	
		if self.debug == 1:
			byteData = self.__i2cRead(self.address, 0x010F, 1)
			print("VL53L1X Model_ID: %s", byteData)

			byteData = self.__i2cRead(self.address, 0x0110, 1)
			print("VL53L1X Module_Type: %s", byteData)

			wordData = self.__i2cRead(self.address, 0x010F, 2)
			print("VL53L1X: %s", wordData)
	
	
		while (not sensorState and not self.status):
			sensorState = self.boot_state()
			time.sleep(2/1000)
		
		if (not self.status):
			self.status = self.sensor_init()
	
		return self.status



	# VL53L1X_api.h functions
	###############################################################################
	###############################################################################

	def get_sw_version(self):
		"""!
		This function returns the SW driver version

		@return **List** [major, minor, build, revision] numbers
		"""
		self.status = 0
		major = self.VL53L1X_IMPLEMENTATION_VER_MAJOR
		minor = self.VL53L1X_IMPLEMENTATION_VER_MINOR
		build = self.VL53L1X_IMPLEMENTATION_VER_SUB
		revision = self.VL53L1X_IMPLEMENTATION_VER_REVISION

		return [major, minor, build, revision]



	def set_i2c_address(self, new_address):
		"""!
		This function sets the sensor I2C address used in case multiple devices application, default address **0x29** (0x52 >> 1)

		@param new_address: I2C address to change device to
		"""
		self.status = 0

		self.status = self.__i2cWrite(self.address, VL53L1_I2C_SLAVE__DEVICE_ADDRESS, new_address, 1)
		self.address = new_address
		
		return self.status

	def sensor_init(self):
		"""!
		This function loads the 135 bytes default values to initialize the sensor.

		@return **Integer** 0 on success or error code
		
		"""
		self.status = 0
		Addr = 0x00
		tmp = 0
		timeout = 0

		for Addr in range(0x2D, 0x87 + 1):
			self.status = self.__i2cWrite(self.address, Addr, VL51L1X_DEFAULT_CONFIGURATION[Addr - 0x2D], 1)
		
		self.status = self.start_ranging()
		while(tmp == 0):
				tmp = self.check_for_data_ready()
				timeout = timeout + 1
				if (timeout > 50):
					self.status = VL53L1_ERROR_TIME_OUT
					return self.status
		
		tmp = 0
		self.status = self.clear_interrupt()
		self.status = self.stop_ranging()
		self.status = self.__i2cWrite(self.address, VL53L1_VHV_CONFIG__TIMEOUT_MACROP_LOOP_BOUND, 0x09, 1) #  two bounds VHV
		self.status = self.__i2cWrite(self.address, 0x0B, 0, 1) #  start VHV from the previous temperature
		
		return self.status


	def clear_interrupt(self):
		"""!
		This function clears the interrupt, to be called after a ranging data reading to arm the interrupt for the next data ready event.
		"""
		self.status = 0
		self.status = self.__i2cWrite(self.address, SYSTEM__INTERRUPT_CLEAR, 0x01, 1)

		return self.status


	def set_interrupt_polarity(self, NewPolarity):
		"""!
		This function programs the interrupt polarity

		@param **Integer** NewPolarity: 1 = active high (default), 0 = active low
		"""
		self.status = 0
		Temp = self.__i2cRead(self.address, GPIO_HV_MUX__CTRL, 1)

		Temp = Temp & 0xEF
		self.status = self.__i2cWrite(self.address, GPIO_HV_MUX__CTRL, Temp | (not (NewPolarity & 1)) << 4, 1)

		return self.status


	def get_interrupt_polarity(self):
		"""!
		This function returns the current interrupt polarity

		@return **Integer** 1 = active high (**default**), 0 = active low
		"""
		self.status = 0
		Temp = self.__i2cRead(self.address, GPIO_HV_MUX__CTRL, 1)
		Temp = Temp & 0x10
		pInterruptPolarity = not (Temp >> 4)

		return pInterruptPolarity


	def start_ranging(self):
		"""!
		This function starts the ranging distance operation
		The ranging operation is continuous. The clear interrupt has to be done after each get data to allow the interrupt to raise when the next data is ready
		1=active high (**default**), 0=active low, use set_interrupt_polarity() to change the interrupt polarity if required.
		"""
		self.status = 0
		self.status = self.__i2cWrite(self.address, SYSTEM__MODE_START, 0x40, 1)	#  Enable VL53L1X

		return self.status


	def stop_ranging(self):
		"""!
		This function stops the ranging.
		"""
		self.status = 0
		self.status = self.__i2cWrite(self.address, SYSTEM__MODE_START, 0x00, 1)	#  Disable VL53L1X

		return self.status


	def check_for_data_ready(self):
		"""!
		This function checks if the new ranging data is available by polling the dedicated register.

		@return **Integer** 1 if new data is ready, 0 if not
		"""
		self.status = 0

		IntPol = self.get_interrupt_polarity()
		Temp = self.__i2cRead(self.address, GPIO__TIO_HV_STATUS, 1)
		
		# Read in the register to check if a new value is available
		if (self.status == 0):
			if ((Temp & 1) == IntPol):
				isDataReady = 1
			else:
				isDataReady = 0
		
		return isDataReady


	def set_timing_budget_in_ms(self, TimingBudgetInMs):
		"""!
		This function programs the timing budget in ms.

		@param TimingBudgetInMs: Predefined values = 15, 20, 33, 50, 100 (**default**), 200, 500.
		"""
		self.status = 0

		DM = self.get_distance_mode()
		if (DM == 0):
			return 1
		elif (DM == 1):	# Short DistanceMode
			if TimingBudgetInMs == 15: # only available in short distance mode
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x01D, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x0027, 2)
			elif TimingBudgetInMs == 20:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x0051, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x006E, 2)
			elif TimingBudgetInMs == 33:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x00D6, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x006E, 2)
			elif TimingBudgetInMs == 50:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x1AE, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x01E8, 2)
			elif TimingBudgetInMs == 100:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x02E1, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x0388, 2)
			elif TimingBudgetInMs == 200:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x03E1, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x0496, 2)
			elif TimingBudgetInMs == 500:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x0591, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x05C1, 2)
			else:
				self.status = 1
			
		else:
			if TimingBudgetInMs == 20:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x001E, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x0022, 2)
			elif TimingBudgetInMs == 33:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x0060, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x006E, 2)
			elif TimingBudgetInMs == 50:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x00AD, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x00C6, 2)
			elif TimingBudgetInMs == 100:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x01CC, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x01EA, 2)
			elif TimingBudgetInMs == 200:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x02D9, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x02F8, 2)
			elif TimingBudgetInMs == 500:
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 0x048F, 2)
				self.__i2cWrite(self.address, RANGE_CONFIG__TIMEOUT_MACROP_B_HI, 0x04A4, 2)
			else:
				self.status = 1
		
		return self.status


	def get_timing_budget_in_ms(self):
		"""!
		This function returns the current timing budget in ms.
		"""
		self.status = 0

		Temp = self.__i2cRead(self.address, RANGE_CONFIG__TIMEOUT_MACROP_A_HI, 2)

		def get_timing_budget_in_ms_switch(var):
			switcher = {
				0x001D:15,
				0x0051:20,
				0x001E:20,
				0x00D6:33,
				0x0060:33,
				0x1AE :50,
				0x00AD:50,
				0x02E1:100,
				0x01CC:100,
				0x03E1:200,
				0x02D9:200,
				0x0591:500,
				0x048F:500}
			return switcher.get(var,0)

		pTimingBudget = get_timing_budget_in_ms_switch(Temp)

		return pTimingBudget


	def set_distance_mode(self, DM):
		"""!
		This function programs the distance mode (1=short, 2=long(default)).

		@param Integer DM: Distance Mode
			* 1- Short mode max distance is limited to 1.3 m but better ambient immunity
			* 2- Long mode can range up to 4 m in the dark with 200 ms timing budget (**default**)
		"""
		self.status = 0

		TB = self.get_timing_budget_in_ms()
		if DM == 1:
			self.status = self.__i2cWrite(self.address, PHASECAL_CONFIG__TIMEOUT_MACROP, 0x14, 1)
			self.status = self.__i2cWrite(self.address, RANGE_CONFIG__VCSEL_PERIOD_A, 0x07, 1)
			self.status = self.__i2cWrite(self.address, RANGE_CONFIG__VCSEL_PERIOD_B, 0x05, 1)
			self.status = self.__i2cWrite(self.address, RANGE_CONFIG__VALID_PHASE_HIGH, 0x38, 1)
			self.status = self.__i2cWrite(self.address, SD_CONFIG__WOI_SD0, 0x0705, 2)
			self.status = self.__i2cWrite(self.address, SD_CONFIG__INITIAL_PHASE_SD0, 0x0606, 2)
		elif DM == 2:
			self.status = self.__i2cWrite(self.address, PHASECAL_CONFIG__TIMEOUT_MACROP, 0x0A, 1)
			self.status = self.__i2cWrite(self.address, RANGE_CONFIG__VCSEL_PERIOD_A, 0x0F, 1)
			self.status = self.__i2cWrite(self.address, RANGE_CONFIG__VCSEL_PERIOD_B, 0x0D, 1)
			self.status = self.__i2cWrite(self.address, RANGE_CONFIG__VALID_PHASE_HIGH, 0xB8, 1)
			self.status = self.__i2cWrite(self.address, SD_CONFIG__WOI_SD0, 0x0F0D, 2)
			self.status = self.__i2cWrite(self.address, SD_CONFIG__INITIAL_PHASE_SD0, 0x0E0E, 2)
		else:
			if self.debug == 1:
				print("Invalid DIstance Mode")

		self.status = self.set_timing_budget_in_ms(TB)
		return self.status


	def get_distance_mode(self):
		"""!
		This function returns the current distance mode (1=short, 2=long).

		@return **Integer** Distance Mode
			* 1- Short mode max distance is limited to 1.3 m but better ambient immunity
			* 2- Long mode can range up to 4 m in the dark with 200 ms timing budget (**default**)
		"""
		self.status = 0

		TempDM = self.__i2cRead(self.address,PHASECAL_CONFIG__TIMEOUT_MACROP, 1)
		if (TempDM == 0x14):
			DM=1
		if(TempDM == 0x0A):
			DM=2
		return DM


	def set_inter_measurement_in_ms(self, InterMeasMs):
		"""!
		This function programs the Intermeasurement period in ms.

		@param InterMeasMs: Intermeasurement period must be >/= timing budget. This condition is not checked by the API,
							the customer has the duty to check the condition. **Default = 100 ms**
		"""
		self.status = 0

		ClockPLL = self.__i2cRead(self.address, VL53L1_RESULT__OSC_CALIBRATE_VAL, 2)
		ClockPLL = ClockPLL&0x3FF

		self.status = self.__i2cWrite(self.address, VL53L1_SYSTEM__INTERMEASUREMENT_PERIOD,
				int(ClockPLL * InterMeasMs * 1.075), 4)

		return self.status


	def get_inter_measurement_in_ms(self):
		"""!
		This function returns the Intermeasurement period in ms.

		@return **Integer** Intermeasurement period in ms
		"""
		tmp = 0
		ClockPLL = 0
		pIM = 0

		tmp = self.__i2cRead(self.address, VL53L1_SYSTEM__INTERMEASUREMENT_PERIOD, 4)
		ClockPLL = self.__i2cRead(self.address, VL53L1_RESULT__OSC_CALIBRATE_VAL, 2)
		ClockPLL = ClockPLL&0x3FF
		pIM= (tmp/(ClockPLL*1.065))

		return pIM


	def boot_state(self):
		"""!
		This function returns the boot state of the device (1:booted, 0:not booted)

		@return **Integer** Boot state
			* 1- booted
			* 0- not booted
		"""
		self.status = 0
		state = 0

		state = self.__i2cRead(self.address,VL53L1_FIRMWARE__SYSTEM_STATUS, 1)

		return state


	def get_sensor_id(self):
		"""!
		This function returns the sensor id, sensor Id must be 0xEEAC

		@return **Integer** Sensor ID
		"""
		self.status = 0
		sensorId = 0

		sensorId = self.__i2cRead(self.address, VL53L1_IDENTIFICATION__MODEL_ID, 2)

		return sensorId


	def get_signal_per_spad(self):
		"""!
		This function returns the returned signal per SPAD in kcps/SPAD (kcps stands for Kilo Count Per Second).

		@return 	Signal per SPAD (Kilo Count Per Second/SPAD).
		
		"""
		self.status = 0
		SpNb=1

		signal = self.__i2cRead(self.address,
			VL53L1_RESULT__PEAK_SIGNAL_COUNT_RATE_CROSSTALK_CORRECTED_MCPS_SD0, 2)
		SpNb = self.__i2cRead(self.address,
			VL53L1_RESULT__DSS_ACTUAL_EFFECTIVE_SPADS_SD0, 2)
		signalRate = (2000.0*signal/SpNb)

		return signalRate


	def get_ambient_per_spad(self):
		"""!
		This function returns the ambient per SPAD in kcps/SPAD

		@return 	Ambient per SPAD
		
		"""
		self.status = 0
		SpNb=1

		AmbientRate = self.__i2cRead(self.address, RESULT__AMBIENT_COUNT_RATE_MCPS_SD, 2)
		SpNb = self.__i2cRead(self.address, VL53L1_RESULT__DSS_ACTUAL_EFFECTIVE_SPADS_SD0, 2)
		ambPerSp=(2000.0 * AmbientRate / SpNb)
		
		return ambPerSp


	def get_signal_rate(self):
		"""!
		This function returns the returned signal in kcps.

		@return 	signal in kcps
		
		"""
		self.status = 0
		tmp = self.__i2cRead(self.address,
			VL53L1_RESULT__PEAK_SIGNAL_COUNT_RATE_CROSSTALK_CORRECTED_MCPS_SD0, 2)
		signal = tmp*8
		
		return signal


	def get_spad_nb(self):
		"""!
		This function returns the current number of enabled SPADs

		@return 	Number of enabled SPADs
		
		"""
		self.status = 0
		tmp = self.__i2cRead(self.address,
					VL53L1_RESULT__DSS_ACTUAL_EFFECTIVE_SPADS_SD0, 2)
		spNb = tmp >> 8
		
		return spNb


	def get_ambient_rate(self):
		"""!
		This function returns the ambient rate in kcps

		@return 	Ambient rate in kcps
		
		"""
		self.status = 0
		tmp = self.__i2cRead(self.address, RESULT__AMBIENT_COUNT_RATE_MCPS_SD, 2)
		ambRate = tmp*8
		
		return ambRate


	def get_range_status(self):
		"""!
		This function returns the ranging status error

		@return 	Ranging status error

						* 0- no error
						* 1- sigma failed
						* 2- signal failed
						* 7- wrap-around
		"""
		self.status = 0
		RgSt = self.__i2cRead(self.address, VL53L1_RESULT__RANGE_STATUS, 1)
		RgSt = RgSt&0x1F

		def get_range_status_switch(var):
			switcher = {
				9:0,
				6:1,
				4:2,
				8:3,
				5:4,
				3:5,
				19:6,
				7:7,
				12:9,
				18:10,
				22:11,
				23:12,
				13:13}
			return switcher.get(var,255)
		
		rangeStatus = get_range_status_switch(RgSt)

		return rangeStatus


	def set_offset(self, OffsetValue):
		"""!
		This function programs the offset correction in mm

		@param OffsetValue: The offset correction value to program in mm
		"""
		self.status = 0
		Temp = OffsetValue*4

		self.__i2cWrite(self.address, ALGO__PART_TO_PART_RANGE_OFFSET_MM,
				Temp, 2)
		self.__i2cWrite(self.address, MM_CONFIG__INNER_OFFSET_MM, 0x0, 2)
		self.__i2cWrite(self.address, MM_CONFIG__OUTER_OFFSET_MM, 0x0, 2)

		return self.status


	def get_offset(self):
		"""!
		This function returns the programmed offset correction value in mm

		@return **Integer** Offset correction value in mm
		"""
		self.status = 0
		Temp = self.__i2cRead(self.address,ALGO__PART_TO_PART_RANGE_OFFSET_MM, 2)
		Temp = Temp << 3
		Temp = Temp >> 5
		offset = Temp

		return offset


	def set_xtalk(self, XtalkValue):
		"""!
		This function programs the xtalk correction value in cps (Count Per Second).
		This is the number of photons reflected back from the cover glass in cps.

		@param XTalkValue: xtalk correction value in count per second to avoid float type
		"""
		self.status = 0
		
		self.status = self.__i2cWrite(self.address,
				ALGO__CROSSTALK_COMPENSATION_X_PLANE_GRADIENT_KCPS,
				0x0000, 2)
		self.status = self.__i2cWrite(self.address, ALGO__CROSSTALK_COMPENSATION_Y_PLANE_GRADIENT_KCPS,
				0x0000, 2)
		self.status = self.__i2cWrite(self.address, ALGO__CROSSTALK_COMPENSATION_PLANE_OFFSET_KCPS,
				(XtalkValue << 9)/1000, 2) # << 9 (7.9 format) and /1000 to convert cps to kpcs
		
		return self.status


	def get_xtalk(self):
		"""!
		This function returns the current programmed xtalk correction value in cps

		@return 	xtalk correction value in cps
		
		"""
		self.status = 0
		tmp = self.__i2cRead(self.address,ALGO__CROSSTALK_COMPENSATION_PLANE_OFFSET_KCPS, 2)
		xtalk = (tmp*1000) >> 9 # 1000 to convert kcps to cps and >> 9 (7.9 format)

		return xtalk


	def set_distance_threshold(self,
					ThreshLow,
					ThreshHigh, Window,
					IntOnNoTarget):
		"""!
		This function programs the threshold detection mode

		@param mm ThreshLow: The threshold under which one the device raises an interrupt if Window = 0
		@param mm ThreshHigh: The threshold above which one the device raises an interrupt if Window = 1
		@param Window: Window detection mode:
										* 0- below
										* 1- above
										* 2- out
										* 3- in
		@param IntOnNoTarget: 1 (No longer used - just set to 1)

		Example:
			* self.set_distance_threshold(100,300,0,1): Below 100 
			* self.set_distance_threshold(100,300,1,1): Above 300 
			* self.set_distance_threshold(100,300,2,1): Out of window 
			* self.set_distance_threshold(100,300,3,1): In window
		"""
		self.status = 0
		Temp = 0

		Temp = self.__i2cRead(self.address, SYSTEM__INTERRUPT_CONFIG_GPIO, 1)
		Temp = Temp & 0x47
		if (IntOnNoTarget == 0):
			self.status = self.__i2cWrite(self.address, SYSTEM__INTERRUPT_CONFIG_GPIO,
					(Temp | (Window & 0x07)), 1)
		else:
			self.status = self.__i2cWrite(self.address, SYSTEM__INTERRUPT_CONFIG_GPIO,
					((Temp | (Window & 0x07)) | 0x40), 1)
		
		self.status = self.__i2cWrite(self.address, SYSTEM__THRESH_HIGH, ThreshHigh, 2)
		self.status = self.__i2cWrite(self.address, SYSTEM__THRESH_LOW, ThreshLow, 2)
		
		return self.status


	def get_distance_threshold_window(self):
		"""!
		This function returns the window detection mode (0=below 1=above 2=out 3=in)

		@return **Integer** Window detection mode
			* 0- below
			* 1- above
			* 2- out
			* 3- in
		"""
		self.status = 0
		tmp = self.__i2cRead(self.address,SYSTEM__INTERRUPT_CONFIG_GPIO, 1)
		window = (tmp & 0x7)
		
		return window


	def get_distance_threshold_low(self):
		"""!
		This function returns the low threshold in mm

		@return **Integer** Low threshold in mm
		"""
		self.status = 0
		low = self.__i2cRead(self.address,SYSTEM__THRESH_LOW, 2)
		
		return low


	def get_distance_threshold_high(self):
		"""!
		This function returns the high threshold in mm

		@return **Integer** High threshold in mm
		"""
		self.status = 0
		high = self.__i2cRead(self.address,SYSTEM__THRESH_HIGH, 2)
		
		return high


	def set_roi(self, X, Y, OpticalCenter = 199):
		"""!
		This function programs the ROI (Region of Interest). The height and width of the ROI (X, Y) are set in SPADs; the smallest acceptable ROI size = 4 (4 x 4). The optical center is set based on table below.
		To set the center, use the pad that is to the right and above (i.e. upper right of) the exact center of the region you'd like to measure as your optical center.

		Table of Optical Centers:
		
			128,136,144,152,160,168,176,184,  192,200,208,216,224,232,240,248
			129,137,145,153,161,169,177,185,  193,201,209,217,225,233,241,249
			130,138,146,154,162,170,178,186,  194,202,210,218,226,234,242,250
			131,139,147,155,163,171,179,187,  195,203,211,219,227,235,243,251
			132,140,148,156,164,172,180,188,  196,204,212,220,228,236,244,252
			133,141,149,157,165,173,181,189,  197,205,213,221,229,237,245,253
			134,142,150,158,166,174,182,190,  198,206,214,222,230,238,246,254
			135,143,151,159,167,175,183,191,  199,207,215,223,231,239,247,255
			
			127,119,111,103,095,087,079,071,  063,055,047,039,031,023,015,007
			126,118,110,102,094,086,078,070,  062,054,046,038,030,022,014,006
			125,117,109,101,093,085,077,069,  061,053,045,037,029,021,013,005
			124,116,108,100,092,084,076,068,  060,052,044,036,028,020,012,004
			123,115,107,099,091,083,075,067,  059,051,043,035,027,019,011,003
			122,114,106,098,090,082,074,066,  058,050,042,034,026,018,010,002
			121,113,105,097,089,081,073,065,  057,049,041,033,025,017,009,001
			120,112,104,096,088,080,072,064,  056,048,040,032,024,016,008,0 Pin 1
			
			(Each SPAD has a number which is not obvious.)

		@param X: ROI Width
		@param Y: ROI Height
		@param OpticalCenter: The pad that is to the upper right of the exact center of the ROI (see table above). (default=199)
		"""
		self.status = 0
		# OpticalCenter =self.__i2cRead(self.address, VL53L1_ROI_CONFIG__MODE_ROI_CENTRE_SPAD, 1)
		if (X > 16):
			X = 16
		if (Y > 16):
			Y = 16
		if (X > 10 or Y > 10):
			OpticalCenter = 199

		self.status = self.__i2cWrite(self.address, ROI_CONFIG__USER_ROI_CENTRE_SPAD, OpticalCenter, 1)
		self.status = self.__i2cWrite(self.address, ROI_CONFIG__USER_ROI_REQUESTED_GLOBAL_XY_SIZE,
				(Y - 1) << 4 | (X - 1), 1)
		
		return self.status


	def get_roi_xy(self):
		"""!
		This function returns width X and height Y

		@return **List** Region of Interest Width (X) and Height (Y)
		"""
		self.status = 0
		tmp = self.__i2cRead(self.address,ROI_CONFIG__USER_ROI_REQUESTED_GLOBAL_XY_SIZE, 1)
		ROI_X = (tmp & 0x0F) + 1
		ROI_Y = ((tmp & 0xF0) >> 4) + 1

		return [ROI_X, ROI_Y]


	def set_signal_threshold(self, Signal):
		"""!
		This function programs a new signal threshold in kcps (default=1024 kcps)

		@param Signal: Signal threshold in kcps (**default=1024 kcps**)
		"""
		self.status = 0

		self.__i2cWrite(self.address,RANGE_CONFIG__MIN_COUNT_RATE_RTN_LIMIT_MCPS,Signal >> 3, 2)
		
		return self.status


	def get_signal_threshold(self):
		"""!
		This function returns the current signal threshold in kcps

		@return 	Signal threshold in kcps
		
		"""
		self.status = 0
		tmp = self.__i2cRead(self.address,
					RANGE_CONFIG__MIN_COUNT_RATE_RTN_LIMIT_MCPS, 2)
		signal = tmp << 3
		return signal


	def set_sigma_threshold(self, Sigma):
		"""!
		This function programs a new sigma threshold in mm (default=15 mm)

		@param Sigma: Sigma threshold in mm (**default=15 mm**)
		"""
		self.status = 0

		if(Sigma>(0xFFFF >> 2)):
			return 1
		
		# 16 bits register 14.2 format
		self.status = self.__i2cWrite(self.address,RANGE_CONFIG__SIGMA_THRESH,Sigma << 2, 2)

		return self.status


	def get_sigma_threshold(self):
		"""!
		This function returns the current sigma threshold in mm

		@return **Integer** Sigma threshold in mm
		"""
		self.status = 0
		
		tmp = self.__i2cRead(self.address,RANGE_CONFIG__SIGMA_THRESH, 2)
		sigma = tmp >> 2

		return sigma


	def start_temperature_update(self):
		"""!
		This function performs the temperature calibration.
		It is recommended to call this function any time the temperature might have changed by more than 8 deg C
		without sensor ranging activity for an extended period.
		"""
		self.status = 0
		tmp=0

		self.status = self.__i2cWrite(self.address,VL53L1_VHV_CONFIG__TIMEOUT_MACROP_LOOP_BOUND,0x81, 1) #  full VHV
		self.status = self.__i2cWrite(self.address,0x0B,0x92, 1)
		self.status = self.start_ranging()
		while(tmp==0):
			tmp = self.check_for_data_ready()
		
		tmp = 0
		self.status = self.clear_interrupt()
		self.status = self.stop_ranging()
		self.status = self.__i2cWrite(self.address, VL53L1_VHV_CONFIG__TIMEOUT_MACROP_LOOP_BOUND, 0x09, 1) #  two bounds VHV
		self.status = self.__i2cWrite(self.address, 0x0B, 0, 1) #  start VHV from the previous temperature

		return self.status



	# VL53L1X_calibration.h functions
	###############################################################################
	###############################################################################

	def calibrate_offset(self, TargetDistInMm):
		"""!
		This function performs the offset calibration.
		The function returns the offset value found and programs the offset compensation into the device.

		@param TargetDistInMm: * Target distance in mm, ST recommended 100 mm
								* Target reflectance = grey17%

		@return int status: 0 if no error, other if error
		"""
		tmp = 0
		AverageDistance = 0
		self.status = 0

		self.status = self.__i2cWrite(self.address, ALGO__PART_TO_PART_RANGE_OFFSET_MM, 0x0, 2)
		self.status = self.__i2cWrite(self.address, MM_CONFIG__INNER_OFFSET_MM, 0x0, 2)
		self.status = self.__i2cWrite(self.address, MM_CONFIG__OUTER_OFFSET_MM, 0x0, 2)
		self.status = self.start_ranging()	# Enable VL53L1X sensor
		for i in range(0, 50):
			while (tmp == 0):
				tmp = self.check_for_data_ready()
			
			tmp = 0
			distance = self.get_distance()
			self.status = self.clear_interrupt()
			AverageDistance = AverageDistance + distance
		
		self.status = self.stop_ranging()
		AverageDistance = AverageDistance / 50
		offset = TargetDistInMm - AverageDistance
		self.status = self.__i2cWrite(self.address, ALGO__PART_TO_PART_RANGE_OFFSET_MM, offset*4, 2)

		return self.status #,offset???


	def calibrate_xtalk(self, TargetDistInMm):
		"""!
		This function performs the xtalk calibration.
		The function returns the xtalk value found and programs the xtalk compensation to the device

		@param TargetDistInMm: Target distance in mm
		* The target distance is the distance where the sensor start to "under range" due to the influence of the photons reflected back from the cover glass becoming strong (also called the inflection point).
		* Target reflectance = grey 17%

		@return **int** status: 0 if no error, other if error				
		"""
		tmp= 0
		AverageSignalRate = 0
		AverageDistance = 0
		AverageSpadNb = 0
		distance = 0
		self.status = 0

		self.status = self.__i2cWrite(self.address, 0x0016,0, 2)
		self.status = self.start_ranging()
		for i in range(0, 50):
			while (tmp == 0):
				tmp = self.check_for_data_ready()
			
			tmp=0
			sr= self.get_signal_rate()
			distance= self.get_distance()
			self.status = self.clear_interrupt()
			AverageDistance = AverageDistance + distance
			spadNum = self.get_spad_nb()
			AverageSpadNb = AverageSpadNb + spadNum
			AverageSignalRate =	AverageSignalRate + sr
		
		self.status = self.stop_ranging()
		AverageDistance = AverageDistance / 50
		AverageSpadNb = AverageSpadNb / 50
		AverageSignalRate = AverageSignalRate / 50
		# Calculate Xtalk value
		xtalk = (512*(AverageSignalRate*(1-(AverageDistance/TargetDistInMm)))/AverageSpadNb)
		self.status = self.__i2cWrite(self.address, 0x0016, xtalk, 2)
		
		return self.status #,xtalk???


###############################################################################
###############################################################################

# protected:

	def __get_tick_count(self):
		"""!
		Returns current tick count in [ms]
		"""
		self.status = VL53L1_ERROR_NONE

		# ptick_count_ms = timeGetTime()
		ptick_count_ms = 0

		return ptick_count_ms


	def __wait_us(self, wait_us):
		time.sleep(wait_us/1000/1000)
		return VL53L1_ERROR_NONE


	def __wait_ms(self, wait_ms):
		time.sleep(wait_ms/1000)
		return VL53L1_ERROR_NONE
	

	def __wait_value_mask_ex(self, timeout_ms, index, value, mask, poll_delay_ms):
		"""!
		Platform implementation of ```WaitValueMaskEx``` V2WReg script command
		"""

		self.status	 = VL53L1_ERROR_NONE
		start_time_ms	= 0
		current_time_ms	= 0
		polling_time_ms	= 0
		byte_value		= 0
		found			= 0



		# calculate time limit in absolute time

		start_time_ms = self.__get_tick_count()

		# remember current trace functions and temporarily disable function logging

		# wait until value is found, timeout reached on error occurred

		while ((self.status == VL53L1_ERROR_NONE) and
			(polling_time_ms < timeout_ms) and
			(found == 0)):

			if (self.status == VL53L1_ERROR_NONE):
				byte_value = self.__i2cRead(self.address, index, 1)

			if ((byte_value & mask) == value):
				found = 1

			if (self.status == VL53L1_ERROR_NONE and
				found == 0 and
				poll_delay_ms > 0):
				self.status = self.__wait_ms(poll_delay_ms)

			# Update polling time (Compare difference rather than absolute to negate 32bit wrap around issue)
			current_time_ms = self.__get_tick_count()
			polling_time_ms = current_time_ms - start_time_ms

		if (found == 0 and self.status == VL53L1_ERROR_NONE):
			self.status = VL53L1_ERROR_TIME_OUT

		return self.status


# Write and read functions for I2C
###############################################################################
###############################################################################

	def __i2cWrite(self, address, register, data, nbytes):
		"""!
		A wrapper for the I2C driver since device needs 16-bit register addresses. Formats register and data values so that they can be written to device as a block for proper I2C transactions.

		@param register: 16-bit register address
							(can be 8-bit, just writes 0x00 byte prior to value)
		@param data: Data to be set in register
							(should be 4, 2, or 1 bytes in length)
		@param nbytes: number of bytes in data (*to be set*)
							(needs to be specified as python passes in integer value, but device expects a specific nuber of bytes for that value)

		@return **Boolean** status- (*self*) Indicator for I2C transaction success???
		"""
		
		registerMSB = register >> 8
		registerLSB = register & 0xFF

		buffer = [registerLSB]

		if nbytes == 4:
			buffer.append( (data >> 24) & 0xFF )
			buffer.append( (data >> 16) & 0xFF )
			buffer.append( (data >>  8) & 0xFF )
			buffer.append( (data >>  0) & 0xFF )
		elif nbytes == 2:
			buffer.append( (data >>  8) & 0xFF )
			buffer.append( (data >>  0) & 0xFF )
		elif nbytes == 1:
			buffer.append( data )
		else:
			if self.debug == 1:
				print("in __i2cWriteBlock, nbytes entered invalid")
			
			return
		
		self.status = self._i2c.writeBlock(address, registerMSB, buffer)

		return self.status
	

	def __i2cRead(self, address, register, nbytes):
		"""!
		A wrapper for the I2C driver since device needs 16-bit register addresses. Formats register and data values so that they can be written to device as a block for proper I2C transactions.

		@param register: 16-bit register address
							(can be 8-bit, just writes 0x00 byte prior to value)
		@param nbytes: number of bytes in data (*to be read*)
							(needs to be specified for transaction)

		@return **integer** data
		"""
		
		data = 0
		registerMSB = register >> 8
		registerLSB = register & 0xFF

		if nbytes not in [1, 2, 4]:
			if self.debug == 1:
				print("in __i2cWriteBlock, nbytes entered invalid")
			return

		# Setup for read/write transactions on smbus 2
		# write = self.i2c_custom.write(address, [registerMSB, registerLSB])	# Write part of transaction
		# read = self.i2c_custom.read(address, nbytes)						# Read part of transaction

		# self._i2c.i2c_rdwr(write, read)
		# read_data = self._i2c.__i2c_rdwr__(address, [registerMSB, registerLSB], nbytes)
		read_data = self._i2c.write_read_block(address, [registerMSB, registerLSB], nbytes)
		buffer = list(read_data)

		for i in range(0, nbytes):
			data = ( buffer[ (nbytes - 1) - i ] << (i*8) ) + data

		#for i, val in enumerate(read):
		#	data = ( val << (i*8) ) + data

		return data
