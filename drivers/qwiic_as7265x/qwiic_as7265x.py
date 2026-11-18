#-------------------------------------------------------------------------------
# qwiic_as7265x.py
#
# Python library for the SparkFun Qwiic Triad Spectroscopy Sensor AS7265x, available here:
# https://www.sparkfun.com/products/15050
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
qwiic_as7265x
============
Python module for the [SparkFun Qwiic Triad Spectroscopy Sensor AS7265x](https://www.sparkfun.com/products/15050)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_AS7265x_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c
import struct # Confirmed present on both CircuitPython and MicroPython

__version__ = "3.0.0"

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic AS7265x"
# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x49]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicAS7265x(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Device Regs
    STATUS_REG = 0x00
    WRITE_REG = 0x01
    READ_REG = 0x02

    TX_VALID = 0x02
    RX_VALID = 0x01

    # Register addresses
    HW_VERSION_HIGH = 0x00
    HW_VERSION_LOW = 0x01

    FW_VERSION_HIGH = 0x02
    FW_VERSION_LOW = 0x03

    CONFIG = 0x04
    INTEGRATION_TIME = 0x05
    DEVICE_TEMP = 0x06
    LED_CONFIG = 0x07

    # Raw channel registers
    RGA = 0x08
    SHB = 0x0A
    TIC = 0x0C
    UJD = 0x0E
    VKE = 0x10
    WLF = 0x12

    # Calibrated channel registers
    RGA_CAL = 0x14
    SHB_CAL = 0x18
    TIC_CAL = 0x1C
    UJD_CAL = 0x20
    VKE_CAL = 0x24
    WLF_CAL = 0x28

    DEV_SELECT_CONTROL = 0x4F

    COEF_DATA0 = 0x50
    COEF_DATA1 = 0x51
    COEF_DATA2 = 0x52
    COEF_DATA3 = 0x53
    COEF_DATA_READ = 0x54
    COEF_DATA_WRITE = 0x55

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

    # Necessary DEV_SEL Register bits
    DEV_SEL_SECOND_SLAVE_SHIFT = 5
    DEV_SEL_SECOND_SLAVE_MASK = 0b1 << DEV_SEL_SECOND_SLAVE_SHIFT
    DEV_SEL_FIRST_SLAVE_SHIFT = 4
    DEV_SEL_FIRST_SLAVE_MASK = 0b1 << DEV_SEL_FIRST_SLAVE_SHIFT
    DEV_SEL_SELECT_SHIFT = 0
    DEV_SEL_SELECT_MASK = 0b11 << DEV_SEL_SELECT_SHIFT

    # Necessary LED Config Register Bits
    LED_CONFIG_LED_DRV_SHIFT = 4
    LED_CONFIG_LED_DRV_MASK = 0b11 << LED_CONFIG_LED_DRV_SHIFT
    LED_CONFIG_LED_ENABLE_SHIFT = 3
    LED_CONFIG_LED_ENABLE_MASK = 0b1 << LED_CONFIG_LED_ENABLE_SHIFT
    LED_CONFIG_IND_CURRENT_SHIFT = 1
    LED_CONFIG_IND_CURRENT_MASK = 0b11 << LED_CONFIG_IND_CURRENT_SHIFT
    LED_CONFIG_IND_ENABLE_SHIFT = 0
    LED_CONFIG_IND_ENABLE_MASK = 0b1 << LED_CONFIG_IND_ENABLE_SHIFT

    # Settings
    POLLING_DELAY = 5  # Amount of ms to wait between checking for virtual register changes

    AS72651_NIR = 0x00
    AS72652_VISIBLE = 0x01
    AS72653_UV = 0x02

    LED_WHITE = 0x00  # White LED is connected to x51
    LED_IR = 0x01     # IR LED is connected to x52
    LED_UV = 0x02     # UV LED is connected to x53

    LED_CURRENT_LIMIT_12_5MA = 0b00
    LED_CURRENT_LIMIT_25MA = 0b01
    LED_CURRENT_LIMIT_50MA = 0b10
    LED_CURRENT_LIMIT_100MA = 0b11

    INDICATOR_CURRENT_LIMIT_1MA = 0b00
    INDICATOR_CURRENT_LIMIT_2MA = 0b01
    INDICATOR_CURRENT_LIMIT_4MA = 0b10
    INDICATOR_CURRENT_LIMIT_8MA = 0b11

    GAIN_1X = 0b00
    GAIN_37X = 0b01
    GAIN_16X = 0b10
    GAIN_64X = 0b11

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

        # This is based on integration cycles and set by set_integration_cycles
        # We will initialize to the max value of 255 so that the device will wait 
        # for the maximum amount of time before timing out
        self._max_wait_time = int(255 * 2.8 * 1.5)

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
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        # Check to see if both slaves are detected
        value = self.virtual_read_register(self.DEV_SELECT_CONTROL)
        if value & (self.DEV_SEL_FIRST_SLAVE_MASK | value & self.DEV_SEL_SECOND_SLAVE_MASK) == 0:
            return False # No slaves detected
        
        self.set_bulb_current(self.LED_CURRENT_LIMIT_12_5MA, self.LED_WHITE)
        self.set_bulb_current(self.LED_CURRENT_LIMIT_12_5MA, self.LED_IR)
        self.set_bulb_current(self.LED_CURRENT_LIMIT_12_5MA, self.LED_UV)

        # Turn off bulbs to avoid heating sensor
        self.disable_bulb(self.LED_WHITE)
        self.disable_bulb(self.LED_IR)
        self.disable_bulb(self.LED_UV)

        # Set the indicator LED to 8mA (max)
        self.set_indicator_current(self.INDICATOR_CURRENT_LIMIT_8MA)
        self.enable_indicator()

        self.set_integration_cycles(49) # 50 * 2.8ms = 140ms. 0 to 255 is valid.
        # If you use Mode 2 or 3 (all the colors) then integration time is double. 140*2 = 280ms between readings.

        # Set to 64x gain and one-shot read of VBGYOR
        self.set_gain(self.GAIN_64X)
        self.set_measurement_mode(self.MEASUREMENT_MODE_6CHAN_ONE_SHOT)

        self.enable_interrupt()

        return True
    
    def get_device_type(self):
        """!
        Returns the device type (HW Version High Byte)

        @return **int** The device type
        """
        return self.virtual_read_register(self.HW_VERSION_HIGH)

    def get_hardware_version(self):
        """!
        Returns the hardware version of the device

        @return **int** The hardware version of the device
        """
        return self.virtual_read_register(self.HW_VERSION_LOW)

    def get_major_firmware_version(self):
        """!
        Get the major firmware version of the device

        @return **int** The major firmware version
        """
        self.virtual_write_register(self.FW_VERSION_HIGH, 0x01) # Set to 0x01 for Major
        self.virtual_write_register(self.FW_VERSION_LOW, 0x01) # Set to 0x01 for Major

        return self.virtual_read_register(self.FW_VERSION_LOW)

    def get_patch_firmware_version(self):
        """!
        Get the patch firmware version of the device

        @return **int** The patch firmware version
        """
        self.virtual_write_register(self.FW_VERSION_HIGH, 0x02)  # Set to 0x02 for Patch
        self.virtual_write_register(self.FW_VERSION_LOW, 0x02)   # Set to 0x02 for Patch

        return self.virtual_read_register(self.FW_VERSION_LOW)

    def get_build_firmware_version(self):
        """!
        Get the build firmware version of the device

        @return **int** The build firmware version
        """
        self.virtual_write_register(self.FW_VERSION_HIGH, 0x03)  # Set to 0x03 for Build
        self.virtual_write_register(self.FW_VERSION_LOW, 0x03)   # Set to 0x03 for Build

        return self.virtual_read_register(self.FW_VERSION_LOW)

    def get_temperature(self, device = 0):
        """!
        Returns the temperature of a given device in Celsius

        @param device: **int** The device to get the temperature from

        @return **int** The temperature in Celsius
        """
        self.select_device(device)
        return self.virtual_read_register(self.DEVICE_TEMP)

    def get_temperature_average(self):
        """!
        Get the average temperature from all three devices

        @return **float** The average temperature in Celsius
        """
        average = 0.0

        for device in [self.LED_WHITE, self.LED_IR, self.LED_UV]:
            average += self.get_temperature(device)

        return average / 3

    def take_measurements(self):
        """!
        Tells IC to take all channel measurements and polls for data ready flag
        """
        # Set mode to all 6-channels, one-shot
        self.set_measurement_mode(self.MEASUREMENT_MODE_6CHAN_ONE_SHOT)

        time_waited = 0
        while self.data_available() == False:
            if time_waited > self._max_wait_time:
                return
            self._i2c.delay_ms(self.POLLING_DELAY)
            time_waited += self.POLLING_DELAY
        
        # Readings can now be accessed via get_calibrated_a(), get_j(), etc.

    def take_measurements_with_bulb(self):
        """!
        Turns on all bulbs, takes measurements of all channels, turns off all bulbs
        """
        self.enable_bulb(self.LED_WHITE)
        self.enable_bulb(self.LED_IR)
        self.enable_bulb(self.LED_UV)

        self.take_measurements()

        self.disable_bulb(self.LED_WHITE)
        self.disable_bulb(self.LED_IR)
        self.disable_bulb(self.LED_UV)

    def enable_indicator(self):
        """!
        Enable the onboard indicator LED
        """
        self.select_device(self.AS72651_NIR)

        value = self.virtual_read_register(self.LED_CONFIG)
        value |= self.LED_CONFIG_IND_ENABLE_MASK

        self.virtual_write_register(self.LED_CONFIG, value)

    def disable_indicator(self):
        """!
        Disable the onboard indicator LED
        """
        self.select_device(self.AS72651_NIR)

        value = self.virtual_read_register(self.LED_CONFIG)
        value &= ~self.LED_CONFIG_IND_ENABLE_MASK

        self.virtual_write_register(self.LED_CONFIG, value)

    def enable_bulb(self, device):
        """!
        Enable the LED or bulb on a given device

        @param device: **int** The device to enable the LED for

        Allowable device values are:
            - LED_WHITE
            - LED_IR
            - LED_UV
        """
        self.select_device(device)

        value = self.virtual_read_register(self.LED_CONFIG)
        value |= self.LED_CONFIG_LED_ENABLE_MASK

        self.virtual_write_register(self.LED_CONFIG, value)

    def disable_bulb(self, device):
        """!
        Disable the LED or bulb on a given device

        @param device: **int** The device to disable the LED for

        Allowable device values are:
            - LED_WHITE
            - LED_IR
            - LED_UV
        """
        self.select_device(device)

        value = self.virtual_read_register(self.LED_CONFIG)
        value &= ~self.LED_CONFIG_LED_ENABLE_MASK

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

    def set_integration_cycles(self, cycle_value):
        """!
        Sets the integration cycle amount. 
        Give this function a byte from 0 to 255.
        Time will be 2.8ms * [integration cycles + 1]

        @param cycle_value: **int** The number of integration cycles to set
        """
        self._max_wait_time = int(cycle_value * 2.8 * 1.5) + 1 # Wait for 1.5 times the integration time before timing out
        self.virtual_write_register(self.INTEGRATION_TIME, cycle_value)

    def set_bulb_current(self, current, device):
        """!
        Set the current for the specified LED

        @param current: **int** The current to set the LED to

        Allowable current values are:
            - LED_CURRENT_LIMIT_12_5MA
            - LED_CURRENT_LIMIT_25MA
            - LED_CURRENT_LIMIT_50MA
            - LED_CURRENT_LIMIT_100MA
        @param device: **int** The device to set the current for
        """
        self.select_device(device)

        if current > self.LED_CURRENT_LIMIT_100MA:
            current = self.LED_CURRENT_LIMIT_100MA
        
        value = self.virtual_read_register(self.LED_CONFIG)
        value &= ~self.LED_CONFIG_LED_DRV_MASK
        value |= current << self.LED_CONFIG_LED_DRV_SHIFT

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
        self.select_device(self.AS72651_NIR)

        if current > self.INDICATOR_CURRENT_LIMIT_8MA:
            current = self.INDICATOR_CURRENT_LIMIT_8MA

        value = self.virtual_read_register(self.LED_CONFIG)
        value &= ~self.LED_CONFIG_IND_CURRENT_MASK

        value |= current << self.LED_CONFIG_IND_CURRENT_SHIFT

        self.virtual_write_register(self.LED_CONFIG, value)

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

    def soft_reset(self):
        """!
        Does a soft reset. Give sensor at least 1000ms to reset
        """
        value = self.virtual_read_register(self.CONFIG)
        value |= (1 << self.CONFIG_SRST_SHIFT)
        self.virtual_write_register(self.CONFIG, value) 

    def data_available(self):
        """!
        Check if the data ready flag is set in the control setup register

        @return **bool** `True` if the data ready flag is set, otherwise `False`
        """
        value = self.virtual_read_register(self.CONFIG)
        return (value & self.CONFIG_DATA_READY_MASK) != 0

    # The below functions return the various calibration data
    # UV
    def get_calibrated_a(self):
        return self.get_calibrated_value(self.RGA_CAL, self.AS72653_UV)

    def get_calibrated_b(self):
        return self.get_calibrated_value(self.SHB_CAL, self.AS72653_UV)

    def get_calibrated_c(self):
        return self.get_calibrated_value(self.TIC_CAL, self.AS72653_UV)

    def get_calibrated_d(self):
        return self.get_calibrated_value(self.UJD_CAL, self.AS72653_UV)

    def get_calibrated_e(self):
        return self.get_calibrated_value(self.VKE_CAL, self.AS72653_UV)

    def get_calibrated_f(self):
        return self.get_calibrated_value(self.WLF_CAL, self.AS72653_UV)

    # Visible
    def get_calibrated_g(self):
        return self.get_calibrated_value(self.RGA_CAL, self.AS72652_VISIBLE)

    def get_calibrated_h(self):
        return self.get_calibrated_value(self.SHB_CAL, self.AS72652_VISIBLE)

    def get_calibrated_i(self):
        return self.get_calibrated_value(self.TIC_CAL, self.AS72652_VISIBLE)

    def get_calibrated_j(self):
        return self.get_calibrated_value(self.UJD_CAL, self.AS72652_VISIBLE)

    def get_calibrated_k(self):
        return self.get_calibrated_value(self.VKE_CAL, self.AS72652_VISIBLE)

    def get_calibrated_l(self):
        return self.get_calibrated_value(self.WLF_CAL, self.AS72652_VISIBLE)

    # NIR
    def get_calibrated_r(self):
        return self.get_calibrated_value(self.RGA_CAL, self.AS72651_NIR)

    def get_calibrated_s(self):
        return self.get_calibrated_value(self.SHB_CAL, self.AS72651_NIR)

    def get_calibrated_t(self):
        return self.get_calibrated_value(self.TIC_CAL, self.AS72651_NIR)

    def get_calibrated_u(self):
        return self.get_calibrated_value(self.UJD_CAL, self.AS72651_NIR)

    def get_calibrated_v(self):
        return self.get_calibrated_value(self.VKE_CAL, self.AS72651_NIR)

    def get_calibrated_w(self):
        return self.get_calibrated_value(self.WLF_CAL, self.AS72651_NIR)

    # Get the various Channel data

    # Visible
    def get_g(self):
        return self.get_channel(self.RGA, self.AS72652_VISIBLE)

    def get_h(self):
        return self.get_channel(self.SHB, self.AS72652_VISIBLE)

    def get_i(self):
        return self.get_channel(self.TIC, self.AS72652_VISIBLE)

    def get_j(self):
        return self.get_channel(self.UJD, self.AS72652_VISIBLE)

    def get_k(self):
        return self.get_channel(self.VKE, self.AS72652_VISIBLE)

    def get_l(self):
        return self.get_channel(self.WLF, self.AS72652_VISIBLE)

    # NIR
    def get_r(self):
        return self.get_channel(self.RGA, self.AS72651_NIR)

    def get_s(self):
        return self.get_channel(self.SHB, self.AS72651_NIR)

    def get_t(self):
        return self.get_channel(self.TIC, self.AS72651_NIR)

    def get_u(self):
        return self.get_channel(self.UJD, self.AS72651_NIR)

    def get_v(self):
        return self.get_channel(self.VKE, self.AS72651_NIR)

    def get_w(self):
        return self.get_channel(self.WLF, self.AS72651_NIR)

    # UV
    def get_a(self):
        return self.get_channel(self.RGA, self.AS72653_UV)

    def get_b(self):
        return self.get_channel(self.SHB, self.AS72653_UV)

    def get_c(self):
        return self.get_channel(self.TIC, self.AS72653_UV)

    def get_d(self):
        return self.get_channel(self.UJD, self.AS72653_UV)

    def get_e(self):
        return self.get_channel(self.VKE, self.AS72653_UV)

    def get_f(self):
        return self.get_channel(self.WLF, self.AS72653_UV)

    def get_channel(self, channel_reg, device):
        """!
        Get the channel data for a specific device

        @param channel_reg: **int** The register address of the channel
        @param device: **int** The device to get the channel data from

        @return **int** The channel data
        """
        self.select_device(device)
        color_data = self.virtual_read_register(channel_reg) << 8  # High byte
        color_data |= self.virtual_read_register(channel_reg + 1)  # Low byte
        return color_data

    def get_calibrated_value(self, cal_address, device):
        """!
        Given an address, read four bytes and return the floating point calibrated value

        @param cal_address: **int** The address to read the calibrated value from
        @param device: **int** The device to read the calibrated value from

        @return **float** The calibrated value
        """
        self.select_device(device)

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

    def select_device(self, device):
        """!
        Point the master at either the first or the second slave

        @param device: **int** The device to select

        Allowable device values are:
            - LED_WHITE
            - LED_IR
            - LED_UV
            - AS72651_NIR (arduino lib uses this value in the indicator() functions)
        """
        self.virtual_write_register(self.DEV_SELECT_CONTROL, device)

    def virtual_read_register(self, virtual_addr):
        """!
        Read a virtual register from the AS7265x

        @param virtual_addr: **int** The virtual register address to read

        @return **int** The value of the virtual register
        """
        status = self._i2c.read_byte(self.address, self.STATUS_REG)

        # Do a prelim check of the read register
        if status & self.RX_VALID:
            self._i2c.read_byte(self.address, self.READ_REG) # Read byte but do nothing with it

        # Wait for WRITE flag to clear
        time_waited = 0
        while time_waited <= self._max_wait_time:
            status = self._i2c.read_byte(self.address, self.STATUS_REG)
            if status & self.TX_VALID == 0:
                break
            self._i2c.delay_ms(self.POLLING_DELAY)
            time_waited += self.POLLING_DELAY

        # Write the virtual register address to the device
        self._i2c.write_byte(self.address, self.WRITE_REG, virtual_addr)

        # Wait for READ flag to be set
        time_waited = 0
        while time_waited <= self._max_wait_time:
            status = self._i2c.read_byte(self.address, self.STATUS_REG)
            if status & self.RX_VALID:
                break
            self._i2c.delay_ms(self.POLLING_DELAY)
            time_waited += self.POLLING_DELAY
        
        # Read the virtual register
        return self._i2c.read_byte(self.address, self.READ_REG)
    
    def virtual_write_register(self, virtual_addr, data):
        """!
        Write a virtual register to the AS7265x

        @param virtual_addr: **int** The virtual register address to write
        @param data: **int** The data byte to write to the virtual register
        """

        # Wait for WRITE regiser to be empty
        time_waited = 0
        while time_waited <= self._max_wait_time:
            status = self._i2c.read_byte(self.address, self.STATUS_REG)
            if status & self.TX_VALID == 0:
                break
            self._i2c.delay_ms(self.POLLING_DELAY)
            time_waited += self.POLLING_DELAY
        
        # Write the virtual register address to the device (we set the MSB to 1 to indicate a write)
        self._i2c.write_byte(self.address, self.WRITE_REG, virtual_addr | 0x80)

        # Wait for WRITE register to be empty
        time_waited = 0
        while time_waited <= self._max_wait_time:
            status = self._i2c.read_byte(self.address, self.STATUS_REG)
            if status & self.TX_VALID == 0:
                break
            self._i2c.delay_ms(self.POLLING_DELAY)
            time_waited += self.POLLING_DELAY

        # Write the data to the virtual register
        self._i2c.write_byte(self.address, self.WRITE_REG, data)

