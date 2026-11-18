#-----------------------------------------------------------------------------
# qwiic_serlcd.py
#
# Python library for I2C control of the SparkFun Serial LCDs (QWIIC):
#
#   SparkFun 16x2 SerLCD - RGB Backlight (Qwiic)
#   https://www.sparkfun.com/products/16396
#
#   SparkFun 16x2 SerLCD - RGB Text (Qwiic)
#   https://www.sparkfun.com/products/16397
#
#   SparkFun 20x4 SerLCD - RGB Backlight (Qwiic)
#   https://www.sparkfun.com/products/16398
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, August 2020
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
# The goal is to keep the public interface pythonic, but internal is internal.
#
# pylint: disable=line-too-long, too-many-public-methods, invalid-name
#

"""
qwiic_serlcd
===============
Python module for the SparkFun SerLCD QWIIC products:

[SparkFun 16x2 SerLCD - RGB Backlight (Qwiic)](https://www.sparkfun.com/products/16396)
[SparkFun 16x2 SerLCD - RGB Text (Qwiic)](https://www.sparkfun.com/products/16397)
[SparkFun 20x4 SerLCD - RGB Backlight (Qwiic)](https://www.sparkfun.com/products/16398)

This python package enables the user to control the SerLCDs via I2C.
It is intended to be used by simply plugging in a qwiic cable for power and I2C communication.

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""
#-----------------------------------------------------------------------------
import qwiic_i2c

__version__ = "3.0.0"

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at
# runtine
#
# The name of this device
_DEFAULT_NAME = "SparkFun Qwiic SerLCD"

# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x72] # default address, note it can be changed via software commands

# Register codes for the SparkFun SerLCD

DISPLAY_ADDRESS1 = 0x72 # This is the default address of the OpenLCD
MAX_ROWS = 4
MAX_COLUMNS = 20

# OpenLCD command characters
SPECIAL_COMMAND = 254  # Magic number for sending a special command
SETTING_COMMAND = 0x7C # 124, |, the pipe character: The command to change settings: baud, lines, width, backlight, splash, etc

# OpenLCD commands
CLEAR_COMMAND = 0x2D					# 45, -, the dash character: command to clear and home the display
CONTRAST_COMMAND = 0x18				# Command to change the contrast setting
ADDRESS_COMMAND = 0x19				# Command to change the i2c address
SET_RGB_COMMAND = 0x2B				# 43, +, the plus character: command to set backlight RGB value
ENABLE_SYSTEM_MESSAGE_DISPLAY = 0x2E  # 46, ., command to enable system messages being displayed
DISABLE_SYSTEM_MESSAGE_DISPLAY = 0x2F # 47, /, command to disable system messages being displayed
ENABLE_SPLASH_DISPLAY = 0x30			# 48, 0, command to enable splash screen at power on
DISABLE_SPLASH_DISPLAY = 0x31			# 49, 1, command to disable splash screen at power on
SAVE_CURRENT_DISPLAY_AS_SPLASH = 0x0A # 10, Ctrl+j, command to save current text on display as splash

# special commands
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

def map(x, in_min, in_max, out_min, out_max):
    """!
    Map a value from one range to another

    @param x: **float** The value to be mapped
    @param in_min: **float** Minimum of input range
    @param in_max: **float** Maximum of input range
    @param out_min: **float** Minimum of output range
    @param out_max: **float** Maximum of output range
    @return **int** The value scaled to the new range
    """
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicSerLCD(object):
    """!
    This class implements the basic functions of the Qwiic SerLCD device via the I2C bus.
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS
    _display_control = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
    _display_mode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT

    # Constructor
    def __init__(self, address=None, i2c_bus=None):
        """!
        @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        @param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.
        """
        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address?
        self.address = address if address is not None else self.available_addresses[0]

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

    def is_connected(self):
        """!
        @brief Determine if a device is connected to the system.
        This method checks if the device with the specified I2C address is connected to the system.
        @return **bool** True if the device is connected, otherwise False.
        """
        # Another possible comment could be @retval bool True: Device is connected. above
        return qwiic_i2c.is_device_connected(self.address)

    def begin(self):
        """!
        Initialize the operation of the SerLCD module

        @return **bool** Returns true if the initialization was successful, otherwise False.
        """
        if not self.is_connected():
            return False

        # set default settings, as defined in constructor
        self.special_command(LCD_DISPLAYCONTROL | self._display_control)
        self._i2c.delay_ms(1000)
        self.special_command(LCD_ENTRYMODESET | self._display_mode)
        self._i2c.delay_ms(1000)
        self.clear_screen()
        self._i2c.delay_ms(1000)

        return True

    def print(self, string):
        """!
            Print a string of characters to the LCD

            @param string string: The string you would like to print. Aka ASCII characters. example: "Hello"

            @return **bool** Returns True if the I2C writes were successful, otherwise False.
        """
        for c in string:
            self._i2c.write_byte(self.address, None, ord(c))
            self._i2c.delay_ms(10)
        return True

    def clear_screen(self):
        """!
            Sends the command to clear the screen
        """
        self.command(CLEAR_COMMAND)
        self._i2c.delay_ms(10)

    def home(self):
        """!
            Send the home command to the display. This returns the cursor
            to the beginning of the display, without clearing
            the display.
        """
        self.special_command(LCD_RETURNHOME)
        self._i2c.delay_ms(10)

    def set_cursor(self, col, row):
        """!
            Set the cursor position to a particular column and row.

            @param col: **int** The column position (0-19)
            @param row: **int** The row position (0-3)
        """
        row_offsets = [0x00, 0x40, 0x14, 0x54]

        # keep variables in bounds
        row = max(0, row)            # row cannot be less than 0
        row = min(row, (MAX_ROWS - 1)) # row cannot be greater than max rows

        # construct the cursor "command"
        command = LCD_SETDDRAMADDR | (col + row_offsets[row])

        # send the complete bytes (special command + command)
        self._i2c.write_byte(self.address, SPECIAL_COMMAND, command)

    def set_contrast(self, contrast):
        """!
            Set the contrast of the LCD screen (0-255)

            @param contrast: **int** The new contrast value (0-255)
        """
        # To set the contrast we need to send 3 bytes:
        # (1) SETTINGS_COMMAND
        # (2) CONTRAST_COMMAND
        # (3) contrast value
        #
        # To do this, we are going to use write_block(),
        # so we need our "block of bytes" to include
        # CONTRAST_COMMAND and contrast value

        block = [CONTRAST_COMMAND, contrast]

        # send the complete bytes (address, settings command , contrast command, contrast value)
        self._i2c.write_block(self.address, SETTING_COMMAND, block)
        self._i2c.delay_ms(10)

    def set_backlight(self, r, g, b):
        """!
            Set the brightness of each backlight (red, green, blue)

            @param r: **int** The new red brightness value (0-255)
            @param g: **int** The new green brightness value (0-255)
            @param b: **int** The new blue brightness value (0-255)
        """
        # To set the backlight values, we are going to send 10 bytes
        # They will all live in a list called "block"
        # Let's fill up block with what we need to transmit...

        block = [0,1,2,3,4,5,6,7,8,9]

        # map our incoming values (0-255) to the backlight command range (0-29)
        red = 128 + map(r, 0, 255, 0, 29)
        green = 158 + map(g, 0, 255, 0, 29)
        blue = 188 + map(b, 0, 255, 0, 29)

        # Turn display off to hide confirmation messages
        self._display_control &= ~LCD_DISPLAYON
        block[0] = SPECIAL_COMMAND
        block[1] = (LCD_DISPLAYCONTROL | self._display_control)

        # Set the red, green and blue values
        block[2] = SETTING_COMMAND
        block[3] = red
        block[4] = SETTING_COMMAND
        block[5] = green
        block[6] = SETTING_COMMAND
        block[7] = blue

        # Turn display back on and end
        self._display_control |= LCD_DISPLAYON
        block[8] = SPECIAL_COMMAND
        block[9] = (LCD_DISPLAYCONTROL | self._display_control)

        # send the complete bytes (address, settings command , contrast command, contrast value)
        self._i2c.write_block(self.address, SETTING_COMMAND, block)
        self._i2c.delay_ms(50)

    def special_command(self, command, count = 1):
        """!
            Send one (or multiple) special commands to the display.
            Used by other functions.

            @param command: **int** Command to send (a single byte)
            @param count: **int** Number of times to send the command (if omitted, then default is once)
        """
        for i in range(0, count):
            # send the complete bytes (special command + command)
            self._i2c.write_byte(self.address, SPECIAL_COMMAND, command)
        self._i2c.delay_ms(50)

    def command(self, command):
        """!
            Send one setting command to the display.
            Used by other functions.

            @param command: **int** Command to send (a single byte)
        """
        self._i2c.write_byte(self.address, SETTING_COMMAND, command)
        self._i2c.delay_ms(10)

    def move_cursor_left(self, count = 1):
        """!
            Move the cursor one or more characters to the left.

            @param count: **int** Number of character spaces you'd like to move
        """
        self.special_command(LCD_CURSORSHIFT | LCD_CURSORMOVE | LCD_MOVELEFT, count)

    def move_cursor_right(self, count = 1):
        """!
            Move the cursor one or more characters to the right.

            @param count: **int** Number of character spaces you'd like to move
        """
        self.special_command(LCD_CURSORSHIFT | LCD_CURSORMOVE | LCD_MOVERIGHT, count)

    def cursor(self):
        """!
            Turn the underline cursor on.
        """
        self._display_control |= LCD_CURSORON
        self.special_command(LCD_DISPLAYCONTROL | self._display_control)

    def no_cursor(self):
        """!
            Turn the underline cursor off.
        """
        self._display_control &= ~LCD_CURSORON
        self.special_command(LCD_DISPLAYCONTROL | self._display_control)

    def blink(self):
        """!
            Turn the blink cursor on.
        """
        self._display_control |= LCD_BLINKON
        self.special_command(LCD_DISPLAYCONTROL | self._display_control)

    def no_blink(self):
        """!
            Turn the blink cursor off.
        """
        self._display_control &= ~LCD_BLINKON
        self.special_command(LCD_DISPLAYCONTROL | self._display_control)

    def scroll_display_left(self, count = 1):
        """!
            Scroll the display one or multiple characters to the left, without changing the text.

            @param count: **int** Number of character spaces you'd like to scroll
        """
        self.special_command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT, count)

    def scroll_display_right(self, count = 1):
        """!
            Scroll the display one or multiple characters to the right, without changing the text.

            @param count: **int** Number of character spaces you'd like to scroll
        """
        self.special_command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT, count)

    def autoscroll(self):
        """!
            Turn autoscrolling on. This will right-justify text from the cursor.
        """
        self._display_control |= LCD_ENTRYSHIFTINCREMENT
        self.special_command(LCD_ENTRYMODESET | self._display_control)

    def no_autoscroll(self):
        """!
            Turn autoscrolling off.
        """
        self._display_control &= ~LCD_ENTRYSHIFTINCREMENT
        self.special_command(LCD_ENTRYMODESET | self._display_control)

    def left_to_right(self):
        """!
            Set the text to flow from left to right.
        """
        self._display_control |= LCD_ENTRYLEFT
        self.special_command(LCD_ENTRYMODESET | self._display_control)

    def right_to_left(self):
        """!
            Set the text to flow from right to left
        """
        self._display_control &= ~LCD_ENTRYLEFT
        self.special_command(LCD_ENTRYMODESET | self._display_control)

    def create_char(self, location, charmap):
        """!
            Create a custom character

            @param location: **int** character number 0 to 7
            @param charmap: **list of int** byte array for character
        """
        location &= 0x7 # we only have 8 locations 0-7

        # create a block of data bytes to send to the screen
        # This will include the location (with the addition of 27 to let the screen know)
        # and the 8 bytes of charmap
        block = [0,1,2,3,4,5,6,7,8,9]

        block[0] = (27 + location) # command type/location

        for i in range(1,9):
            block[i] = charmap[i-1]

        # send the complete bytes (address, settings command , write char command (includes location), charmap)
        self._i2c.write_block(self.address, SETTING_COMMAND, block)
        self._i2c.delay_ms(50)

    def write_char(self, location):
        """!
            Write a custom character to the display

            @param location: **int** character number 0 to 7
        """
        location &= 0x7 # we only have 8 locations 0-7

        # send command
        self.command(35 + location)
        self._i2c.delay_ms(50)

    def display(self):
        """!
            Turn the display on quickly.
        """
        self._display_control |= LCD_DISPLAYON
        self.special_command(LCD_DISPLAYCONTROL | self._display_control)

    def no_display(self):
        """!
            Turn the display off quickly.
        """
        self._display_control &= ~LCD_DISPLAYON
        self.special_command(LCD_DISPLAYCONTROL | self._display_control)

    def set_fast_backlight(self, r, g, b):
        """!
            Set backlight with no LCD messages or delays

            @param r: **int** red backlight value 0-255
            @param g: **int** green backlight value 0-255
            @param b: **int** blue backlight value 0-255
        """
        # create a block of data bytes to send to the screen
        # This will include the SET_RGB_COMMAND, and three bytes of backlight values
        block = [0,1,2,3]

        block[0] = SET_RGB_COMMAND # command
        block[1] = r
        block[2] = g
        block[3] = b

        # send the complete bytes (address, settings command , rgb command , red byte, green byte, blue byte)
        self._i2c.write_block(self.address, SETTING_COMMAND, block)
        self._i2c.delay_ms(10)

    def enable_system_messages(self):
        """!
            Enable system messages
        """
        # send command
        self.command(ENABLE_SYSTEM_MESSAGE_DISPLAY)
        self._i2c.delay_ms(10)

    def disable_system_messages(self):
        """!
            Disable system messages
        """
        # send command
        self.command(DISABLE_SYSTEM_MESSAGE_DISPLAY)
        self._i2c.delay_ms(10)

    def enable_splash(self):
        """!
            Enable splash screen at power on
        """
        # send command
        self.command(ENABLE_SPLASH_DISPLAY)
        self._i2c.delay_ms(10)

    def disable_splash(self):
        """!
            Disable splash screen at power on
        """
        # send command
        self.command(DISABLE_SPLASH_DISPLAY)
        self._i2c.delay_ms(10)

    def save_splash(self):
        """!
            Save the current display as the splash
            Saves whatever is currently being displayed into EEPROM
            This will be displayed at next power on as the splash screen
        """
        # send command
        self.command(SAVE_CURRENT_DISPLAY_AS_SPLASH)
        self._i2c.delay_ms(10)

    def set_address(self, new_addr):
        """!
            Change the I2C Address. 0x72 is the default.
            Note that this change is persistent. If anything
            goes wrong you may need to do a hardware reset
            to unbrick the display.

            @param new_addr: **int** new i2c address
        """
        # create a block of data bytes to send to the screen
        # This will include the ADDRESS_COMMAND, and the new address byte value.
        block = [0,1]

        block[0] = ADDRESS_COMMAND # command
        block[1] = new_addr

        # send the complete bytes (address, settings command , address command , new_addr byte)
        self._i2c.write_block(self.address, SETTING_COMMAND, block)
        self._i2c.delay_ms(50)
        self.address = new_addr # update our own address, so we can still talk to the display
