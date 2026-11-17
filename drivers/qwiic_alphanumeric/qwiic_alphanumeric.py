#-----------------------------------------------------------------------------
# qwiic_alphanumeric.py
#
# Python library for the SparkFun Qwiic Alphanumeric displays.
#   https://www.sparkfun.com/products/16916
#   https://www.sparkfun.com/products/16917
#   https://www.sparkfun.com/products/16918
#   https://www.sparkfun.com/products/16919
#   https://www.sparkfun.com/products/18565
#   https://www.sparkfun.com/products/18566
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, August 2021
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
qwiic_alphanumeric
==================
Python module for the SparkFun Qwiic Alphanumeric displays.

This package is a port of the existing [SparkFun Alphanumeric Display Arduino Library](https://github.com/sparkfun/SparkFun_Alphanumeric_Display_Arduino_Library).

This package can be used in conjunction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py).

New to qwiic? Take a look at the entire [SparkFun Qwiic Ecosystem](https://www.sparkfun.com/qwiic).
"""
# ---------------------------------------------------------------------------------

import time
import qwiic_i2c

_DEFAULT_NAME = "Qwiic Alphanumeric"

_QWIIC_ALPHANUMERIC_DEFAULT_ADDRESS = 0x70
_AVAILABLE_I2C_ADDRESS = [_QWIIC_ALPHANUMERIC_DEFAULT_ADDRESS, 0x71, 0x72, 0x73]

class QwiicAlphanumeric(object):
    """!
    QwiicAlphanumeric

    @param address: The I2C address to use for the device.
                    If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided a
                    a driver is created.

    @return  The 
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    DEFAULT_NOTHING_ATTACHED = 0xFF

    # Define constants for segment bits
    SEG_A = 0x0001
    SEG_B = 0x0002
    SEG_C = 0x0004
    SEG_D = 0x0008
    SEG_E = 0x0010
    SEG_F = 0x0020
    SEG_G = 0x0040
    SEG_H = 0x0080
    SEG_I = 0x0100
    SEG_J = 0x0200
    SEG_K = 0x0400
    SEG_L = 0x0800
    SEG_M = 0x1000
    SEG_N = 0x2000

    # Blink rate
    ALPHA_BLINK_RATE_NOBLINK = 0b00
    ALPHA_BLINK_RATE_2HZ = 0b01
    ALPHA_BLINK_RATE_1HZ = 0b10
    ALPHA_BLINK_RATE_0_5HZ = 0b11

    # Display settings
    ALPHA_DISPLAY_ON = 0b1
    ALPHA_DISPLAY_OFF = 0b0

    # Decimal settings
    ALPHA_DECIMAL_ON = 0b1
    ALPHA_DECIMAL_OFF = 0b0

    # Colon settings
    ALPHA_COLON_ON = 0b1
    ALPHA_COLON_OFF = 0b0

    # Commands
    ALPHA_CMD_SYSTEM_SETUP = 0b00100000
    ALPHA_CMD_DISPLAY_SETUP = 0b10000000
    ALPHA_CMD_DIMMING_SETUP = 0b11100000

    SFE_ALPHANUM_UNKNOWN_CHAR = 95

    # Lookup table of segments for various characters
    alphanumeric_segs = []
    # nmlkjihgfedcba
    alphanumeric_segs.append(0b00000000000000)  # ' ' (space)
    alphanumeric_segs.append(0b00001000001000)  # '!'
    alphanumeric_segs.append(0b00001000000010)  # '"'
    alphanumeric_segs.append(0b01001101001110)  # '#'
    alphanumeric_segs.append(0b01001101101101)  # '$'
    alphanumeric_segs.append(0b10010000100100)  # '%'
    alphanumeric_segs.append(0b00110011011001)  # '&'
    alphanumeric_segs.append(0b00001000000000)  # '''
    alphanumeric_segs.append(0b00000000111001)  # '('
    alphanumeric_segs.append(0b00000000001111)  # ')'
    alphanumeric_segs.append(0b11111010000000)  # '*'
    alphanumeric_segs.append(0b01001101000000)  # '+'
    alphanumeric_segs.append(0b10000000000000)  # ','
    alphanumeric_segs.append(0b00000101000000)  # '-'
    alphanumeric_segs.append(0b00000000000000)  # '.'
    alphanumeric_segs.append(0b10010000000000)  # '/'
    alphanumeric_segs.append(0b00000000111111)  # '0'
    alphanumeric_segs.append(0b00010000000110)  # '1'
    alphanumeric_segs.append(0b00000101011011)  # '2'
    alphanumeric_segs.append(0b00000101001111)  # '3'
    alphanumeric_segs.append(0b00000101100110)  # '4'
    alphanumeric_segs.append(0b00000101101101)  # '5'
    alphanumeric_segs.append(0b00000101111101)  # '6'
    alphanumeric_segs.append(0b01010000000001)  # '7'
    alphanumeric_segs.append(0b00000101111111)  # '8'
    alphanumeric_segs.append(0b00000101100111)  # '9'
    alphanumeric_segs.append(0b00000000000000)  # ':'
    alphanumeric_segs.append(0b10001000000000)  # ';'
    alphanumeric_segs.append(0b00110000000000)  # '<'
    alphanumeric_segs.append(0b00000101001000)  # '='
    alphanumeric_segs.append(0b01000010000000)  # '>'
    alphanumeric_segs.append(0b01000100000011)  # '?'
    alphanumeric_segs.append(0b00001100111011)  # '@'
    alphanumeric_segs.append(0b00000101110111)  # 'A'
    alphanumeric_segs.append(0b01001100001111)  # 'B'
    alphanumeric_segs.append(0b00000000111001)  # 'C'
    alphanumeric_segs.append(0b01001000001111)  # 'D'
    alphanumeric_segs.append(0b00000101111001)  # 'E'
    alphanumeric_segs.append(0b00000101110001)  # 'F'
    alphanumeric_segs.append(0b00000100111101)  # 'G'
    alphanumeric_segs.append(0b00000101110110)  # 'H'
    alphanumeric_segs.append(0b01001000001001)  # 'I'
    alphanumeric_segs.append(0b00000000011110)  # 'J'
    alphanumeric_segs.append(0b00110001110000)  # 'K'
    alphanumeric_segs.append(0b00000000111000)  # 'L'
    alphanumeric_segs.append(0b00010010110110)  # 'M'
    alphanumeric_segs.append(0b00100010110110)  # 'N'
    alphanumeric_segs.append(0b00000000111111)  # 'O'
    alphanumeric_segs.append(0b00000101110011)  # 'P'
    alphanumeric_segs.append(0b00100000111111)  # 'Q'
    alphanumeric_segs.append(0b00100101110011)  # 'R'
    alphanumeric_segs.append(0b00000110001101)  # 'S'
    alphanumeric_segs.append(0b01001000000001)  # 'T'
    alphanumeric_segs.append(0b00000000111110)  # 'U'
    alphanumeric_segs.append(0b10010000110000)  # 'V'
    alphanumeric_segs.append(0b10100000110110)  # 'W'
    alphanumeric_segs.append(0b10110010000000)  # 'X'
    alphanumeric_segs.append(0b01010010000000)  # 'Y'
    alphanumeric_segs.append(0b10010000001001)  # 'Z'
    alphanumeric_segs.append(0b00000000111001)  # '['
    alphanumeric_segs.append(0b00100010000000)  # '\'
    alphanumeric_segs.append(0b00000000001111)  # ']'
    alphanumeric_segs.append(0b10100000000000)  # '^'
    alphanumeric_segs.append(0b00000000001000)  # '_'
    alphanumeric_segs.append(0b00000010000000)  # '`'
    alphanumeric_segs.append(0b00000101011111)  # 'a'
    alphanumeric_segs.append(0b00100001111000)  # 'b'
    alphanumeric_segs.append(0b00000101011000)  # 'c'
    alphanumeric_segs.append(0b10000100001110)  # 'd'
    alphanumeric_segs.append(0b00000001111001)  # 'e'
    alphanumeric_segs.append(0b00000001110001)  # 'f'
    alphanumeric_segs.append(0b00000110001111)  # 'g'
    alphanumeric_segs.append(0b00000101110100)  # 'h'
    alphanumeric_segs.append(0b01000000000000)  # 'i'
    alphanumeric_segs.append(0b00000000001110)  # 'j'
    alphanumeric_segs.append(0b01111000000000)  # 'k'
    alphanumeric_segs.append(0b01001000000000)  # 'l'
    alphanumeric_segs.append(0b01000101010100)  # 'm'
    alphanumeric_segs.append(0b00100001010000)  # 'n'
    alphanumeric_segs.append(0b00000101011100)  # 'o'
    alphanumeric_segs.append(0b00010001110001)  # 'p'
    alphanumeric_segs.append(0b00100101100011)  # 'q'
    alphanumeric_segs.append(0b00000001010000)  # 'r'
    alphanumeric_segs.append(0b00000110001101)  # 's'
    alphanumeric_segs.append(0b00000001111000)  # 't'
    alphanumeric_segs.append(0b00000000011100)  # 'u'
    alphanumeric_segs.append(0b10000000010000)  # 'v'
    alphanumeric_segs.append(0b10100000010100)  # 'w'
    alphanumeric_segs.append(0b10110010000000)  # 'x'
    alphanumeric_segs.append(0b00001100001110)  # 'y'
    alphanumeric_segs.append(0b10010000001001)  # 'z'
    alphanumeric_segs.append(0b10000011001001)  # '{'
    alphanumeric_segs.append(0b01001000000000)  # '|'
    alphanumeric_segs.append(0b00110100001001)  # '}'
    alphanumeric_segs.append(0b00000101010010)  # '~'
    alphanumeric_segs.append(0b11111111111111)  # Unknown character (DEL or RUBOUT)

    # Globals
    _device_address_display_one = 0    # Address of primary alphanumeric display
    _device_address_display_two = 0
    _device_address_display_three = 0
    _device_address_display_four = 0
    digit_position = 0  # Tracks the position of the current digit
    number_of_displays = 1 # Tracks the number of displays connected to the I2C bus, default is one display
    display_on_off = 0  # Tracks the on/off state of the display
    decimal_on_off = 0  # Tracks the on/off state of the decimal segment
    colon_on_off = 0    # Tracks the on/off state of the colon segment
    blink_rate = ALPHA_BLINK_RATE_NOBLINK   # Tracks the current blinking status

    display_RAM = [0] * 16 * 4
    display_content = [' '] * (4 * 4 + 1)

    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver
    
    # ---------------------------------------------------------------------------------
    # begin(address_left, address_left_center, address_right_center, address_right)
    #
    # Initialize the system and validate the baord.
    def begin(self, address_display_one = _QWIIC_ALPHANUMERIC_DEFAULT_ADDRESS, address_display_two = DEFAULT_NOTHING_ATTACHED, address_display_three = DEFAULT_NOTHING_ATTACHED, address_display_four = DEFAULT_NOTHING_ATTACHED):
        """!
        Initialize the operation of the Qwiic Alphanumeric.
        Assign addresses to displays and determine the number of displays connected to the bus.
        Run is_connected().
        Initialize and clear displays.

        @param address_display_one: I2C address of first display
        @param address_display_two: I2C address of the second display
        @param address_dispplay_three: I2C address of the third display
        @param address_display_four: I2C address of the fourth display

        @return **bool** Returns true if a Qwiic Alphanumeric is connected to the system.
                False otherwise.
        """
        self._device_address_display_one = address_display_one # Grab the address(es) of the alphanumeric(s)
        self._device_address_display_two = address_display_two
        self._device_address_display_three = address_display_three
        self._device_address_display_four = address_display_four

        # Figure out how many displays are attached by the number of addresses the user specified
        if self._device_address_display_four != self.DEFAULT_NOTHING_ATTACHED:
            self.number_of_displays = 4
        elif self._device_address_display_three != self.DEFAULT_NOTHING_ATTACHED:
            self.number_of_displays = 3
        elif self._device_address_display_two != self.DEFAULT_NOTHING_ATTACHED:
            self.number_of_displays = 2
        else:
            self.number_of_displays = 1

        for i in range(1, self.number_of_displays + 1):
            if self.is_connected(i) == False:
                return False
            time.sleep(0.01)
        
        if self.initialize() == False:
            return False
        
        if self.clear() == False:
            return False
        
        self.display_content[4 * 4] = '\0'  # Terminate the array because we are doing direct prints
    
    # ---------------------------------------------------------------------------------
    # is_connected(display_number)
    #
    # Check if there are acutal boards connected to the system
    def is_connected(self, display_number):
        """!
        Check that dispplays are responding on the I2C bus.

        @param display_number: The number of the display on the bus

        @return **bool** True if the device is connected, false otherwise.
        """
        tries_before_giveup = 5 
        
        # The LED driver IC sometimes fails to respond. This attempts multiple times before giving up.
        for x in range(0, tries_before_giveup):
            if self._i2c.isDeviceConnected(self.look_up_display_address(display_number)) == True:
                return True
            time.sleep(0.01)
        return False

    # ---------------------------------------------------------------------------------
    # initialize()
    #
    # Run through initialization sequence for each display connected on the I2C bus
    def initialize(self):
        """!
        Run through initialization sequence for each display connected on the I2C bus
        Enable clocks, set brightness default to full brightness, turn off blinking, and
        turn all displays on

        @return **bool** True if all function calls passed, False if there's a failure somewhere
        """
        # Turn on system clock of all displays
        if self.enable_system_clock() == False:
            return False
        
        # Set brightness of all displays to full brightness
        if self.set_brightness(15) == False:
            return False

        # Turn blinking off for all displays
        if self.set_blink_rate(self.ALPHA_BLINK_RATE_NOBLINK) == False:
            return False
        
        # Turn on all displays
        if self.display_on() == False:
            return False
        
        return True
    
    # ---------------------------------------------------------------------------------
    # enable_system_clock()
    #
    # Turn on the system oscillator for all displays on the I2C bus
    def enable_system_clock(self):
        """!
        Turn on the system oscillator for all displays on the I2C bus

        @return **bool** True if all clocks successfully enabled, false otherwise.
        """
        status = True
        
        for i in range(1, self.number_of_displays + 1):
            if self.enable_system_clock_single(i) == False:
                status = False
        
        return status

    # ---------------------------------------------------------------------------------
    # disable_system_clock()
    #
    # Turn off the system oscillator for all displays on the bus
    def disable_system_clock(self):
        """!
        Turn off the system oscillator for all displays on the bus

        @return **bool** True if all clocks successfully disabled, false otherwise.
        """
        status = True

        for i in range(1, self.number_of_displays + 1):
            if self.disable_system_clock_single(i) == False:
                status = False
        
        return status
    
    # ---------------------------------------------------------------------------------
    # enable_system_clock_single(display_number)
    #
    # Turn on the system oscillator for normal operation mode
    def enable_system_clock_single(self, display_number):
        """!
        Turn on the system oscillator for normal operation mode

        @param display_number: number of display on I2C bus to enable the system clock
            for.

        @return **bool** True if setting updated successfully, false otherwise.
        """
        data_to_write = self.ALPHA_CMD_SYSTEM_SETUP | 1 # Enable system clock  bit

        status = self.write_RAM_byte(self.look_up_display_address(display_number), data_to_write)
        time.sleep(0.001)   # Allow display to start

        return status

    # ---------------------------------------------------------------------------------
    # disable_system_clock_single(display_number)
    #
    # Turn off the system oscillator for standby mode
    def disable_system_clock_single(self, display_number):
        """!
        Turn off the system oscillator for standby mode

        @param display_number: number of display on I2C bus to disable the system
            clock for.

        @return **bool** True if setting updated successfully, false otherwise.
        """
        data_to_write = self.ALPHA_CMD_SYSTEM_SETUP | 0 # Standby mode

        return self.write_RAM(self.look_up_display_address(display_number), data_to_write)

    # ---------------------------------------------------------------------------------
    # look_up_display_address(display_number)
    #
    # This function connects the display number to its coressponding address
    def look_up_display_address(self, display_number):
        """!
        This function connects the display number to its coressponding address

        @param display_number: number of display on I2C bus. The left-most display is zero
            and display number increments by 1 with each additional display on bus.

        @return **int** The I2C address of given display. 0 if display_number is not valid
        """
        if display_number == 1:
            return self._device_address_display_one
        elif display_number == 2:
            return self._device_address_display_two
        elif display_number == 3:
            return self._device_address_display_three
        elif display_number == 4:
            return self._device_address_display_four
        
        return 0    # We shouldn't get here

    # ---------------------------------------------------------------------------------
    # clear()
    #
    # Turn off all segments of all displays connected to bus
    def clear(self):
        """!
        Turn off all segments of all displays connected to bus

        @return **bool** True if display was updated correctly, false otherwise
        """
        # Clear the display_RAM array
        for i in range(0, 16 * self.number_of_displays):
            self.display_RAM[i] = 0
        
        # Reset digit position
        self.digit_position = 0

        return self.update_display()

    # ---------------------------------------------------------------------------------
    # set_brightness(duty)
    # 
    # This function sets the brightness of all displays on the bus
    def set_brightness(self, duty):
        """!
        This function sets the brightness of all displays on the bus.
        Duty cycle over 16.

        @param duty: Valid between 0 (1/16 brightnss) and 15 (full brightness)

        @return **bool** True if brightness is successfully updated, false otherwise.
        """
        status = True

        for i in range(1, self.number_of_displays + 1):
            if self.set_brightness_single(i, duty) == False:
                status = False
        
        return status

    # ---------------------------------------------------------------------------------
    # set_brightness_single(display_number, duty)
    #
    # Set the brightness of a single display
    def set_brightness_single(self, display_number, duty):
        """!
        Set the brightness of a single display

        @param display_number: The number of display on the I2C bus.
        @param duty: Over 16. Valid between 0 (display off) and 15 (full brightness)

        @return **bool** True if brightness is successfully updated, false otherwise.
        """
        # Error check
        if duty > 15:
            duty = 15
        elif duty < 0:
            duty = 0
        
        data_to_write = self.ALPHA_CMD_DIMMING_SETUP | duty
        return self.write_RAM_byte(self.look_up_display_address(display_number), data_to_write)

    # ---------------------------------------------------------------------------------
    # set_blink_rate(rate)
    #
    # Set the blink rate of all displays on the bus
    def set_blink_rate(self, rate):
        """!
        Set the blink rate of all displays on the bus as defined by the datasheet.

        @param rate: Blink frequency in Hz. Valid options are defined by datasheet:
            2.0, 1.0, or 0.5 Hz. Any other input to this function will result in steady
            alphanumeric display (no blink).

        @return **bool** True if blink setting is successfully updated, false otherwise.
        """
        status = True

        for i in range(1, self.number_of_displays + 1):
            if self.set_blink_rate_single(i, rate) == False:
                status = False
        
        return status
    
    # ---------------------------------------------------------------------------------
    # set_blink_rate_single(display_number, rate)
    #
    # Set the blink rate of a single display on the bus
    def set_blink_rate_single(self, display_number, rate):
        """!
        Set the blink rate of a single display on the bus

        @param display_number: the number of display to be updated
        @param rate: Blink frequency in Hz. Valid options are defined by datasheet:
            2.0, 1.0, or 0.5 Hz. Any other input to this function will result in steady
            alphanumeric display (no blink).

        @return **bool** True if blink setting is successfully updated, false otherwise.
        """
        if rate == 2.0:
            blink_rate = self.ALPHA_BLINK_RATE_2HZ
        elif rate == 1.0:
            blink_rate = self.ALPHA_BLINK_RATE_1HZ
        elif rate == 0.5:
            blink_rate = self.ALPHA_BLINK_RATE_0_5HZ
        # Default to no blink
        else:
            blink_rate = self.ALPHA_BLINK_RATE_NOBLINK
        
        data_to_write = self.ALPHA_CMD_DISPLAY_SETUP | (blink_rate << 1) | self.display_on_off
        return self.write_RAM_byte(self.look_up_display_address(display_number), data_to_write)
    
    # ---------------------------------------------------------------------------------
    # display_on_single(display_number)
    #
    # Turn a single alphanumeric display on
    def display_on_single(self, display_number):
        """!
        Turn a single alphanumeric display on

        @param display_number: the number of display to be updated

        @return **bool** True if display is successfully turned on, false otherwise
        """
        return self.set_display_on_off(display_number, True)
    
    # ---------------------------------------------------------------------------------
    # display_off_single(display_number)
    #
    # Turn a single alphanumeric display off
    def display_off_single(self, display_number):  
        """!
        Turn a single alphanumeric display off

        @param display_number: the number of display to be updated

        @return **bool** True if display is successfully turned off, false otherwise
        """
        return self.set_display_on_off(display_number, False)
    
    # ---------------------------------------------------------------------------------
    # set_display_on_off(display_number, turn_on_display)
    #
    # Set or clear the display on/off bit of a given display number
    def set_display_on_off(self, display_number, turn_on_display):
        """!
        Set or clear the display on/off bit of a given display number

        @param display_number: the number of display to be updated
        @param turn_on_display: boolean variable. If true, will turn display on.
            If false, will turn display off

        @return **bool** True if display is successfully updated, false otherwise.
        """
        if turn_on_display:
            self.display_on_off = self.ALPHA_DISPLAY_ON
        else:
            self.display_on_off = self.ALPHA_DISPLAY_OFF
        
        data_to_write = self.ALPHA_CMD_DISPLAY_SETUP | (self.blink_rate << 1) | self.display_on_off
        return self.write_RAM_byte(self.look_up_display_address(display_number), data_to_write)
    
    # ---------------------------------------------------------------------------------
    # display_on()
    #
    # Turn on all displays on the I2C bus
    def display_on(self):
        """!
        Turn on all displays on the I2C bus

        @return **bool** True if displays are successfully turned on, false otherwise.
        """
        status = True

        self.display_on_off = self.ALPHA_DISPLAY_ON

        for i in range(1, self.number_of_displays + 1):
            if self.display_on_single(i) == False:
                status = False
        
        return status
    
    # ---------------------------------------------------------------------------------
    # display_off()
    #
    # Turn off all displays on the I2C bus
    def display_off(self):
        """!
        Turn off all displays on the I2C bus

        @return **bool** True if all displays are successfully turned off, false otherwise.
        """
        status = True

        self.display_on_off = self.ALPHA_DISPLAY_OFF

        for i in range(1, self.number_of_displays + 1):
            if self.display_off_single(i) == False:
                status = False
        
        return status
    
    # ---------------------------------------------------------------------------------
    # decimal_on_single(display_number)
    #
    # Turn the decimal point on for a single display
    def decimal_on_single(self, display_number):
        """!
        Turn the decimal point on for a single display

        @param display_number: the number of display to turn the decimal on for.

        @return **bool** true if decimal is successfully turned on, false otherwise.
        """        
        return self.set_decimal_on_off(display_number, True)

    # ---------------------------------------------------------------------------------
    # decimal_off_single(display_number)
    #
    # Turn the decimal point off for a single display
    def decimal_off_single(self, display_number):
        """!
        Turn the decimal point off for a single display

        @param display_number: the number of display to turn the decimal point off for.

        @return **bool** true if decimal is successfully turned off, false otherwise.
        """
        return self.set_decimal_on_off(display_number, False)
    
    # ---------------------------------------------------------------------------------
    # set_decimal_on_off(display_number, turn_on_decimal)
    #
    # Set or clear the decimal on/off bit
    def set_decimal_on_off(self, display_number, turn_on_decimal):
        """!
        Set or clear the decimal on/off bit

        @param display_number: the number of display to update.
        @param turn_on_decimal: boolean variable. If true, will turn decimal on.
            If false, will turn decimal off.

        @return **bool** true if the display is updated successfully, false otherwise.
        """
        adr = 0x03
        dat = 0

        if turn_on_decimal == True:
            self.decimal_on_off = self.ALPHA_DECIMAL_ON
            dat = 0x01
        else:
            self.decimal_on_off = self.ALPHA_DECIMAL_OFF
            dat = 0x00
        
        self.display_RAM[adr + (display_number - 1) * 16] &= 0xFE
        self.display_RAM[adr + (display_number - 1) * 16] |= dat
        return self.update_display()
    
    # ---------------------------------------------------------------------------------
    # decimal_on()
    #
    # Turn the decimal on for all displays on bus
    def decimal_on(self):
        """!
        Turn the decimal on for all displays on the bus

        @return **bool** true if displays are updated successfully, false otherwise.
        """
        status = True

        self.decimal_on_off = self.ALPHA_DECIMAL_ON

        for i in range(1, self.number_of_displays + 1):
            if self.decimal_on_single(i) == False:
                status = False
            
        return status
    
    # ---------------------------------------------------------------------------------
    # decimal_off()
    #
    # Turn the decimal point off for all displays on bus
    def decimal_off(self):
        """!
        Turn the decimal point off for all displays on the bus

        @return **bool** true if displays are updated successfully, false otherwise.
        """
        status = True

        self.decimal_on_off = self.ALPHA_DECIMAL_OFF

        for i in range(1, self.number_of_displays + 1):
            if self.decimal_off_single(i) == False:
                status = False
        
        return status
    
    # ---------------------------------------------------------------------------------
    # colon_on_single(display_number)
    #
    # Turn the colon on for a single display
    def colon_on_single(self, display_number):
        """!
        Turn the colon on for a single display

        @param display_number: number of display to update.

        @return **bool** true if display updated successfully, false otherwise.
        """
        return self.set_colon_on_off(display_number, True)

    # ---------------------------------------------------------------------------------
    # colon_off_single(display_number)
    # 
    # Turn the colon off for a single display
    def colon_off_single(self, display_number):
        """!
        Turn the colon off for a single display

        @param display_number: number of display to update.

        @return **bool** true if display updated successfully, false otherwise.
        """
        return self.set_colon_on_off(display_number, False)
    
    # ---------------------------------------------------------------------------------
    # set_colon_on_off(display_number, turn_on_colon)
    #
    # Set or clear the colon on/off bit
    def set_colon_on_off(self, display_number, turn_on_colon):
        """!
        Set or clear the colon on/off bit

        @param display_number: number of display to update.
        @param turn_on_colon: boolean variable. If true, colon will turn on.
            If false, colon will turn off.
        """
        adr = 0x01
        dat = 0

        if turn_on_colon == True:
            self.colon_on_off = self.ALPHA_COLON_ON
            dat = 0x01
        else:
            self.colon_on_off = self.ALPHA_COLON_OFF
            dat = 0x00
        
        self.display_RAM[adr + (display_number - 1) * 16] &= 0xFE
        self.display_RAM[adr + (display_number - 1) * 16] |= dat
        return self.update_display()

    # ---------------------------------------------------------------------------------
    # colon_on()
    #
    # Turn the colon on for all displays on the bus
    def colon_on(self):
        """!
        Turn the colon on for all displays on the bus

        @return **bool** true if displays successfully updated, false otherwise.
        """
        status = True
        
        self.colon_on_off = self.ALPHA_COLON_ON
        
        for i in range(1, self.number_of_displays + 1):
            if self.colon_on_single(i) == False:
                return False
        
        return status
    
    # ---------------------------------------------------------------------------------
    # colon_off()
    #
    # Turn the colon off for all displays on the bus
    def colon_off(self):
        """!
        Turn the colon off for all displays on the bus

        @return **bool** true if all displays are successfully updated, false otherwise.
        """
        status = True

        self.colon_on_off = self.ALPHA_COLON_OFF

        for i in range(1, self.number_of_displays + 1):
            if self.colon_off_single(i) == False:
                status = False
        
        return status
    
    # ---------------------------------------------------------------------------------
    # illuminate_segment(segment, digit)
    # 
    # Given a segment and a digit, set the matching bit within the RAM of the Holtek RAM set
    def illuminate_segment(self, segment, digit):
        """!
        Given a segment and a digit, set the matching bit within the RAM of the Holtek RAM set

        @param segment: the segment to illuminate. There are 14 segments available, so A-N
        @param digit: the digit on the display to turn the segment on. There are 4 digits 
            per display

        @return **Void** nothing
        """
        segment = ord(segment)
        com = segment - ord('A') # Convert the segment letter back to a number
        
        if com > 6:
            com = com - 7
        # Special cases in which the segment order is a lil switched.
        if segment == ord('I'):
            com = 0
        if segment == ord('H'):
            com = 1
        
        row = digit % 4 # Convert digit (1 to 16) back to a relative position on a given 
                        # digit on a display
        if segment > ord('G'):
            row = row + 4
        
        offset = int(digit / 4) * 16
        adr = com * 2 + offset

        # Determine the address
        if row > 7:
            adr = adr + 1

        # Determine the data bit
        if row > 7:
            row = row - 8

        dat = 1 << row

        self.display_RAM[adr] = self.display_RAM[adr] | dat

    # ---------------------------------------------------------------------------------
    # illuminate_char(segments_to_turn_on, digit)
    #
    # Given a binary set of segments and a digit, store this data into the RAM array
    def illuminate_char(self, segments_to_turn_on, digit):
        """!
        Fiven a binary set of segments and a digit, store this data into the RAM array

        @param segments_to_turn_on: list of segments to illuminate which create an 
            alphanumeric character
        @param digit: digit on which to illuminate this char (list of segments)

        @return **Void** nothing
        """
        for i in range(0, 14):
            if (segments_to_turn_on >> i) & 0b1:
                temp_char = ord('A') + i
                temp_char = chr(temp_char)
                self.illuminate_segment(temp_char, digit) # Convert the segment number to a letter
        
    # ---------------------------------------------------------------------------------
    # print_char(display_char, digit)
    #
    # Print a character, for a given digit, on display
    def print_char(self, display_char, digit):
        """!
        Print a character, for a given digit, on display

        @param display_char: the character to be printed to display
        @param digit: the digit position where character should be printed

        @return **Void** nothing
        """
        # Convert character to ASCII representation
        display_char = ord(display_char)
        character_position = 65532

        # Space
        if display_char == ord(' '):
            character_position = 0
        # Printable symbols -- between first character '!' and last character '~'
        elif display_char >= ord('!') and display_char <= ord('~'):
            character_position = display_char - ord('!') + 1

        disp_num = int(self.digit_position / 4)

        # Take care of special characters by turning correct segment on 
        if character_position == 14:    # '.'
            self.decimal_on_single(disp_num+1)
        if character_position == 26:    # ':'
            self.colon_on_single(disp_num+1)
        if character_position == 65532: # unknown character
            character_position = self.SFE_ALPHANUM_UNKNOWN_CHAR

        self.illuminate_char(self.alphanumeric_segs[character_position], digit)
    
    # ---------------------------------------------------------------------------------
    # print(print_string)
    #
    # Print a whole string to the alphanumeric display(s)
    def print(self, print_string):
        """!
        Print a whole string to the alphanumeric display(s)

        @param print_string: string to be printed

        @return **bool** true if update_display() is successful, false otherwise
        """
        # Clear the display_RAM array
        self.clear()
        
        self.digit_position = 0
        string_index = 0

        while string_index < len(print_string) and self.digit_position < (4 * self.number_of_displays):
            # For special characters like '.' or ':', do not increment the digit position
            if print_string[string_index] == '.':
                self.print_char('.', 0)
            elif print_string[string_index] == ':':
                self.print_char(':', 0)
            else:
                self.print_char(print_string[string_index], self.digit_position)
                # Record to internal list
                self.display_content[self.digit_position] = print_string[string_index]

                self.digit_position += 1
            string_index += 1
        
        self.update_display()
    
    # ---------------------------------------------------------------------------------
    # update_display()
    #
    # Push the contents of display_RAM out to the various displays in 16 byte chunks
    def update_display(self):
        """!
        Push the contents of display_RAM out on to the various displays in 16 byte chunks

        @return **bool** true if displays are updated successfully, false otherwise.
        """
        status = True

        for i in range(1, self.number_of_displays + 1):
            
            if self.write_RAM(self.look_up_display_address(i), 0, self.display_RAM[(i-1)*16:(i*16)-1]) == False:
                status = False
        
        return status
    
    # ---------------------------------------------------------------------------------
    # shift_right(shift_amt)
    #
    # Shift the display content to the right a number of digits
    def shift_right(self, shift_amt = 1):
        """!
        Shift the display content to the right a number of digits

        @param shift_amt: the number of digits to shift the string

        @return **bool** true if display updates successfully, false otherwise.
        """
        for x in range((4 * self.number_of_displays) - shift_amt, shift_amt-1, -1):
            self.display_content[x] = self.display_content[x - shift_amt]
        
        # Clear the leading characters
        for x in range(0, shift_amt):
            if x + shift_amt > (4 * self.number_of_displays):
                break   # Error check

            self.display_content[0 + x] = ' '     
        
        # Convert list of characters into string
        temp = ""
        for x in range(0, len(self.display_content)):
            if self.display_content[x] != '\x00':
                temp += self.display_content[x]

        self.print(temp)

    # ---------------------------------------------------------------------------------
    # shift_left(shift_amt)
    #
    # Shift the display content to the left a number of digits
    def shift_left(self, shift_amt = 1):
        """!
        Shift the display content to the left a number of digits

        @param shift_amt: the number of digits to shift the string

        @return **bool** true if display updates successfully, false otherwise.
        """
        for x in range(0, 4 * self.number_of_displays):
            if (x + shift_amt) > (4 * self.number_of_displays):
                break   # Error check
            self.display_content[x] = self.display_content[x + shift_amt]
        
        # Clear the trailing characters
        for x in range(0, shift_amt):
            if (4 * self.number_of_displays - 1 - x) < 0:
                break   # Error check
            
            self.display_content[4 * self.number_of_displays - 1 - x] = ' ' 
        
        # Convert list of characters into string
        temp = ''
        for x in range(0, len(self.display_content)):
            if self.display_content[x] != '\x00':
                temp += self.display_content[x]
        
        self.print(temp)

    # ---------------------------------------------------------------------------------
    # write_RAM(address, reg, buff)
    #
    # write LED updates to the RAM of the LED driver IC
    def write_RAM(self, address, reg, buff):
        """!
        Write LED updates to the RAM of the LED driver IC

        @param address: I2C address of the display
        @param reg: the location in RAM to write to
        @param buff: the bytes to be written

        @return **bool** true if RAM has been written to successfully, false otherwise.
        """
        display_num = 1 
        if address == self._device_address_display_two:
            display_num = 2
        elif address == self._device_address_display_three:
            display_num = 3
        elif address == self._device_address_display_four:
            display_num = 4

        self.is_connected(display_num)

        self._i2c.writeBlock(address, reg, buff)
    
    def write_RAM_byte(self, address, data_to_write):
        self._i2c.writeCommand(address, data_to_write)
