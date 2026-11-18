#-------------------------------------------------------------------------------
# qwiic_mcp4725.py
#
# Python library for the SparkFun I2C DAC Breakout Board (MCP4725), available here:
#  https://www.sparkfun.com/products/12918
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
# This python library supports the SparkFun Electroncis Qwiic Ecosystem 
# (although the board does not have a Qwiic connector)
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
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
#===============================================================================

"""!
qwiic_mcp4725
============
Python module for the [SparkFun I2C DAC Breakout Board (MCP4725)](https://www.sparkfun.com/products/12918)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_MCP4725_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c

__version__ = "3.0.0"

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic MCP4725"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x60, 0x61]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicMCP4725(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    POWER_DOWN_MODE_NORMAL = 0  # PD1=0, PD0=0
    POWER_DOWN_MODE_1K = 1      # PD1=0, PD0=1
    POWER_DOWN_MODE_100K = 2    # PD1=1, PD0=0
    POWER_DOWN_MODE_500K = 3    # PD1=1, PD0=1

    def __init__(self, address=None, i2c_bus=None):
        """!
        Constructor

        @param address: **int, optional** The I2C address to use for the device
            If not provided, the default address is used
        @param i2c_bus: **I2CBus, optional** A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.
        """
        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        # TODO: If the device has a product ID register, that should be
        # checked in addition to the ACK
        return self._i2c.is_device_connected(self.address)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        return self.is_connected()
    
    def write_block_no_address(self, data):
        """!
        Writes a block of data to the device without specifying an address

        @param data: **list** Bytes to write to the device
        """

        # For devices that don't require an address to be sent before the data
        self._i2c.write_block(self.address, data[0], data[1:])


    def write_fast_mode(self, value, power_down_mode=POWER_DOWN_MODE_NORMAL):
        """!
        Updates DAC register in fast mode

        @param value: **int** 12-bit value to write to DAC register
        @param power_down_mode: **int** Power down mode to write to DAC register

        Allowable values for power_down_mode are:
            - `POWER_DOWN_MODE_NORMAL`
            - `POWER_DOWN_MODE_1K`
            - `POWER_DOWN_MODE_100K`
            - `POWER_DOWN_MODE_500K`
        """
        if power_down_mode not in [self.POWER_DOWN_MODE_NORMAL, self.POWER_DOWN_MODE_1K, self.POWER_DOWN_MODE_100K, self.POWER_DOWN_MODE_500K]:
            return

        if value > 4095:
            value = 4095
        elif value < 0:
            value = 0

        # In Fast mode, writes take the form (see datasheet pg. 24): 
        # byte 0: C2=0 | C0=0 | PD1 | PD0 | D11 | D10 | D9 | D8
        # byte 1: D7   | D6   | D5  | D4  | D3  | D2  | D1 | D0

        bytes_to_write = [0] * 2
        bytes_to_write[0] = (power_down_mode << 4) | ( (value & 0x0F00) >> 8 )
        bytes_to_write[1] = value & 0xFF
        self.write_block_no_address(bytes_to_write)

    def write_dac(self, value, power_down_mode=POWER_DOWN_MODE_NORMAL):
        """!
        Updates DAC register

        @param value: **int** 12-bit value to write to DAC register
        @param power_down_mode: **int** Power down mode to write to DAC register

        Allowable values for power_down_mode are:
            - `POWER_DOWN_MODE_NORMAL`
            - `POWER_DOWN_MODE_1K`
            - `POWER_DOWN_MODE_100K`
            - `POWER_DOWN_MODE_500K`
        """

        if power_down_mode not in [self.POWER_DOWN_MODE_NORMAL, self.POWER_DOWN_MODE_1K, self.POWER_DOWN_MODE_100K, self.POWER_DOWN_MODE_500K]:
            return

        if value > 4095:
            value = 4095
        elif value < 0:
            value = 0
        
        # Dac writes take the form (see datasheet pg. 25): 
        # byte 0: C2=0 | C1=1  | C0=0 | X  | X  | PD1 | PD0 | X
        # byte 1: D11  | D10   | D9   | D8 | D7 | D6  | D5  | D4
        # byte 2: D3   | D2    | D1   | D0 | X  | X   | X   | X

        bytes_to_write = [0] * 3
        bytes_to_write[0] = (0x40 | (power_down_mode << 1))
        bytes_to_write[1] = ( (value & 0x0FF0) >> 4 )
        bytes_to_write[2] = ( (value & 0x000F) << 4 )
        self.write_block_no_address(bytes_to_write)


    def write_dac_eeprom(self, value, power_down_mode=POWER_DOWN_MODE_NORMAL):
        """!
        Updates DAC register and EEPROM register

        @param value: **int** 12-bit value to write to DAC and EEPROM registers
        @param power_down_mode: **int** Power down mode to write to DAC and EEPROM registers

        Allowable values for power_down_mode are:
            - `POWER_DOWN_MODE_NORMAL`
            - `POWER_DOWN_MODE_1K`
            - `POWER_DOWN_MODE_100K`
            - `POWER_DOWN_MODE_500K`
        """

        if power_down_mode not in [self.POWER_DOWN_MODE_NORMAL, self.POWER_DOWN_MODE_1K, self.POWER_DOWN_MODE_100K, self.POWER_DOWN_MODE_500K]:
            return

        if value > 4095:
            value = 4095
        elif value < 0:
            value = 0

        # Dac writes take the form (see datasheet pg. 25): 
        # byte 0: C2=0 | C1=1  | C0=1 | X  | X  | PD1 | PD0 | X
        # byte 1: D11  | D10   | D9   | D8 | D7 | D6  | D5  | D4
        # byte 2: D3   | D2    | D1   | D0 | X  | X   | X   | X

        bytes_to_write = [0] * 3
        bytes_to_write[0] = (0x60 | (power_down_mode << 1))
        bytes_to_write[1] = ( (value & 0x0FF0) >> 4 )
        bytes_to_write[2] = ( (value & 0x000F) << 4 )
        self.write_block_no_address(bytes_to_write)

    def read_dac_eeprom(self):
        """!
        Reads the DAC and EEPROM registers

        @return **dict** A dictionary containing the DAC and EEPROM register values and flags

        The dictionary contains the following keys:
            - `rdy_flag`: Ready flag
            - `por_flag`: Power-on reset flag
            - `dac_power_down_mode`: DAC power down mode
            - `dac_value`: DAC register value
            - `eeprom_power_down_mode`: EEPROM power down mode
            - `eeprom_value`: EEPROM register value
        """
        # Data Returned from Read commands take the form (see datasheet pg. 26):
        # byte 0 (Settings):   RDY | POR | X   | X  | X   | PD1 | PD0 | X
        # byte 1 (DAC Reg):    D11 | D10 | D9  | D8 | D7  | D6  | D5  | D4
        # byte 2 (DAC Reg):    D3  | D2  | D1  | D0 | X   | X   | X   | X
        # byte 3 (EEPROM Reg): X   | PD1 | PD0 | X  | D11 | D10 | D9  | D8
        # byte 4 (EEPROM Reg): D7  | D6  | D5  | D4 | D3  | D2  | D1  | D0

        # A read is just the address byte, with no register (datasheet pg. 26)
        read_bytes = self._i2c.read_block(self.address, None, 5)

        data = {
            'rdy_flag': (read_bytes[0] & 0x80) >> 7,
            'por_flag': (read_bytes[0] & 0x40) >> 6,
            'dac_power_down_mode': (read_bytes[0] & 0x06) >> 1,
            'dac_value': (read_bytes[1] << 4) | ((read_bytes[2] & 0xF0) >> 4),
            'eeprom_power_down_mode': (read_bytes[3] & 0x60) >> 5,
            'eeprom_value': ((read_bytes[3] & 0x0F) << 8) | read_bytes[4]
        }

        return data
