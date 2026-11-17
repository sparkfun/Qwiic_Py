#-------------------------------------------------------------------------------
# qwiic_ultrasonic.py
#
# Python library for the SparkFun Qwiic Ultrasonic Sensor, available here:
# https://www.sparkfun.com/products/17777
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2023
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
# This code was generated in part with ChatGPT, created by OpenAI. The code was
# reviewed and edited by the following human(s):
#
# Dryw Wade
#===============================================================================

"""!
qwiic_ultrasonic
============
Python module for the [SparkFun Qwiic Ultrasonic Sensor](https://www.sparkfun.com/products/17777)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_Ultrasonic_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic Ultrasonic"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x2F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26,
                          0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 
                          0x00] # 0x00 for old versions of the sensor (SEN-17777)

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicUltrasonic(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Range of available I2C addresses of the Qwiic Ultrasonic
    kMinAddress = 0x20
    kMaxAddress = 0x2F
    kDefaultAddress = 0x2F

    # Register to trigger a new measurement and read the previous one
    kRegisterTrigger = 0x01

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

        # Nothing else to do
        return True

    def trigger_and_read(self):
        """!
        Triggers a new measurement and reads the previous one

        @return **int** Distance in mm
        """
        self._i2c.writeCommand(self.address, self.kRegisterTrigger)
        raw_data = self._i2c.readBlock(self.address, self.kRegisterTrigger, 2)
        return (raw_data[0] << 8) | raw_data[1]
    
    def change_address(self, address):
        """!
        Changes the I2C address of the Qwiic Ultrasonic sensor

        @param int address: New address, must be in the range 0x20 to 0x2F

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Check whether the address is valid
        if address < self.kMinAddress or address > self.kMaxAddress:
            return False

        # The first bit of the address must be set to 1
        address |= 0x80

        # Write the new address to the device
        self._i2c.writeCommand(self.address, address)

        # Update the address of this object
        self.address = address

        # Done!
        return True

    def get_address(self):
        """!
        Gets the current I2C address of the Qwiic Ultrasonic sensor

        @return **int** The current I2C address, 7-bit unshifted
        """
        return self.address
