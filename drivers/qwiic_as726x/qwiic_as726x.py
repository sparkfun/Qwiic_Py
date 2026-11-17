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
import time
import struct

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
    kStatusReg = 0x00
    kWriteReg = 0x01
    kReadReg = 0x02

    kTxValid = 0x02
    kRxValid = 0x01

    # Register Addresses
    kDeviceType = 0x00
    kHwVersion = 0x01
    kConfig = 0x04
    kIntegrationTime = 0x05
    kDeviceTemp = 0x06
    kLedConfig = 0x07

    # The same register locations are shared between the AS7262 and AS7263, they're just called something different
    # AS7262 Registers
    kAs7262V = 0x08
    kAs7262B = 0x0A
    kAs7262G = 0x0C
    kAs7262Y = 0x0E
    kAs7262O = 0x10
    kAs7262R = 0x12
    kAs7262VCal = 0x14
    kAs7262BCal = 0x18
    kAs7262GCal = 0x1C
    kAs7262YCal = 0x20
    kAs7262OCal = 0x24
    kAs7262RCal = 0x28

    # AS7263 Registers
    kAs7263R = 0x08
    kAs7263S = 0x0A
    kAs7263T = 0x0C
    kAs7263U = 0x0E
    kAs7263V = 0x10
    kAs7263W = 0x12
    kAs7263RCal = 0x14
    kAs7263SCal = 0x18
    kAs7263TCal = 0x1C
    kAs7263UCal = 0x20
    kAs7263VCal = 0x24
    kAs7263WCal = 0x28

    # AS7261 Registers
    kAs7261X = 0x08  # 16b
    kAs7261Y = 0x0A  # 16b
    kAs7261Z = 0x0C  # 16b
    kAs7261Nir = 0x0E  # 16b
    kAs7261Dark = 0x10  # 16b
    kAs7261Clear = 0x12  # 16b
    kAs7261XCal = 0x14
    kAs7261YCal = 0x18
    kAs7261ZCal = 0x1C
    kAs7261X1931Cal = 0x20
    kAs7261Y1931Cal = 0x24
    kAs7261UpriCal = 0x28
    kAs7261VpriCal = 0x2C
    kAs7261UCal = 0x30
    kAs7261VCal = 0x34
    kAs7261DuvCal = 0x38
    kAs7261LuxCal = 0x3C  # 16b
    kAs7261CctCal = 0x3E  # 16b

    kSensorTypeAs7261 = 0x3D
    kSensorTypeAs7262 = 0x3E
    kSensorTypeAs7263 = 0x3F

    kPollingDelay = 5  # Amount of ms to wait between checking for virtual register changes
    kMaxRetries = 3
    kTimeout = 3000
    
    # Necessary Config Register bits
    kConfigSRSTShift = 7
    kConfigSRSTMask = 0b1 << kConfigSRSTShift
    kConfigIntShift = 6
    kConfigIntMask = 0b1 << kConfigIntShift
    kConfigGainShift = 4
    kConfigGainMask = 0b11 << kConfigGainShift
    kConfigModeShift = 2
    kConfigModeMask = 0b11 << kConfigModeShift
    kConfigDataReadyShift = 1
    kConfigDataReadyMask = 0b1 << kConfigDataReadyShift
    kConfigFRSTShift = 0
    kConfigFRSTMask = 0b1 << kConfigFRSTShift

    # Necessary LED Config Register Bits
    kLedConfigLedDrvShift = 4
    kLedConfigLedDrvMask = 0b11 << kLedConfigLedDrvShift
    kLedConfigLedEnableShift = 3
    kLedConfigLedEnableMask = 0b1 << kLedConfigLedEnableShift
    kLedConfigIndCurrentShift = 1
    kLedConfigIndCurrentMask = 0b11 << kLedConfigIndCurrentShift
    kLedConfigIndEnableShift = 0
    kLedConfigIndEnableMask = 0b1 << kLedConfigIndEnableShift

    # Values to write to current limit, gain, and mode 
    kLedCurrentLimit12_5mA = 0b00
    kLedCurrentLimit25mA = 0b01
    kLedCurrentLimit50mA = 0b10
    kLedCurrentLimit100mA = 0b11

    kIndicatorCurrentLimit1mA = 0b00
    kIndicatorCurrentLimit2mA = 0b01
    kIndicatorCurrentLimit4mA = 0b10
    kIndicatorCurrentLimit8mA = 0b11

    kGain1x = 0b00
    kGain37x = 0b01 #3.7x 
    kGain16x = 0b10 #16x
    kGain64x = 0b11 #64x

    kMeasurementMode4Chan = 0b00
    kMeasurementMode4Chan2 = 0b01
    kMeasurementMode6ChanContinuous = 0b10
    kMeasurementMode6ChanOneShot = 0b11

    def __init__(self, address=None, i2c_driver=None):
        """!
        Constructor

        @param int, optional address: The I2C address to use for the device
            If not provided, the default address is used
        @param I2CDriver, optional i2c_driver: An existing i2c driver object
            If not provided, a driver object is created
        """

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

        self._sensorVersion = 0

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self, gain = kGain64x, measurementMode = kMeasurementMode6ChanOneShot):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        self._sensorVersion = self.virtual_read_register(self.kHwVersion)

        if self._sensorVersion not in [self.kSensorTypeAs7261, self.kSensorTypeAs7262, self.kSensorTypeAs7263]:
            return False
        
        # Set Bulb to 12.5mA (minimum)
        self.set_bulb_current(self.kLedCurrentLimit12_5mA)
        self.disable_bulb() # To avoid overheating

        # Set Indicator to 8mA (maximum)
        self.set_indicator_current(self.kIndicatorCurrentLimit8mA)
        self.disable_indicator() # To save power

        self.set_integration_time(50) # 50 * 2.8ms = 140ms. 0 to 255 is valid.

        # If you use Mode 2 or 3 (all the colors) then integration time is double.
        # 140*2 = 280ms between readings.

        # Set gain and measurement mode (default to 64x and 6 channel one-shot)
        self.set_gain(gain)
        self.set_measurement_mode(measurementMode)

        return True

    def take_measurements(self):
        """!
        Tells IC to take measurements and polls for data ready flag

        @return  `True` if successful, otherwise `False`
        
        """
        # Clear the data ready flag
        self.clear_data_available()

        # Set the measurement mode to one-shot for all 6 channels
        self.set_measurement_mode(self.kMeasurementMode6ChanOneShot)

        time_waited = 0
        while self.data_available() == False:
            time.sleep(self. kPollingDelay / 1000)
            time_waited += self.kPollingDelay
            if time_waited > self.kTimeout:
                return False

        # Readings can now be accessed via getViolet(), getBlue(), etc
        return True

    def get_version(self):
        """!
        Get the version of the sensor. Value is only valid after a call to `begin()`

        @return **int** The version of the sensor
        """
        return self._sensorVersion

    def take_measurements_with_bulb(self):
        """!
        Turns on bulb, takes measurements, turns off bulb.

        NOTE: We don't turn on the indicator as it is red and may corrupt the readings
        """
        self.enable_bulb()
        self.take_measurements()
        self.disable_bulb()

    def get_temperature(self, device):
        """!
        Returns the temperature of a given device in Celsius

        @param int device: The device to get the temperature from
        """
        return self.virtual_read_register(self.kDeviceTemp)

    def get_temperature_f(self):
        """!
        Returns the temperature of a given device in Fahrenheit

        @param int device: The device to get the temperature from
        """
        return (self.virtual_read_register(self.kDeviceTemp) * 1.8) + 32

    def set_measurement_mode(self, mode):
        """!
        Sets the measurement mode

        Mode 0: 4 channels out of 6 (see datasheet)
        Mode 1: Different 4 channels out of 6 (see datasheet)
        Mode 2: All 6 channels continuously
        Mode 3: One-shot reading of all channels

        @param int mode: The mode to set

        Allowable mode values are:
            - kMeasurementMode4Chan
            - kMeasurementMode4Chan2
            - kMeasurementMode6ChanContinuous
            - kMeasurementMode6ChanOneShot
        """
        if mode > self.kMeasurementMode6ChanOneShot:
            mode = self.kMeasurementMode6ChanOneShot

        value = self.virtual_read_register(self.kConfig)
        value &= ~self.kConfigModeMask
        value |= mode << self.kConfigModeShift

        self.virtual_write_register(self.kConfig, value)

    def get_measurement_mode(self):
        """!
        Get the measurement mode

        @return **int** The measurement mode

        Allowable mode values are:
            - kMeasurementMode4Chan
            - kMeasurementMode4Chan2
            - kMeasurementMode6ChanContinuous
            - kMeasurementMode6ChanOneShot
        """
        value = self.virtual_read_register(self.kConfig)
        return (value & self.kConfigModeMask) >> self.kConfigModeShift

    def data_available(self):
        """!
        Check if the data ready flag is set in the control setup register

        @return **bool** `True` if the data ready flag is set, otherwise `False`
        """
        value = self.virtual_read_register(self.kConfig)
        return (value & self.kConfigDataReadyMask) != 0

    def enable_indicator(self):
        """!
        Enable the onboard indicator LED
        """

        value = self.virtual_read_register(self.kLedConfig)
        value |= self.kLedConfigIndEnableMask

        self.virtual_write_register(self.kLedConfig, value)

    def disable_indicator(self):
        """!
        Disable the onboard indicator LED
        """

        value = self.virtual_read_register(self.kLedConfig)
        value &= ~self.kLedConfigIndEnableMask

        self.virtual_write_register(self.kLedConfig, value)

    def set_indicator_current(self, current):
        """!
        Set the current limit of onboard LED. Default is max 8mA = 0b11.

        @param int current: The current limit to set the indicator LED to

        Allowable current values are:
            - kIndicatorCurrentLimit1mA
            - kIndicatorCurrentLimit2mA
            - kIndicatorCurrentLimit4mA
            - kIndicatorCurrentLimit8mA
        """
        if current > self.kIndicatorCurrentLimit8mA:
            current = self.kIndicatorCurrentLimit8mA

        value = self.virtual_read_register(self.kLedConfig)
        value &= ~self.kLedConfigIndCurrentMask

        value |= current << self.kLedConfigIndCurrentShift

        self.virtual_write_register(self.kLedConfig, value)

    def enable_bulb(self):
        """!
        Enable the LED or bulb on a given device
        """

        value = self.virtual_read_register(self.kLedConfig)
        value |= self.kLedConfigLedEnableMask

        self.virtual_write_register(self.kLedConfig, value)

    def disable_bulb(self):
        """!
        Disable the LED or bulb on a given device
        """

        value = self.virtual_read_register(self.kLedConfig)
        value &= ~self.kLedConfigLedEnableMask

        self.virtual_write_register(self.kLedConfig, value)


    def set_bulb_current(self, current):
        """!
        Set the current for the specified LED

        @param int current: The current to set the LED to

        Allowable current values are:
            - kLedCurrentLimit12_5mA
            - kLedCurrentLimit25mA
            - kLedCurrentLimit50mA
            - kLedCurrentLimit100mA
        """

        if current > self.kLedCurrentLimit100mA:
            current = self.kLedCurrentLimit100mA
        
        value = self.virtual_read_register(self.kLedConfig)
        value &= ~self.kLedConfigLedDrvMask
        value |= current << self.kLedConfigLedDrvShift

        self.virtual_write_register(self.kLedConfig, value)

    def set_gain(self, gain):
        """!
        Sets the gain value
        Gain 0: 1x (power-on default)
        Gain 1: 3.7x
        Gain 2: 16x
        Gain 3: 64x

        @param int gain: The gain value to set
        """
        if gain > self.kGain64x:
            gain = self.kGain64x

        value = self.virtual_read_register(self.kConfig)
        value &= ~self.kConfigGainMask
        value |= gain << self.kConfigGainShift

        self.virtual_write_register(self.kConfig, value)

    def get_gain(self):
        """!
        Get the gain value

        @return **int** The gain value
        """
        value = self.virtual_read_register(self.kConfig)
        return (value & self.kConfigGainMask) >> self.kConfigGainShift

    def soft_reset(self):
        """!
        Does a soft reset. Give sensor at least 1000ms to reset
        """
        value = self.virtual_read_register(self.kConfig)
        value |= (1 << self.kConfigSRSTShift)
        self.virtual_write_register(self.kConfig, value) 

    def set_integration_time(self, integrationValue):
        """!
        Sets the integration cycle amount. 
        Give this function a byte from 0 to 255.
        Time will be 2.8ms * [integration cycles + 1]

        @param int integrationValue: The number of integration cycles to set
        """
        self.virtual_write_register(self.kIntegrationTime, integrationValue)

    def get_integration_time(self):
        """!
        Get the integration time

        @return **int** The integration time
        """
        return self.virtual_read_register(self.kIntegrationTime)

    def enable_interrupt(self):
        """!
        Enable the interrupt pin
        """
        value = self.virtual_read_register(self.kConfig)
        value |= self.kConfigIntMask

        self.virtual_write_register(self.kConfig, value)

    def disable_interrupt(self):
        """!
        Disable the interrupt pin
        """
        value = self.virtual_read_register(self.kConfig)
        value &= ~self.kConfigIntMask

        self.virtual_write_register(self.kConfig, value)

    # Get the various color readings
    def get_violet(self):
        return self.get_channel(self.kAs7262V)

    def get_blue(self):
        return self.get_channel(self.kAs7262B)

    def get_green(self):
        return self.get_channel(self.kAs7262G)

    def get_yellow(self):
        return self.get_channel(self.kAs7262Y)

    def get_orange(self):
        return self.get_channel(self.kAs7262O)

    def get_red(self):
        return self.get_channel(self.kAs7262R)

    # Get the various NIR readings
    def get_r(self):
        return self.get_channel(self.kAs7263R)

    def get_s(self):
        return self.get_channel(self.kAs7263S)

    def get_t(self):
        return self.get_channel(self.kAs7263T)

    def get_u(self):
        return self.get_channel(self.kAs7263U)

    def get_v(self):
        return self.get_channel(self.kAs7263V)

    def get_w(self):
        return self.get_channel(self.kAs7263W)

    # Get the various CIE readings
    def get_x(self):
        return self.get_channel(self.kAs7261X)

    def get_y(self):
        return self.get_channel(self.kAs7261Y)

    def get_z(self):
        return self.get_channel(self.kAs7261Z)

    def get_nir(self):
        return self.get_channel(self.kAs7261Nir)

    def get_dark(self):
        return self.get_channel(self.kAs7261Dark)

    def get_clear(self):
        return self.get_channel(self.kAs7261Clear)

    # Returns the various calibration data

    # AS7262
    def get_calibrated_violet(self):
        return self.get_calibrated_value(self.kAs7262VCal)

    def get_calibrated_blue(self):
        return self.get_calibrated_value(self.kAs7262BCal)

    def get_calibrated_green(self):
        return self.get_calibrated_value(self.kAs7262GCal)

    def get_calibrated_yellow(self):
        return self.get_calibrated_value(self.kAs7262YCal)

    def get_calibrated_orange(self):
        return self.get_calibrated_value(self.kAs7262OCal)

    def get_calibrated_red(self):
        return self.get_calibrated_value(self.kAs7262RCal)

    # AS7263
    def get_calibrated_r(self):
        return self.get_calibrated_value(self.kAs7263RCal)

    def get_calibrated_s(self):
        return self.get_calibrated_value(self.kAs7263SCal)

    def get_calibrated_t(self):
        return self.get_calibrated_value(self.kAs7263TCal)

    def get_calibrated_u(self):
        return self.get_calibrated_value(self.kAs7263UCal)

    def get_calibrated_v(self):
        return self.get_calibrated_value(self.kAs7263VCal)

    def get_calibrated_w(self):
        return self.get_calibrated_value(self.kAs7263WCal)

    # AS7261
    def get_calibrated_x(self):
        return self.get_calibrated_value(self.kAs7261XCal)

    def get_calibrated_y(self):
        return self.get_calibrated_value(self.kAs7261YCal)

    def get_calibrated_z(self):
        return self.get_calibrated_value(self.kAs7261ZCal)

    def get_calibrated_x1931(self):
        return self.get_calibrated_value(self.kAs7261X1931Cal)

    def get_calibrated_y1931(self):
        return self.get_calibrated_value(self.kAs7261Y1931Cal)

    def get_calibrated_upri1976(self):
        return self.get_calibrated_value(self.kAs7261UpriCal)

    def get_calibrated_vpri1976(self):
        return self.get_calibrated_value(self.kAs7261VpriCal)

    def get_calibrated_u1976(self):
        return self.get_calibrated_value(self.kAs7261UCal)

    def get_calibrated_v1976(self):
        return self.get_calibrated_value(self.kAs7261VCal)

    def get_calibrated_duv1976(self):
        return self.get_calibrated_value(self.kAs7261DuvCal)

    def get_calibrated_lux(self):
        return self.get_channel(self.kAs7261LuxCal)

    def get_calibrated_cct(self):
        return self.get_channel(self.kAs7261CctCal)
    
    # Helper functions
    def get_channel(self, channelReg):
        """!
        Get the value of a channel

        @param int channel_register: The register to read the channel from
        """
        color_data = self.virtual_read_register(channelReg) << 8  # High byte
        color_data |= self.virtual_read_register(channelReg + 1)  # Low byte
        return color_data

    def get_calibrated_value(self, calAddress):
        """!
        Given an address, read four bytes and return the floating point calibrated value

        @param int calAddress: The address to read the calibrated value from

        @return **float** The calibrated value
        """
        b0 = self.virtual_read_register(calAddress + 0)
        b1 = self.virtual_read_register(calAddress + 1)
        b2 = self.virtual_read_register(calAddress + 2)
        b3 = self.virtual_read_register(calAddress + 3)

        # Channel calibrated values are stored big-endian
        calBytes = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3

        return self.convert_bytes_to_float(calBytes)
    
    def convert_bytes_to_float(self, myLong):
        """!
        Convert a 4-byte value containing the bytes of a float respresentation of a number 
        to a float value

        @param int myLong: The 4-byte value to convert

        @return **float** The float value
        """
        packed_val = struct.pack('I', myLong)
        return struct.unpack('f', packed_val)[0]

    def clear_data_available(self):
        """!
        Clear the data ready flag in the config register
        """
        value = self.virtual_read_register(self.kConfig)
        value &= ~self.kConfigDataReadyMask
        self._i2c.write_byte(self.address, self.kConfig, value)

    def virtual_read_register(self, virtualAddr):
        """!
        Read a virtual register from the AS726x

        @param int virtualAddr: The virtual register address to read

        @return **int** The value read from the register or -1 if an error occurred
        """
        status = self._i2c.read_byte(self.address, self.kStatusReg)

        # Do a prelim check of the read register
        if status & self.kRxValid != 0:
               self._i2c.read_byte(self.address, self.kReadReg) # read, but do nothing with it
        
        # Wait for WRITE flag to clear
        retries = 0
        while True:
            status = self._i2c.read_byte(self.address, self.kStatusReg)
            if status & self.kTxValid == 0:
                break
            time.sleep(self.kPollingDelay / 1000)
            retries += 1
            if retries > self.kMaxRetries:
                return -1
        
        # Send the virtual register address
        self._i2c.write_byte(self.address, self.kWriteReg, virtualAddr)

        # Wait for READ flag to be set
        retries = 0
        while True:
            status = self._i2c.read_byte(self.address, self.kStatusReg)
            if status & self.kRxValid != 0:
                break
            time.sleep(self.kPollingDelay / 1000)
            retries += 1
            if retries > self.kMaxRetries:
                return -1

        return self._i2c.read_byte(self.address, self.kReadReg)


    def virtual_write_register(self, virtualAddr, dataToWrite):
        """!
        Write a virtual register to the AS726x

        @param int virtualAddr: The virtual register address to write
        @param int dataToWrite: The value to write to the register

        @return **bool** `True` if successful, otherwise `False`
        """
        # Wait for WRITE register to be empty
        retries = 0
        while True:
            status = self._i2c.read_byte(self.address, self.kStatusReg)
            if status & self.kTxValid == 0:
                break
            time.sleep(self.kPollingDelay / 1000)
            retries += 1
            if retries > self.kMaxRetries:
                return False
        
        # Send the virtual register address (bit 7 should be 1 to indicate we're writing)
        self._i2c.write_byte(self.address, self.kWriteReg, virtualAddr | 0x80)

        # Wait for WRITE register to be empty
        retries = 0
        while True:
            status = self._i2c.read_byte(self.address, self.kStatusReg)
            if status & self.kTxValid == 0:
                break
            time.sleep(self.kPollingDelay / 1000)
            retries += 1
            if retries > self.kMaxRetries:
                return False
        
        # Send the data to write
        self._i2c.write_byte(self.address, self.kWriteReg, dataToWrite)
        
        return True
    