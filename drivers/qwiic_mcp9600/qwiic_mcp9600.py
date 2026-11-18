#-------------------------------------------------------------------------------
# qwiic_mcp9600.py
#
# Python library for the SparkFun Qwiic Awiic Thermocouple Amplifier - MCP9600, available here:
# https://www.sparkfun.com/products/16295
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
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
qwiic_mcp9600
============
Python module for the [SparkFun Qwiic MCP9600](https://www.sparkfun.com/products/16295)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_MCP9600_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic MCP9600"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x60]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicMCP9600(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    DEVICE_ID_UPPER = 0x40 # value of the upper half of the device ID register. lower half is used for device revision
    DEVICE_RESOLUTION = 0.0625 # device resolution (temperature in C that the LSB represents)
    RETRY_ATTEMPTS = 3 # how many times to attempt to read a register from the thermocouple before giving up
    
    # TODO: We could potentially remove any of these that are not used in the library, but they are nice if users ever want to use them
    # MCP9600 Registers
    REGISTER_HOT_JUNC_TEMP = 0x00
    REGISTER_DELTA_JUNC_TEMP = 0x01
    REGISTER_COLD_JUNC_TEMP = 0x02
    REGISTER_RAW_ADC = 0x03
    REGISTER_SENSOR_STATUS = 0x04
    REGISTER_THERMO_SENSOR_CONFIG = 0x05
    REGISTER_DEVICE_CONFIG = 0x06
    REGISTER_ALERT_1_CONFIG = 0x08
    REGISTER_ALERT_2_CONFIG = 0x09
    REGISTER_ALERT_3_CONFIG = 0x0A
    REGISTER_ALERT_4_CONFIG = 0x0B
    REGISTER_ALERT_1_HYSTERESIS = 0x0C
    REGISTER_ALERT_2_HYSTERESIS = 0x0D
    REGISTER_ALERT_3_HYSTERESIS = 0x0E
    REGISTER_ALERT_4_HYSTERESIS = 0x0F
    REGISTER_ALERT_1_LIMIT = 0x10
    REGISTER_ALERT_2_LIMIT = 0x11
    REGISTER_ALERT_3_LIMIT = 0x12
    REGISTER_ALERT_4_LIMIT = 0x13
    REGISTER_DEVICE_ID = 0x20

    # Thermocouple Types
    TYPE_K = 0b000
    TYPE_J = 0b001
    TYPE_T = 0b010
    TYPE_N = 0b011
    TYPE_S = 0b100
    TYPE_E = 0b101
    TYPE_B = 0b110
    TYPE_R = 0b111

    # Ambient Resolution
    AMBIENT_RESOLUTION_ZERO_POINT_0625 = 0
    AMBIENT_RESOLUTION_ZERO_POINT_25 = 1

    # Thermocouple Resolution
    THERMOCOUPLE_RESOLUTION_18_BIT = 0b00
    THERMOCOUPLE_RESOLUTION_16_BIT = 0b01
    THERMOCOUPLE_RESOLUTION_14_BIT = 0b10
    THERMOCOUPLE_RESOLUTION_12_BIT = 0b11

    # Burst Sample
    BURST_SAMPLE_1 = 0b000
    BURST_SAMPLE_2 = 0b001
    BURST_SAMPLE_4 = 0b010
    BURST_SAMPLE_8 = 0b011
    BURST_SAMPLE_16 = 0b100
    BURST_SAMPLE_32 = 0b101
    BURST_SAMPLE_64 = 0b110
    BURST_SAMPLE_128 = 0b111

    # Shutdown Mode
    SHUTDOWN_MODE_NORMAL = 0x00
    SHUTDOWN_MODE_SHUTDOWN = 0x01
    SHUTDOWN_MODE_BURST = 0x02

    # Status bits shifts and masks
    STATUS_SHIFT_ALERT_1 = 0
    STATUS_SHIFT_ALERT_2 = 1
    STATUS_SHIFT_ALERT_3 = 2
    STATUS_SHIFT_ALERT_4 = 3
    SHIFT_INPUT_RANGE = 4
    SHIFT_DATA_READY = 6
    SHIFT_BURST_COMPLETE = 7

    STATUS_MASK_ALERT_1 = 0b1 << STATUS_SHIFT_ALERT_1
    STATUS_MASK_ALERT_2 = 0b1 << STATUS_SHIFT_ALERT_2
    STATUS_MASK_ALERT_3 = 0b1 << STATUS_SHIFT_ALERT_3
    STATUS_MASK_ALERT_4 = 0b1 << STATUS_SHIFT_ALERT_4
    MASK_INPUT_RANGE = 0b11 << SHIFT_INPUT_RANGE
    MASK_DATA_READY = 0b1 << SHIFT_DATA_READY
    MASK_BURST_COMPLETE = 0b1 << SHIFT_BURST_COMPLETE

    # Device Config bits shifts and masks
    CONFIG_SHIFT_SHUTDOWN_MODE = 0
    CONFIG_SHIFT_BURST_MODE_SAMPLE = 2
    CONFIG_SHIFT_ADC_RESOLUTION = 5
    CONFIG_SHIFT_COLD_JUNC_RES = 7

    CONFIG_MASK_SHUTDOWN_MODE = 0b11 << CONFIG_SHIFT_SHUTDOWN_MODE
    CONFIG_MASK_BURST_MODE_SAMPLE = 0b111 << CONFIG_SHIFT_BURST_MODE_SAMPLE
    CONFIG_MASK_ADC_RESOLUTION = 0b11 << CONFIG_SHIFT_ADC_RESOLUTION
    CONFIG_MASK_COLD_JUNC_RES = 0b1 << CONFIG_SHIFT_COLD_JUNC_RES

    # Thermocouple Sensor Config bits shifts and masks
    THERMO_SENSOR_CONFIG_SHIFT_FILTER = 0
    THERMO_SENSOR_CONFIG_SHIFT_TYPE = 4

    THERMO_SENSOR_CONFIG_MASK_FILTER = 0b111 << THERMO_SENSOR_CONFIG_SHIFT_FILTER
    THERMO_SENSOR_CONFIG_MASK_TYPE = 0b111 << THERMO_SENSOR_CONFIG_SHIFT_TYPE

    # Alert Limit bits
    ALERT_LIMIT_SHIFT_SIGN_BIT = 15
    ALERT_LIMIT_MASK_SIGN_BIT = 0b1 << ALERT_LIMIT_SHIFT_SIGN_BIT

    # Alert Config bits shifts and masks
    ALERT_CONFIG_SHIFT_ENABLE = 0
    ALERT_CONFIG_SHIFT_COMP_INT_MODE = 1
    ALERT_CONFIG_SHIFT_ACTIVE_HIGH = 2
    ALERT_CONFIG_SHIFT_RISING = 3
    ALERT_CONFIG_SHIFT_JUNC_HOT = 4
    ALERT_CONFIG_SHIFT_INT_CLEAR = 7

    ALERT_CONFIG_MASK_ENABLE = 0b1 << ALERT_CONFIG_SHIFT_ENABLE
    ALERT_CONFIG_MASK_COMP_INT_MODE = 0b1 << ALERT_CONFIG_SHIFT_COMP_INT_MODE
    ALERT_CONFIG_MASK_ACTIVE_HIGH = 0b1 << ALERT_CONFIG_SHIFT_ACTIVE_HIGH
    ALERT_CONFIG_MASK_RISING = 0b1 << ALERT_CONFIG_SHIFT_RISING
    ALERT_CONFIG_MASK_JUNC_HOT = 0b1 << ALERT_CONFIG_SHIFT_JUNC_HOT
    ALERT_CONFIG_MASK_INT_CLEAR = 0b1 << ALERT_CONFIG_SHIFT_INT_CLEAR

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
    
    def available(self):
        """!
        Returns true if the thermocouple (hot) junction temperature has been updated since we last checked. Also referred to as the data ready bit.

        @return **bool** `True` if the data is ready, otherwise `False`
        """
        status = self.read_block_retry(self.REGISTER_SENSOR_STATUS, 1)
        if status == -1:
            return False
        return (status[0] & self.MASK_DATA_READY) != 0

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """

        # Check if connected by seeing if an ACK is received
        return self._i2c.is_device_connected(self.address)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`

        From Arduino Lib:
        The MCP9600 is a fussy device. If we call isConnected twice in succession, the second call fails
        as the MCP9600 does not ACK on the second call. Only on the first.
        So we should not call is_connected here(). We should only call check_device_id().
        """
        return self.check_device_id()

    def check_device_id(self):
        """!
        Returns true if the constant upper 8 bits in the device ID register are what they should be according to the datasheet.

        @return **bool** `True` if the device ID is correct, otherwise `False`
        """
        
        # According to Arduino lib: this is here because the first read doesn't seem to work, but the second does. No idea why :/
        self.read_block_retry(self.REGISTER_DEVICE_ID, 2)

        device_id_upper = self.read_block_retry(self.REGISTER_DEVICE_ID, 2)

        if device_id_upper == -1: # We were unable to read the device ID successfully
            return False
        
        return device_id_upper[0] == self.DEVICE_ID_UPPER

    def read_block_retry(self, register, num_bytes):
        """!
        Attempt to read the register until we exit with no error code
        This attempts to fix the bug where clock stretching sometimes failes, as
        described in the MCP9600 eratta. Maximum retries defined by RETRY_ATTEMPTS.

        @param register: **int** The register to read
        @param num_bytes: **int** The number of bytes to read

        @return **int** The value of the register
        """

        for i in range(self.RETRY_ATTEMPTS):
            try:
                # Read the register
                value = self._i2c.read_block(self.address, register, num_bytes)
            except Exception:
                # If there's an error, try again
                continue
            else:
                # If no error, return the value
                return list(value)
        
        return -1
    
    def write_double_register(self, register, value):
        """!
        Writes a 16-bit value to a register

        @param register: **int** The register to write to
        @param value: **int** The value to write

        Necessary because we have to write with opposite endianness as write_word
        """
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF

        self._i2c.write_block(self.address, register, [high_byte, low_byte])
    
    def reset_to_defaults(self):
        """!
        Resets all device parameters to their default values.
        """
        self._i2c.write_byte(self.address, self.REGISTER_SENSOR_STATUS, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_THERMO_SENSOR_CONFIG, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_DEVICE_CONFIG, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_ALERT_1_CONFIG, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_ALERT_2_CONFIG, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_ALERT_3_CONFIG, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_ALERT_4_CONFIG, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_ALERT_1_HYSTERESIS, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_ALERT_2_HYSTERESIS, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_ALERT_3_HYSTERESIS, 0x00)
        self._i2c.write_byte(self.address, self.REGISTER_ALERT_4_HYSTERESIS, 0x00)
        self.write_double_register(self.REGISTER_ALERT_1_LIMIT, 0x0000)
        self.write_double_register(self.REGISTER_ALERT_2_LIMIT, 0x0000)
        self.write_double_register(self.REGISTER_ALERT_3_LIMIT, 0x0000)
        self.write_double_register(self.REGISTER_ALERT_4_LIMIT, 0x0000)
    
    def get_thermocouple_temp(self, units = True):
        """!
        Returns the thermocouple temperature, and clears the data ready bit. Set units to true for Celcius, or false for freedom units (Fahrenheit)

        @param units: **bool, optional** The units to use for the temperature as specified above

        @return  The temperature of the thermocouple or -1 on error
        
        """
        raw = self.read_block_retry(self.REGISTER_HOT_JUNC_TEMP, 2)
        if raw == -1:
            return -1
        
        status = self.read_block_retry(self.REGISTER_SENSOR_STATUS, 1)
        if status == -1:
            return -1
        
        # Clear the data ready bit
        status[0] &= ~self.MASK_DATA_READY
        self._i2c.write_byte(self.address, self.REGISTER_SENSOR_STATUS, status[0])

        celcius = (raw[0] << 8 | raw[1])
        # convert from unsigned 16-bit value to a signed 16-bit value
        if celcius > 32767:
            celcius -= 65536

        celcius *= self.DEVICE_RESOLUTION

        return celcius if units else celcius * 1.8 + 32

    def get_ambient_temp(self, units=True):
        """!
        Returns the ambient (IC die) temperature. Set units to true for Celsius, or false for Fahrenheit.

        @param units: **bool, optional** The units to use for the temperature as specified above

        @return  The temperature of the ambient sensor or -1 on error
        
        """
        raw = self.read_block_retry(self.REGISTER_COLD_JUNC_TEMP, 2)
        if raw == -1:
            return -1

        celcius = (raw[0] << 8 | raw[1])
        # convert from unsigned 16-bit value to a signed 16-bit value
        if celcius > 32767:
            celcius -= 65536

        celcius *= self.DEVICE_RESOLUTION

        return celcius if units else celcius * 1.8 + 32
    
    def get_temp_delta(self, units=True):
        """!
        Returns the difference in temperature between the thermocouple and ambient junctions. Set units to true for Celsius, or false for Fahrenheit.

        @param units: **bool, optional** The units to use for the temperature as specified above

        @return  The temperature difference or -1 on error
        
        """
        raw = self.read_block_retry(self.REGISTER_DELTA_JUNC_TEMP, 2)
        if raw == -1:
            return -1

        celcius = (raw[0] << 8 | raw[1])
        # convert from unsigned 16-bit value to a signed 16-bit value
        if celcius > 32767:
            celcius -= 65536

        celcius *= self.DEVICE_RESOLUTION

        return celcius if units else celcius * 1.8 + 32
    
    def get_raw_adc(self):
        """!
        Returns the raw contents of the raw ADC register

        @return  The raw ADC value or -1 on error
        
        """

        raw = self.read_block_retry(self.REGISTER_RAW_ADC, 3)
        if raw == -1:
            return -1
        
        return (raw[0] << 16 | raw[1] << 8 | raw[2])
    
    def is_input_range_exceeded(self):
        """!
        Returns true if the input range has been exceeded

        @return **bool** `True` if the input range has been exceeded, otherwise `False`
        """
        status = self.read_block_retry(self.REGISTER_SENSOR_STATUS, 1)
        if status == -1:
            return False # TODO: We might want to return a third value here rather than true or false to indicate that we couldn't read the status register
        
        return (status[0] & self.MASK_INPUT_RANGE) != 0
    
    # --------------------------- Measurement Configuration ---------------
    def set_ambient_resolution(self, res):
        """!
        Changes the resolution on the cold (ambient) junction, for either 0.0625 or 0.25 degree C resolution. Lower resolution reduces conversion time.
        Valid inputs are:
            AMBIENT_RESOLUTION_ZERO_POINT_0625
            AMBIENT_RESOLUTION_ZERO_POINT_25

        @param res: **int** The resolution to use for the ambient sensor

        @return **bool** `True` if the resolution was set successfully, otherwise `False`
        """
        if res not in [self.AMBIENT_RESOLUTION_ZERO_POINT_0625, self.AMBIENT_RESOLUTION_ZERO_POINT_25]:
            return False

        config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if config == -1:
            return False

        # Set the bit that controls the ambient (cold) junction resolution
        config[0] = (config[0] & ~self.CONFIG_MASK_COLD_JUNC_RES) | (res << self.CONFIG_SHIFT_COLD_JUNC_RES)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.REGISTER_DEVICE_CONFIG, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_ambient_resolution(self):
        """!
        Returns the resolution on the cold (ambient) junction, for either 0.0625 or 0.25 degree C resolution. Lower resolution reduces conversion time.

        @return **int** The resolution of the ambient sensor or -1 on error
        """
        config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if config == -1:
            return -1
        
        return (config[0] >> self.CONFIG_SHIFT_COLD_JUNC_RES) & 0x01
    
    def set_thermocouple_resolution(self, res):
        """!
        Changes the resolution on the hot (thermocouple) junction, for either 18, 16, 14, or 12-bit resolution. Lower resolution reduces conversion time.
        Valid inputs are:
            THERMOCOUPLE_RESOLUTION_18_BIT
            THERMOCOUPLE_RESOLUTION_16_BIT
            THERMOCOUPLE_RESOLUTION_14_BIT
            THERMOCOUPLE_RESOLUTION_12_BIT

        @param res: **int** The resolution to use for the thermocouple sensor

        @return **bool** `True` if the resolution was set successfully, otherwise `False`
        """
        if res not in [self.THERMOCOUPLE_RESOLUTION_18_BIT, self.THERMOCOUPLE_RESOLUTION_16_BIT, self.THERMOCOUPLE_RESOLUTION_14_BIT, self.THERMOCOUPLE_RESOLUTION_12_BIT]:
            return False

        config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if config == -1:
            return False

        # Set the bits that control the thermocouple resolution
        config[0] = (config[0] & ~self.CONFIG_MASK_ADC_RESOLUTION) | (res << self.CONFIG_SHIFT_ADC_RESOLUTION)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.REGISTER_DEVICE_CONFIG, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_thermocouple_resolution(self):
        """!
        Returns the resolution on the hot (thermocouple) junction, for either 18, 16, 14, or 12-bit resolution. Lower resolution reduces conversion time.

        @return **int** The resolution of the thermocouple sensor or -1 on error

        Possible return values:
            THERMOCOUPLE_RESOLUTION_18_BIT
            THERMOCOUPLE_RESOLUTION_16_BIT
            THERMOCOUPLE_RESOLUTION_14_BIT
            THERMOCOUPLE_RESOLUTION_12_BIT
        """
        config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if config == -1:
            return -1

        return ((config[0] & self.CONFIG_MASK_ADC_RESOLUTION ) >> self.CONFIG_SHIFT_ADC_RESOLUTION)

    def set_thermocouple_type(self, type):
        """!
        Changes the type of thermocouple connected to the MCP9600. Supported types are:
            TYPE_K
            TYPE_J
            TYPE_T
            TYPE_N
            TYPE_S
            TYPE_E
            TYPE_B
            TYPE_R

        @param type: **int** The type of thermocouple to use

        @return **bool** `True` if the type was set successfully, otherwise `False`
        """
        if type not in [self.TYPE_K, self.TYPE_J, self.TYPE_T, self.TYPE_N, self.TYPE_S, self.TYPE_E, self.TYPE_B, self.TYPE_R]:
            return False

        config = self.read_block_retry(self.REGISTER_THERMO_SENSOR_CONFIG, 1)
        if config == -1:
            return False

        # Clear the bits that control the thermocouple type
        config[0] &= ~self.THERMO_SENSOR_CONFIG_MASK_TYPE
        # Set the bits that control the thermocouple type
        config[0] |= (type << self.THERMO_SENSOR_CONFIG_SHIFT_TYPE)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.REGISTER_THERMO_SENSOR_CONFIG, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.REGISTER_THERMO_SENSOR_CONFIG, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_thermocouple_type(self):
        """!
        Returns the type of thermocouple connected to the MCP9600 as found in its configuration register. 
        Supported types are:
            TYPE_K
            TYPE_J
            TYPE_T
            TYPE_N
            TYPE_S
            TYPE_E
            TYPE_B
            TYPE_R

        @return **int** The type of thermocouple sensor or -1 on error
        """

        config = self.read_block_retry(self.REGISTER_THERMO_SENSOR_CONFIG, 1)
        if config == -1:
            return -1

        return ((config[0] & self.THERMO_SENSOR_CONFIG_MASK_TYPE ) >> self.THERMO_SENSOR_CONFIG_SHIFT_TYPE)
    
    def set_filter_coefficient(self, filter):
        """!
        Changes the weight of the on-chip exponential moving average filter. Set this to 0 for no filter, 1 for minimum filter, and 7 for maximum filter.

        @param filter: **int** The filter coefficient to use

        @return **bool** `True` if the filter coefficient was set successfully, otherwise `False`

        TODO: Arduino function for this looked a bit odd...it might need to be reworked
        """
        if filter > 7:
            return False  # return immediately if the value is too big

        config = self.read_block_retry(self.REGISTER_THERMO_SENSOR_CONFIG, 1)
        if config == -1:
            return False

        # Clear the bits that control the filter coefficient
        config[0] &= ~self.THERMO_SENSOR_CONFIG_MASK_FILTER
        # Set the bits that control the filter coefficient
        config[0] |= (filter << self.THERMO_SENSOR_CONFIG_SHIFT_FILTER)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.REGISTER_THERMO_SENSOR_CONFIG, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.REGISTER_THERMO_SENSOR_CONFIG, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_filter_coefficient(self):
        """!
        Returns the weight of the on-chip exponential moving average filter.

        @return **int** The filter coefficient or -1 on error
        """
        config = self.read_block_retry(self.REGISTER_THERMO_SENSOR_CONFIG, 1)
        if config == -1:
            return -1

        coeff = (config[0] & self.THERMO_SENSOR_CONFIG_MASK_FILTER) >> self.THERMO_SENSOR_CONFIG_SHIFT_FILTER

        return coeff

    def set_burst_samples(self, samples):
        """!
        Changes the amount of samples to take in burst mode.

        @param samples: **int** The number of samples to take in burst mode

        Available options are:
            BURST_SAMPLE_1
            BURST_SAMPLE_2
            BURST_SAMPLE_4
            BURST_SAMPLE_8
            BURST_SAMPLE_16
            BURST_SAMPLE_32
            BURST_SAMPLE_64
            BURST_SAMPLE_128

        @return **bool** `True` if the burst samples were set successfully, otherwise `False`
        """
        if samples not in [self.BURST_SAMPLE_1, self.BURST_SAMPLE_2, self.BURST_SAMPLE_4, self.BURST_SAMPLE_8, self.BURST_SAMPLE_16, self.BURST_SAMPLE_32, self.BURST_SAMPLE_64, self.BURST_SAMPLE_128]:
            return False

        config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if config == -1:
            return False

        # Clear the bits that control the burst samples
        config[0] &= ~self.CONFIG_MASK_BURST_MODE_SAMPLE
        # Set the bits that control the burst samples
        config[0] |= (samples << self.CONFIG_SHIFT_BURST_MODE_SAMPLE)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.REGISTER_DEVICE_CONFIG, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_burst_samples(self):
        """!
        Returns the amount of samples to take in burst mode, according to the device's configuration register.

        @return **int** The number of samples to take in burst mode or -1 on error

        Possible return values:
            BURST_SAMPLE_1
            BURST_SAMPLE_2
            BURST_SAMPLE_4
            BURST_SAMPLE_8
            BURST_SAMPLE_16
            BURST_SAMPLE_32
            BURST_SAMPLE_64
            BURST_SAMPLE_128
        """
        config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if config == -1:
            return -1

        samples = (config[0] & self.CONFIG_MASK_BURST_MODE_SAMPLE) >> self.CONFIG_SHIFT_BURST_MODE_SAMPLE
        return samples
    
    def burst_available(self):
        """!
        Checks if burst mode data is available.

        @return **bool** Returns `True` if all the burst samples have been taken and the results are ready. Returns `False` otherwise.
        """
        status = self.read_block_retry(self.REGISTER_SENSOR_STATUS, 1)
        if status == -1:
            return False

        return (status[0] & self.MASK_BURST_COMPLETE) != 0
    
    def start_burst(self):
        """!
        Initiates a burst on the MCP9600.

        @return **bool** `True` if the burst was started successfully, otherwise `False`
        """
        status = self.read_block_retry(self.REGISTER_SENSOR_STATUS, 1)
        if status == -1:
            return False

        # Clear the burst complete bit
        status[0] &= ~self.MASK_BURST_COMPLETE
        self._i2c.write_byte(self.address, self.REGISTER_SENSOR_STATUS, status[0])

        # Set the device to burst mode
        return self.set_shutdown_mode(self.SHUTDOWN_MODE_BURST)

    def set_shutdown_mode(self, mode):
        """!
        Changes the shutdown "operating" mode of the MCP9600. Configurable to Normal, Shutdown, and Burst.

        @param mode: **int** The mode to set the device to

        Available options are:
            SHUTDOWN_MODE_NORMAL
            SHUTDOWN_MODE_SHUTDOWN
            SHUTDOWN_MODE_BURST

        @return **bool** `True` if the mode was set successfully, otherwise `False`
        """

        config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if config == -1:
            return False

        # Clear the last two bits of the device config register
        config[0] = (config[0] & ~self.CONFIG_MASK_SHUTDOWN_MODE) | mode

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.REGISTER_DEVICE_CONFIG, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_shutdown_mode(self, mode):
        """!
        Returns the shutdown "operating" mode of the MCP9600. Configurable to Normal, Shutdown, and Burst.

        @return **int** The current mode of the device or -1 on error

        Possible return values:
            SHUTDOWN_MODE_NORMAL
            SHUTDOWN_MODE_SHUTDOWN
            SHUTDOWN_MODE_BURST
        """

        config = self.read_block_retry(self.REGISTER_DEVICE_CONFIG, 1)
        if config == -1:
            return -1

        return (config[0] & self.CONFIG_MASK_SHUTDOWN_MODE) >> self.CONFIG_SHIFT_SHUTDOWN_MODE
    
    #---------------------------- Temperature Alerts -------------------
    def config_alert_temp(self, number, temp):
        """!
        Configures the temperature at which to trigger the alert for a given alert number.

        @param number: **int** The alert number (1-4)
        @param temp: **float** The temperature at which to trigger the alert

        @return **bool** `True` if the alert temperature was set successfully, otherwise `False`
        """
        
        # Pick the right register to put the temp limit in
        if number == 1:
            temp_limit_register = self.REGISTER_ALERT_1_LIMIT
        elif number == 2:
            temp_limit_register = self.REGISTER_ALERT_2_LIMIT
        elif number == 3:
            temp_limit_register = self.REGISTER_ALERT_3_LIMIT
        elif number == 4:
            temp_limit_register = self.REGISTER_ALERT_4_LIMIT
        else:
            return False

        # Convert the temp limit from a float to actual bits in the register
        # See datasheet pg. 23 for the structure of this register
        unsigned_temp_limit = int(abs(temp) * 4)
        unsigned_temp_limit = (unsigned_temp_limit << 2) & 0xFFFC
        signed_temp_limit = unsigned_temp_limit 
        if temp < 0:
            signed_temp_limit |= self.ALERT_LIMIT_MASK_SIGN_BIT   # if the original temp limit was negative we shifted away the sign bit, so reapply it if necessary

        # Write the new temp limit to the MCP9600, return if it was successful
        return self.write_double_register(temp_limit_register, signed_temp_limit)
    
    def config_alert_junction(self, number, junction):
        """!
        Configures the junction to monitor the temperature of to trigger the alert. Set to fALSE for the thermocouple (hot) junction, or True for the ambient (cold) junction.

        @param number: **int** The alert number (1-4)
        @param junction: **bool** The junction to monitor False for the hot junction, True for the cold junction

        @return **bool** `True` if the junction was set successfully, otherwise `False`
        """

        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.REGISTER_ALERT_1_CONFIG
        elif number == 2:
            alert_config_register = self.REGISTER_ALERT_2_CONFIG
        elif number == 3:
            alert_config_register = self.REGISTER_ALERT_3_CONFIG
        elif number == 4:
            alert_config_register = self.REGISTER_ALERT_4_CONFIG
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the junction
        config[0] = (config[0] & ~self.ALERT_CONFIG_MASK_JUNC_HOT)
        if junction:
            config[0] |= self.ALERT_CONFIG_MASK_JUNC_HOT 

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True
    
    def config_alert_hysteresis(self, number, hysteresis):
        """!
        Configures the hysteresis to use around the temperature set point, in degrees Celsius.

        @param number: **int** The alert number (1-4)
        @param hysteresis: **float** The hysteresis value to set

        @return **bool** `True` if the hysteresis was set successfully, otherwise `False`
        """
        
        # Pick the register that points to the right alert
        if number == 1:
            alert_hysteresis_register = self.REGISTER_ALERT_1_HYSTERESIS
        elif number == 2:
            alert_hysteresis_register = self.REGISTER_ALERT_2_HYSTERESIS
        elif number == 3:
            alert_hysteresis_register = self.REGISTER_ALERT_3_HYSTERESIS
        elif number == 4:
            alert_hysteresis_register = self.REGISTER_ALERT_4_HYSTERESIS
        else:
            return False

        # Write the new hysteresis value to the MCP9600
        self._i2c.write_byte(self.address, alert_hysteresis_register, hysteresis)
        return True
    
    def config_alert_edge(self, number, edge):
        """!
        Configures whether to trigger the alert on the rising (cold -> hot) or falling (hot -> cold) edge of the temperature change. Set to True for rising, False for falling.

        @param number: **int** The alert number (1-4)
        @param edge: **bool** The edge to trigger the alert on

        @return **bool** `True` if the edge was set successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.REGISTER_ALERT_1_CONFIG
        elif number == 2:
            alert_config_register = self.REGISTER_ALERT_2_CONFIG
        elif number == 3:
            alert_config_register = self.REGISTER_ALERT_3_CONFIG
        elif number == 4:
            alert_config_register = self.REGISTER_ALERT_4_CONFIG
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the edge
        config[0] &= ~self.ALERT_CONFIG_MASK_RISING
        if edge:
            config[0] |= self.ALERT_CONFIG_MASK_RISING
            
        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def config_alert_logic_level(self, number, level):
        """!
        Configures whether the hardware alert pin is active-high or active-low. Set to True for active-high, False for active-low.

        @param number: **int** The alert number (1-4)
        @param level: **bool** The logic level to set

        @return **bool** `True` if the logic level was set successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.REGISTER_ALERT_1_CONFIG
        elif number == 2:
            alert_config_register = self.REGISTER_ALERT_2_CONFIG
        elif number == 3:
            alert_config_register = self.REGISTER_ALERT_3_CONFIG
        elif number == 4:
            alert_config_register = self.REGISTER_ALERT_4_CONFIG
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the logic level
        config[0] &= ~self.ALERT_CONFIG_MASK_ACTIVE_HIGH
        if level:
            config[0] |= self.ALERT_CONFIG_MASK_ACTIVE_HIGH

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def config_alert_mode(self, number, mode):
        """!
        Configures whether the MCP9600 treats the alert like a comparator or an interrrupt. Set to True for interrupt, False for comparator. More information is on pg. 34 of the datasheet.

        @param number: **int** The alert number (1-4)
        @param mode: **bool** The mode to set the alert to

        @return **bool** `True` if the alert mode was set successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.REGISTER_ALERT_1_CONFIG
        elif number == 2:
            alert_config_register = self.REGISTER_ALERT_2_CONFIG
        elif number == 3:
            alert_config_register = self.REGISTER_ALERT_3_CONFIG
        elif number == 4:
            alert_config_register = self.REGISTER_ALERT_4_CONFIG
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the mode
        config[0] &= ~self.ALERT_CONFIG_MASK_COMP_INT_MODE

        if mode:
            config[0] |= self.ALERT_CONFIG_MASK_COMP_INT_MODE
        
        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def config_alert_enable(self, number, enable):
        """!
        Configures whether or not the interrupt is enabled or not. Set to True to enable, or False to disable.

        @param number: **int** The alert number (1-4)
        @param enable: **bool** Set to True to enable the alert, False to disable

        @return **bool** `True` if the alert was enabled/disabled successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.REGISTER_ALERT_1_CONFIG
        elif number == 2:
            alert_config_register = self.REGISTER_ALERT_2_CONFIG
        elif number == 3:
            alert_config_register = self.REGISTER_ALERT_3_CONFIG
        elif number == 4:
            alert_config_register = self.REGISTER_ALERT_4_CONFIG
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the enable state
        config[0] &= ~self.ALERT_CONFIG_MASK_ENABLE
        
        if enable:
            config[0] |= self.ALERT_CONFIG_MASK_ENABLE

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def clear_alert_pin(self, number):
        """!
        Clears the interrupt on the specified alert channel, resetting the value of the pin.

        @param number: **int** The alert number (1-4)

        @return **bool** `True` if the alert pin was cleared successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.REGISTER_ALERT_1_CONFIG
        elif number == 2:
            alert_config_register = self.REGISTER_ALERT_2_CONFIG
        elif number == 3:
            alert_config_register = self.REGISTER_ALERT_3_CONFIG
        elif number == 4:
            alert_config_register = self.REGISTER_ALERT_4_CONFIG
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that clears the alert pin
        config[0] |= self.ALERT_CONFIG_MASK_INT_CLEAR

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def is_temp_greater_than_limit(self, number):
        """!
        Returns true if the interrupt has been triggered, false otherwise

        @param number: **int** The alert number (1-4)

        @return **bool** `True` if the temperature is greater than the limit, otherwise `False`
        """
        if number < 1 or number > 4:
            return False  # if a nonexistent alert number is given, return False

        status = self.read_block_retry(self.REGISTER_SENSOR_STATUS, 1)
        if status == -1:
            return False

        return (status[0] & (1 << (number - 1))) != 0