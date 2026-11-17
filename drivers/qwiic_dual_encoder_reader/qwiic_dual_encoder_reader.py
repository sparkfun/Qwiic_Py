#-----------------------------------------------------------------------------
# qwiic_dual_encoder_reader.py
#
# Python library for the dual encoder reader that is part of the SparkFun Auto pHAT.
#
#   https://www.sparkfun.com/products/15083
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, March 2020
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
# pylint: disable=line-too-long, too-many-public-methods, invalid-name
#

"""
qwiic_dual_encoder_reader
===============
Python module for the[SparkFun Auto pHAT for Raspberry Pi](https://www.sparkfun.com/products/16328)

This python package enables the user to take count readings from the on-board ATTINY84 that handles reading the dual motor encoders.

The firmware that is used on the ATTiny84 is located in a separate repository here: [SparkFun Dual Encoder Reader Firmware Repository](https://github.com/sparkfun/Qwiic_Dual_Encoder_Reader)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""
#-----------------------------------------------------------------------------
from __future__ import print_function
import struct

import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at
# runtine
#
# The name of this device
_DEFAULT_NAME = "SparkFun Qwiic Dual Encoder Reader"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x73, 0x74] # open ADR jumper (default) = 0x73, closed ADR jumper = 0x74

# Register codes for the SparkFun Dual Encoder Reader
QDER_ID = 0x00
QDER_STATUS = 0x01 #2 - button clicked, 1 - button pressed, 0 - encoder moved
QDER_VERSION = 0x02
QDER_ENABLE_INTS = 0x04 #1 - button interrupt, 0 - encoder interrupt
QDER_COUNT1 = 0x05
QDER_DIFFERENCE1 = 0x07
QDER_COUNT2 = 0x09
QDER_DIFFERENCE2 = 0x0B
QDER_LAST_ENCODER_EVENT = 0x0D #Millis since last movement of encoder
QDER_TURN_INT_TIMEOUT = 0x0F
QDER_CHANGE_ADDRESS = 0x11
QDER_LIMIT = 0x12

_statusEncoderMovedBit = 0
_enableInterruptEncoderBit = 0

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicDualEncoderReader(object):
    """
    QwiicDualEncoderReader

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The QwiicDualEncoderReader device object.
        :rtype: Object
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self.address = address if address is not None else self.available_addresses[0]

        # load the I2C driver if one isn't provided

        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    # ----------------------------------
    # isConnected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """
            Determine if a device is conntected to the system..

            :return: True if the device is connected, otherwise False.
            :rtype: bool

        """
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)
    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """
            Initialize the operation of the Dual Encoder Reader module

            :return: Returns true of the initializtion was successful, otherwise False.
            :rtype: bool

        """

        # Basically return True if we are connected...

        return self.is_connected()

    #----------------------------------------------------------------
    # clear_interrupts()
    #
    # Clears the moved bit

    def clear_interrupts(self):
        """
            Clears the moved bit

            :return: No return Value

        """
        self._i2c.writeByte(self.address, QDER_STATUS, 0)

    #----------------------------------------------------------------
    # get_count1()
    #
    # Returns the number of "ticks" the encoder1 has turned

    def get_count1(self):
        """
            Returns the number of "ticks" the encoder1 has turned

            :return: number of encoder pulses
            :rtype: word as integer

        """
        c1 = self._i2c.readWord(self.address, QDER_COUNT1)
        # encoder reader returns a SIGNED 16 bit int
        # python receives this as simply 16 bits of data
        # we need to accept negative values
        if c1 > 32767:
            c1 -= 65536
        return c1

    #----------------------------------------------------------------
    # get_count2()
    #
    # Returns the number of "ticks" the encoder2 has turned

    def get_count2(self):
        """
            Returns the number of "ticks" the encoder2 has turned

            :return: number of encoder pulses
            :rtype: word as integer

        """
        c2 = self._i2c.readWord(self.address, QDER_COUNT2)
        # encoder reader returns a SIGNED 16 bit int
        # python receives this as simply 16 bits of data
        # we need to accept negative values
        if c2 > 32767:
            c2 -= 65536
        return c2

    #----------------------------------------------------------------
    # set_count1()
    #
    # Set the encoder count1 to a specific amount
    def set_count1(self, amount):
        """
            Set the encoder count1 to a specific amount

            :param amount: the value to set the counter to
            :return: no return value

        """

        return self._i2c.writeWord(self.address, QDER_COUNT1, amount)

    #----------------------------------------------------------------
    # set_count2()
    #
    # Set the encoder count2 to a specific amount
    def set_count2(self, amount):
        """
            Set the encoder count2 to a specific amount

            :param amount: the value to set the counter to
            :return: no return value

        """

        return self._i2c.writeWord(self.address, QDER_COUNT2, amount)        

    count1 = property(get_count1, set_count1)
    count2 = property(get_count2, set_count2)

    #----------------------------------------------------------------
    # get_limit()
    #
    # Returns the limit of allowed counts before wrapping. 0 is disabled

    def get_limit(self):
        """
            Returns the limit of allowed counts before wrapping. 0 is disabled

            :return: The limit
            :rtype: integer

        """
        return self._i2c.readWord(self.address, QDER_LIMIT)


    #----------------------------------------------------------------
    # set_limit()
    #
    # Set the encoder count limit to a specific amount
    def set_limit(self, amount):
        """
            Set the encoder count limit to a specific amount

            :param amount: the value to set the limit to
            :return: no return value

        """
        return self._i2c.writeWord(self.address, QDER_LIMIT, amount)

    limit = property(get_limit, set_limit)

    #----------------------------------------------------------------
    # get_diff()
    #
    # Returns the number of ticks since last check

    def get_diff(self, clear_value=False):
        """
            Returns the number of ticks since last check

            :param clearValue: Set to True to clear the current value. Default is False

            :return: the difference
            :rtype: integer

        """
        difference = self._i2c.readWord(self.address, QDER_DIFFERENCE1)

        if clear_value:
            self._i2c.writeWord(self.address, QDER_DIFFERENCE1, 0)

        return difference

    #----------------------------------------------------------------
    # has_moved()
    #
    # Returns true if encoder has moved

    def has_moved(self):
        """
            Returns true if encoder has moved

            :return: Moved state
            :rtype: Boolean

        """
        status = self._i2c.readByte(self.address, QDER_STATUS)

        self._i2c.writeByte(self.address, QDER_STATUS, \
                        status & ~(1 << _statusEncoderMovedBit))

        return (status & (1 << _statusEncoderMovedBit)) != 0

    moved = property(has_moved)
    #----------------------------------------------------------------
    # since_last_movement()
    #
    # Returns the number of milliseconds since the last encoder movement
    # By default, clear the current value
    def since_last_movement(self, clear_value=True):
        """
            Returns the number of milliseconds since the last encoder movement
            By default, clear the current value

            :param clearValue: Clear out the value? True by default

            :return: time since last encoder movement
            :rtype: integer

        """
        time_elapsed = self._i2c.readWord(self.address, QDER_LAST_ENCODER_EVENT)

        # Clear the current value if requested
        if clear_value:
            self._i2c.writeWord(QDER_LAST_ENCODER_EVENT, 0)

        return time_elapsed

    #----------------------------------------------------------------
    # get_version()
    #
    # Returns a int of the firmware version number

    def get_version(self):
        """
        Returns a integer of the firmware version number

        :return: The firmware version
        :rtype: integer
        """
        return self._i2c.readWord(self.address, QDER_VERSION)

    version = property(get_version)
    

    #----------------------------------------------------------------
    # set_int_timeout()
    #
    # Set number of milliseconds that elapse between end of encoder turning and interrupt firing

    def set_int_timeout(self, timeout):
        """
            Set number of milliseconds that elapse between end of encoder turning and interrupt firing

            :param timeout: the timeout value in milliseconds

            :return: No return value

        """
        self._i2c.writeWord(self.address, QDER_TURN_INT_TIMEOUT, timeout)

    #----------------------------------------------------------------
    # get_int_timeout()
    #
    # Get number of milliseconds that elapse between end of encoder turning and interrupt firing

    def get_int_timeout(self):
        """
            Get number of milliseconds that elapse between end of encoder turning and interrupt firing

            :return: the timeout value
            :rtype: integer

        """
        return self._i2c.readWord(self.address, QDER_TURN_INT_TIMEOUT)

    int_timeout = property(get_int_timeout, set_int_timeout)
