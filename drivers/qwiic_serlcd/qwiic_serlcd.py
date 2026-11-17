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
import struct
import time

import qwiic_i2c

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

    @param float x: The value to be mapped
    @param float in_min: Minimum of input range
    @param float in_max: Maximum of input range
    @param float out_min: Minimum of output range
    @param float out_max: Maximum of output range
    @return **int** The value scaled to the new range
    """
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicSerlcd(object):
    """!
    This class implements the basic functions of the Qwiic SerLCD device via the I2C bus.
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS
    _displayControl = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
    _displayMode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT

    # Constructor
    def __init__(self, address=None, i2c_driver=None):
        """!
        @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        @param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        @return: **Object** The QwiicSerlcd device object.
        """
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

    def is_connected(self):
        """!
        @brief Determine if a device is connected to the system.
        This method checks if the device with the specified I2C address is connected to the system.
        @return **bool** True if the device is connected, otherwise False.
        """
        # Another possible comment could be @retval bool True: Device is connected. above
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):
        """!
        Initialize the operation of the SerLCD module

        @return **bool** Returns true if the initialization was successful, otherwise False.
        """
        # set default settings, as defined in constructor
        result0 = self.specialCommand(LCD_DISPLAYCONTROL | self._displayControl)
        time.sleep(1)
        result1 = self.specialCommand(LCD_ENTRYMODESET | self._displayMode)
        time.sleep(1)
        result2 = self.clearScreen()
        time.sleep(1)

        return (bool(result0) & bool(result1) & bool(result2))

    def print(self, string):
        """!
            Print a string of characters to the LCD

            @param string string: The string you would like to print. Aka ASCII characters. example: "Hello"

            @return **bool** Returns True if the I2C writes were successful, otherwise False.
        """
        for c in string:
                if self._i2c.writeCommand(self.address, ord(c)) == False:
                        return False
                time.sleep(0.01)
        return True

    def clearScreen(self):
        """!
            Sends the command to clear the screen

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        result = self.command(CLEAR_COMMAND)
        time.sleep(0.01)
        return result

    def home(self):
        """!
            Send the home command to the display. This returns the cursor
            to the beginning of the display, without clearing
            the display.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        result = self.specialCommand(LCD_RETURNHOME)
        time.sleep(0.01)
        return result

    def setCursor(self, col, row):
        """!
            Set the cursor position to a particular column and row.

            @param int col: The column position (0-19)
            @param int row: The row position (0-3)

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        row_offsets = [0x00, 0x40, 0x14, 0x54]

        # keep variables in bounds
        row = max(0, row)            # row cannot be less than 0
        row = min(row, (MAX_ROWS - 1)) # row cannot be greater than max rows

        # construct the cursor "command"
        command = LCD_SETDDRAMADDR | (col + row_offsets[row])

        # send the complete bytes (special command + command)
        return self._i2c.writeByte(self.address, SPECIAL_COMMAND, command)

    def setContrast(self, contrast):
        """!
            Set the contrast of the LCD screen (0-255)

            @param int contrast: The new contrast value (0-255)

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        # To set the contrast we need to send 3 bytes:
        # (1) SETTINGS_COMMAND
        # (2) CONTRAST_COMMAND
        # (3) contrast value
        #
        # To do this, we are going to use writeBlock(),
        # so we need our "block of bytes" to include
        # CONTRAST_COMMAND and contrast value

        block = [CONTRAST_COMMAND, contrast]

        # send the complete bytes (address, settings command , contrast command, contrast value)
        result = self._i2c.writeBlock(self.address, SETTING_COMMAND, block)
        time.sleep(0.01)
        return result

    def setBacklight(self, r, g, b):
        """!
            Set the brightness of each backlight (red, green, blue)

            @param int red: The new red brightness value (0-255)
            @param int green: The new green brightness value (0-255)
            @param int blue: The new blue brightness value (0-255)

            @return **bool** Returns True if the I2C write was successful, otherwise False.
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
        self._displayControl &= ~LCD_DISPLAYON
        block[0] = SPECIAL_COMMAND
        block[1] = (LCD_DISPLAYCONTROL | self._displayControl)

        # Set the red, green and blue values
        block[2] = SETTING_COMMAND
        block[3] = red
        block[4] = SETTING_COMMAND
        block[5] = green
        block[6] = SETTING_COMMAND
        block[7] = blue

        # Turn display back on and end
        self._displayControl |= LCD_DISPLAYON
        block[8] = SPECIAL_COMMAND
        block[9] = (LCD_DISPLAYCONTROL | self._displayControl)

        # send the complete bytes (address, settings command , contrast command, contrast value)
        result = self._i2c.writeBlock(self.address, SETTING_COMMAND, block)
        time.sleep(0.05)
        return result

    def specialCommand(self, command, count = 1):
        """!
            Send one (or multiple) special commands to the display.
            Used by other functions.

            @param int command: Command to send (a single byte)
            @param int count: Number of times to send the command (if omitted, then default is once)

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        for i in range(0, count):
            # send the complete bytes (special command + command)
            result = self._i2c.writeByte(self.address, SPECIAL_COMMAND, command)
        time.sleep(0.05)
        return result

    def command(self, command):
        """!
            Send one setting command to the display.
            Used by other functions.

            @param int command: Command to send (a single byte)

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        result = self._i2c.writeByte(self.address, SETTING_COMMAND, command)
        time.sleep(0.01)
        return result

    def moveCursorLeft(self, count = 1):
        """!
            Move the cursor one or more characters to the left.

            @param int count: Number of character spaces you'd like to move

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        return self.specialCommand(LCD_CURSORSHIFT | LCD_CURSORMOVE | LCD_MOVELEFT, count)

    def moveCursorRight(self, count = 1):
        """!
            Move the cursor one or more characters to the right.

            @param int count: Number of character spaces you'd like to move

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        return self.specialCommand(LCD_CURSORSHIFT | LCD_CURSORMOVE | LCD_MOVERIGHT, count)

    def cursor(self):
        """!
            Turn the underline cursor on.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl |= LCD_CURSORON
        return self.specialCommand(LCD_DISPLAYCONTROL | self._displayControl)

    def noCursor(self):
        """!
            Turn the underline cursor off.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl &= ~LCD_CURSORON
        return self.specialCommand(LCD_DISPLAYCONTROL | self._displayControl)

    def blink(self):
        """!
            Turn the blink cursor on.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl |= LCD_BLINKON
        return self.specialCommand(LCD_DISPLAYCONTROL | self._displayControl)

    def noBlink(self):
        """!
            Turn the blink cursor off.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl &= ~LCD_BLINKON
        return self.specialCommand(LCD_DISPLAYCONTROL | self._displayControl)

    def scrollDisplayLeft(self, count = 1):
        """!
            Scroll the display one or multiple characters to the left, without changing the text.

            @param int count: Number of character spaces you'd like to scroll

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        return self.specialCommand(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT, count)

    def scrollDisplayRight(self, count = 1):
        """!
            Scroll the display one or multiple characters to the right, without changing the text.

            @param int count: Number of character spaces you'd like to scroll

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        return self.specialCommand(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT, count)

    def autoscroll(self):
        """!
            Turn autoscrolling on. This will right-justify text from the cursor.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl |= LCD_ENTRYSHIFTINCREMENT
        return self.specialCommand(LCD_ENTRYMODESET | self._displayControl)

    def noAutoscroll(self):
        """!
            Turn autoscrolling off.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl &= ~LCD_ENTRYSHIFTINCREMENT
        return self.specialCommand(LCD_ENTRYMODESET | self._displayControl)

    def leftToRight(self):
        """!
            Set the text to flow from left to right.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl |= LCD_ENTRYLEFT
        return self.specialCommand(LCD_ENTRYMODESET | self._displayControl)

    def rightToLeft(self):
        """!
            Set the text to flow from right to left

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl &= ~LCD_ENTRYLEFT
        return self.specialCommand(LCD_ENTRYMODESET | self._displayControl)

    def createChar(self, location, charmap):
        """!
            Create a custom character

            @param int location: character number 0 to 7
            @param list of int charmap: byte array for character

            @return **bool** Returns True if the I2C write was successful, otherwise False.
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
        result = self._i2c.writeBlock(self.address, SETTING_COMMAND, block)
        time.sleep(0.05)
        return result

    def writeChar(self, location):
        """!
            Write a custom character to the display

            @param int location: character number 0 to 7

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        location &= 0x7 # we only have 8 locations 0-7

        # send command
        result = self.command(35 + location)
        time.sleep(0.05)
        return result

    def display(self):
        """!
            Turn the display on quickly.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl |= LCD_DISPLAYON
        return self.specialCommand(LCD_DISPLAYCONTROL | self._displayControl)

    def noDisplay(self):
        """!
            Turn the display off quickly.

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        self._displayControl &= ~LCD_DISPLAYON
        return self.specialCommand(LCD_DISPLAYCONTROL | self._displayControl)

    def setFastBacklight(self, r, g, b):
        """!
            Set backlight with no LCD messages or delays

            @param int r: red backlight value 0-255
            @param int g: green backlight value 0-255
            @param int b: blue backlight value 0-255

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        # create a block of data bytes to send to the screen
        # This will include the SET_RGB_COMMAND, and three bytes of backlight values
        block = [0,1,2,3]

        block[0] = SET_RGB_COMMAND # command
        block[1] = r
        block[2] = g
        block[3] = b

        # send the complete bytes (address, settings command , rgb command , red byte, green byte, blue byte)
        result = self._i2c.writeBlock(self.address, SETTING_COMMAND, block)
        time.sleep(0.01)
        return result

    def enableSystemMessages(self):
        """!
            Enable system messages

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        # send command
        result = self.command(ENABLE_SYSTEM_MESSAGE_DISPLAY)
        time.sleep(0.01)
        return result

    def disableSystemMessages(self):
        """!
            Disable system messages

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        # send command
        result = self.command(DISABLE_SYSTEM_MESSAGE_DISPLAY)
        time.sleep(0.01)
        return result

    def enableSplash(self):
        """!
            Enable splash screen at power on

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        # send command
        result = self.command(ENABLE_SPLASH_DISPLAY)
        time.sleep(0.01)
        return result

    def disableSplash(self):
        """!
            Disable splash screen at power on

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        # send command
        result = self.command(DISABLE_SPLASH_DISPLAY)
        time.sleep(0.01)
        return result

    def saveSplash(self):
        """!
            Save the current display as the splash
            Saves whatever is currently being displayed into EEPROM
            This will be displayed at next power on as the splash screen

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        # send command
        result = self.command(SAVE_CURRENT_DISPLAY_AS_SPLASH)
        time.sleep(0.01)
        return result

    def setAddress(self, new_addr):
        """!
            Change the I2C Address. 0x72 is the default.
            Note that this change is persistent. If anything
            goes wrong you may need to do a hardware reset
            to unbrick the display.

            @param int new_addr: new i2c address

            @return **bool** Returns True if the I2C write was successful, otherwise False.
        """
        # create a block of data bytes to send to the screen
        # This will include the ADDRESS_COMMAND, and the new address byte value.
        block = [0,1]

        block[0] = ADDRESS_COMMAND # command
        block[1] = new_addr

        # send the complete bytes (address, settings command , address command , new_addr byte)
        result = self._i2c.writeBlock(self.address, SETTING_COMMAND, block)
        time.sleep(0.05)
        self.address = new_addr # update our own address, so we can still talk to the display
        return result
