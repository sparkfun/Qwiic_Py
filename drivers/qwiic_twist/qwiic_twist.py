#-----------------------------------------------------------------------------
# qwiic_twist.py
#
# Python library for the SparkFun qwiic twist.
#
#   https://www.sparkfun.com/products/15083
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
# pylint: disable=line-too-long, too-many-public-methods, invalid-name
#

"""!
qwiic_twist
===============
Python module for the[SparkFun Qwiic Twist](https://www.sparkfun.com/products/15083)

This python package is a port of the existing [SparkFun Qwiic Twist Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_Twist_Arduino_Library)

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
_DEFAULT_NAME = "SparkFun Qwiic Twist"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x3F]

# Register codes for the twist
TWIST_ID = 0x00
TWIST_STATUS = 0x01 #2 - button clicked, 1 - button pressed, 0 - encoder moved
TWIST_VERSION = 0x02
TWIST_ENABLE_INTS = 0x04 #1 - button interrupt, 0 - encoder interrupt
TWIST_COUNT = 0x05
TWIST_DIFFERENCE = 0x07
TWIST_LAST_ENCODER_EVENT = 0x09 #Millis since last movement of knob
TWIST_LAST_BUTTON_EVENT = 0x0B  #Millis since last press/releas
TWIST_RED = 0x0D
TWIST_GREEN = 0x0E
TWIST_BLUE = 0x0F
TWIST_CONNECT_RED = 0x10 #Amount to change red LED for each encoder tick
TWIST_CONNECT_GREEN = 0x12
TWIST_CONNECT_BLUE = 0x14
TWIST_TURN_INT_TIMEOUT = 0x16
TWIST_CHANGE_ADDRESS = 0x18
TWIST_LIMIT = 0x19

_statusButtonClickedBit = 2
_statusButtonPressedBit = 1
_statusEncoderMovedBit = 0

_enableInterruptButtonBit = 1
_enableInterruptEncoderBit = 0

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicTwist(object):
    """!
    QwiicTwist

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.

    @return The Twist device object.
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
        """!
        Determine if a Tesit device is conntected to the system..

        @return **bool** True if the device is connected, otherwise False.
        """
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)
    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """!
        Initialize the operation of the Twist module

        @return **bool** Returns true of the initializtion was successful, otherwise False.
        """

        # Basically return True if we are connected...

        return self.is_connected()

    #----------------------------------------------------------------
    # clear_interrupts()
    #
    # Clears the moved, clicked, and pressed bits

    def clear_interrupts(self):
        """!
        Clears the moved, clicked, and pressed bits

        @return No return Value
        """
        self._i2c.writeByte(self.address, TWIST_STATUS, 0)

    #----------------------------------------------------------------
    # get_count()
    #
    # Returns the number of indents the user has twisted the knob

    def get_count(self):
        """!
        Returns the number of indents the user has twisted the knob

        @return **word as integer** number of indents
        """
        return self._i2c.readWord(self.address, TWIST_COUNT)

    #----------------------------------------------------------------
    # set_count()
    #
    # Set the encoder count to a specific amount
    def set_count(self, amount):
        """!
        Set the encoder count to a specific amount

        @param amount: the value to set the counter to

        @return no return value
        """

        return self._i2c.writeWord(self.address, TWIST_COUNT, int(amount))

    count = property(get_count, set_count)

    #----------------------------------------------------------------
    # get_limit()
    #
    # Returns the limit of allowed counts before wrapping. 0 is disabled

    def get_limit(self):
        """!
        Returns the limit of allowed counts before wrapping. 0 is disabled

        @return **integer** The limit
        """
        return self._i2c.readWord(self.address, TWIST_LIMIT)


    #----------------------------------------------------------------
    # set_limit()
    #
    # Set the encoder count limit to a specific amount
    def set_limit(self, amount):
        """!
        Set the encoder count limit to a specific amount

        @param amount: the value to set the limit to

        @return no return value
        """
        return self._i2c.writeWord(self.address, TWIST_LIMIT, int(amount))

    limit = property(get_limit, set_limit)

    #----------------------------------------------------------------
    # get_diff()
    #
    # Returns the number of ticks since last check

    def get_diff(self, clear_value=False):
        """!
        Returns the number of ticks since last check

        @param clearValue: Set to True to clear the current value. Default is False

        @return **integer** the difference
        """
        difference = self._i2c.readWord(self.address, TWIST_DIFFERENCE)

        if clear_value:
            self._i2c.writeWord(self.address, TWIST_DIFFERENCE, 0)

        return difference

    #----------------------------------------------------------------
    # is_pressed()
    #
    # Returns true if button is currently being pressed

    def is_pressed(self):
        """!
        Returns true if button is currently being pressed

        @return **Boolean** Button pressed state
        """
        status = self._i2c.readByte(self.address, TWIST_STATUS)

        self._i2c.writeByte(self.address, TWIST_STATUS, \
                        status & ~(1 << _statusButtonPressedBit))

        return (status & (1 << _statusButtonPressedBit)) != 0

    pressed = property(is_pressed)
    #----------------------------------------------------------------
    # was_clicked()
    #
    # Returns true if a click event has occurred

    def was_clicked(self):
        """!
        Returns true if a click event has occurred

        @return **Boolean** Click event state
        """
        status = self._i2c.readByte(self.address, TWIST_STATUS)

        self._i2c.writeByte(self.address, TWIST_STATUS, \
                        status & ~(1 << _statusButtonClickedBit))

        return (status & (1 << _statusButtonClickedBit)) != 0

    clicked = property(was_clicked)
    #----------------------------------------------------------------
    # has_moved()
    #
    # Returns true if knob has been twisted

    def has_moved(self):
        """!
        Returns true if knob has been twisted

        @return **Boolean** Moved state
        """
        status = self._i2c.readByte(self.address, TWIST_STATUS)

        self._i2c.writeByte(self.address, TWIST_STATUS, \
                        status & ~(1 << _statusEncoderMovedBit))

        return (status & (1 << _statusEncoderMovedBit)) != 0

    moved = property(has_moved)
    #----------------------------------------------------------------
    # since_last_movement()
    #
    # Returns the number of milliseconds since the last encoder movement
    # By default, clear the current value
    def since_last_movement(self, clear_value=True):
        """!
        Returns the number of milliseconds since the last encoder movement
            By default, clear the current value

        @param clearValue: Clear out the value? True by default

        @return **integer** time since last encoder movement
        """
        time_elapsed = self._i2c.readWord(self.address, TWIST_LAST_ENCODER_EVENT)

        # Clear the current value if requested
        if clear_value:
            self._i2c.writeWord(TWIST_LAST_ENCODER_EVENT, 0)

        return time_elapsed

    #----------------------------------------------------------------
    # since_last_press()
    #
    # Returns the number of milliseconds since the last button event (press and release)
    # By default, clear the current value
    def since_last_press(self, clear_value=True):
        """!
        Returns the number of milliseconds since the last button event (press and release)
            By default, clear the current value

        @param clearValue: Clear out the value? False by default

        @return **integer** time since last button press
        """
        time_elapsed = self._i2c.readWord(self.address, TWIST_LAST_BUTTON_EVENT)

        # Clear the current value if requested
        if clear_value:
            self._i2c.writeWord(TWIST_LAST_BUTTON_EVENT, 0)

        return time_elapsed

    #----------------------------------------------------------------
    # set_color()
    #
    # Sets the color of the encoder LEDs

    def set_color(self, red, green, blue):
        """!
        Sets the color of the encoder LEDs

        @param red: Red component
        @param green: Green component
        @param blue: Blue component

        @return No return value
        """
        self._i2c.writeBlock(self.address, TWIST_RED, [int(red), int(green), int(blue)])

    #----------------------------------------------------------------
    # set_red()
    #
    # Sets the red color component

    def set_red(self, red):
        """!
        Sets the red color of the encoder LEDs

        @param red: Red component

        @return No return value
        """
        self._i2c.writeByte(self.address, TWIST_RED, int(red))

    #----------------------------------------------------------------
    # get_red()
    #
    # Gets the red color component

    def get_red(self):
        """!
        Gets the red color of the encoder LEDs

        @return Red component of the color
        """
        return self._i2c.readByte(self.address, TWIST_RED)

    red = property(get_red, set_red)
    #----------------------------------------------------------------
    # set_green()
    #
    # Sets the green color component

    def set_green(self, green):
        """!
        Sets the green color of the encoder LEDs

        @param green: Green component

        @return **integer** No return value
        """
        self._i2c.writeByte(self.address, TWIST_GREEN, int(green))

    #----------------------------------------------------------------
    # get_green()
    #
    # Gets the green color component

    def get_green(self):
        """!
        Gets the green color of the encoder LEDs

        @return **integer** green component of the color
        """
        return self._i2c.readByte(self.address, TWIST_GREEN)

    green = property(get_green, set_green)

    #----------------------------------------------------------------
    # set_blue()
    #
    # Sets the blue color component

    def set_blue(self, blue):
        """!
        Sets the blue color of the encoder LEDs

        @param blue: blue component

        @return No return value
        """
        self._i2c.writeByte(self.address, TWIST_BLUE, int(blue))

    #----------------------------------------------------------------
    # get_blue()
    #
    # Gets the blue color component

    def get_blue(self):
        """!
        Gets the blue color of the encoder LEDs

        @return **integer** blue component of the color
        """
        return self._i2c.readByte(self.address, TWIST_BLUE)

    blue = property(get_blue, set_blue)

    #----------------------------------------------------------------
    # get_version()
    #
    # Returns a int of the firmware version number

    def get_version(self):
        """!
        Returns a integer of the firmware version number

        @return **integer** The firmware version
        """
        return self._i2c.readWord(self.address, TWIST_VERSION)

    version = property(get_version)
    #----------------------------------------------------------------
    # connect_color()
    #
    # Sets the relation between each color and the twisting of the knob
    # Connect the LED so it changes [amount] with each encoder tick
    # Negative numbers are allowed (so LED gets brighter the more you turn the encoder down)

    def connect_color(self, red, green, blue):
        """!
        Sets the relation between each color and the twisting of the knob
            Connect the LED so it changes [amount] with each encoder tick
            Negative numbers are allowed (so LED gets brighter the more you turn the encoder down)

        @param red: Red component
        @param green: Green component
        @param blue: Blue component

        @return No return value
        """
        self._i2c.writeBlock(self.address, TWIST_CONNECT_RED, [int(red), int(green), int(blue)])

    #----------------------------------------------------------------
    # set_connect_red()
    #
    # Sets the connect red color component

    def set_connect_red(self, red):
        """!
        Sets the connect red color of the encoder LEDs

        @param red: Red component

        @return No return value
        """
        self._i2c.writeWord(self.address, TWIST_CONNECT_RED, int(red))

    #----------------------------------------------------------------
    # get_connect_red()
    #
    # Gets the red color component

    def get_connect_red(self):
        """!
        Gets the connect red color of the encoder LEDs

        @return Red component of the color
        """
        return self._i2c.readWord(self.address, TWIST_CONNECT_RED)

    connect_red = property(get_connect_red, set_connect_red)

    #----------------------------------------------------------------
    # set_connect_green()
    #
    # Sets the connect green color component

    def set_connect_green(self, green):
        """!
        Sets the connect green color of the encoder LEDs

        @param green: Green component

        @return No return value
        """
        self._i2c.writeWord(self.address, TWIST_CONNECT_GREEN, int(green))

    #----------------------------------------------------------------
    # get_connect_green()
    #
    # Gets the green color component

    def get_connect_green(self):
        """!
        Gets the connect green color of the encoder LEDs

        @return green component of the color
        """
        return self._i2c.readWord(self.address, TWIST_CONNECT_GREEN)

    connect_green = property(get_connect_green, set_connect_green)

    #----------------------------------------------------------------
    # set_connect_blue()
    #
    # Sets the connect blue color component

    def set_connect_blue(self, blue):
        """!
        Sets the connect blue color of the encoder LEDs

        @param blue: blue component

        @return No return value
        """
        self._i2c.writeWord(self.address, TWIST_CONNECT_BLUE, int(blue))

    #----------------------------------------------------------------
    # get_connect_blue()
    #
    # Gets the blue color component

    def get_connect_blue(self):
        """!
        Gets the connect blue color of the encoder LEDs

        @return Blue component of the color
        """
        return self._i2c.readWord(self.address, TWIST_CONNECT_BLUE)

    connect_blue = property(get_connect_blue, set_connect_blue)

    #----------------------------------------------------------------
    # set_int_timeout()
    #
    # Set number of milliseconds that elapse between end of knob turning and interrupt firing

    def set_int_timeout(self, timeout):
        """!
        Set number of milliseconds that elapse between end of knob turning and interrupt firing

        @param timeout: the timeout value in milliseconds

        @return No return value
        """
        self._i2c.writeWord(self.address, TWIST_TURN_INT_TIMEOUT, int(timeout))

    #----------------------------------------------------------------
    # get_int_timeout()
    #
    # Get number of milliseconds that elapse between end of knob turning and interrupt firing

    def get_int_timeout(self):
        """!
        Get number of milliseconds that elapse between end of knob turning and interrupt firing

        @return **integer** the timeout value
        """
        return self._i2c.readWord(self.address, TWIST_TURN_INT_TIMEOUT)

    int_timeout = property(get_int_timeout, set_int_timeout)
