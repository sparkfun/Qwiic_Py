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
import time
import struct # Confirmed present on both CircuitPython and MicroPython

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
    kStatusReg = 0x00
    kWriteReg = 0x01
    kReadReg = 0x02

    kTxValid = 0x02
    kRxValid = 0x01

    # Register addresses
    kHwVersionHigh = 0x00
    kHwVersionLow = 0x01

    kFwVersionHigh = 0x02
    kFwVersionLow = 0x03

    kConfig = 0x04
    kIntegrationTime = 0x05
    kDeviceTemp = 0x06
    kLedConfig = 0x07

    # Raw channel registers
    kRGA = 0x08
    kSHB = 0x0A
    kTIC = 0x0C
    kUJD = 0x0E
    kVKE = 0x10
    kWLF = 0x12

    # Calibrated channel registers
    kRGACal = 0x14
    kSHBCal = 0x18
    kTICCal = 0x1C
    kUJDCal = 0x20
    kVKECal = 0x24
    kWLFCal = 0x28

    kDevSelectControl = 0x4F

    kCoefData0 = 0x50
    kCoefData1 = 0x51
    kCoefData2 = 0x52
    kCoefData3 = 0x53
    kCoefDataRead = 0x54
    kCoefDataWrite = 0x55

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

    # Necessary DEV_SEL Register bits
    kDevSelSecondSlaveShift = 5
    kDevSelSecondSlaveMask = 0b1 << kDevSelSecondSlaveShift
    kDevSelFirstSlaveShift = 4
    kDevSelFirstSlaveMask = 0b1 << kDevSelFirstSlaveShift
    kDevSelSelectShift = 0
    kDevSelSelectMask = 0b11 << kDevSelSelectShift

    # Necessary LED Config Register Bits
    kLedConfigLedDrvShift = 4
    kLedConfigLedDrvMask = 0b11 << kLedConfigLedDrvShift
    kLedConfigLedEnableShift = 3
    kLedConfigLedEnableMask = 0b1 << kLedConfigLedEnableShift
    kLedConfigIndCurrentShift = 1
    kLedConfigIndCurrentMask = 0b11 << kLedConfigIndCurrentShift
    kLedConfigIndEnableShift = 0
    kLedConfigIndEnableMask = 0b1 << kLedConfigIndEnableShift

    # Settings
    kPollingDelay = 5  # Amount of ms to wait between checking for virtual register changes

    kAS72651Nir = 0x00
    kAS72652Visible = 0x01
    kAS72653Uv = 0x02

    kLedWhite = 0x00  # White LED is connected to x51
    kLedIr = 0x01     # IR LED is connected to x52
    kLedUv = 0x02     # UV LED is connected to x53

    kLedCurrentLimit12_5mA = 0b00
    kLedCurrentLimit25mA = 0b01
    kLedCurrentLimit50mA = 0b10
    kLedCurrentLimit100mA = 0b11

    kIndicatorCurrentLimit1mA = 0b00
    kIndicatorCurrentLimit2mA = 0b01
    kIndicatorCurrentLimit4mA = 0b10
    kIndicatorCurrentLimit8mA = 0b11

    kGain1x = 0b00
    kGain37x = 0b01
    kGain16x = 0b10
    kGain64x = 0b11

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

        # This is based on integration cycles and set by set_integration_cycles
        # We will initialize to the max value of 255 so that the device will wait 
        # for the maximum amount of time before timing out
        self._maxWaitTime = int(255 * 2.8 * 1.5)

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        # Check to see if both slaves are detected
        value = self.virtual_read_register(self.kDevSelectControl)
        if value & (self.kDevSelFirstSlaveMask | value & self.kDevSelSecondSlaveMask) == 0:
            return False # No slaves detected
        
        self.set_bulb_current(self.kLedCurrentLimit12_5mA, self.kLedWhite)
        self.set_bulb_current(self.kLedCurrentLimit12_5mA, self.kLedIr)
        self.set_bulb_current(self.kLedCurrentLimit12_5mA, self.kLedUv)

        # Turn off bulbs to avoid heating sensor
        self.disable_bulb(self.kLedWhite)
        self.disable_bulb(self.kLedIr)
        self.disable_bulb(self.kLedUv)

        # Set the indicator LED to 8mA (max)
        self.set_indicator_current(self.kIndicatorCurrentLimit8mA)
        self.enable_indicator()

        self.set_integration_cycles(49) # 50 * 2.8ms = 140ms. 0 to 255 is valid.
        # If you use Mode 2 or 3 (all the colors) then integration time is double. 140*2 = 280ms between readings.

        # Set to 64x gain and one-shot read of VBGYOR
        self.set_gain(self.kGain64x)
        self.set_measurement_mode(self.kMeasurementMode6ChanOneShot)

        self.enable_interrupt()

        return True
    
    def get_device_type(self):
        """!
        Returns the device type (HW Version High Byte)

        @return **int** The device type
        """
        return self.virtual_read_register(self.kHwVersionHigh)

    def get_hardware_version(self):
        """!
        Returns the hardware version of the device

        @return **int** The hardware version of the device
        """
        return self.virtual_read_register(self.kHwVersionLow)

    def get_major_firmware_version(self):
        """!
        Get the major firmware version of the device

        @return **int** The major firmware version
        """
        self.virtual_write_register(self.kFwVersionHigh, 0x01) # Set to 0x01 for Major
        self.virtual_write_register(self.kFwVersionLow, 0x01) # Set to 0x01 for Major

        return self.virtual_read_register(self.kFwVersionLow)

    def get_patch_firmware_version(self):
        """!
        Get the patch firmware version of the device

        @return **int** The patch firmware version
        """
        self.virtual_write_register(self.kFwVersionHigh, 0x02)  # Set to 0x02 for Patch
        self.virtual_write_register(self.kFwVersionLow, 0x02)   # Set to 0x02 for Patch

        return self.virtual_read_register(self.kFwVersionLow)

    def get_build_firmware_version(self):
        """!
        Get the build firmware version of the device

        @return **int** The build firmware version
        """
        self.virtual_write_register(self.kFwVersionHigh, 0x03)  # Set to 0x03 for Build
        self.virtual_write_register(self.kFwVersionLow, 0x03)   # Set to 0x03 for Build

        return self.virtual_read_register(self.kFwVersionLow)

    def get_temperature(self, device = 0):
        """!
        Returns the temperature of a given device in Celsius

        @param int device: The device to get the temperature from

        @return **int** The temperature in Celsius
        """
        self.select_device(device)
        return self.virtual_read_register(self.kDeviceTemp)

    def get_temperature_average(self):
        """!
        Get the average temperature from all three devices

        @return **float** The average temperature in Celsius
        """
        average = 0.0

        for device in [self.kLedWhite, self.kLedIr, self.kLedUv]:
            average += self.get_temperature(device)

        return average / 3

    def take_measurements(self):
        """!
        Tells IC to take all channel measurements and polls for data ready flag
        """
        # Set mode to all 6-channels, one-shot
        self.set_measurement_mode(self.kMeasurementMode6ChanOneShot)

        timeWaited = 0
        while self.data_available() == False:
            if timeWaited > self._maxWaitTime:
                return
            time.sleep(self.kPollingDelay / 1000)
            timeWaited += self.kPollingDelay
        
        # Readings can now be accessed via getCalibratedA(), getJ(), etc.

    def take_measurements_with_bulb(self):
        """!
        Turns on all bulbs, takes measurements of all channels, turns off all bulbs
        """
        self.enable_bulb(self.kLedWhite)
        self.enable_bulb(self.kLedIr)
        self.enable_bulb(self.kLedUv)

        self.take_measurements()

        self.disable_bulb(self.kLedWhite)
        self.disable_bulb(self.kLedIr)
        self.disable_bulb(self.kLedUv)

    def enable_indicator(self):
        """!
        Enable the onboard indicator LED
        """
        self.select_device(self.kAS72651Nir)

        value = self.virtual_read_register(self.kLedConfig)
        value |= self.kLedConfigIndEnableMask

        self.virtual_write_register(self.kLedConfig, value)

    def disable_indicator(self):
        """!
        Disable the onboard indicator LED
        """
        self.select_device(self.kAS72651Nir)

        value = self.virtual_read_register(self.kLedConfig)
        value &= ~self.kLedConfigIndEnableMask

        self.virtual_write_register(self.kLedConfig, value)

    def enable_bulb(self, device):
        """!
        Enable the LED or bulb on a given device

        @param int device: The device to enable the LED for

        Allowable device values are:
            - kLedWhite
            - kLedIr
            - kLedUv
        """
        self.select_device(device)

        value = self.virtual_read_register(self.kLedConfig)
        value |= self.kLedConfigLedEnableMask

        self.virtual_write_register(self.kLedConfig, value)

    def disable_bulb(self, device):
        """!
        Disable the LED or bulb on a given device

        @param int device: The device to disable the LED for

        Allowable device values are:
            - kLedWhite
            - kLedIr
            - kLedUv
        """
        self.select_device(device)

        value = self.virtual_read_register(self.kLedConfig)
        value &= ~self.kLedConfigLedEnableMask

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

    def set_integration_cycles(self, cycleValue):
        """!
        Sets the integration cycle amount. 
        Give this function a byte from 0 to 255.
        Time will be 2.8ms * [integration cycles + 1]

        @param int cycleValue: The number of integration cycles to set
        """
        self._maxWaitTime = int(cycleValue * 2.8 * 1.5) + 1 # Wait for 1.5 times the integration time before timing out
        self.virtual_write_register(self.kIntegrationTime, cycleValue)

    def set_bulb_current(self, current, device):
        """!
        Set the current for the specified LED

        @param int current: The current to set the LED to

        Allowable current values are:
            - kLedCurrentLimit12_5mA
            - kLedCurrentLimit25mA
            - kLedCurrentLimit50mA
            - kLedCurrentLimit100mA
        @param int device: The device to set the current for
        """
        self.select_device(device)

        if current > self.kLedCurrentLimit100mA:
            current = self.kLedCurrentLimit100mA
        
        value = self.virtual_read_register(self.kLedConfig)
        value &= ~self.kLedConfigLedDrvMask
        value |= current << self.kLedConfigLedDrvShift

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
        self.select_device(self.kAS72651Nir)

        if current > self.kIndicatorCurrentLimit8mA:
            current = self.kIndicatorCurrentLimit8mA

        value = self.virtual_read_register(self.kLedConfig)
        value &= ~self.kLedConfigIndCurrentMask

        value |= current << self.kLedConfigIndCurrentShift

        self.virtual_write_register(self.kLedConfig, value)

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

    def soft_reset(self):
        """!
        Does a soft reset. Give sensor at least 1000ms to reset
        """
        value = self.virtual_read_register(self.kConfig)
        value |= (1 << self.kConfigSRSTShift)
        self.virtual_write_register(self.kConfig, value) 

    def data_available(self):
        """!
        Check if the data ready flag is set in the control setup register

        @return **bool** `True` if the data ready flag is set, otherwise `False`
        """
        value = self.virtual_read_register(self.kConfig)
        return (value & self.kConfigDataReadyMask) != 0

    # The below functions return the various calibration data
    # UV
    def get_calibrated_a(self):
        return self.get_calibrated_value(self.kRGACal, self.kAS72653Uv)

    def get_calibrated_b(self):
        return self.get_calibrated_value(self.kSHBCal, self.kAS72653Uv)

    def get_calibrated_c(self):
        return self.get_calibrated_value(self.kTICCal, self.kAS72653Uv)

    def get_calibrated_d(self):
        return self.get_calibrated_value(self.kUJDCal, self.kAS72653Uv)

    def get_calibrated_e(self):
        return self.get_calibrated_value(self.kVKECal, self.kAS72653Uv)

    def get_calibrated_f(self):
        return self.get_calibrated_value(self.kWLFCal, self.kAS72653Uv)

    # Visible
    def get_calibrated_g(self):
        return self.get_calibrated_value(self.kRGACal, self.kAS72652Visible)

    def get_calibrated_h(self):
        return self.get_calibrated_value(self.kSHBCal, self.kAS72652Visible)

    def get_calibrated_i(self):
        return self.get_calibrated_value(self.kTICCal, self.kAS72652Visible)

    def get_calibrated_j(self):
        return self.get_calibrated_value(self.kUJDCal, self.kAS72652Visible)

    def get_calibrated_k(self):
        return self.get_calibrated_value(self.kVKECal, self.kAS72652Visible)

    def get_calibrated_l(self):
        return self.get_calibrated_value(self.kWLFCal, self.kAS72652Visible)

    # NIR
    def get_calibrated_r(self):
        return self.get_calibrated_value(self.kRGACal, self.kAS72651Nir)

    def get_calibrated_s(self):
        return self.get_calibrated_value(self.kSHBCal, self.kAS72651Nir)

    def get_calibrated_t(self):
        return self.get_calibrated_value(self.kTICCal, self.kAS72651Nir)

    def get_calibrated_u(self):
        return self.get_calibrated_value(self.kUJDCal, self.kAS72651Nir)

    def get_calibrated_v(self):
        return self.get_calibrated_value(self.kVKECal, self.kAS72651Nir)

    def get_calibrated_w(self):
        return self.get_calibrated_value(self.kWLFCal, self.kAS72651Nir)

    # Get the various Channel data

    # Visible
    def get_g(self):
        return self.get_channel(self.kRGA, self.kAS72652Visible)

    def get_h(self):
        return self.get_channel(self.kSHB, self.kAS72652Visible)

    def get_i(self):
        return self.get_channel(self.kTIC, self.kAS72652Visible)

    def get_j(self):
        return self.get_channel(self.kUJD, self.kAS72652Visible)

    def get_k(self):
        return self.get_channel(self.kVKE, self.kAS72652Visible)

    def get_l(self):
        return self.get_channel(self.kWLF, self.kAS72652Visible)

    # NIR
    def get_r(self):
        return self.get_channel(self.kRGA, self.kAS72651Nir)

    def get_s(self):
        return self.get_channel(self.kSHB, self.kAS72651Nir)

    def get_t(self):
        return self.get_channel(self.kTIC, self.kAS72651Nir)

    def get_u(self):
        return self.get_channel(self.kUJD, self.kAS72651Nir)

    def get_v(self):
        return self.get_channel(self.kVKE, self.kAS72651Nir)

    def get_w(self):
        return self.get_channel(self.kWLF, self.kAS72651Nir)

    # UV
    def get_a(self):
        return self.get_channel(self.kRGA, self.kAS72653Uv)

    def get_b(self):
        return self.get_channel(self.kSHB, self.kAS72653Uv)

    def get_c(self):
        return self.get_channel(self.kTIC, self.kAS72653Uv)

    def get_d(self):
        return self.get_channel(self.kUJD, self.kAS72653Uv)

    def get_e(self):
        return self.get_channel(self.kVKE, self.kAS72653Uv)

    def get_f(self):
        return self.get_channel(self.kWLF, self.kAS72653Uv)

    def get_channel(self, channelReg, device):
        """!
        Get the channel data for a specific device

        @param int channelReg: The register address of the channel
        @param int device: The device to get the channel data from

        @return **int** The channel data
        """
        self.select_device(device)
        color_data = self.virtual_read_register(channelReg) << 8  # High byte
        color_data |= self.virtual_read_register(channelReg + 1)  # Low byte
        return color_data

    def get_calibrated_value(self, calAddress, device):
        """!
        Given an address, read four bytes and return the floating point calibrated value

        @param int calAddress: The address to read the calibrated value from
        @param int device: The device to read the calibrated value from

        @return **float** The calibrated value
        """
        self.select_device(device)

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

    def select_device(self, device):
        """!
        Point the master at either the first or the second slave

        @param int device: The device to select

        Allowable device values are:
            - kLedWhite
            - kLedIr
            - kLedUv
            - kAS72651Nir (arduino lib uses this value in the indicator() functions)
        """
        self.virtual_write_register(self.kDevSelectControl, device)

    def virtual_read_register(self, virtualAddr):
        """!
        Read a virtual register from the AS7265x

        @param int virtualAddr: The virtual register address to read

        @return **int** The value of the virtual register
        """
        status = self._i2c.read_byte(self.address, self.kStatusReg)

        # Do a prelim check of the read register
        if status & self.kRxValid:
            self._i2c.read_byte(self.address, self.kReadReg) # Read byte but do nothing with it

        # Wait for WRITE flag to clear
        timeWaited = 0
        while timeWaited <= self._maxWaitTime:
            status = self._i2c.read_byte(self.address, self.kStatusReg)
            if status & self.kTxValid == 0:
                break
            time.sleep(self.kPollingDelay / 1000)
            timeWaited += self.kPollingDelay

        # Write the virtual register address to the device
        self._i2c.write_byte(self.address, self.kWriteReg, virtualAddr)

        # Wait for READ flag to be set
        timeWaited = 0
        while timeWaited <= self._maxWaitTime:
            status = self._i2c.read_byte(self.address, self.kStatusReg)
            if status & self.kRxValid:
                break
            time.sleep(self.kPollingDelay / 1000)
            timeWaited += self.kPollingDelay
        
        # Read the virtual register
        return self._i2c.read_byte(self.address, self.kReadReg)
    
    def virtual_write_register(self, virtualAddr, data):
        """!
        Write a virtual register to the AS7265x

        @param int virtualAddr: The virtual register address to write
        @param int data: The data byte to write to the virtual register
        """

        # Wait for WRITE regiser to be empty
        timeWaited = 0
        while timeWaited <= self._maxWaitTime:
            status = self._i2c.read_byte(self.address, self.kStatusReg)
            if status & self.kTxValid == 0:
                break
            time.sleep(self.kPollingDelay / 1000)
            timeWaited += self.kPollingDelay
        
        # Write the virtual register address to the device (we set the MSB to 1 to indicate a write)
        self._i2c.write_byte(self.address, self.kWriteReg, virtualAddr | 0x80)

        # Wait for WRITE register to be empty
        timeWaited = 0
        while timeWaited <= self._maxWaitTime:
            status = self._i2c.read_byte(self.address, self.kStatusReg)
            if status & self.kTxValid == 0:
                break
            time.sleep(self.kPollingDelay / 1000)
            timeWaited += self.kPollingDelay

        # Write the data to the virtual register
        self._i2c.write_byte(self.address, self.kWriteReg, data)

