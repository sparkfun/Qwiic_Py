#-----------------------------------------------------------------------------
# qwiic_joystick.py
#
# Python library for the SparkFun qwiic joystick.
#
#   https://www.sparkfun.com/products/15168
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, July 2019
#
# This python library supports the SparkFun Electroncis qwiic
# qwiic sensor/board ecosystem
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
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
#==================================================================================
#
# This is mostly a port of existing Arduino functionaly, so pylint is sad.
# The goal is to keep the public interface pthonic, but internal is internal
#
# pylint: disable=line-too-long, bad-whitespace, invalid-name
#
"""!
qwiic_joystick
===============
Python module for the[SparkFun Qwiic Joystick](https://www.sparkfun.com/products/15168)

This python package is a port of the existing [SparkFun Qwiic Joystick Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_Joystick_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""
#-----------------------------------------------------------------------------

import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at
# runtine
#
# The name of this device
_DEFAULT_NAME = "SparkFun Qwiic Joystick"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x20]

# Register codes for the Joystick
JOYSTICK_ID             = 0x00
JOYSTICK_VERSION1       = 0x01
JOYSTICK_VERSION2       = 0x02
JOYSTICK_X_MSB          = 0x03
JOYSTICK_X_LSB          = 0x04
JOYSTICK_Y_MSB          = 0x05
JOYSTICK_Y_LSB          = 0x06
JOYSTICK_BUTTON         = 0x07
JOYSTICK_STATUS         = 0x08   # 1  -> button clicked
JOYSTICK_I2C_LOCK       = 0x09
JOYSTICK_CHANGE_ADDREESS = 0x0A


# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicJoystick(object):
    """!
    QwiicJoystick

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.

    @return The
    """
    # Constructor
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # load the I2C driver if one isn't provided

        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """!
        Determine if a Joystick device is conntected to the system..

        @return **bool** True if the device is connected, otherwise False.
        """
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """!
        Initialize the operation of the Joystick module

        @return **bool** Returns true of the initializtion was successful, otherwise False.
        """

        # Basically return True if we are connected...

        return self.is_connected()

    #----------------------------------------------------------------
    # get_horizontal()
    #
    # Returns the 10-bit ADC value of the joystick horizontal position

    def get_horizontal(self):
        """!
        Returns the 10-bit ADC value of the joystick horizontal position

        @return **byte as integer** The next button value
        """
        msb = self._i2c.readByte(self.address, JOYSTICK_X_MSB)
        lsb = self._i2c.readByte(self.address, JOYSTICK_X_LSB)

        return ((msb << 8) | lsb)>>6

    horizontal = property(get_horizontal)
    #----------------------------------------------------------------
    # get_vertical()
    #
    # Returns the 10-bit ADC value of the joystick vertical position

    def get_vertical(self):
        """!
        Returns the 10-bit ADC value of the joystick vertical position

        @return **byte as integer** The next button value
        """
        msb = self._i2c.readByte(self.address, JOYSTICK_Y_MSB)
        lsb = self._i2c.readByte(self.address, JOYSTICK_Y_LSB)

        return ((msb << 8) | lsb)>>6

    vertical = property(get_vertical)
    #----------------------------------------------------------------
    # get_button()
    #
    # Returns 0 button is currently being pressed.
    def get_button(self):
        """!
        Returns 0 button is currently being pressed.

        @return **integer** button status
        """

        return self._i2c.readByte(self.address, JOYSTICK_BUTTON)

    button = property(get_button)
    #----------------------------------------------------------------
    # check_button()
    #
    # Returns 1 if button was pressed between reads of .getButton() or .checkButton()
    # the register is then cleared after read.

    def check_button(self):
        """!
        Returns 1 if button was pressed between reads of .getButton() or .checkButton()
            the register is then cleared after read.

        @return **integer** button status
        """

        status = self._i2c.readByte(self.address, JOYSTICK_STATUS)

        # We've read this status bit, now clear it
        self._i2c.writeByte(self.address, JOYSTICK_STATUS, 0x00)

        return status


    #----------------------------------------------------------------
    # get_version()
    #
    # Returns a string of the firmware version number

    def get_version(self):
        """!
        Returns a string of the firmware version number

        @return **string** The firmware version
        """
        vMajor = self._i2c.readByte(self.address, JOYSTICK_VERSION1)
        vMinor = self._i2c.readByte(self.address, JOYSTICK_VERSION2)

        return "v %d.%d" % (vMajor, vMinor)

    version = property(get_version)
