#-----------------------------------------------------------------------
# SparkFun Qwiic TCA9548A Library
#-----------------------------------------------------------------------
#
# Ported by SparkFun Electronics, December 2019
# Author: Wes Furuya
#
# Compatibility:
#     * Original: https://www.sparkfun.com/products/14685
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on Qwiic Mux Breakout, check out the product
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

"""!
qwiic_tca9548a
=================
Python module for the [Qwiic Mux Breakout](https://www.sparkfun.com/products/14685)
This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# Load Necessary Modules:
#----------------------------------------------
import qwiic_i2c					# I2C bus driver package

__version__ = "3.0.0"

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
#
# The name of this device - note this is private
_DEFAULT_NAME = "Qwiic Mux"

# Some devices have multiple availabel addresses - this is a list of these addresses (0x70 - 0x77).
# NOTE: The first address in this list is considered the default I2C address for the
# device (0x70).
_AVAILABLE_I2C_ADDRESS = list(range(0x70,0x77 + 1))

class QwiicTCA9548A(object):
	"""!
	Initialise the TCA9548A chip at ``address`` with ``i2c_bus``.

	@param address: The I2C address to use for the device.
						If not provided, the default address is
						used.
	@param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.

	@return **Bool** Constructor Initialization
						True-	Successful
						False-	Issue loading I2C bus
	"""

	#----------------------------------------------
	# Device Name:
	device_name = _DEFAULT_NAME

	#----------------------------------------------
	# Available Addresses:
	available_addresses = _AVAILABLE_I2C_ADDRESS

	#----------------------------------------------
	# Available Channels:
	available_channels = list(range(0,7+1))

	#----------------------------------------------
	# Constructor
	def __init__(self, address = None, i2c_bus = None):
		"""!
		This method initializes the class object. If no 'address' or
		'i2c_bus' are inputed or 'None' is specified, the method will
		use the defaults.

		@param address: The I2C address to use for the device.
							If not provided, the method will default to
							the first address in the
							'available_addresses' list.
							Default = 0x70
		@param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.
		"""
		# The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
		address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)

		# Did the user specify an I2C address?
		# Defaults to 0x70 if unspecified.
		self.address = address if address is not None else self.available_addresses[0]

		# Use the given I2C bus, or the platform's default bus
		self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

	#--------------------------------------------------------------------------
	def is_connected(self):
		"""!
			Determine if the device is connected to the system.

			@return **bool** True if the device is connected, otherwise False.
			"""
		return qwiic_i2c.is_device_connected(self.address)

	def begin(self):
		"""!
		Initialize the operation of the Qwiic Mux. There is nothing to
		configure, so this only checks the connection.

		@return **bool** True if the device is connected, otherwise False.
		"""
		return self.is_connected()

	def get_enabled_channels(self):
		"""!
		This method returns the enabled channels on the Qwiic Mux.

		@return **Integer** Enabled channels on the Qwiic Mux
		"""

		# Return enabled channels
		return self._i2c.read_byte(self.address, None) # Note, passing "None" will simply read from device rather than targetting a specific register

	def enable_channels(self, enable):
		"""!
		This method enables the connection of specific channels on the
		Qwiic Mux.

		@param enable: Channel(s) to enable on the Qwiic Mux. Input
							must be either an individual integer or
							list. The method will automatically convert
							an individual integer into a list.
							Range- 0 to 7
		"""
		# If entry is an integer and not a list; turn it into a list of (1)
		if type(enable) is not list: enable = [ enable ]

		command = self.get_enabled_channels()

		# Iterate through list
		for entry in enable:
			# Skip entries that aren't channel numbers (0-7)
			if type(entry) is not int or entry < 0 or 7 < entry:
				continue
			# Set bit to 1
			command = command | (1<<entry)

		self._i2c.write_byte(self.address, None, command)

	def disable_channels(self, disable):
		"""!
		This method disables the connection of specific channels on the
		Qwiic Mux.

		@param disable: Channel(s) to disable on the Qwiic Mux.
							Input must be either an individual integer
							or list. The method will automatically
							convert an individual integer into a list.
							Range- 0 to 7
		"""
		# If entry is an integer and not a list; turn it into a list of (1)
		if type(disable) is not list: disable = [ disable ]

		command = self.get_enabled_channels()

		# Iterate through list
		for entry in disable:
			# Skip entries that aren't channel numbers (0-7)
			if type(entry) is not int or entry < 0 or 7 < entry:
				continue
			# Clear bit to 0
			command = command & ~(1 << entry)

		self._i2c.write_byte(self.address, None, command & 0xFF)

	def enable_all(self):
		"""!
		This method enables the connection of specific channels on the
		Qwiic Mux.
		"""

		# Enable all channels
		self._i2c.write_byte(self.address, None, 0xFF)

	def disable_all(self):
		"""!
		This method disables the connection of all channels on the
		Qwiic Mux.
		"""

		# Disable all channels
		self._i2c.write_byte(self.address, None, 0x00)

	def list_channels(self):
		"""!
		This method lists the channels that are currently enabled on the
		Qwiic Mux.

		@return **list** The enabled channel numbers (0 to 7), in
					ascending order. Channels not in the list are
					disabled.
		"""

		enabled_channels = self.get_enabled_channels()

		return [x for x in self.available_channels if (enabled_channels >> x) & 1]
