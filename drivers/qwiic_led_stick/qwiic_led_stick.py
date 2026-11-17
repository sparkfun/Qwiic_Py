#-----------------------------------------------------------------------------
# qwiic_led_stick.py
#
# Python library for the SparkFun Qwiic LED Stick - APA102C.
#   https://www.sparkfun.com/products/18354
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2020 SparkFun Electronics
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

"""!
qwiic_led_stick
===============
Python module for the SparkFun Qwiic LED Stick - APA102C.

This package is a port of the existing [SparkFun Qwiic LED Stick Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_LED_Stick_Arduino_Library).

This package can be used in conjunction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py).

New to qwiic? Take a look at the entire [SparkFun Qwiic Ecoststem](https://www.sparkfun.com/qwiic).
"""
# ---------------------------------------------------------------------------------

import math
import time
import qwiic_i2c

_DEFAULT_NAME = "Qwiic LED Stick"

_QWIIC_LED_STICK_DEFAULT_ADDRESS = 0x23
_FULL_ADDRESS_LIST = list(range(0x08, 0x77+1)) # Full address list (excluding reserved addresses)
_FULL_ADDRESS_LIST.remove(_QWIIC_LED_STICK_DEFAULT_ADDRESS >> 1) # Remove default address from list
_AVAILABLE_I2C_ADDRESS = [_QWIIC_LED_STICK_DEFAULT_ADDRESS] # Initialize with default address
_AVAILABLE_I2C_ADDRESS.extend(_FULL_ADDRESS_LIST) # Add full range of I2C addresses

class QwiicLEDStick(object):
    """!
    QwiicLEDStick

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided a 
                        a driver is created.

    @return **Object** The GPIO device object.
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Qwiic LED Stick commands
    COMMAND_CHANGE_ADDRESS = 0xC7
    COMMAND_CHANGE_LED_LENGTH = 0x70
    COMMAND_WRITE_SINGLE_LED_COLOR = 0x71
    COMMAND_WRITE_ALL_LED_COLOR = 0x72
    COMMAND_WRITE_RED_ARRAY = 0x73
    COMMAND_WRITE_GREEN_ARRAY = 0x74
    COMMAND_WRITE_BLUE_ARRAY = 0x75
    COMMAND_WRITE_SINGLE_LED_BRIGHTNESS = 0x76
    COMMAND_WRITE_ALL_LED_BRIGHTNESS = 0x77
    COMMAND_WRITE_ALL_LED_OFF = 0x78

    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self.address = address if address != None else self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver
    
    # ------------------------------------------------------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?
    def is_connected(self):
        """!
        Determine if a Qwiic SGP40 device is connected to the system.

        @return **bool** True if the device is connected, false otherwise.
        """
        return qwiic_i2c.isDeviceConnected(self.address)

    # ------------------------------------------------------------------------------
    # begin()
    #
    # Initialize the system and validate the board.
    def begin(self):
        """!
        Initialize the operation of the Qwiic LED Stick.
            Run is_connected()

        @return **bool** Returns true if an LED Stick is connected to the system
                    False otherwise.
        """
        return self.is_connected()
    
    # ------------------------------------------------------------------------------
    # set_single_LED_color(number, red, green, blue)
    #
    # Change the color of a specific LED.
    def set_single_LED_color(self, number, red, green, blue):
        """!
        Change the color of a specific LED.

        @param number: the number of LED. Indexing starts at 1.
        @param red: the red value between 0 and 255
        @param green: the green value between 0 and 255
        @param blue: the blue value between 0 and 255

        @return **bool** Returns true if command written successfully, false otherwise
        """
        # First, check the boundary cases
        if red > 255:
            red = 255
        if red < 0:
            red = 0
        if green > 255:
            green = 255
        if green < 0:
            green = 0
        if blue > 255:
            blue = 255
        if blue < 0:
            blue = 0
        

        data = [int(number), int(red), int(green), int(blue)]
        return self._i2c.writeBlock(self.address, self.COMMAND_WRITE_SINGLE_LED_COLOR, data)

    # ------------------------------------------------------------------------------
    # set_all_LED_color(red, green, blue)
    #
    # Set the color of all LEDs in the string
    def set_all_LED_color(self, red, green, blue):
        """!
        Set the color of all LEDs in the string. Each will be shining the same color.
            The color value must be between 0-255.

        @param red: the red value to set all LEDs to. Between 0 and 255.
        @param green: the green value to set all LEDs to. Between 0 and 255.
        @param blue: the blue value to set all the LEDs to. Between 0 and 255.

        @return **bool** Returns true if command is written successfully, false otherwise
        """
        # First, check the boundary cases
        if red > 255:
            red = 255
        if red < 0:
            red = 0
        if green > 255:
            green = 255
        if green < 0:
            green = 0
        if blue > 255:
            blue = 255
        if blue < 0:
            blue = 0
        

        data_list = [int(red), int(green), int(blue)]
        return self._i2c.writeBlock(self.address, self.COMMAND_WRITE_ALL_LED_COLOR, data_list)
    
    # ------------------------------------------------------------------------------
    # set_all_LED_unique_color(red_list, blue_list, green_list, length)
    #
    # Change the color of all LEDs at once to individual values
    def set_all_LED_unique_color(self, red_list, green_list, blue_list, length):
        """!
        Change the color of all LEDs at once to individual values.

        @param red_list: a list of red values for the LEDs. Index 0 of red_list 
                corresponds to the red value of LED 0.
        @param blue_list: a list of blue values for the LEDs.
        @param green_list: a list of green  values for the LEDs.
        @param length: the length of the LED string.

        @return **bool** True if commands are written successfully, false otherwise
        """
        # First, check the boundary cases
        for i in range(0, length):
            if red_list[i] > 255:
                red_list[i] = 255
            if red_list[i] < 0:
                red_list[i] = 0
            if green_list[i] > 255:
                green_list[i] = 255
            if green_list[i] < 0:
                green_list[i] = 0
            if blue_list[i] > 255:
                blue_list[i] = 255
            if blue_list[i] < 0:
                blue_list[i] = 0

        # ATtiny has a 16 byte limit on an I2C transmission, so we need to chop up 
        # our color lists into chunks of 12 values
        # Use list comprehension to break list into a list of lists of length 12
        n = 12
        red_2dim_list = [red_list[i * n:(i + 1) * n] for i in range((len(red_list) + n - 1) // n)]
        green_2dim_list = [green_list[i * n:(i +1) * n] for i in range((len(green_list) + n - 1) // n)]
        blue_2dim_list = [blue_list[i * n:(i + 1) * n] for i in range((len(blue_list) + n - 1) // n)]
        
        # Send out red values
        for i in range(0, len(red_2dim_list)):
            transmission_len = len(red_2dim_list[i])    # Calculate the number of red values to send
            offset = i * n                              # Calculate LED offset
            data_list = [transmission_len, offset] + red_2dim_list[i]
            self._i2c.writeBlock(self.address, self.COMMAND_WRITE_RED_ARRAY, data_list)
        
        # Send out green values
        for i in range(0, len(green_2dim_list)):
            transmission_len = len(green_2dim_list[i])
            offset = i * n
            data_list = [transmission_len, offset] + green_2dim_list[i]
            self._i2c.writeBlock(self.address, self.COMMAND_WRITE_GREEN_ARRAY, data_list)

        # Send out blue values
        for i in range(0, len(blue_2dim_list)):
            transmission_len = len(blue_2dim_list[i])
            offset = i * n
            data_list = [transmission_len, offset] + blue_2dim_list[i]
            self._i2c.writeBlock(self.address, self.COMMAND_WRITE_BLUE_ARRAY, data_list)
    
    # -----------------------------------------------------------------------------
    # set_single_LED_brightness(number, brightness)
    #
    # Change the brightness of a specific LED while keeping their current color
    def set_single_LED_brightness(self, number, brightness):
        """!
        Change the brightness of a specific LED while keeping their current color.
            To turn LEDs off but remember their previous color, set brightness to 0.

        @param number: number of LED to change brightness. LEDs indexed starting at 1.
        @param brightness: value of LED brightness between 0 and 31.

        @return **bool** true if the command was sent successfully, false otherwise.
        """
        # First, check the boundary cases
        if brightness > 31:
            brightness = 31
        if brightness < 0:
            brightness = 0
        
        data = [int(number), int(brightness)]
        return self._i2c.writeBlock(self.address, self.COMMAND_WRITE_SINGLE_LED_BRIGHTNESS, data)
    
    # ----------------------------------------------------------------------------
    # set_all_LED_brightness(brightness)
    #
    # Change the brightness of all LEDs while keeping their current color
    def set_all_LED_brightness(self, brightness):
        """!
        Change the brightness of all LEDs while keeping their current color.
            To turn all LEDs off but remember their previous color, set brightness to 0

        @param brightness: value of LED brightness between 0 and 31.

        @return **bool** true if the command was sent successfully, false otherwise.
        """
        # First, check the boundary cases
        if brightness > 31:
            brightness = 31
        if brightness < 0:
            brightness = 0
        
        return self._i2c.writeByte(self.address, self.COMMAND_WRITE_ALL_LED_BRIGHTNESS, int(brightness))
    
    # ---------------------------------------------------------------------------
    # led_off()
    #
    # Turn all LEDs off by setting color to 0
    def LED_off(self):
        """!
        Turn all LEDs off by setting color to 0

        @return **bool** true if the command was sent successfully, false otherwise.
        """
        return self._i2c.writeByte(self.address, self.COMMAND_WRITE_ALL_LED_OFF, 0)
    
    # ---------------------------------------------------------------------------
    # change_address(new_address)
    #
    # Change the I2C address from one address to another
    def change_address(self, new_address):
        """!
        Change the I2C address from one address to another.

        @param new_address: the new address to be set to. Must be valid.

        @return **Void** Nothing
        """
        # First, check if the specified address is valid
        if new_address < 0x08 or new_address > 0x77:
            return False
        
        self._i2c.writeByte(self.address, self.COMMAND_CHANGE_ADDRESS, new_address)
        
        # Update address variable
        self.address = new_address
    
    # --------------------------------------------------------------------------
    # change_length(new_length)
    #
    # Change the length of the LED string
    def change_length(self, new_length):
        """!
        Change the length of the LED string

        @param new_length: the new length of the LED string

        @return **bool** true if the command was sent successfully, false otherwise.
        """
        # TODO: need to figure out the max length of the LED string
        return self._i2c.writeByte(self.address, self.COMMAND_CHANGE_LED_LENGTH, new_length)
        
