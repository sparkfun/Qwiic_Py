#-------------------------------------------------------------------------------
# qwiic_as726x.py
#
# Python library for the SparkFun Qwiic SparkFun Qwiic AS7262 Visible Spectral Sensor, available here:
# https://www.sparkfun.com/products/14347
# and the SparkFun Qwiic AS7263 Near Infrared Spectral Sensor, available here:
# https://www.sparkfun.com/products/14351
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2023 SparkFun Electronics
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
qwiic_as726x
============
Python module for the [SparkFun Qwiic AS7262 Visible Spectral Sensor](https://www.sparkfun.com/products/14347)
and the [SparkFun Qwiic AS7263 Near Infrared Spectral Sensor](https://www.sparkfun.com/products/14351)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_AS726X_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c
import struct

__version__ = "3.0.0"

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic AS726x"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x49]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicAS726x(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Device Regs
    STATUS_REG = 0x00
    WRITE_REG = 0x01
    READ_REG = 0x02

    TX_VALID = 0x02
    RX_VALID = 0x01

    # Register Addresses
    DEVICE_TYPE = 0x00
    HW_VERSION = 0x01
    CONFIG = 0x04
    INTEGRATION_TIME = 0x05
    DEVICE_TEMP = 0x06
    LED_CONFIG = 0x07

    # The same register locations are shared between the AS7262 and AS7263, they're just called something different
    # AS7262 Registers
    AS7262V = 0x08
    AS7262B = 0x0A
    AS7262G = 0x0C
    AS7262Y = 0x0E
    AS7262O = 0x10
    AS7262R = 0x12
    AS7262V_CAL = 0x14
    AS7262B_CAL = 0x18
    AS7262G_CAL = 0x1C
    AS7262Y_CAL = 0x20
    AS7262O_CAL = 0x24
    AS7262R_CAL = 0x28

    # AS7263 Registers
    AS7263R = 0x08
    AS7263S = 0x0A
    AS7263T = 0x0C
    AS7263U = 0x0E
    AS7263V = 0x10
    AS7263W = 0x12
    AS7263R_CAL = 0x14
    AS7263S_CAL = 0x18
    AS7263T_CAL = 0x1C
    AS7263U_CAL = 0x20
    AS7263V_CAL = 0x24
    AS7263W_CAL = 0x28

    # AS7261 Registers
    AS7261X = 0x08  # 16b
    AS7261Y = 0x0A  # 16b
    AS7261Z = 0x0C  # 16b
    AS7261_NIR = 0x0E  # 16b
    AS7261_DARK = 0x10  # 16b
    AS7261_CLEAR = 0x12  # 16b
    AS7261X_CAL = 0x14
    AS7261Y_CAL = 0x18
    AS7261Z_CAL = 0x1C
    AS7261X1931_CAL = 0x20
    AS7261Y1931_CAL = 0x24
    AS7261_UPRI_CAL = 0x28
    AS7261_VPRI_CAL = 0x2C
    AS7261U_CAL = 0x30
    AS7261V_CAL = 0x34
    AS7261_DUV_CAL = 0x38
    AS7261_LUX_CAL = 0x3C  # 16b
    AS7261_CCT_CAL = 0x3E  # 16b

    SENSOR_TYPE_AS7261 = 0x3D
    SENSOR_TYPE_AS7262 = 0x3E
    SENSOR_TYPE_AS7263 = 0x3F

    POLLING_DELAY = 5  # Amount of ms to wait between checking for virtual register changes
    MAX_RETRIES = 3
    TIMEOUT = 3000
    
    # Necessary Config Register bits
    CONFIG_SRST_SHIFT = 7
    CONFIG_SRST_MASK = 0b1 << CONFIG_SRST_SHIFT
    CONFIG_INT_SHIFT = 6
    CONFIG_INT_MASK = 0b1 << CONFIG_INT_SHIFT
    CONFIG_GAIN_SHIFT = 4
    CONFIG_GAIN_MASK = 0b11 << CONFIG_GAIN_SHIFT
    CONFIG_MODE_SHIFT = 2
    CONFIG_MODE_MASK = 0b11 << CONFIG_MODE_SHIFT
    CONFIG_DATA_READY_SHIFT = 1
    CONFIG_DATA_READY_MASK = 0b1 << CONFIG_DATA_READY_SHIFT
    CONFIG_FRST_SHIFT = 0
    CONFIG_FRST_MASK = 0b1 << CONFIG_FRST_SHIFT

    # Necessary LED Config Register Bits
    LED_CONFIG_LED_DRV_SHIFT = 4
    LED_CONFIG_LED_DRV_MASK = 0b11 << LED_CONFIG_LED_DRV_SHIFT
    LED_CONFIG_LED_ENABLE_SHIFT = 3
    LED_CONFIG_LED_ENABLE_MASK = 0b1 << LED_CONFIG_LED_ENABLE_SHIFT
    LED_CONFIG_IND_CURRENT_SHIFT = 1
    LED_CONFIG_IND_CURRENT_MASK = 0b11 << LED_CONFIG_IND_CURRENT_SHIFT
    LED_CONFIG_IND_ENABLE_SHIFT = 0
    LED_CONFIG_IND_ENABLE_MASK = 0b1 << LED_CONFIG_IND_ENABLE_SHIFT

    # Values to write to current limit, gain, and mode 
    LED_CURRENT_LIMIT_12_5MA = 0b00
    LED_CURRENT_LIMIT_25MA = 0b01
    LED_CURRENT_LIMIT_50MA = 0b10
    LED_CURRENT_LIMIT_100MA = 0b11

    INDICATOR_CURRENT_LIMIT_1MA = 0b00
    INDICATOR_CURRENT_LIMIT_2MA = 0b01
    INDICATOR_CURRENT_LIMIT_4MA = 0b10
    INDICATOR_CURRENT_LIMIT_8MA = 0b11

    GAIN_1X = 0b00
    GAIN_37X = 0b01 #3.7x 
    GAIN_16X = 0b10 #16x
    GAIN_64X = 0b11 #64x

    MEASUREMENT_MODE_4CHAN = 0b00
    MEASUREMENT_MODE_4CHAN2 = 0b01
    MEASUREMENT_MODE_6CHAN_CONTINUOUS = 0b10
    MEASUREMENT_MODE_6CHAN_ONE_SHOT = 0b11

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

        self._sensor_version = 0

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        return self._i2c.is_device_connected(self.address)

    def begin(self, gain = GAIN_64X, measurement_mode = MEASUREMENT_MODE_6CHAN_ONE_SHOT):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        self._sensor_version = self.virtual_read_register(self.HW_VERSION)

        if self._sensor_version not in [self.SENSOR_TYPE_AS7261, self.SENSOR_TYPE_AS7262, self.SENSOR_TYPE_AS7263]:
            return False
        
        # Set Bulb to 12.5mA (minimum)
        self.set_bulb_current(self.LED_CURRENT_LIMIT_12_5MA)
        self.disable_bulb() # To avoid overheating

        # Set Indicator to 8mA (maximum)
        self.set_indicator_current(self.INDICATOR_CURRENT_LIMIT_8MA)
        self.disable_indicator() # To save power

        self.set_integration_time(50) # 50 * 2.8ms = 140ms. 0 to 255 is valid.

        # If you use Mode 2 or 3 (all the colors) then integration time is double.
        # 140*2 = 280ms between readings.

        # Set gain and measurement mode (default to 64x and 6 channel one-shot)
        self.set_gain(gain)
        self.set_measurement_mode(measurement_mode)

        return True

    def take_measurements(self):
        """!
        Tells IC to take measurements and polls for data ready flag

        @return  `True` if successful, otherwise `False`
        
        """
        # Clear the data ready flag
        self.clear_data_available()

        # Set the measurement mode to one-shot for all 6 channels
        self.set_measurement_mode(self.MEASUREMENT_MODE_6CHAN_ONE_SHOT)

        time_waited = 0
        while self.data_available() == False:
            self._i2c.delay_ms(self.POLLING_DELAY)
            time_waited += self.POLLING_DELAY
            if time_waited > self.TIMEOUT:
                return False

        # Readings can now be accessed via get_violet(), get_blue(), etc
        return True

    def get_version(self):
        """!
        Get the version of the sensor. Value is only valid after a call to `begin()`

        @return **int** The version of the sensor
        """
        return self._sensor_version

    def take_measurements_with_bulb(self):
        """!
        Turns on bulb, takes measurements, turns off bulb.

        NOTE: We don't turn on the indicator as it is red and may corrupt the readings
        """
        self.enable_bulb()
        self.take_measurements()
        self.disable_bulb()

    def get_temperature(self):
        """!
        Returns the temperature of the device in Celsius
        """
        return self.virtual_read_register(self.DEVICE_TEMP)

    def get_temperature_f(self):
        """!
        Returns the temperature of the device in Fahrenheit
        """
        return (self.virtual_read_register(self.DEVICE_TEMP) * 1.8) + 32

    def set_measurement_mode(self, mode):
        """!
        Sets the measurement mode

        Mode 0: 4 channels out of 6 (see datasheet)
        Mode 1: Different 4 channels out of 6 (see datasheet)
        Mode 2: All 6 channels continuously
        Mode 3: One-shot reading of all channels

        @param mode: **int** The mode to set

        Allowable mode values are:
            - MEASUREMENT_MODE_4CHAN
            - MEASUREMENT_MODE_4CHAN2
            - MEASUREMENT_MODE_6CHAN_CONTINUOUS
            - MEASUREMENT_MODE_6CHAN_ONE_SHOT
        """
        if mode > self.MEASUREMENT_MODE_6CHAN_ONE_SHOT:
            mode = self.MEASUREMENT_MODE_6CHAN_ONE_SHOT

        value = self.virtual_read_register(self.CONFIG)
        value &= ~self.CONFIG_MODE_MASK
        value |= mode << self.CONFIG_MODE_SHIFT

        self.virtual_write_register(self.CONFIG, value)

    def get_measurement_mode(self):
        """!
        Get the measurement mode

        @return **int** The measurement mode

        Allowable mode values are:
            - MEASUREMENT_MODE_4CHAN
            - MEASUREMENT_MODE_4CHAN2
            - MEASUREMENT_MODE_6CHAN_CONTINUOUS
            - MEASUREMENT_MODE_6CHAN_ONE_SHOT
        """
        value = self.virtual_read_register(self.CONFIG)
        return (value & self.CONFIG_MODE_MASK) >> self.CONFIG_MODE_SHIFT

    def data_available(self):
        """!
        Check if the data ready flag is set in the control setup register

        @return **bool** `True` if the data ready flag is set, otherwise `False`
        """
        value = self.virtual_read_register(self.CONFIG)
        return (value & self.CONFIG_DATA_READY_MASK) != 0

    def enable_indicator(self):
        """!
        Enable the onboard indicator LED
        """

        value = self.virtual_read_register(self.LED_CONFIG)
        value |= self.LED_CONFIG_IND_ENABLE_MASK

        self.virtual_write_register(self.LED_CONFIG, value)

    def disable_indicator(self):
        """!
        Disable the onboard indicator LED
        """

        value = self.virtual_read_register(self.LED_CONFIG)
        value &= ~self.LED_CONFIG_IND_ENABLE_MASK

        self.virtual_write_register(self.LED_CONFIG, value)

    def set_indicator_current(self, current):
        """!
        Set the current limit of onboard LED. Default is max 8mA = 0b11.

        @param current: **int** The current limit to set the indicator LED to

        Allowable current values are:
            - INDICATOR_CURRENT_LIMIT_1MA
            - INDICATOR_CURRENT_LIMIT_2MA
            - INDICATOR_CURRENT_LIMIT_4MA
            - INDICATOR_CURRENT_LIMIT_8MA
        """
        if current > self.INDICATOR_CURRENT_LIMIT_8MA:
            current = self.INDICATOR_CURRENT_LIMIT_8MA

        value = self.virtual_read_register(self.LED_CONFIG)
        value &= ~self.LED_CONFIG_IND_CURRENT_MASK

        value |= current << self.LED_CONFIG_IND_CURRENT_SHIFT

        self.virtual_write_register(self.LED_CONFIG, value)

    def enable_bulb(self):
        """!
        Enable the LED or bulb on a given device
        """

        value = self.virtual_read_register(self.LED_CONFIG)
        value |= self.LED_CONFIG_LED_ENABLE_MASK

        self.virtual_write_register(self.LED_CONFIG, value)

    def disable_bulb(self):
        """!
        Disable the LED or bulb on a given device
        """

        value = self.virtual_read_register(self.LED_CONFIG)
        value &= ~self.LED_CONFIG_LED_ENABLE_MASK

        self.virtual_write_register(self.LED_CONFIG, value)


    def set_bulb_current(self, current):
        """!
        Set the current for the specified LED

        @param current: **int** The current to set the LED to

        Allowable current values are:
            - LED_CURRENT_LIMIT_12_5MA
            - LED_CURRENT_LIMIT_25MA
            - LED_CURRENT_LIMIT_50MA
            - LED_CURRENT_LIMIT_100MA
        """

        if current > self.LED_CURRENT_LIMIT_100MA:
            current = self.LED_CURRENT_LIMIT_100MA
        
        value = self.virtual_read_register(self.LED_CONFIG)
        value &= ~self.LED_CONFIG_LED_DRV_MASK
        value |= current << self.LED_CONFIG_LED_DRV_SHIFT

        self.virtual_write_register(self.LED_CONFIG, value)

    def set_gain(self, gain):
        """!
        Sets the gain value
        Gain 0: 1x (power-on default)
        Gain 1: 3.7x
        Gain 2: 16x
        Gain 3: 64x

        @param gain: **int** The gain value to set
        """
        if gain > self.GAIN_64X:
            gain = self.GAIN_64X

        value = self.virtual_read_register(self.CONFIG)
        value &= ~self.CONFIG_GAIN_MASK
        value |= gain << self.CONFIG_GAIN_SHIFT

        self.virtual_write_register(self.CONFIG, value)

    def get_gain(self):
        """!
        Get the gain value

        @return **int** The gain value
        """
        value = self.virtual_read_register(self.CONFIG)
        return (value & self.CONFIG_GAIN_MASK) >> self.CONFIG_GAIN_SHIFT

    def soft_reset(self):
        """!
        Does a soft reset. Give sensor at least 1000ms to reset
        """
        value = self.virtual_read_register(self.CONFIG)
        value |= (1 << self.CONFIG_SRST_SHIFT)
        self.virtual_write_register(self.CONFIG, value) 

    def set_integration_time(self, integration_value):
        """!
        Sets the integration cycle amount. 
        Give this function a byte from 0 to 255.
        Time will be 2.8ms * [integration cycles + 1]

        @param integration_value: **int** The number of integration cycles to set
        """
        self.virtual_write_register(self.INTEGRATION_TIME, integration_value)

    def get_integration_time(self):
        """!
        Get the integration time

        @return **int** The integration time
        """
        return self.virtual_read_register(self.INTEGRATION_TIME)

    def enable_interrupt(self):
        """!
        Enable the interrupt pin
        """
        value = self.virtual_read_register(self.CONFIG)
        value |= self.CONFIG_INT_MASK

        self.virtual_write_register(self.CONFIG, value)

    def disable_interrupt(self):
        """!
        Disable the interrupt pin
        """
        value = self.virtual_read_register(self.CONFIG)
        value &= ~self.CONFIG_INT_MASK

        self.virtual_write_register(self.CONFIG, value)

    # Get the various color readings
    def get_violet(self):
        return self.get_channel(self.AS7262V)

    def get_blue(self):
        return self.get_channel(self.AS7262B)

    def get_green(self):
        return self.get_channel(self.AS7262G)

    def get_yellow(self):
        return self.get_channel(self.AS7262Y)

    def get_orange(self):
        return self.get_channel(self.AS7262O)

    def get_red(self):
        return self.get_channel(self.AS7262R)

    # Get the various NIR readings
    def get_r(self):
        return self.get_channel(self.AS7263R)

    def get_s(self):
        return self.get_channel(self.AS7263S)

    def get_t(self):
        return self.get_channel(self.AS7263T)

    def get_u(self):
        return self.get_channel(self.AS7263U)

    def get_v(self):
        return self.get_channel(self.AS7263V)

    def get_w(self):
        return self.get_channel(self.AS7263W)

    # Get the various CIE readings
    def get_x(self):
        return self.get_channel(self.AS7261X)

    def get_y(self):
        return self.get_channel(self.AS7261Y)

    def get_z(self):
        return self.get_channel(self.AS7261Z)

    def get_nir(self):
        return self.get_channel(self.AS7261_NIR)

    def get_dark(self):
        return self.get_channel(self.AS7261_DARK)

    def get_clear(self):
        return self.get_channel(self.AS7261_CLEAR)

    # Returns the various calibration data

    # AS7262
    def get_calibrated_violet(self):
        return self.get_calibrated_value(self.AS7262V_CAL)

    def get_calibrated_blue(self):
        return self.get_calibrated_value(self.AS7262B_CAL)

    def get_calibrated_green(self):
        return self.get_calibrated_value(self.AS7262G_CAL)

    def get_calibrated_yellow(self):
        return self.get_calibrated_value(self.AS7262Y_CAL)

    def get_calibrated_orange(self):
        return self.get_calibrated_value(self.AS7262O_CAL)

    def get_calibrated_red(self):
        return self.get_calibrated_value(self.AS7262R_CAL)

    # AS7263
    def get_calibrated_r(self):
        return self.get_calibrated_value(self.AS7263R_CAL)

    def get_calibrated_s(self):
        return self.get_calibrated_value(self.AS7263S_CAL)

    def get_calibrated_t(self):
        return self.get_calibrated_value(self.AS7263T_CAL)

    def get_calibrated_u(self):
        return self.get_calibrated_value(self.AS7263U_CAL)

    def get_calibrated_v(self):
        return self.get_calibrated_value(self.AS7263V_CAL)

    def get_calibrated_w(self):
        return self.get_calibrated_value(self.AS7263W_CAL)

    # AS7261
    def get_calibrated_x(self):
        return self.get_calibrated_value(self.AS7261X_CAL)

    def get_calibrated_y(self):
        return self.get_calibrated_value(self.AS7261Y_CAL)

    def get_calibrated_z(self):
        return self.get_calibrated_value(self.AS7261Z_CAL)

    def get_calibrated_x1931(self):
        return self.get_calibrated_value(self.AS7261X1931_CAL)

    def get_calibrated_y1931(self):
        return self.get_calibrated_value(self.AS7261Y1931_CAL)

    def get_calibrated_upri1976(self):
        return self.get_calibrated_value(self.AS7261_UPRI_CAL)

    def get_calibrated_vpri1976(self):
        return self.get_calibrated_value(self.AS7261_VPRI_CAL)

    def get_calibrated_u1976(self):
        return self.get_calibrated_value(self.AS7261U_CAL)

    def get_calibrated_v1976(self):
        return self.get_calibrated_value(self.AS7261V_CAL)

    def get_calibrated_duv1976(self):
        return self.get_calibrated_value(self.AS7261_DUV_CAL)

    def get_calibrated_lux(self):
        return self.get_channel(self.AS7261_LUX_CAL)

    def get_calibrated_cct(self):
        return self.get_channel(self.AS7261_CCT_CAL)
    
    # Helper functions
    def get_channel(self, channel_reg):
        """!
        Get the value of a channel

        @param channel_reg: **int** The register to read the channel from
        """
        color_data = self.virtual_read_register(channel_reg) << 8  # High byte
        color_data |= self.virtual_read_register(channel_reg + 1)  # Low byte
        return color_data

    def get_calibrated_value(self, cal_address):
        """!
        Given an address, read four bytes and return the floating point calibrated value

        @param cal_address: **int** The address to read the calibrated value from

        @return **float** The calibrated value
        """
        b0 = self.virtual_read_register(cal_address + 0)
        b1 = self.virtual_read_register(cal_address + 1)
        b2 = self.virtual_read_register(cal_address + 2)
        b3 = self.virtual_read_register(cal_address + 3)

        # Channel calibrated values are stored big-endian
        cal_bytes = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3

        return self.convert_bytes_to_float(cal_bytes)
    
    def convert_bytes_to_float(self, my_long):
        """!
        Convert a 4-byte value containing the bytes of a float respresentation of a number 
        to a float value

        @param my_long: **int** The 4-byte value to convert

        @return **float** The float value
        """
        packed_val = struct.pack('I', my_long)
        return struct.unpack('f', packed_val)[0]

    def clear_data_available(self):
        """!
        Clear the data ready flag in the config register
        """
        value = self.virtual_read_register(self.CONFIG)
        value &= ~self.CONFIG_DATA_READY_MASK
        self.virtual_write_register(self.CONFIG, value)

    def virtual_read_register(self, virtual_addr):
        """!
        Read a virtual register from the AS726x

        @param virtual_addr: **int** The virtual register address to read

        @return **int** The value read from the register or -1 if an error occurred
        """
        status = self._i2c.read_byte(self.address, self.STATUS_REG)

        # Do a prelim check of the read register
        if status & self.RX_VALID != 0:
               self._i2c.read_byte(self.address, self.READ_REG) # read, but do nothing with it
        
        # Wait for WRITE flag to clear
        retries = 0
        while True:
            status = self._i2c.read_byte(self.address, self.STATUS_REG)
            if status & self.TX_VALID == 0:
                break
            self._i2c.delay_ms(self.POLLING_DELAY)
            retries += 1
            if retries > self.MAX_RETRIES:
                return -1
        
        # Send the virtual register address
        self._i2c.write_byte(self.address, self.WRITE_REG, virtual_addr)

        # Wait for READ flag to be set
        retries = 0
        while True:
            status = self._i2c.read_byte(self.address, self.STATUS_REG)
            if status & self.RX_VALID != 0:
                break
            self._i2c.delay_ms(self.POLLING_DELAY)
            retries += 1
            if retries > self.MAX_RETRIES:
                return -1

        return self._i2c.read_byte(self.address, self.READ_REG)


    def virtual_write_register(self, virtual_addr, data_to_write):
        """!
        Write a virtual register to the AS726x

        @param virtual_addr: **int** The virtual register address to write
        @param data_to_write: **int** The value to write to the register

        @return **bool** `True` if successful, otherwise `False`
        """
        # Wait for WRITE register to be empty
        retries = 0
        while True:
            status = self._i2c.read_byte(self.address, self.STATUS_REG)
            if status & self.TX_VALID == 0:
                break
            self._i2c.delay_ms(self.POLLING_DELAY)
            retries += 1
            if retries > self.MAX_RETRIES:
                return False
        
        # Send the virtual register address (bit 7 should be 1 to indicate we're writing)
        self._i2c.write_byte(self.address, self.WRITE_REG, virtual_addr | 0x80)

        # Wait for WRITE register to be empty
        retries = 0
        while True:
            status = self._i2c.read_byte(self.address, self.STATUS_REG)
            if status & self.TX_VALID == 0:
                break
            self._i2c.delay_ms(self.POLLING_DELAY)
            retries += 1
            if retries > self.MAX_RETRIES:
                return False
        
        # Send the data to write
        self._i2c.write_byte(self.address, self.WRITE_REG, data_to_write)
        
        return True
    