#-------------------------------------------------------------------------------
# qwiic_micropressure.py
#
# Python library for the SparkFun Qwiic MicroPressure Sensor, available here:
# https://www.sparkfun.com/products/16476
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
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
qwiic_micropressure
============
Python module for the [SparkFun Qwiic MicroPressure Sensor](https://www.sparkfun.com/products/16476)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_MicroPressure_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c
import time

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic MicroPressure"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x18]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicMicroPressure(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Regs and other constants
    kReadPressureCommandReg  = 0xAA # The register to write to in order to trigger a pressure reading
    kReadPressureCommandData = 0x0000 # Writing this command data to the command register will trigger a pressure reading

    # Status Byte Masks
    kMathSatMask = 1 << 0 # 1 = Math saturation has occurred
    kMemoryIntegrityMask = 1 << 1 # 0 = Integrity test passed, 1 = Integrity test failed
    kBusyMask = 1 << 5 # 1 = Device is busy
    kPowerIndicationMask = 1 << 6 # 1 = Device is powered, 0 = Device is not powered 

    # Minimum and maximum outputs
    kOutputMin = 0x19999A
    kOutputMax = 0xE66666

    # Minimum and maximum PSI
    kMaxPSI = 25
    kMinPSI = 0

    # Options for unit types
    kPressurePsi = 0 # Pounds per square inch
    kPressurePa = 1 # Pascals
    kPressureKpa = 2 # kiloPascals
    kPressureTorr = 3 # Torr
    kPressureInHg = 4 # Inch of Mercury
    kPressureAtm = 5 # Atmospheres
    kPressureBar = 6 # Bars

    def __init__(self, address=None, i2c_driver=None):
        """!
        Constructor

        @param int address: The I2C address to use for the device. If not provided, the default address is used
        @param I2CDriver i2c_driver: An existing i2c driver object. If not provided, a driver object is created
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

    def is_connected(self):
        """!
        Determines if the device is connected

        @return **bool** `True` if the device is connected, otherwise `False`
        """
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes the device with default parameters

        @return **bool** `True`` if the device was successfully initialized, otherwise `False``
        """
        # Confirm device is connected before doing anything
        return self.is_connected()

    def read_pressure(self, units=kPressurePsi):
        """!
        Reads the pressure from the sensor

        @param int units: The units to return the pressure in. Use one of the kPressure* constants
        @return: The pressure in Pascals, or -1 on error
        """

        # Request the pressure reading
        self._i2c.write_word(self.address, self.kReadPressureCommandReg, self.kReadPressureCommandData)
        
        # Wait until the device is no longer busy (alternative would be to sleep for at least 5ms)
        while self._i2c.read_byte(self.address, None) & self.kBusyMask: # Passing "None" will cause us to read but not from a specific register. Requires the updated qwiic_i2c.py
             time.sleep(0.001)

        # Read the pressure data
        pressure_bytes = self._i2c.read_block(self.address, None, 4) # Passing "None" will cause us to read but not from a specific register. Requires the updated qwiic_i2c.py

        # Verify the data integrity and saturation
        status = pressure_bytes[0]
        if (status & self.kMemoryIntegrityMask) or (status & self.kMathSatMask):
            return -1
        
        # Extract 24-bit pressure reading
        reading = pressure_bytes[1] << 16 | pressure_bytes[2] << 8 | pressure_bytes[3]

        # Convert from 24-bit to float psi value
        pressure = ((reading - self.kOutputMin) * (self.kMaxPSI - self.kMinPSI) / (self.kOutputMax - self.kOutputMin)) + self.kMinPSI

        if units == self.kPressurePsi:
            return pressure
        elif units == self.kPressurePa:
            return pressure * 6894.7573
        elif units == self.kPressureKpa:
            return pressure * 6.8947573
        elif units == self.kPressureTorr:
            return pressure * 51.7149
        elif units == self.kPressureInHg:
            return pressure * 2.03602
        elif units == self.kPressureAtm:
            return pressure * 0.06805
        elif units == self.kPressureBar:
            return pressure * 0.06895
