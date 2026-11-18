#-------------------------------------------------------------------------------
# qwiic_tmp117.py
#
# Python library for the SparkFun Qwiic TMP117, available here:
# https://www.sparkfun.com/products/15805
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
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
qwiic_tmp117
============
Python module for the [SparkFun Qwiic TMP117 High Precision Temperature Sensor](https://www.sparkfun.com/products/15805)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_TMP117_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic TMP117"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x48, 0x49, 0x4A, 0x4B]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicTMP117(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Register Addresses:
    REG_TEMP_RESULT = 0x00
    REG_CONFIGURATION = 0x01
    REG_T_HIGH_LIMIT = 0x02
    REG_T_LOW_LIMIT = 0x03
    REG_EEPROM_UL = 0x04
    REG_EEPROM_1 = 0x05
    REG_EEPROM_2 = 0x06
    REG_TEMP_OFFSET = 0x07
    REG_EEPROM_3 = 0x08
    REG_DEVICE_ID = 0x0F

    # Configuration Register Masks and Shifts:
    CONFIG_SOFT_RESET_SHIFT = 1
    CONFIG_SOFT_RESET_MASK  = 0b1 << CONFIG_SOFT_RESET_SHIFT

    CONFIG_DR_ALERT_SHIFT = 2
    CONFIG_DR_ALERT_MASK = 0b1 << CONFIG_DR_ALERT_SHIFT

    CONFIG_POL_SHIFT = 3
    CONFIG_POL_MASK = 0b1 << CONFIG_POL_SHIFT

    CONFIG_T_NA_SHIFT = 4
    CONFIG_T_NA_MASK = 0b1 << CONFIG_T_NA_SHIFT
    
    CONFIG_AVG_SHIFT = 5
    CONFIG_AVG_MASK = 0b11 << CONFIG_AVG_SHIFT

    CONFIG_CONV_SHIFT = 7
    CONFIG_CONV_MASK = 0b111 << CONFIG_CONV_SHIFT

    CONFIG_MOD_SHIFT = 10
    CONFIG_MOD_MASK = 0b11 << CONFIG_MOD_SHIFT

    CONFIG_EEPROM_BUSY_SHIFT = 12
    CONFIG_EEPROM_BUSY_MASK = 0b1 << CONFIG_EEPROM_BUSY_SHIFT

    CONFIG_DATA_READY_SHIFT = 13
    CONFIG_DATA_READY_MASK = 0b1 << CONFIG_DATA_READY_SHIFT

    CONFIG_LOW_ALERT_SHIFT = 14
    CONFIG_LOW_ALERT_MASK = 0b1 << CONFIG_LOW_ALERT_SHIFT

    CONFIG_HIGH_ALERT_SHIFT = 15
    CONFIG_HIGH_ALERT_MASK = 0b1 << CONFIG_HIGH_ALERT_SHIFT
    
    # Device ID Register Masks and Shifts:
    CONFIG_DEVICE_ID_SHIFT = 0
    CONFIG_DEVICE_ID_MASK = 0xFFF

    CONFIG_REV_SHIFT = 12
    CONFIG_REV_MASK = 0xF << CONFIG_REV_SHIFT

    # Conversion Modes
    CONTINUOUS_CONVERSION_MODE = 0b00  # Continuous Conversion Mode
    ONE_SHOT_MODE = 0b11  # One Shot Conversion Mode
    SHUTDOWN_MODE = 0b01  # Shutdown Conversion Mode

    # Therm/alert Modes
    THERM_MODE = 1
    ALERT_MODE = 0

    # Conversion Averaging Modes
    CONV_AVG_NONE = 0b00  # No Averaging
    CONV_AVG_8 = 0b01  # 8 Averaged Conversions
    CONV_AVG_32 = 0b10  # 32 Averaged Conversions
    CONV_AVG_64 = 0b11  # 64 Averaged Conversions

    # Constants to index into the Return Value of get_high_low_alert()
    LOW_ALERT_IDX = 0
    HIGH_ALERT_IDX = 1

    # Misc Constants:
    DEVICE_ID_VALUE = 0x0117  # Value found in the device ID register on reset (page 24 Table 3 of datasheet)
    TMP117_RESOLUTION = 0.0078125  # Resolution of the device, found on (page 1 of datasheet)


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

        if not self._i2c.is_device_connected(self.address):
            return False

        # Check the device has a product ID register
        device_id = self.read_register(self.REG_DEVICE_ID)

        return device_id == self.DEVICE_ID_VALUE

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """

        # Confirm device is connected before doing anything
        return self.is_connected()
    
    def get_address(self):
        """!
        Returns the I2C address of the device

        @return **int** The I2C address of the device
        """
        return self.address
    
    def read_temp_c(self):
        """!
        This function reads the temperature reading from the sensor
	    and returns the value in degrees celsius.

        @return **float** The temperature in degrees celsius
        """
        raw_temp = self.read_register(self.REG_TEMP_RESULT)
        
        # Convert to signed 16-bit value
        if raw_temp > 32767:
            raw_temp -= 65536

        return raw_temp * self.TMP117_RESOLUTION
    
    def read_temp_f(self):
        """!
        This function calculates the fahrenheit reading from the
	    celsius reading initially found.

        @return **float** The temperature in degrees fahrenheit
        """
        return self.read_temp_c() * 1.8 + 32

    def get_temperature_offset(self):
        """!
        This function reads the temperature offset value from the device

        @return **float** The temperature offset value
        """
        offset = self.read_register(self.REG_TEMP_OFFSET)
        
        # Convert to signed 16-bit value
        if offset > 32767:
            offset -= 65536
        return offset * self.TMP117_RESOLUTION

    def set_temperature_offset(self, offset):
        """!
        This function sets the temperature offset value on the device

        @param offset: **float** The offset value to set
        """
        # Convert to 16-bit value
        offset = int(offset / self.TMP117_RESOLUTION)
        
        # Write the offset to the device
        self.write_register(self.REG_TEMP_OFFSET, offset)

    def get_low_limit(self):
        """!
        This function reads the low limit register that is set by the user.

        @return **float** The low limit temperature in degrees celsius
        """
        low_limit = self.read_register(self.REG_T_LOW_LIMIT)
        
        # Convert to signed 16-bit value
        if low_limit > 32767:
            low_limit -= 65536

        return low_limit * self.TMP117_RESOLUTION
    
    def set_low_limit(self, low_limit):
        """!
        This function allows the user to set the low limit register to whatever
        specified value, as long as in the range for the temperature sensor. This
        function can be used as a threshold for Therm mode and or Alert mode.

        @param low_limit: **float** The low limit temperature in degrees celsius
        """
        scaled_limit = int(low_limit / self.TMP117_RESOLUTION)
        self.write_register(self.REG_T_LOW_LIMIT, scaled_limit)

    def get_high_limit(self):
        """!
        This function reads the high limit register that is set by the user.

        @return **float** The high limit temperature in degrees celsius
        """
        high_limit = self.read_register(self.REG_T_HIGH_LIMIT)
        
        # Convert to signed 16-bit value
        if high_limit > 32767:
            high_limit -= 65536

        return high_limit * self.TMP117_RESOLUTION
    
    def set_high_limit(self, high_limit):
        """!
        This function allows the user to set the high limit register to whatever
	    specified value, as long as in the range for the temperature sensor. This
	    function can be used as a threshold for Therm mode and or Alert mode

        @param high_limit: **float** The high limit temperature in degrees celsius
        """
        scaled_limit = int(high_limit / self.TMP117_RESOLUTION)
        self.write_register(self.REG_T_HIGH_LIMIT, scaled_limit)

    def get_configuration_register(self):
        """!
        This function reads configuration register. Use this function if you need to read
        certain flags before they are cleared. This can be found on page 25 of the
        datasheet.

        @return **int** The configuration register value
        """
        return self.read_register(self.REG_CONFIGURATION)
    
    def get_high_low_alert(self):
        """!
        This function reads configuration register and saves the high and low alert flags. 
	    Use this function if you need to read the alert flags before they are cleared.

        @return **list of bool** The high and low alert flags in a list [low, high]

        Index into the list with the LOW_ALERT_IDX and HIGH_ALERT_IDX constants
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        high_alert = ( (config_reg & self.CONFIG_HIGH_ALERT_MASK) == self.CONFIG_HIGH_ALERT_MASK )
        low_alert = ( (config_reg & self.CONFIG_LOW_ALERT_MASK) == self.CONFIG_LOW_ALERT_MASK )
        return [low_alert, high_alert]
    
    def get_high_alert(self):
        """!
        This function reads the 15th bit of the configuration register to
        tell if the conversion result is higher than the high limit. This
        is set as a High Alert flag.

        @return **bool** `True` if the high alert flag is set, otherwise `False`
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        return ( (config_reg & self.CONFIG_HIGH_ALERT_MASK) == self.CONFIG_HIGH_ALERT_MASK )

    def get_low_alert(self):
        """!
        This function reads the 14th bit of the configuration register to
        tell if the conversion result is lower than the low limit. This
        is set as a Low Alert flag.

        @return **bool** `True` if the low alert flag is set, otherwise `False`
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        return ( (config_reg & self.CONFIG_LOW_ALERT_MASK) == self.CONFIG_LOW_ALERT_MASK )
    
    def set_alert_function_mode(self, set_alert_mode):
        """!
        This function sets the alert function mode to either "alert" or
        "therm" mode

        @param set_alert_mode: **bool** The alert mode to set

        Allowable set_alert_mode values are:
            THERM_MODE
            ALERT_MODE

        @return **bool** `True` if successful, otherwise `False`
        """
        if set_alert_mode not in [self.THERM_MODE, self.ALERT_MODE]:
            return False

        config_reg = self.read_register(self.REG_CONFIGURATION)

        if set_alert_mode == self.THERM_MODE:
            config_reg |= self.CONFIG_T_NA_MASK
        else:
            config_reg &= ~self.CONFIG_T_NA_MASK

        self.write_register(self.REG_CONFIGURATION, config_reg)

        return True

    def get_alert_function_mode(self):
        """!
        This function gets the alert function mode to either "alert" or 
	    "therm" mode.

        @return **int** The alert mode

        Allowable return values are:
            THERM_MODE
            ALERT_MODE
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        return (config_reg & self.CONFIG_T_NA_MASK) >> self.CONFIG_T_NA_SHIFT
    
    def soft_reset(self):
        """!
        This function performs a software reset, loading all the default
	    values into the configuration register
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        config_reg |= self.CONFIG_SOFT_RESET_MASK
        self.write_register(self.REG_CONFIGURATION, config_reg)

    # TODO: could combine all of the below functions into one function that takes a mode parameter, 
    # but since Arduino library has them separate, kept them separate for now
    def set_continuous_conversion_mode(self):
        """!
        This function sets the conversion mode of the sensor to be 
        continuous. The TMP117 defaults to Continuous Conversion Mode on reset.
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        config_reg &= ~self.CONFIG_MOD_MASK
        config_reg |= (self.CONTINUOUS_CONVERSION_MODE << self.CONFIG_MOD_SHIFT)

        self.write_register(self.REG_CONFIGURATION, config_reg)
    
    def set_shutdown_mode(self):
        """!
        This function sets the conversion mode of the sensor to be 
	    in shutdown mode. The TMP117 defaults to Continuous Conversion Mode 
	    on reset.
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        config_reg &= ~self.CONFIG_MOD_MASK
        config_reg |= (self.SHUTDOWN_MODE << self.CONFIG_MOD_SHIFT)

        self.write_register(self.REG_CONFIGURATION, config_reg)

    def set_one_shot_mode(self):
        """!
        This function sets the conversion mode of the sensor to be
        in one shot mode. The TMP117 defaults to Continuous Conversion Mode
        on reset.
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        config_reg &= ~self.CONFIG_MOD_MASK
        config_reg |= (self.ONE_SHOT_MODE << self.CONFIG_MOD_SHIFT)

        self.write_register(self.REG_CONFIGURATION, config_reg)

    def get_conversion_mode(self):
        """!
        This function reads the mode for the conversions.

        @return **int** The conversion mode

        Allowable return values are:
            CONTINUOUS_CONVERSION_MODE
            ONE_SHOT_MODE
            SHUTDOWN_MODE
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        return (config_reg & self.CONFIG_MOD_MASK) >> self.CONFIG_MOD_SHIFT
    
    def set_conversion_average_mode(self, conv_mode):
        """!
        This function sets the conversion averaging mode of the device
	    when in Continuous Conversion Mode.

        @param conv_mode: **int** The conversion averaging mode to set

        Allowable conv_mode values are:
            CONV_AVG_NONE
            CONV_AVG_8
            CONV_AVG_32
            CONV_AVG_64

        @return **bool** `True` if successful, otherwise `False`
        """
        if conv_mode not in [self.CONV_AVG_NONE, self.CONV_AVG_8, self.CONV_AVG_32, self.CONV_AVG_64]:
            return False

        config_reg = self.read_register(self.REG_CONFIGURATION)
        config_reg &= ~self.CONFIG_AVG_MASK
        config_reg |= (conv_mode << self.CONFIG_AVG_SHIFT)

        self.write_register(self.REG_CONFIGURATION, config_reg)

        return True

    def get_conversion_average_mode(self):
        """!
        This function reads the conversion averaging mode

        @return **int** The conversion averaging mode

        Allowable return values are:
            CONV_AVG_NONE
            CONV_AVG_8
            CONV_AVG_32
            CONV_AVG_64
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        return (config_reg & self.CONFIG_AVG_MASK) >> self.CONFIG_AVG_SHIFT

    def set_conversion_cycle_bit(self, conv):
        """!
        This function sets the conversion cycle time bit in 
        Continuous Conversion mode. The times for the conversions
        can be found below. The user puts in 0-7 and it will
	    return the cycle time accoring to the values in the chart.

        Conversion Cycle Time in CC Mode (found on the datasheet page 27 table 7)
               AVG       0       1       2       3
       CONV  averaging  (0)     (8)     (32)   (64)
         0             15.5ms  125ms   500ms    1s     
         1             125ms   125ms   500ms    1s     
         2             250ms   250ms   500ms    1s     
         3             500ms   500ms   500ms    1s     
         4             1s      1s      1s       1s     
         5             4s      4s      4s       4s     
         6             8s      8s      8s       8s     
         7             16s     16s     16s      16s

        @param conv: **int** The conversion cycle time bit to set

        Allowable conv values are 0-7

        @return **bool** `True` if successful, otherwise `False`
        """
        if conv < 0 or conv > 7:
            return False

        config_reg = self.read_register(self.REG_CONFIGURATION)
        config_reg &= ~self.CONFIG_CONV_MASK
        config_reg |= (conv << self.CONFIG_CONV_SHIFT)

        self.write_register(self.REG_CONFIGURATION, config_reg)
    
    def get_conversion_cycle_bit(self):
        """!
        This function returns the Conversion Cycle Bit value that the 
	    device is currently in at the time. This bit can help determine
	    the conversion cycle time that the device is in while being in
	    continuous conversion mode. (See table in set_conversion_cycle_bit, or page 27 of datasheet)

        @return **int** The conversion cycle bit value

        Allowable return values are 0-7
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        return (config_reg & self.CONFIG_CONV_MASK) >> self.CONFIG_CONV_SHIFT

    def data_ready(self):
        """!
        This function checks to see if there is data ready to be sent
	    from the TMP117.

        @return **bool** `True` if the data is ready, otherwise `False`
        """
        config_reg = self.read_register(self.REG_CONFIGURATION)
        return ( (config_reg & self.CONFIG_DATA_READY_MASK) == self.CONFIG_DATA_READY_MASK )

    def read_register(self, register):
        """!
        Reads a register from the device

        @param register: **int** The register to read

        @return **int** The 16-bit value read from the register

        Used because the device returns bytes as big-endian
        """
        data = self._i2c.read_block(self.address, register, 2)
        return (data[0] << 8) | data[1]
    
    def write_register(self, register, value):
        """!
        Writes a value to a register on the device

        @param register: **int** The register to write to
        @param value: **int** The 16-bit value to write to the register

        Used because the device expects bytes as big-endian
        """
        self._i2c.write_block(self.address, register, [(value >> 8) & 0xFF, value & 0xFF])
