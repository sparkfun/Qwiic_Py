#-----------------------------------------------------------------------
# SparkFun Pi Servo Hat Python Library
#-----------------------------------------------------------------------
#
# Written by  SparkFun Electronics, June 2019
# Author: Wes Furuya
#
# Compatibility:
#     * Original: https://www.sparkfun.com/products/14328
#     * v2: https://www.sparkfun.com/products/15316
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

"""!
pi_servo_hat
===============
Python module for the [SparkFun Pi Servo HAT](https://www.sparkfun.com/products/14328) and [SparkFun Servo pHAT for Raspberry Pi](https://www.sparkfun.com/products/15316).
This package should be used in conjunction with the sparkfun_pca9685
package.
"""
#-----------------------------------------------------------------------


# Load Necessary Modules:
import time				# Time access and conversion package
import math				# Basic math package
import qwiic_pca9685	# PCA9685 LED driver package
						# (used on Pi Servo pHAT)

# Device Name:
_DEFAULT_NAME = "Pi Servo HAT"


# Device Address:
# Some devices have multiple available addresses - this is a list of
# these addresses.
# NOTE: The first address in this list is considered the default I2C
# address for the device.
#
# Currently, the Pi Servo Hat (original and v2), the I2C address is
# fixed at 0x40. In the future, should this option become available,
# users will only need to modify the list below.

# Fixed Address:
_AVAILABLE_I2C_ADDRESS = [0x40]

# Full List:
#_AVAILABLE_I2C_ADDRESS = list(range(0x40,0x7F+1))					# Full Address List
#_AVAILABLE_I2C_ADDRESS = _AVAILABLE_I2C_ADDRESS.remove(acAddr)		# Exclude All Call
#_AVAILABLE_I2C_ADDRESS = _AVAILABLE_I2C_ADDRESS.remove(subAddr_1)	# Exclude Sub Addr 1
#_AVAILABLE_I2C_ADDRESS = _AVAILABLE_I2C_ADDRESS.remove(subAddr_2)	# Exclude Sub Addr 2
#_AVAILABLE_I2C_ADDRESS = _AVAILABLE_I2C_ADDRESS.remove(subAddr_3)	# Exclude Sub Addr 3

# Default Servo Frequency:
_DEFAULT_SERVO_FREQUENCY = 50	# Hz

class PiServoHat(object):
	"""!
	SparkFun PiServoHat
	Initialise the qwiic_pca9685 python module at ``address`` with ``i2c_driver``.

	@param address: The I2C address to use for the device.
						If not provided, the default address is
						used.
	@param i2c_driver: An existing i2c driver object. If not
						provided a driver object is created.

	@return **Bool** Constructor Initialization
						True-	Successful
						False-	Issue loading I2C driver
	"""

	# Constructor

	#----------------------------------------------
	# Device Name:
	device_name = _DEFAULT_NAME
	
	#----------------------------------------------
	# Available Addresses:
	available_addresses = _AVAILABLE_I2C_ADDRESS
	
	# Special Use Addresses:
	gcAddr = 0x00 		# General Call address for software reset
	acAddr = 0x70		# All Call address- used for modifications to
						# multiple PCA9685 chips reguardless of thier
						# I2C address set by hardware pins (A0 to A5).
	subAddr_1 = 0x71	# 1110 001X or 0xE2 (7-bit)
	subAddr_2 = 0x72	# 1110 010X or 0xE4 (7-bit)
	subAddr_3 = 0x74	# 1110 100X or 0xE8 (7-bit)

	# _AVAILABLE_I2C_ADDRESS = _AVAILABLE_I2C_ADDRESS.remove(acAddr)	# Exclude All Call
	# _AVAILABLE_I2C_ADDRESS = _AVAILABLE_I2C_ADDRESS.remove(subAddr_1)	# Exclude Sub Addr 1
	# _AVAILABLE_I2C_ADDRESS = _AVAILABLE_I2C_ADDRESS.remove(subAddr_2)	# Exclude Sub Addr 2
	# _AVAILABLE_I2C_ADDRESS = _AVAILABLE_I2C_ADDRESS.remove(subAddr_3)	# Exclude Sub Addr 3
	
	#----------------------------------------------
	# Default Servo frequency:
	frequency = _DEFAULT_SERVO_FREQUENCY
	
	#----------------------------------------------
	# Constructor
	def __init__(self, address=None, debug = None, min_pt=1, max_pt=2):
		"""!
		This method initializes the class object. If no 'address' or
		'i2c_driver' are inputed or 'None' is specified, the method will
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
		@param min_pt: The minimum pulse time of the servos in 
							milliseconds.  If not provided, default to 
							1 ms
		@param max_pt: The maximum pulse time of the servos in 
							milliseconds.  If not provided, default to 
							2 ms
		"""
		
		# Did the user specify an I2C address?
		# Defaults to 0x40 if unspecified.
		self.address = address if address != None else self.available_addresses[0]

		# Do you want debug statements?
		if debug == None:
			self.debug = 0	# Debug Statements Disabled
		else:
			self.debug = debug	# Debug Statements Enabled (1)
		
		# Initialization
		self.PCA9685 = qwiic_pca9685.QwiicPCA9685(self.address, debug)
		
		#----------------------------------------------
		# Grab Available Channels:
		self.available_pwm_channels = qwiic_pca9685.QwiicPCA9685.available_pwm_channels

		# #----------------------------------------------
		# # Grab Current PWM Frequency
		# self.frequency = piservohat.get_pwm_frequency()
		
		# #----------------------------------------------
		# # If not 50 Hz; #change
		# if self.frequency != 50:
		# 	piservohat.set_pwm_frequency(_DEFAULT_SERVO_FREQUENCY)
		
		#----------------------------------------------
		# Sets PWM frequency to Default = 50 Hz
		self.set_pwm_frequency(_DEFAULT_SERVO_FREQUENCY)

		#----------------------------------------------
		# Sets the minimum pulse widths for the servos
		self.minimum_pulse_width = float(min_pt)

		#----------------------------------------------
		# Sets the maximum pulse widths for the servos
		self.maximum_pulse_width = float(max_pt)

		#----------------------------------------------
		# Error check to make sure minimum pulse is less than max
		if self.maximum_pulse_width < self.minimum_pulse_width:
			self.minimum_pulse_width = max_pt
			self.maximum_pulse_width = min_pt

		#----------------------------------------------
		# Begin operation
		self.PCA9685.begin()

	#----------------------------------------------
	# Check if Connected
	def is_connected(self):
		"""!
		Is an I2C connection established with the device?

		@return **Bool** Device Connection Status
					True-	Connected
					False-	Not Connected
		"""
		return self.PCA9685.is_connected()

	#----------------------------------------------
	# Restart PCA9685
	def restart(self):
		"""!
		Soft resets the chip and then clears the MODE1 register to
		restart the PWM functionality. The PWM frequency is returned to
		the default 50 Hz setting.
		"""
		# Soft Reset Chip
		self.PCA9685.soft_reset()

		# Clear MODE1 Register
		self.PCA9685.restart()

		#----------------------------------------------
		# Sets PWM frequency to Default = 50 Hz
		self.set_pwm_frequency(_DEFAULT_SERVO_FREQUENCY)


	#----------------------------------------------
	# Read PWM Frequency
	def get_pwm_frequency(self):
		"""!
		Reads the PWM frequency used on outputs. 50 Hz is recommended
		for most servos.

		@return **Integer** PWM Frequency
					Range: 24 Hz to 1526 Hz
		"""

		# Get pre-scale value (determines PWM frequency)
		prescale = self.PCA9685.get_pre_scale()

		# Calculate frequency based off internal clock frequency (default)
		self.frequency = int((25*10**6)/((prescale + 1)*4096))

		return self.frequency

	#----------------------------------------------
	# Change PWM Frequency
	def set_pwm_frequency(self, frequency = None):
		"""!
		Configures the PWM frequency used on outputs. 50 Hz is the
		default and recommended for most servos.

		@param frequency: PWM Frequency
							Range: 24 Hz to 1526 Hz

		@return **Bool** Function Operation
					True-	Successful
					False-	Issue in Execution

		NOTE: Changing PWM frequency affects timing for servo
		positioning. Additionally, the servo position needs to be reset
		for the output control (on all channels).
		The output on all channels is initially turned off after the
		frequency change, but is re-enabled after any of the channels is
		reconfigured. However, the new PWM frequency will be in affect,
		so the timing of the outputs on the other channels will be off.
		(i.e. if a PWM frequency is doubled; the timing of that signal
		may be halfed.)
		"""
		
		# Debug message
		if self.debug == 1:
			print("PWM Frequency: %s" % frequency)
		
		if frequency == None:
			frequency = 50	# Default (50 Hz)
				
		if self.PCA9685.set_pre_scale(frequency) == True:
			self.frequency = frequency
			return True
		else:
			return False

	#----------------------------------------------
	# Lists the current min and max pulse times
	def get_pulse_time(self):
		"""!
		Reads and returns the current min and max pulse times for servo movement

		Returns:
			tuple: The minimum and maximum pulse times in milliseconds
		"""

		return (self.minimum_pulse_width, self.maximum_pulse_width)

	#----------------------------------------------
	# Updates the min and max pulse times for all servos by times in milliseconds
	def set_pulse_time(self, min_pulse_time, max_pulse_time):
		"""!
		Updates the minimum and maximum pulse widths for the servos

		Args:
			min_pulse_time (float): The new minimum pulse width in ms
			max_pulse_time (float): The new maximum pulse width in ms

		Returns:
			bool: Returns true if update was successful, false if an error was encountered
		"""

		try:
			if float(min_pulse_time) < float(max_pulse_time):
				self.minimum_pulse_width = min_pulse_time
				self.maximum_pulse_width = max_pulse_time
			else:
				self.maximum_pulse_width = min_pulse_time
				self.minimum_pulse_width = max_pulse_time

			return True
		except:
			return False
	#----------------------------------------------
	# Moves Servo on Specified Channel to Position (in Degrees)
	def move_servo_position(self, channel, position, swing = None):
		"""!
		Moves servo to specified location in degrees.

		@param channel: Channel of Servo to Control
							Range: 0 to 15
		@param position: Position (Degrees)
							Range: Open, but should between 0 and
							specified servo 'swing'. The range is not
							regulated because most servos have extra
							room for play (i.e. a 90 degree servo may
							have a +120 degree usable swing). If 'None'
							is specified, the default setting is 90
							degrees.
		@param swing: Range of Servo Movement
							90-		90 Degree Servo
							180-	180 Degree Servo
		"""
		
		# # Check Auto-Increment Bit
		# if self.PCA9685.get_auto_increment_bit != 1:
		# 	# Enable Word Reads/Writes
		# 	self.PCA9685.set_auto_increment_bit(1)

		# Debug message
		if self.debug == 1:
			try:
				self.available_pwm_channels.index(channel)
			except:
				print("available Channels list:")
				print(self.available_pwm_channels)
				print("Selected Channel: %s" % channel)


		period = 1 / self.frequency			# seconds
		resolution = period / 4096			# seconds

		# Initial Condition
		delay = 0
		
		# Calculate Positioning- Linear Interpolation:

		# Debug message
		if self.debug == 1:
			print("Servo Range: %s" % swing)
		
		if swing == None:
			swing = 90	# Default
		elif swing != 90 and swing != 180:
			raise Exception("Error: 'swing' input value. Must be 90 or 180.")
		
		# Servo Timing
		ratio = float(position) / swing # the ratio of the movement to the max angle
		time_dif = self.maximum_pulse_width - self.minimum_pulse_width # the representation of the max movement range in terms of time

		# converts movement back into a position time
		position_time = ((ratio * time_dif) + self.minimum_pulse_width) / 1000 # convert back into seconds (float)

		if self.debug == 1:
			print(f"Ratio: {str(ratio)}, time_dif: {str(time_dif)}, pt: {str(position_time)}")

		
		# Round Values from Float to Integers
		on_value = round(delay)									# integer
		off_value = round(position_time / resolution + delay)	# integer

		# Debug message
		if self.debug == 1:
			print("On value: %s" % on_value)
			print("Off value: %s" % off_value)
			print("Total (max. 4096): %s" % (on_value + off_value))
		
		# Move servo to position immediately
		self.PCA9685.set_channel_word(channel, 1, on_value)	# Timing for "On" edge of PWM
		self.PCA9685.set_channel_word(channel, 0, off_value)	# Timing for "Off" edge of PWM
		

	def set_duty_cycle(self, channel, duty_cycle):
		"""!
		Moves servo to specified location based on duty-cycle.

		@param channel: Channel of Servo to Control
							Range: 0 to 15
		@param duty_cycle: Duty-Cycle (Percentage)
							Float Range: 0 to 100 (%)
							Resolution: 1/4096
		"""
		
		# # Check Auto-Increment Bit
		# if self.PCA9685.get_auto_increment_bit != 1:
		# 	# Enable Word Reads/Writes
		# 	self.PCA9685.set_auto_increment_bit(1)

		# Debug message
		if self.debug == 1:
			try:
				self.available_pwm_channels.index(channel)
			except:
				print("available Channels list:")
				print(self.available_pwm_channels)
				print("Selected Channel: %s" % channel)

		# Initial Condition
		delay = 0
		
		# Round Values from Float to Integers
		on_value = round(delay)						# integer
		off_value = round(duty_cycle/100*4096) - 1	# integer

		# Debug message
		if self.debug == 1:
			print("On value: %s" % on_value)
			print("Off value: %s" % off_value)
			print("Total (max. 4096): %s" % (on_value + off_value))
		
		# Change Duty-Cycle
		self.PCA9685.set_channel_word(channel, 1, on_value)	# Timing for "On" edge of PWM
		self.PCA9685.set_channel_word(channel, 0, off_value)	# Timing for "Off" edge of PWM

	#----------------------------------------------
	# Retrieves Servo Position on Specified Channel (in Degrees)
	def get_servo_position(self, channel, swing = None):
		"""!
		Reads the specified location for the servo in degrees.

		@param channel: Channel of Servo to Control
							Range: 0 to 15
		@param swing: Range of Servo Movement
							90-		90 Degree Servo
							180-	180 Degree Servo

		@return **Float** Esitmated Position (Degrees)
		"""
		
		# # Check Auto-Increment Bit
		# if self.PCA9685.get_auto_increment_bit != 1:
		# 	# Enable Word Reads/Writes
		# 	self.PCA9685.set_auto_increment_bit(1)

		# Debug message
		if self.debug == 1:
			try:
				self.available_pwm_channels.index(channel)
			except:
				print("available Channels list:")
				print(self.available_pwm_channels)
				print("Selected Channel: %s" % channel)

		initial_on = self.PCA9685.get_channel_word(channel, 1)	# Timing for "On" edge of PWM
		initial_off = self.PCA9685.get_channel_word(channel, 0)	# Timing for "Off" edge of PWM

		# Debug message
		if self.debug == 1:
			print("On value: %s" % initial_on)
			print("Off value: %s" % initial_off)
			print("Total (max. 4096): %s" % (initial_on + initial_off))
			print("Difference: %s" % (initial_on - initial_off))

		period = 1 / self.frequency			# seconds
		resolution = period / 4096			# seconds

		# Debug message
		if self.debug == 1:
			print("Servo Range: %s" % swing)

		# 180 Degree Servo Timing:
		# 	0 	Degrees	=	1.0	ms
		#	90	Degrees	=	1.5	ms
		#	180	Degrees	=	2.0	ms
		# 90 Degree Servo Timing:
		# 	0 	Degrees	=	1.0	ms
		# 	45	Degrees	=	1.5	ms
		#	90	Degrees	=	2.0	ms
		
		if swing == None:
			swing = 90	# Default
		elif swing != 90 and swing != 180:
			raise Exception("Error: 'swing' input value. Must be 90 or 180.")
			
		
		# Servo Timing
		m = 1 / swing											# ms/degree
		difference = (initial_off - initial_on) * resolution	# steps/second
		position = ((difference * 1000) - 1) / m				# degrees

		# Debug message
		if self.debug == 1:
			print("On value: %s" % initial_on)
		
		return position
			
	#----------------------------------------------
	# Sleep PCA9685
	def sleep(self):
		"""!
		Set the SLEEP bit to 1, which will unpower the servos. This preserves the life of the servos.
		"""
		self.PCA9685.set_sleep_bit(1)

	#----------------------------------------------
	# Wake PCA9685
	def wake(self):
		"""!
		Set the SLEEP bit to 0, which will power the servos.
		"""
		self.PCA9685.set_sleep_bit(0)
		time.sleep(0.001)  # wait for oscillator to stabilize
