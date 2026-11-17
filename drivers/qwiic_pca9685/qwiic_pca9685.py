#-----------------------------------------------------------------------
# SparkFun PCA9685 Python Library
#-----------------------------------------------------------------------
#
# Written by SparkFun Electronics, June 2019
# Author: Wes Furuya
#
# Compatibility:
#	* Original: https://www.sparkfun.com/products/14328
#	* v2: https://www.sparkfun.com/products/15316
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on Pi Servo Hat, check out the product page
# linked above.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http:www.gnu.org/licenses/>.
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

"""!
qwiic_pca9685
===============
Python module for the `SparkFun Pi Servo HAT <https://www.sparkfun.com/products/14328>` and `SparkFun Servo pHAT for Raspberry Pi <https://www.sparkfun.com/products/15316>`
This package should be used in conjunction with the i2c_driver package contained in the `SparkFun qwiic Python Package <https://github.com/sparkfun/Qwiic_Py>`
"""

# Load Necessary Modules:
#----------------------------------------------
import time						# Time access and conversion package
import math						# Basic math package
import qwiic_i2c				# I2C bus driver package

# Device Name:
#----------------------------------------------
_DEFAULT_NAME = "Qwiic PCA9685"

# Device Address:
#----------------------------------------------
"""!
Some devices have multiple available addresses - this is a list of these
addresses.
NOTE: The first address in this list is considered the default I2C
address for the device.

According to the datasheet, the I2C address for the PCA9865 chip is
hardware selectable, with 64 options (7-bit: 1000 000 to 1111 111);
excluding the Software Reset (0000 0110) and LED All Call (1110 000),
leaving a maximum of 62 addresses.

	Reserved Addresses:
		All Call Address = 			0x70			(7-bit: 1110 000X or E0h)
		General Call Address = 		0x00			(Part of I2C Protocol)

	Reserved Addresses (Optional):
		Sub Call Address 1 = 		0x71			(7-bit: 1110 001X or E2h)
		Sub Call Address 2 = 		0x72			(7-bit: 1110 010X or E4h)
		Sub Call Address 3 = 		0x74			(7-bit: 1110 100X or E8h)
		10-bit Addressing Scheme = 	0x78 to 0x7B

	Reserved Addresses (I2C Protocol):
		General Call Address = 		0x00			(7-bit: 0000 000)
		CBUS Address = 				0x01			(not listed in Datasheet)
		Alternative Bus Format =	0x02			(not listed in Datasheet)
		Future Use = 				0x03			(7-bit: 0000 011)
		Hs-mode Master Code = 		0x04 to 0x07	(7-bit: 0000 1XX)
		10-bit Addressing Scheme = 	0x78 to 0x7B	(7-bit: 1111 0XX)
		Future Use = 				0x7C to 0x7F	(7-bit: 1111 1XX)

	NOTE: I'm not sure how NXP got to 62 as the Software Reset address
	doesn't fall in the available options. Additionally, it is a command
	bit sent after the General Call Address. (Let me know if you
	figure this out, so I can comment this library properly.)
"""
_AVAILABLE_I2C_ADDRESS = list(range(0x40,0x7F+1))		# Full Address List

# Special Use Addresses:
_gcAddr =		0x00 	# General Call address for software reset
_acAddr =		0x70	# All Call address- used for modifications to
						# multiple PCA9685 chips regardless of their
						# I2C address set by hardware pins (A0 to A5).
_subAddr_1 =	0x71	# 1110 001X or 0xE2 (7-bit)
_subAddr_2 =	0x72	# 1110 010X or 0xE4 (7-bit)
_subAddr_3 =	0x74	# 1110 100X or 0xE8 (7-bit)


# Software Reset "Address":
#----------------------------------------------
"""!
Used when a reset needs to be performed by the master.

NOTE: Used with General Call address... more like a command
"""
_SWRST =	0x06 	# Equivalent of reset byte 0000 011

# Registers:
#----------------------------------------------
"""!
List of available registers and their functions

According to the datasheet, these registers are access by the 'Control
Register', which acts as a pointer register. The control register takes
the following format:

[D7 D6 D5 D4 D3 D2 D1 D0]

Reset State = 00h

To list all available registers:
list(range(69+1)) + list(range(250, 255+1))
Auto Increment past register 69 will point to MODE1 register (register
0). Auto Increment also works from register 250 to register 254, then
rolls over to register 0.
"""

MODE1 = 			0x00	# Mode register 1
MODE2 = 			0x01	# Mode register 2
SUBADR1 = 			0x02	# I2C subaddress 1
SUBADR2 = 			0x03	# I2C subaddress 2
SUBADR3 = 			0x04	# I2C subaddress 3
ALLCALLADR = 		0x05	# LED All Call I2C adress

LED0_ON_L =			0X06	# LED0 output and brightness control byte 0
LED0_ON_H = 		0X07	# LED0 output and brightness control byte 1
LED0_OFF_L = 		0X08	# LED0 output and brightness control byte 2
LED0_OFF_H = 		0X09	# LED0 output and brightness control byte 3

ALL_LED_ON_L = 		0XFA	# ALL_LED output and brightness control byte 0
# ALL_LED_ON_H = 		0XFB	# ALL_LED output and brightness control byte 1
ALL_LED_OFF_L = 	0XFC	# ALL_LED output and brightness control byte 2
# ALL_LED_OFF_H = 	0XFD	# ALL_LED output and brightness control byte 3

PRE_SCALE = 		0XFE	# Prescaler for PWM output frequency
_TESTMODE = 		0xFF	# Defines test mode to be entered (Should not be used!)

# LED1_ON_L = 		0X0A	# LED1 output and brightness control byte 0
# LED1_ON_H = 		0X0B	# LED1 output and brightness control byte 1
# LED1_OFF_L = 		0X0C	# LED1 output and brightness control byte 2
# LED1_OFF_H = 		0X0D	# LED1 output and brightness control byte 3

# LED2_ON_L = 		0X0E	# LED2 output and brightness control byte 0
# LED2_ON_H = 		0X0F	# LED2 output and brightness control byte 1
# LED2_OFF_L = 		0X10	# LED2 output and brightness control byte 2
# LED2_OFF_H = 		0X11	# LED2 output and brightness control byte 3

# LED3_ON_L = 		0X12	# LED3 output and brightness control byte 0
# LED3_ON_H = 		0X13	# LED3 output and brightness control byte 1
# LED3_OFF_L = 		0X14	# LED3 output and brightness control byte 2
# LED3_OFF_H = 		0X15	# LED3 output and brightness control byte 3

# LED4_ON_L = 		0X16	# LED4 output and brightness control byte 0
# LED4_ON_H = 		0X17	# LED4 output and brightness control byte 1
# LED4_OFF_L = 		0X18	# LED4 output and brightness control byte 2
# LED4_OFF_H = 		0X19	# LED4 output and brightness control byte 3

# LED5_ON_L = 		0X1A	# LED5 output and brightness control byte 0
# LED5_ON_H = 		0X1B	# LED5 output and brightness control byte 1
# LED5_OFF_L = 		0X1C	# LED5 output and brightness control byte 2
# LED5_OFF_H = 		0X1D	# LED5 output and brightness control byte 3

# LED6_ON_L = 		0X1E	# LED6 output and brightness control byte 0
# LED6_ON_H = 		0X1F	# LED6 output and brightness control byte 1
# LED6_OFF_L = 		0X20	# LED6 output and brightness control byte 2
# LED6_OFF_H = 		0X21	# LED6 output and brightness control byte 3

# LED7_ON_L = 		0X22	# LED7 output and brightness control byte 0
# LED7_ON_H = 		0X23	# LED7 output and brightness control byte 1
# LED7_OFF_L = 		0X24	# LED7 output and brightness control byte 2
# LED7_OFF_H = 		0X25	# LED7 output and brightness control byte 3

# LED8_ON_L = 		0X26	# LED8 output and brightness control byte 0
# LED8_ON_H = 		0X27	# LED8 output and brightness control byte 1
# LED8_OFF_L = 		0X28	# LED8 output and brightness control byte 2
# LED8_OFF_H = 		0X29	# LED8 output and brightness control byte 3

# LED9_ON_L = 		0X2A	# LED9 output and brightness control byte 0
# LED9_ON_H = 		0X2B	# LED9 output and brightness control byte 1
# LED9_OFF_L = 		0X2C	# LED9 output and brightness control byte 2
# LED9_OFF_H = 		0X2D	# LED9 output and brightness control byte 3

# LED10_ON_L = 		0X2E	# LED10 output and brightness control byte 0
# LED10_ON_H = 		0X2F	# LED10 output and brightness control byte 1
# LED10_OFF_L = 	0X30	# LED10 output and brightness control byte 2
# LED10_OFF_H = 	0X31	# LED10 output and brightness control byte 3

# LED11_ON_L = 		0X32	# LED11 output and brightness control byte 0
# LED11_ON_H = 		0X33	# LED11 output and brightness control byte 1
# LED11_OFF_L = 	0X34	# LED11 output and brightness control byte 2
# LED11_OFF_H = 	0X35	# LED11 output and brightness control byte 3

# LED12_ON_L = 		0X36	# LED12 output and brightness control byte 0
# LED12_ON_H = 		0X37	# LED12 output and brightness control byte 1
# LED12_OFF_L = 	0X38	# LED12 output and brightness control byte 2
# LED12_OFF_H = 	0X39	# LED12 output and brightness control byte 3

# LED13_ON_L = 		0X3A	# LED13 output and brightness control byte 0
# LED13_ON_H = 		0X3B	# LED13 output and brightness control byte 1
# LED13_OFF_L = 	0X3C	# LED13 output and brightness control byte 2
# LED13_OFF_H = 	0X3D	# LED13 output and brightness control byte 3

# LED14_ON_L = 		0X3E	# LED14 output and brightness control byte 0
# LED14_ON_H = 		0X3F	# LED14 output and brightness control byte 1
# LED14_OFF_L = 	0X40	# LED14 output and brightness control byte 2
# LED14_OFF_H = 	0X41	# LED14 output and brightness control byte 3

# LED15_ON_L = 		0X42	# LED15 output and brightness control byte 0
# LED15_ON_H = 		0X43	# LED15 output and brightness control byte 1
# LED15_OFF_L = 	0X44	# LED15 output and brightness control byte 2
# LED15_OFF_H = 	0X45	# LED15 output and brightness control byte 3


# PWM Channels
#----------------------------------------------
"""!
This device has multiple PWM channels - this is a list of these
channels.
NOTE: The first address in this list is considered the default PWM
channel for the device.

The variable 'pwm_channels' can be modified for chip sets with similar
operations.
"""
pwm_channels = 16
_AVAILABLE_PWM_CHANNELS = list(range(pwm_channels))		# Full List of PWM Channels


# SparkFun PCA9685 Class/Object
#-----------------------------------------------------------------------
class QwiicPCA9685(object):
	"""!
		SparkFunPCA9685
	Initialise the PCA9685 chip at ``address`` with ``i2c_driver``.

		@param address: The I2C address to use for the device.
							If not provided, the default address is
							used.
		@param i2c_driver: An existing i2c driver object. If not
							provided a driver object is created.

		@return **Bool** Constructor Initialization
							True-	Successful
							False-	Issue loading I2C driver
		"""
	#----------------------------------------------
	# Device Name:
	device_name = _DEFAULT_NAME

	#----------------------------------------------
	# Available Addresses:
	available_addresses = _AVAILABLE_I2C_ADDRESS

	#----------------------------------------------
	# Available Channels:
	available_pwm_channels = _AVAILABLE_PWM_CHANNELS

	#----------------------------------------------
	# Constructor
	def __init__(self, address = None, debug = None, i2c_driver = None):
		"""!
		This method initializes the class object. If no 'address' or
		'i2c_driver' are inputted or 'None' is specified, the method will
		use the defaults.

		@param address: The I2C address to use for the device.
							If not provided, the method will default to
							the first address in the
							'available_addresses' list.
								Default = 0x40
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
		# Defaults to 0x40 if unspecified.
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


#=======================================================================
# Secondary Functions
#=======================================================================

	#----------------------------------------------
	# Reads the value of a specific bit in the byte
	def __readBit__(self, byte, bit_number):
		"""!
		This method returns the value of a specific bit in a byte.

		@param byte: Integer or Hex value.
		@param bit_number: The index number of the bit you are
							interested in, starting from LSB = 0 to MSB = 7.

		@return **Integer** Value of bit at bit_number location. (0 or 1)

			:example:
				byte = 0x12 (HEX), 12h, or 16 (DEC)
				Binary:	0001 0010
				index:	7654 3210
				        |       |
				       MSB	   LSB
				bit_number = 4
				returns: 1
		"""
		if (bit_number < 0) or (bit_number > 7):
			# Debug Message: 
			if self.debug == 1:
				print("Bit number is outside the bounds of a byte")
			return 0

		# Returns the value of the bit
		mask = 1 << bit_number
		return (byte & mask) >> bit_number

	#----------------------------------------------
	# Writes a value to a specific bit in the byte
	def __writeBit__(self, byte, bit_number, value):
		"""!
		This method modifies a specific bit in a byte, with a specified
		value.

		@param byte: Integer or Hex value.
		@param bit_number: The index number of the bit you are
							interested in, starting from LSB = 0.
		@param value: Value to be set at specific bit location (0
							or 1).

		@return **Integer** Value of modified byte

			:example:
				Original Byte:
				byte =	0x12 (HEX), 12h, or 16
				Binary:	0001 0010
				index:	7654 3210
				        |       |
				       MSB	   LSB
				Change:
				bit_number =	4
				value =			0
				Output Byte:
				returns:		2
				Binary:	0000 0010
		"""
		if value not in [0, 1]:
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Value must be 0 or 1.")
			return byte
		
		if bit_number < 0 or bit_number > 7:
			# Debug Message: 
			if self.debug == 1:
				print("Bit number is outside the bounds of a byte.")
			return byte
			
		# Returns modified byte
		return (byte & ~(1 << bit_number)) | (value << bit_number)

	#----------------------------------------------
	# Checks I2C connection
	def is_connected(self):
		"""!
		This method checks if the "i2c_driver" can connect to the device
		at the specified or default address.

		@return **Bool** Device Connection
					True-	Successful
					False-	Can't find device
		"""

		return qwiic_i2c.isDeviceConnected(self.address)


	#----------------------------------------------
	# Checks Value of Address Bits
	def get_addr_bit(self, addr_bit = None):
		"""!
		Reads the value of a specified address bit in MODE 1 register.

		@param addr_bit: Specify address bit.
							0-	ALLCALL Bit (Default)
							1-	SUB1 Bit
							2-	SUB2 Bit
							3-	SUB3 Bit

		@return **Integer** Value of specified address bit.
							0-	Normal Mode
							1-	Low Power Mode; Oscillator Off.
								(Default)
		"""
		
		# Read MODE1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		if addr_bit == None:				# If no input for addr_bit, sets to ALLCALL
			get_addr_bit = 0				# ALLCALL bit
		elif addr_bit < 0 or addr_bit > 3:	# Checks for valid input
			# Debug Message: 
			if self.debug == 1:
				print("Invalid addr_bit input. Selecting ALLCALL bit.")
			get_addr_bit = 0				# ALLCALL bit
		else:								# Use input 'addr_bit'
			get_addr_bit = addr_bit

		# Reads specified address bit in MODE1.
		addrMode = self.__readBit__(mode1, get_addr_bit)

		return addrMode

	#----------------------------------------------
	# Writes Value to Address Bits
	def set_addr_bit(self, addr_bit, value):
		"""!
		Writes the value to a specified address bit in MODE 1 register.

		@param addr_bit: Specify address bit.
							0-	ALLCALL Bit
							1-	SUB1 Bit
							2-	SUB2 Bit
							3-	SUB3 Bit
		@param value: Specify address bit.
							0-	Disables specified address (Default on
								SUB1, SUB2, SUB3)
							1-	Enables specified address (Default on
								ALLCALL)
		"""
		
		# Read MODE1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		# Checks for valid input
		if addr_bit < 0 or addr_bit > 3:
			# Debug Message: 
			if self.debug == 1:
				print("Invalid addr_bit input.")
			return #False
		else:							# Use input 'addr_bit'
			set_addr_bit = addr_bit

		if value != 0 and value != 1:	# Checks for valid input
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input.")
			return #False
		else:							# Use input 'value'
			set_value = value

		# Writes to specified address bit in MODE1.
		addrMode = self.__writeBit__(mode1, set_addr_bit, set_value)
		self._i2c.writeByte(self.address, MODE1, addrMode)

	
	#----------------------------------------------
	# Checks Value of SLEEP Bit
	def get_sleep_bit(self):
		"""!
		Reads the value of SLEEP bit in MODE 1 register. When enabled, it
		the chip there is no PWM control.

		@return **Integer** Value of SLEEP bit.
					0-	Normal Mode
					1-	Low Power Mode; Oscillator Off. (Default)
		"""
		
		# Read MODE1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		sleep_bit = 4 # Fifth bit in register

		# Reads SLEEP bit in MODE1.
		sleepMode = self.__readBit__(mode1, sleep_bit)

		return sleepMode

	#----------------------------------------------
	# Writes Value to SLEEP Bit
	def set_sleep_bit(self, value = None):
		"""!
		Changes the value of SLEEP bit in MODE 1 register.

		@param value: Value to set SLEEP bit.
						0-	Normal Mode
						1-	Low Power Mode; Oscillator Off. (Default)
		"""
		
		# Read MODE1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		sleep_bit = 4 # Fifth bit in register

		if value == None:				# If no input value, sets to default value
			set_value = 1				# Default
		elif value != 0 and value != 1:	# Checks for valid input
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Setting to default value (1 = Low Power Mode; Oscillator Off).")
			set_value = 1				# Default
		else:							# Use input 'value'
			set_value = value
		
		# Writes 'value' to the SLEEP bit in the MODE 1 register
		sleepMode = self.__writeBit__(mode1, sleep_bit, set_value)
		self._i2c.writeByte(self.address, MODE1, sleepMode)


	#----------------------------------------------
	# Checks Value of AI Bit
	def get_auto_increment_bit(self):
		"""!
		Reads the value of AI bit in MODE 1 register. When enabled, it
		allows users to write of multiple bytes (i.e. words).

		@return **Integer** Value of AI bit.
					0-	Auto-Increment Disabled (Default)
					1-	Auto-Increment Enabled
		"""

		# Read MODE1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		ai_bit = 5 # Sixth bit in register

		# Reads AI bit in MODE1.
		aiMode = self.__readBit__(mode1, ai_bit)

		return aiMode


	#----------------------------------------------
	# Writes Value to AI Bit
	def set_auto_increment_bit(self, value = None):
		"""!
		Changes value of AI bit in MODE 1 register. When enabled, it
		allows users to write of multiple bytes (i.e. words).

		@param value: Value to set AI bit.
						0-	Auto-Increment Disabled (Default)
						1-	Auto-Increment Enabled
		"""

		# Read MODE1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		ai_bit = 5 # Sixth bit in register

		if value == None:				# If no input value, sets to default value
			set_value = 0				# Default
		elif value != 0 and value != 1:	# Checks for valid input
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Setting to default value (0- Auto-Increment Disabled).")
			set_value = 0				# Default
		else:							# Use input 'value'
			set_value = value

		# Writes 'value' to the AI bit in the MODE 1 register
		aiMode = self.__writeBit__(mode1, ai_bit, set_value)
		self._i2c.writeByte(self.address, MODE1, aiMode)


	#----------------------------------------------
	# Checks Value of EXTCLK Bit
	def get_extclock_bit(self):
		"""!
		Reads the value of EXTCLK bit in MODE 1 register. When enabled, it
		allows for an external clock signal. It also affects the refresh
		rate:

				                       EXTCLK
				refresh_rate = ----------------------
				                4096 x (prescale +1)

		@return **Integer** Value of EXTCLK bit.
					0-	Use Internal Clock (Default)
					1-	Use EXTCLK Pin Clock.

		NOTE: This bit is a "sticky bit", that is, it cannot be cleared
		by writing a logic 0 to it. The EXTCLK can only be cleared by a
		power cycle or software reset.
		"""

		# Read MODE1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		extclk_bit = 6 # Seventh bit in register

		# Reads EXTCLK bit in MODE1.
		extclkMode = self.__readBit__(mode1, extclk_bit)

		return extclkMode


	#----------------------------------------------
	# Checks Value of RESTART Bit
	def get_restart_bit(self):
		"""!
		Reads the value of RESTART bit in MODE 1 register.

		@return **Integer** Value of Restart Mode bit.
					0-	Restart Disabled (Default)
					1-	Restart Enabled
		"""
		
		# Reads MODE 1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		rs_bit = 7 # Eighth bit in register

		# Reads the RESTART bit from the MODE 1 register
		rsMode = self.__readBit__(mode1, rs_bit)

		# Returns the RESTART bit value
		return rsMode

	#----------------------------------------------
	# Writes Value to RESTART Mode Bit
	def write_restart_bit(self, value = None):
		"""!
		Writes values to RESTART bit in MODE 1 register.

		@param value: Value to write to Restart Mode bit.
							0 or 1

		@return **Integer** Value of RESTART bit after changes.
							0- Restart Disabled (Default)
							1- Restart Enabled

		NOTE: Value aren't set, just written. The bit is set by the
		state of the chip and its current operation.
		"""

		# Reads MODE 1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		rs_bit = 7 # Eighth bit in register

		if value == None:				# If no input value
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input.")
			# value = 0 # Default
		elif value != 0 and value != 1:	# Checks for valid input
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input.")
			# value = 0 # Default
		else:
			rsMode = self.__writeBit__(mode1, rs_bit, value)
			self._i2c.writeByte(self.address, MODE1, rsMode)

		# Returns RESTART bit value
		return self.get_restart_bit()


	#----------------------------------------------
	# Checks Value of OUTNE Bits
	def get_outne_bits(self):
		"""!
		Reads the value of OUTNE bits in MODE 2 register. When the active
		LOW output (OE pin) is enabled, this setting allows users to
		enable or disable all the LED outputs at the same time.

		@return **Integer** Value of OUTNE bits. When OE = 1:
					0-		LEDn = 0
					1-		If OUTDRV = 1 then LEDn = 1
							If OUTDRV = 0 then LEDn = high-impedence
								(same as OUTNE[1:0] = b'10')
					2 to 3-	LEDn = high-impedence
		"""
		
		# Read MODE2 register
		mode2 = self._i2c.readByte(self.address, MODE2)

		# outne0_bit = 0 # First bit in register
		# outne1_bit = 1 # Second bit in register

		# Reads OUTNE bits in MODE2.
		outne_bits = mode2 & 3
		# outne0 = self.__readBit__(mode2, outne0_bit)
		# outne1 = self.__readBit__(mode2, outne1_bit)
		# outne_bits  = outne0 << 1 | outne1

		return outne_bits

	#----------------------------------------------
	# Writes Value to OUTNE Bits
	def set_outne_bit(self, value = None):
		"""!
		Reads the value of OUTNE bits in MODE 2 register. When the active
		LOW output (OE pin) is enabled, this setting allows users to
		enable or disable all the LED outputs at the same time.

		@param value: Value of OUTNE bits. When OE = 1:
						0-		LEDn = 0
						1-		If OUTDRV = 1 then LEDn = 1
								If OUTDRV = 0 then LEDn = high-impedence
									(same as OUTNE[1:0] = b'10')
						2 to 3-	LEDn = high-impedence

		@return **Bool** Function Operation
						True-	Successful
						False-	Issue in Execution
		"""
		
		# Read MODE2 register
		mode2 = self._i2c.readByte(self.address, MODE2)

		outne0_bit = 0 # First bit in register
		outne1_bit = 1 # Second bit in register

		if value == None:				# If no input value
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Set bit value.")
			return False
		elif value < 0 or value > 3:	# Checks for valid input
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Value outside bounds.")
			return False
		else:							# Use input 'value'
			set_value = value
		
		# Pulls 'values' to modify OUTNE bits
		outne0_val = (set_value & (1 << outne0_bit)) >> outne0_bit
		outne1_val = (set_value & (1 << outne1_bit)) >> outne1_bit

		# Writes to 'values' OUTNE bits in MODE2.
		outne_temp = self.__writeBit__(mode2, outne0_bit, outne0_val)
		outne_byte = self.__writeBit__(outne_temp, outne1_bit, outne1_val)
		self._i2c.writeByte(self.address, MODE2, outne_byte)

		return True


	#----------------------------------------------
	# Checks Value of OUTDRV Bit
	def get_outdrv_bit(self):
		"""!
		Reads the value of OUTDRV bit in MODE 2 register. Determines how the
		outputs are driven.

		@return **Integer** Value of OUTDRV bits.
					0-	Outputs are configured with an open-drain
						structure
					1-	Outputs are configured with a totem-pole
						structure
		"""
		
		# Read MODE2 register
		mode2 = self._i2c.readByte(self.address, MODE2)

		outdrv_bit = 2 # Third bit in register

		# Reads OUTDRV bit in MODE2.
		outdrvMode = self.__readBit__(mode2, outdrv_bit)

		return outdrvMode

	#----------------------------------------------
	# Writes Value to OUTDRV Bits
	def set_outdrv_bit(self, value = None):
		"""!
		Reads value of OUTDRV bits in MODE 2 register. Configures how
		the outputs are driven.

		@param value: Value of OUTDRV bits.
						0-	Outputs are configured with an open-drain
							structure
						1-	Outputs are configured with a totem-pole
							structure
		"""
		
		# Read MODE2 register
		mode2 = self._i2c.readByte(self.address, MODE2)

		outdrv_bit = 2 # Third bit in register

		if value == None:				# If no input value
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Set bit value.")
			return False
		elif value != 0 and value != 1:	# Checks for valid input
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Value outside bounds.")
			return False
		else:							# Use input 'value'
			set_value = value
		
		# Writes 'value' to the OUTDRV bit in the MODE 2 register
		outdrvMode = self.__writeBit__(mode2, outdrv_bit, set_value)
		self._i2c.writeByte(self.address, MODE2, outdrvMode)


	#----------------------------------------------
	# Checks Value of OCH Bit
	def get_och_bit(self):
		"""!
		Reads the value of OCH bit in MODE 2 register. Determines when the
		outputs change.

		@return **Integer** Value of OCH bits.
					0-	Outputs change on STOP command.
						NOTE: Change of the outputs at the STOP command
						allows synchronizing outputs of more than one
						PCA9685. Applicable to registers from 06h
						(LED0_ON_L) to 45h (LED15_OFF_H) only. 1 or more
						registers can be written, in any order, before
						STOP.
					1-	Outputs change on ACK.
						NOTE: Update on ACK requires all 4 PWM channel
						registers to be loaded before outputs will
						change on the last ACK.
		"""
		
		# Read MODE2 register
		mode2 = self._i2c.readByte(self.address, MODE2)

		och_bit = 3 # Forth bit in register

		# Reads OCH bit in MODE2.
		ochMode = self.__readBit__(mode2, och_bit)

		return ochMode

	#----------------------------------------------
	# Writes Value to OCH Bits
	def set_och_bit(self, value = None):
		"""!
		Reads the value of OCH bits in MODE 2 register. Configures when the
		outputs change.

		@param value: Value of OCH bits.
						0-	Outputs change on STOP command.
							NOTE: Change of the outputs at the STOP
							command allows synchronizing outputs of more
							than one PCA9685. Applicable to registers
							from 06h (LED0_ON_L) to 45h (LED15_OFF_H)
							only. 1 or more registers can be written,
							in any order, before STOP.
						1-	Outputs change on ACK.
							NOTE: Update on ACK requires all 4 PWM
							channel registers to be loaded before
							outputs will change on the last ACK.
		"""
		
		# Read MODE2 register
		mode2 = self._i2c.readByte(self.address, MODE2)

		och_bit = 3 # Forth bit in register

		if value == None:				# If no input value
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Set bit value.")
			return False
		elif value != 0 and value != 1:	# Checks for valid input
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Value outside bounds.")
			return False
		else:							# Use input 'value'
			set_value = value
		
		# Writes 'value' to the OCH bit in the MODE 2 register
		ochMode = self.__writeBit__(mode2, och_bit, set_value)
		self._i2c.writeByte(self.address, MODE2, ochMode)


	#----------------------------------------------
	# Checks Value of INVRT Bit
	def get_invrt_bit(self):
		"""!
		Reads the value of INVRT bit in MODE 2 register. Determines how the
		outputs are driven. See Section 7.7 "Using the PCA9685 with and
		without external drivers" of the datasheet.

		@return **Integer** Value of INVRT bits.
					0-	Outputs change on STOP command.
					1-	Outputs change on ACK.
		"""
		
		# Read MODE2 register
		mode2 = self._i2c.readByte(self.address, MODE2)

		invrt_bit = 4 # Fifth bit in register

		# Reads INVRT bit in MODE2.
		invrtMode = self.__readBit__(mode2, invrt_bit)

		return invrtMode

	#----------------------------------------------
	# Writes Value to INVRT bit
	def set_invrt_bit(self, value = None):
		"""!
		Configures value of INVRT bits in MODE 2 register. Configures
		how the outputs	are driven. See Section 7.7 "Using the PCA9685
		with and without external drivers" of the datasheet.

		@param value: Value of INVRT bits.
						0-	Outputs change on STOP command.
						1-	Outputs change on ACK.
		"""
		
		# Read MODE2 register
		mode2 = self._i2c.readByte(self.address, MODE2)

		invrt_bit = 4 # Fifth bit in register

		if value == None:				# If no input value
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Set bit value.")
			return False
		elif value != 0 and value != 1:	# Checks for valid input
			# Debug Message: 
			if self.debug == 1:
				print("Invalid value input. Value outside bounds.")
			return False
		else:							# Use input 'value'
			set_value = value
		
		# Writes 'value' to the INVRT bit in the MODE 2 register
		invrtMode = self.__writeBit__(mode2, invrt_bit, set_value)
		self._i2c.writeByte(self.address, MODE2, invrtMode)


	#----------------------------------------------
	# Checks Value of LED Channel Bytes
	def get_channel_word(self, channel = None, on_off = None):
		"""!
		Reads the ON/OFF timing for the specified PWM channel.

		@param channel: PWM channel.
						0 to 16
		@param on_off: On or Off setting.
						0-	OFF Start timing (end of ON timing)
						1-	ON Start timing (anything greater than 0 is
							considered a delay)

		@return  Word (2 bytes)

		NOTE: There are two 12-bit registers per LED output. Both
		registers will hold a value from 0 to 4095. One 12-bit register
		will hold a value for the ON time and the other 12-bit register
		will hold the value for the OFF time.

		The ON and OFF times are compared with the value of a 12-bit
		counter that will be running continuously from 0000h to 0FFFh (0
		to 4095 decimal).
		
		"""

		# Did the user specify a PWM channel?
		# Defaults to channel 0 if unspecified.
		self.channel = channel if channel != None else self.available_pwm_channels[0]

		channel_ON_L = LED0_ON_L + 4 * channel
		channel_OFF_L = LED0_OFF_L + 4 * channel

		# Enable word read/writes if not enabled
		if self.get_auto_increment_bit() != 1:
			self.set_auto_increment_bit(1)

		if on_off == None:
			return False
		elif on_off == 0:
			register = channel_OFF_L
		elif on_off == 1:
			register = channel_ON_L

		value = self._i2c.readWord(self.address, register)

		# Debug Message: 
		if self.debug == 1:
			print("Stored value is: %s" % value)

		return value

	
	#----------------------------------------------
	# Writes Value to INVRT LED Channel Bytes
	def set_channel_word(self, channel = None, on_off = None, value = None):
		"""!
		Configures the on/off timing for the specified PWM channel.

		@param channel: PWM channel.
						0 to 16
		@param on_off: ON/OFF setting.
						0-	OFF Start timing (end of ON timing)
						1-	ON Start timing (anything greater than 0 is
							considered a delay)
		@param value: Value to be entered into the ON/OFF 12-bit
						register for the specified LED output.
						Word (2 bytes)

		@return **Bool** Function Operation
					True-	Successful
					False-	Issue in Execution

		NOTE: There are two 12-bit registers per LED output. Both
		registers will hold a value from 0 to 4095. One 12-bit register
		will hold a value for the ON time and the other 12-bit register
		will hold the value for the OFF time.
		The ON and OFF times are compared with the value of a 12-bit
		counter that will be running continuously from 0000h to 0FFFh (0
		to 4095 decimal).
		"""

		# Did the user specify a PWM channel?
		# Defaults to channel 0 if unspecified.
		self.channel = channel if channel != None else self.available_pwm_channels[0]

		channel_ON_L = LED0_ON_L + 4 * channel
		channel_OFF_L = LED0_OFF_L + 4 * channel

		# Enable word read/writes if not enabled
		if self.get_auto_increment_bit() != 1:
			self.set_auto_increment_bit(1)

		if value < 0 or 4095 < value:
			# Debug Message: 
			if self.debug == 1:
				print("Error: Invalid input. Value out of bounds (Range = 0 - 4095).")
			# raise Exception("Error: Invalid input. Value out of bounds (Range = 0 - 4095). Entered value: %s" % value)
			return False

		if on_off == None:
			return False
		elif on_off == 0:
			register = channel_OFF_L
		elif on_off == 1:
			register = channel_ON_L

		self._i2c.writeWord(self.address, register, value)
		return True


#=======================================================================
# Primary Functions
#=======================================================================

	#----------------------------------------------
	# Begin
	# Check I2C connection and configures the MODE 1 register for
	# PWM control functions.
	def begin(self):
		"""!
		This method checks if there is an I2C connection then enables
		the Auto-Increment bit for the writing/reading of words (for the
		output timing).

		@return **Bool** Function Operation
					True-	Successful
					False-	Issue in Execution
		"""

		# //Check connection
		if self.is_connected() == False: 
			return False # I2C comm failure

		# Restart PCA9685? (leave out for now)

		# Enable Auto-Increment (Allows Writing of Words to PWM Channels)
		self.set_auto_increment_bit(1)

		return True


	#----------------------------------------------
	# Software Reset Call
	def soft_reset(self):
		"""!
		Software Reset Call: Allows all the devices in the I2C bus to
		be reset to the power-up state value through a specific
		formatted I2C bus command.

		 General Call Address
		        |    SWRST data byte 1
		Start   |            |      Stop
		 |      |            |       |
		[S][0000 0000][A][0000 0110][A][P]
		               |             |
		      Acknowledge from Slave |
		                    Acknowledge from Slave
		
		PCA9685 then resets to the default value (power-up value) and is
		ready to be addressed again within the specified bus free time.
		A failure or non-acknowledge from the PCA9685 (at any time)
		should be interpreted as an "SWRST Call Abort".
		"""
		
		self._i2c.writeCommand(_gcAddr, _SWRST)


	#----------------------------------------------
	# Restart
	def restart(self):
		"""!
		Restarts the PCA9685 after the soft reset. (Clears MODE1
		register.)
		"""
		
		self._i2c.writeByte(self.address, MODE1, 0x00)


	#----------------------------------------------
	# Read Prescale Value
	def get_pre_scale(self):
		"""!
		Reads the frequency at which the output are modulated. The
		prescale value is determined by Eq 1 (below).
		
		Eq 1:
		                              osc_clock
		prescale value = round(----------------------) - 1
		                        (4096 * update_rate)

		@return **Integer** prescale_value

		NOTE: Range: 24 Hz to 1526 Hz or (0x03 to 0xFF, Default: 0x1E =
		200Hz).
		"""
		# Reads value in PRE_SCALE register.
		prescale = self._i2c.readByte(self.address, PRE_SCALE)
				
		# Debug Message: 
		if self.debug == 1:
			# Print Pre-Scale Value
			print("Prescale value = %s" % prescale)
			
			# Calculate frequency based off internal clock frequency (default)
			est_frequency = float((25*10**6)/((prescale + 1)*4096))
			
			# Print Equivalent Frequency
			print("Est. frequency = %s Hz (*Based on internal clock value)" % int(est_frequency))

		return prescale


	#----------------------------------------------
	# Configure PWM Frequency
	def set_pre_scale(self, frequency = None, ext = None):
		"""!
		Configures the 'prescale_value', which defines the frequency at
		which the output are modulated. The prescale value is determined
		by Eq 1 (below). Additionally, the hardware enforces a minimum
		value that can be loaded into this register is '3'.
		
		Eq 1:
		                              osc_clock
		prescale value = round(----------------------) - 1
		                        (4096 * update_rate)

		@param frequency: PWM Frequency (Hz)
							Range: 24 to 1526 Hz
		@param ext: External Clock Frequency (Hz)
							Default = None; uses internal clock
							frequency (25 MHz)

		@return **Bool** Function Operation
					True-	Successful
					False-	Issue in Execution

		PWM Frequency Range:	24 Hz to 1526 Hz or (0x03 to 0xFF,
		Default: 0x1E = 200Hz)
		Internal Clock:			25 MHz (Default)
		"""
		# Read MODE1 register
		mode1 = self._i2c.readByte(self.address, MODE1)


		if frequency == None:
			# Set default frequency (200 Hz)
			pwmPreScale = 0x1E # Default

		elif frequency < 24 or 1526 < frequency: # Checks for valid input
			print("Invalid frequency input. Setting to the default value (200 Hz)")
			return False
		
		else:
			# 
			if ext != None:
				if 50 * 10**6 < ext: # Checks for valid input
					print("Invalid external clock frequency input.")
					return False
				else:
					# Uses user input
					osc_clock = ext
			# Uses internal clock frequency if set to None
			else:
				# Check if the internal or external clock is used
				# EXTCLK bit:
				# 	0 = Internal Clock (Default)
				# 	1 = External Clock Pin
				extMode = self.get_extclock_bit()

				if extMode == 1:
					print("External clock pin enabled.")						# Notifies users external clock is used	
					osc_clock = input("Enter external clock frequency (Hz): ")	# Prompts user input
					# return False
				elif extMode == 0:
					osc_clock = 25 * 10**6 # 25 MHz (Default)
				# else:
				# 	print("Error reading EXTCLK bit from MODE1 register.")
				# 	return False

		
		# Calculate prescale value
		pwmPreScale = round(float(osc_clock/(4096*frequency))) - 1
		
		# Writes 1 to SLEEP bit in MODE1 register.
		self.set_sleep_bit(1)

		# Writes prescale value to PRE_SCALE register.
		self._i2c.writeByte(self.address, PRE_SCALE, pwmPreScale)	
		
		# Resets MODE1 register to the original value.
		self._i2c.writeByte(self.address, MODE1, mode1)

		return True


	#----------------------------------------------
	# Clears RESTART Mode Bit
	def clear_restart_bit(self):
		"""!
		If RESTART bit is a logic 1, it clears RESTART bit in MODE 1
		register by writing a logic 1.

		@return **Integer** Value of RESTART bit after changes.
					0- Restart Disabled (Default)
					1- Restart Enabled

		NOTE: Other actions that will clear the RESTART bit are:
		1.	Power cycle.
		2.	I2C Software Reset command.
		3.	If the MODE2 OCH bit is logic 0, write to any PWM register
			then issue an I2C-bus STOP.
		4.	If the MODE2 OCH bit is logic 1, write to all four PWM
			registers in any PWM channel.
		Likewise, if the user does an orderly shutdown [1] of all the
		PWM channels before	setting the SLEEP bit, the RESTART bit will
		be cleared. If this is done the contents of all PWM registers
		are invalidated and must be reloaded before reuse.
		[1] Two methods can be used to do an orderly shutdown. The
		fastest is to write a logic 1 to bit 4 in register
		ALL_LED_OFF_H. The other method is to write logic 1 to bit 4 in
		each active PWM channel LEDn_OFF_H register.
		"""

		# Checks if RESTART bit is a logic 1
		if self.get_restart_bit() == 1:
			# Writes logic 1 to clear the RESTART bit in the MODE 1 register
			self.write_restart_bit(1)
		else:
			print("Restart bit already set to 0")

		# Returns RESTART bit value
		return self.get_restart_bit()

	#----------------------------------------------
	# Restart PCA9685 from Sleep Mode
	def restart_pwm_channels(self):
		"""!
		Restarts all of the previously active PWM channels with a few
		I2C-bus cycles.

		@return **Integer** Value of RESTART bit after changes.
					0- Restart Disabled (Default)
					1- Restart Enabled

		NOTE: Only if the PCA9685 was operating and the user put the
		chip to sleep (setting MODE1 bit 4) without stopping any of the
		PWM channels, the RESTART bit (MODE1 bit 7) will be set to logic
		1 at the end of the PWM refresh cycle. The contents of each PWM
		register are held valid when the clock is off.
		Uses the following steps:
		1.	Read MODE1 register.
		2.	Check that bit 7 (RESTART) is a logic 1. If it is, clear bit
			4 (SLEEP). Allow time for the oscillator to stabilize (500us).
		3.	Write logic 1 to bit 7 of MODE1 register. All PWM channels will
			restart and the	RESTART bit will clear.
		Remark: The SLEEP bit must be logic 0 for at least 500us, before
		a logic 1 is written into the RESTART bit.
		"""
		
		# Checks if RESTART bit is a logic 1
		if self.get_restart_bit() == 1:
			# Clear SLEEP bit
			self.set_sleep_bit(0)
				
			# Allow time for the oscillator to stabilize (1ms)
			time.sleep( 10**(-3))

			# Writes logic 1 to RESTART bit
			self.write_restart_bit(1)
		else:
			print("RESTART bit logic 0; not in sleep mode.")
		
		# Returns RESTART bit value
		return self.get_restart_bit()


	#----------------------------------------------
	# Enables EXTCLCK Pin
	def enable_extclock_bit(self):
		"""!
		Changes value of EXTCLK bit in MODE 1 register to enable EXTCLK
		pin. Once enabled, it allows for an external clock signal. It
		also affects the	refresh rate:

				                       EXTCLK
				refresh_rate = ----------------------
				                4096 x (prescale +1)

		NOTE: This EXTCLK bit is a "sticky bit", that is, it cannot be
		cleared by writing a logic 0 to it. The EXTCLK can only be
		cleared by a power cycle or software reset.
		"""

		# Read MODE1 register
		mode1 = self._i2c.readByte(self.address, MODE1)

		sleep_bit = 4	# Fifth bit in register
		extclk_bit = 6	# Seventh bit in register

		# Set SLEEP bit in MODE1. Turns off the internal oscillator.
		self.set_sleep_bit(1)	# Sets SLEEP bit to 1 = Low Power Mode; Oscillator Off.

		# Write logic 1's to both SLEEP and EXTCLK bits in MODE1. The
		# external clock can be active during the switch because the
		# SLEEP bit is set.
		extclk = mode1 | (1 << sleep_bit) | (1 << extclk_bit)	# Sets SLEEP and EXTCLK bits to 1
		self._i2c.writeByte(self.address, MODE1, extclk)		# Sets SLEEP and EXTCLK bits to 1
