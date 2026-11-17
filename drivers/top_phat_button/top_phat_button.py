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
"""
top_phat_button
===============
Python module for the[SparkFun Qwiic Joystick](https://www.sparkfun.com/products/15168)

This python package is a port of the existing [SparkFun Qwiic Joystick Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_Joystick_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""
#-----------------------------------------------------------------------------

from __future__ import print_function

import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at
# runtine
#
# The name of this device
_DEFAULT_NAME = "SparkFun Top pHAT Button"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x71]

# Register codes for the Joystick
BUTTON_ID               = 0x00
BUTTON_VERSION1         = 0x01
BUTTON_VERSION2         = 0x02
BUTTON_PRESSED          = 0x03
BUTTON_CLICKED          = 0x04
BUTTON_INTERRUPT        = 0x05
BUTTON_DEBOUNCE         = 0x06
BUTTON_CHANGE_ADDREESS  = 0x1F

# Define the bit positions of the buttons and interrupt flag
A                     = 0
B                     = 1
UP                    = 2
DOWN                  = 3
LEFT                  = 4
RIGHT                 = 5
CENTER                = 6
EVENT_AVAILABLE       = 7

# Define the positions of the Interrupt Enable Bits
CLICKED_INTERRUPT_ENABLE        = 0
PRESSED_INTERRUPT_ENABLE        = 1

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class ToppHATButton(object):
    """
    ToppHATButton

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The ToppHATButton device object.
        :rtype: Object
    """
    # Constructor
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    a_pressed = 0
    b_pressed = 0
    up_pressed = 0
    down_pressed = 0
    left_pressed = 0
    right_pressed = 0
    center_pressed = 0
    pressed_event_available = 0
    
    a_clicked = 0
    b_clicked = 0
    up_clicked = 0
    down_clicked = 0
    left_clicked = 0
    right_clicked = 0
    center_clicked = 0
    clicked_event_available = 0
    
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
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """
            Determine if the Top pHAT Buttons are connected to the system..

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
            Initialize the operation of the button module

            :return: Returns true of the initializtion was successful, otherwise False.
            :rtype: bool

        """

        # Basically return True if we are connected...

        return self.is_connected()

    #----------------------------------------------------------------
    # get_button_pressed()
    #
    # Updates and returns buffer for all buttons and whether or not they are pressed as well as the pressed interrupt flag
    # Reading this register also clears it.
    # 7(MSB)  6    5    4    3    2    1    0(LSB)
    #   INT  CTR  RGT  LFT  DWN   UP   B    A
    
    def get_button_pressed(self):
        """
            Updates and returns buffer for all buttons and whether or not they are pressed as well as the pressed interrupt flag
            Reading this register also clears it.
            7(MSB)  6    5    4    3    2    1    0(LSB)
              INT  CTR  RGT  LFT  DWN   UP   B    A

            :return: button status
            :rtype: integer
        """
        temp = self._i2c.readByte(self.address, BUTTON_PRESSED)
        self.a_pressed = (temp & (1 << A)) >> A 
        self.b_pressed = (temp & (1 << B)) >> B 
        self.up_pressed = (temp & (1 << UP)) >> UP 
        self.down_pressed = (temp & (1 << DOWN)) >> DOWN 
        self.left_pressed = (temp & (1 << LEFT)) >> LEFT 
        self.right_pressed = (temp & (1 << RIGHT)) >> RIGHT
        self.center_pressed = (temp & (1 << CENTER)) >> CENTER
        self.pressed_event_available = (temp & (1 << EVENT_AVAILABLE)) >>EVENT_AVAILABLE
        
        return temp

    button_pressed = property(get_button_pressed)
    
    #----------------------------------------------------------------
    # get_button_clicked()
    #
    # Updates and returns buffer for all buttons and whether or not they have been clicked as well as the clicked interrupt flag
    # Reading this register also clears it.
    # 7(MSB)  6    5    4    3    2    1    0(LSB)
    #   INT  CTR  RGT  LFT  DWN   UP   B    A
    
    def get_button_clicked(self):
        """
            Returns 1 when a button has received a full click cycle (press and release). The interrupt must be cleared by the user.
            7(MSB)  6    5    4    3    2    1    0(LSB)
              INT  CTR  RGT  LFT  DWN   UP   B    A
            :return: Clicked status of all buttons in a byte
            :rtype: integer
        """
        temp = self._i2c.readByte(self.address, BUTTON_CLICKED)
        self.a_clicked = temp & (1 << A)
        self.b_clicked = (temp & (1 << B)) >> B 
        self.up_clicked = (temp & (1 << UP)) >> UP 
        self.down_clicked = (temp & (1 << DOWN)) >> DOWN 
        self.left_clicked = (temp & (1 << LEFT)) >> LEFT 
        self.right_clicked = (temp & (1 << RIGHT)) >> RIGHT
        self.center_clicked = (temp & (1 << CENTER)) >> CENTER
        self.clicked_event_available = (temp & (1 << EVENT_AVAILABLE)) >> EVENT_AVAILABLE
        return temp

    button_clicked = property(get_button_clicked)
    
    #----------------------------------------------------------------
    # get_version()
    #
    # Returns a string of the firmware version number

    def get_version(self):
        """
            Returns a string of the firmware version number

            :return: The firmware version
            :rtype: string
        """
        vMajor = self._i2c.readByte(self.address, BUTTON_VERSION1)
        vMinor = self._i2c.readByte(self.address, BUTTON_VERSION2)

        return "v %d.%d" % (vMajor, vMinor)

    version = property(get_version)
    
    #----------------------------------------------------------------
    # get__pressed_interrupt()
    #
    # Returns the status of the pressed interrupt enable bit

    def get_pressed_interrupt(self):
        """
            Returns the status of the pressed interrupt enable

            :return: The pressed interrupt enable bit
            :rtype: bool
        """
        interrupt = self._i2c.readByte(self.address, BUTTON_INTERRUPT)
        interrupt = (interrupt & (1 << PRESSED_INTERRUPT_ENABLE)) >> PRESSED_INTERRUPT_ENABLE
                   
        return interrupt
    
    #----------------------------------------------------------------
    # set_pressed_interrupt(bit_setting)
    #
    # Sets the status of the pressed interrupt enable bit

    def set_pressed_interrupt(self, bit_setting):
        """
            Sets the status of the pressed interrupt enable bit

            :param: The pressed interrupt enable bit
            :return: The status of the I2C transaction
            :rtype: bool
        """
        interrupt = self._i2c.readByte(self.address, BUTTON_INTERRUPT)
        interrupt &= ~(1 << PRESSED_INTERRUPT_ENABLE) #Clear enable bit
        interrupt |= (bit_setting << PRESSED_INTERRUPT_ENABLE)
                   
        return self._i2c.writeWord(self.address, BUTTON_INTERRUPT, interrupt)

    pressed_interrupt_enable = property(get_pressed_interrupt, set_pressed_interrupt)    
    #----------------------------------------------------------------
    # get__clicked_interrupt()
    #
    # Returns the status of the clicked interrupt enable bit

    def get_clicked_interrupt(self):
        """
            Returns the status of the clicked interrupt enable

            :return: The clicked interrupt enable bit
            :rtype: bool
        """
        interrupt = self._i2c.readByte(self.address, BUTTON_INTERRUPT)
        interrupt = (interrupt & (1 << CLICKED_INTERRUPT_ENABLE)) >> CLICKED_INTERRUPT_ENABLE
                   
        return interrupt
    
    #----------------------------------------------------------------
    # set_clicked_interrupt(bit_setting)
    #
    # Sets the status of the clicked interrupt enable bit

    def set_clicked_interrupt(self, bit_setting):
        """
            Sets the status of the clicked interrupt enable bit

            :param: The clicked interrupt enable bit
            :return: The status of the I2C transaction
            :rtype: bool
        """
        interrupt = self._i2c.readByte(self.address, BUTTON_INTERRUPT)
        interrupt &= ~(1 << CLICKED_INTERRUPT_ENABLE) #Clear enable bit
        interrupt |= (bit_setting << CLICKED_INTERRUPT_ENABLE)
                   
        return self._i2c.writeWord(self.address, BUTTON_INTERRUPT, interrupt)

    clicked_interrupt_enable = property(get_clicked_interrupt, set_clicked_interrupt)
