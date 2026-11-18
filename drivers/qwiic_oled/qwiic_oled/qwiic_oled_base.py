#-----------------------------------------------------------------------------
# qwiic_oled_base.py
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2021
#
#
# More information on qwiic is at https:= www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2021 SparkFun Electronics
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
# pylint: disable=line-too-long, bad-whitespace, invalid-name, too-many-lines
# pylint: disable=too-many-lines, too-many-arguments, too-many-instance-attributes
# pylint: disable=too-many-public-methods

"""!
qwiic_oled_base
=================
The base Python module for the SSD1306 display driver on the following OLED displays:
- [Qwiic Micro OLED]](https://www.sparkfun.com/products/14532)
- [Qwiic OLED Display](https://www.sparkfun.com/products/17153)

This python package is a port of the existing [SparkFun Micro OLED Arduino Library](https://github.com/sparkfun/SparkFun_Micro_OLED_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

import math

import qwiic_i2c

from . import oled_fonts
from . import oled_logos

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
#
# The name of this device - note this is private
_DEFAULT_NAME = "OLED Display Driver (SSD1306)"

# Use the configuration for the Qwiic Micro OLED display as a default
#==================================================================================
# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x3D, 0x3C]

_LCDWIDTH            = 64
_LCDHEIGHT           = 48
#==================================================================================

# The defines from the OLED Aurdino library

I2C_COMMAND = 0x00
I2C_DATA = 0x40

FONTHEADERSIZE      = 6

WIDGETSTYLE0            = 0
WIDGETSTYLE1            = 1
WIDGETSTYLE2            = 2

SETCONTRAST         = 0x81
DISPLAYALLONRESUME  = 0xA4
DISPLAYALLON        = 0xA5
NORMALDISPLAY       = 0xA6
INVERTDISPLAY       = 0xA7
DISPLAYOFF          = 0xAE
DISPLAYON           = 0xAF
SETDISPLAYOFFSET    = 0xD3
SETCOMPINS          = 0xDA
SETVCOMDESELECT     = 0xDB
SETDISPLAYCLOCKDIV  = 0xD5
SETPRECHARGE        = 0xD9
SETMULTIPLEX        = 0xA8
SETLOWCOLUMN        = 0x00
SETHIGHCOLUMN       = 0x10
SETSTARTLINE        = 0x40
MEMORYMODE          = 0x20
COMSCANINC          = 0xC0
COMSCANDEC          = 0xC8
SEGREMAP            = 0xA0
CHARGEPUMP          = 0x8D
EXTERNALVCC         = 0x01
SWITCHCAPVCC        = 0x02

#  Scroll
ACTIVATESCROLL                  = 0x2F
DEACTIVATESCROLL                = 0x2E
SETVERTICALSCROLLAREA           = 0xA3
RIGHTHORIZONTALSCROLL           = 0x26
LEFT_HORIZONTALSCROLL           = 0x27
VERTICALRIGHTHORIZONTALSCROLL   = 0x29
VERTICALLEFTHORIZONTALSCROLL    = 0x2A


class QwiicOLEDBase(object):
    """!
        QwiicOLEDBase

        @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        @param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.
        @param pixel_width: Width of the display in pixels
        @param pixel_height: Height of the display in pixels

        @return **Object** The SSD1306 OLED device object.
        """

    # Constructor
    device_name         =_DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # user exposed constants
    BLACK = 0
    WHITE = 1

    NORM                = 0
    XOR                 = 1

    PAGE                = 0
    ALL                 = 1


    def __init__(self, address=None, i2c_bus=None, pixel_width = _LCDWIDTH, pixel_height = _LCDHEIGHT):

        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address?
        self.address = address if address is not None else self.available_addresses[0]

        # Screen size:
        self.lcd_height = pixel_height
        self.lcd_width  = pixel_width

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

        # define the screen buffer - since this is a two color display, only bits are used
        # So the height is 8  bits / byte or LCDHEIGHT/8
        self._screenbuffer = bytearray(self.lcd_width * int(math.ceil(self.lcd_height/8.)))

        # Set initial contents
        self._screenbuffer = [0x00]*int(self.lcd_width*self.lcd_height/8) #Screen Area in bytes (Total Pixels/8)
        
        # Display SparkFun Logo
        oled_logos.add_logo(self._screenbuffer)
        
        # Display ans Clear Page
        # self.display()
        # time.sleep(2)
        # self.clear(self.PAGE)
        
        self.cursor_x = 0
        self.cursor_y = 0

        self.fore_color = self.WHITE
        self.draw_mode  = self.NORM

        # self.font_width = 0
        # self.font_height = 0
        # self.font_start_char = 0
        # self.font_total_char = 0
        self.font_type = 0
        # self.font_data = None
        self._font = None

        self.n_fonts = oled_fonts.count()


    #--------------------------------------------------------------------------
    def is_connected(self):
        """!
            Determine if a SSD1306 OLED device is connected to the system.

            @return **bool** True if the device is connected, otherwise False.
            """
        return qwiic_i2c.is_device_connected(self.address)

    #--------------------------------------------------------------------------
    def begin(self):
        """!
            Initialize the operation of the SSD1306 display driver for the OLED module

            @return **bool** Returns true of the initializtion was successful, otherwise False.
            """

        self.set_font_type(0)
        self.set_color(self.WHITE)
        self.set_draw_mode(self.NORM)
        self.set_cursor(0,0)

        #  Display Init sequence
        self._i2c.write_byte(self.address, I2C_COMMAND, DISPLAYOFF)          #  0xAE

        self._i2c.write_byte(self.address, I2C_COMMAND, SETDISPLAYCLOCKDIV)  #  0xD5
        self._i2c.write_byte(self.address, I2C_COMMAND, 0x80)                    #  the suggested ratio 0x80

        self._i2c.write_byte(self.address, I2C_COMMAND, SETMULTIPLEX)            #  0xA8
        self._i2c.write_byte(self.address, I2C_COMMAND, self.lcd_height - 1)

        self._i2c.write_byte(self.address, I2C_COMMAND, SETDISPLAYOFFSET)        #  0xD3
        self._i2c.write_byte(self.address, I2C_COMMAND, 0x0)                 #  no offset

        self._i2c.write_byte(self.address, I2C_COMMAND, SETSTARTLINE | 0x0)  #  line #0

        self._i2c.write_byte(self.address, I2C_COMMAND, CHARGEPUMP)          #  enable charge pump
        self._i2c.write_byte(self.address, I2C_COMMAND, 0x14)

        self._i2c.write_byte(self.address, I2C_COMMAND, NORMALDISPLAY)           #  0xA6
        self._i2c.write_byte(self.address, I2C_COMMAND, DISPLAYALLONRESUME)  #  0xA4

        self._i2c.write_byte(self.address, I2C_COMMAND, SEGREMAP | 0x1)
        self._i2c.write_byte(self.address, I2C_COMMAND, COMSCANDEC)

        self._i2c.write_byte(self.address, I2C_COMMAND, SETCOMPINS)          #  0xDA
        if len(self._screenbuffer) == 512:
            self._i2c.write_byte(self.address, I2C_COMMAND, 0x02)                # rect (128x32 OLED modules)
        else:
            self._i2c.write_byte(self.address, I2C_COMMAND, 0x12)                # square and large (64x48 or 128x64 OLED modules)

        self._i2c.write_byte(self.address, I2C_COMMAND, SETCONTRAST)         #  0x81
        self._i2c.write_byte(self.address, I2C_COMMAND, 0x8F)

        self._i2c.write_byte(self.address, I2C_COMMAND, SETPRECHARGE)            #  0xd9
        self._i2c.write_byte(self.address, I2C_COMMAND, 0x22)

        self._i2c.write_byte(self.address, I2C_COMMAND, SETVCOMDESELECT)         #  0xDB
        self._i2c.write_byte(self.address, I2C_COMMAND, 0x30)

        self._i2c.write_byte(self.address, I2C_COMMAND, DISPLAYON)               # --turn on oled panel
        self.clear(self.ALL)                        #  Erase hardware memory inside the OLED controller to aself random data in memory.

        return True

    #----------------------------------------------------
    # brief Set SSD1306 page address.
    #     Send page address command and address to the SSD1306 OLED controller.

    def set_page_address(self, page_address):
        """!
            Set SSD1306 page address.

            @param page_address: The page address command and address

            @return  No return value

        
            """

        # self._i2c.write_byte(self.address, I2C_COMMAND, 0xb0|page_address)

        self._i2c.write_byte(self.address, I2C_COMMAND, 0x22)
        self._i2c.write_byte(self.address, I2C_COMMAND, (page_address& (self.lcd_height - 1)))
        self._i2c.write_byte(self.address, I2C_COMMAND, self.lcd_height - 1)

    #----------------------------------------------------
    # Send column address command and address to the SSD1306 OLED controller.
    def set_column_address(self, col_address):
        """!
            Set SSD1306 column address.

            @param col_address: The column address command and address

            @return  No return value

        
            """
        
        if len(self._screenbuffer) == 384:
            self._i2c.write_byte(self.address, I2C_COMMAND, (0x10|(col_address>>4))+0x02)
            self._i2c.write_byte(self.address, I2C_COMMAND, (0x0f&col_address))
        else:
            self._i2c.write_byte(self.address, I2C_COMMAND, 0x21)
            self._i2c.write_byte(self.address, I2C_COMMAND, (col_address& (self.lcd_width - 1)))
            self._i2c.write_byte(self.address, I2C_COMMAND, self.lcd_width -1)

    #----------------------------------------------------
    #  To clear GDRAM inside the LCD controller, pass in the variable mode = ALL and to clear screen page buffer pass in the variable mode = PAGE.

    def clear(self, mode, value=0):
        """!
            Clear the display on the OLED Device.

            @param mode: To clear GDRAM inside the LCD controller, pass in the variable mode = ALL,
                 and to clear screen page buffer pass in the variable mode = PAGE.
            @param value: The value to clear the screen to. Default value is 0

            @return  No return value

        
            """

        if mode == self.ALL:
            for i in range(8):
                self.set_page_address(i)
                self.set_column_address(0)
                #pylint: disable=unused-variable
                for j in range(0x80):
                    self._i2c.write_byte(self.address, I2C_DATA, value)
                #pylint: enable=unused-variable
        else:
            self._screenbuffer[:] = [value]*len(self._screenbuffer)

    #--------------------------------------------------------------------------
    # The WHITE color of the display will turn to BLACK and the BLACK will turn to WHITE.

    def invert(self, inv):
        """!
            Invert the display of the display. The WHITE color of the display will turn to BLACK and the BLACK will turn to WHITE.

            @param inv: If True, the screen is inverted. If False the screen is set to Normal mode.

            @return  No return value

        
            """
        if inv:
            self._i2c.write_byte(self.address, I2C_COMMAND, INVERTDISPLAY)
        else:
            self._i2c.write_byte(self.address, I2C_COMMAND, NORMALDISPLAY)

    #--------------------------------------------------------------------------
    # OLED contract value from 0 to 255. Note: Contrast level is not very obvious.

    def contrast(self, contrast):
        """!
            Set the OLED contract value from 0 to 255. Note: Contrast level is not very obvious on the display.

            @param contrast: Contrast Value between 0-255

            @return  No return value

        
            """
        self._i2c.write_byte(self.address, I2C_COMMAND, SETCONTRAST)     #  0x81
        self._i2c.write_byte(self.address, I2C_COMMAND, contrast)

    #--------------------------------------------------------------------------
    # Bulk move the screen buffer to the SSD1306 controller's memory so that images/graphics drawn on the screen buffer will be displayed on the OLED.

    def display(self):
        """!
            Display the current screen buffer on the Display device.
            Bulk move the screen buffer to the SSD1306 controller's memory so that images/graphics drawn on the screen buffer will be displayed on the OLED.

            @return  No return value

        
            """
        # the I2C library being used allows blocks upto 32 ints to be sent at a time.
        #
        # The screenbuffer is sliced into 32 int blocks and set. This results in a faster
        # refresh than the ported method (Good god, it was updating a pixel at a time ... )
        #
        lenBlock = 32
        lenLine = self.get_lcd_width()
        lenHieght = self.get_lcd_height()
        nBlocks = int(math.ceil(lenLine/lenBlock))
        mBlocks = int(math.ceil(lenHieght/8))

        for i in range(mBlocks):

            self.set_page_address(i)
            lineStart = i * lenLine  # offset in the screen buffer for the current line/row

            for iBlock in range(nBlocks):

                iStart = iBlock * lenBlock
                self.set_column_address(iStart)
                iEnd = iStart  + min(lenLine - iStart, lenBlock) # what's left - not > 32 in len

                # Send the block - take into account the current line/row offset
                self._i2c.write_block(self.address, I2C_DATA, self._screenbuffer[lineStart+iStart:lineStart+iEnd])

    #     Leftover from port -> Arduino's print overridden so that we can use uView.print().
    #--------------------------------------------------------------------------
    def write(self, c):
        """!
            Write a character on the display using the current font, at the current position.

            @param c: Character to write. A value of '\\\\n' starts a new line.

            @return  1 on success

        
            """
        if c == '\n':
            # self.cursor_y += self.font_height
            self.cursor_y += self._font.height
            self.cursor_x = 0
        elif c != '\r':
            self.draw_char(self.cursor_x, self.cursor_y, c)
            self.cursor_x += self._font.width+1
            if self.cursor_x > (self.lcd_width - self._font.width):
                self.cursor_y += self._font.height
                self.cursor_x = 0

        return 1

    #--------------------------------------------------------------------------
    def print(self, text):
        """!
            Print a line of text on the display using the current font,
            starting at the current position.

            @param text: The line of text to write.

            @return  No return value

        
            """

        # a list or array? If not, make it one
        if not hasattr(text, '__len__'): # scalar?
            text = str(text)

        if isinstance(text, str):
            text = bytearray(text, 'ascii')

        for curr in text:
            self.write(curr)


    #--------------------------------------------------------------------------
    # OLED's cursor position to x,y.

    def set_cursor(self, x, y):
        """!
            Set the current cusor position for writing text

            @param x: The X position on the display
            @param y: The Y position on the display

            @return  No return value

        
            """
        self.cursor_x = x
        self.cursor_y = y

    #--------------------------------------------------------------------------
    # Draw color pixel in the screen buffer's x,y position with NORM or XOR draw mode.

    def pixel(self, x, y, color=None, mode=None):
        """!
            Draw a pixel at a given position, with a given color. Pixel copy mode is
            either Normal (source copy) or XOR

            @param x: The X position on the display
            @param y: The Y position on the display
            @param color: The color to draw. If not set, the default foreground color is used.
            @param mode: The mode to draw the pixl to the screen bufffer. Value can be either
                        XOR or NORM. Default is NORM

            @return  No return value

        
            """

        if color is None:
            color = self.fore_color

        if mode is None:
            mode = self.draw_mode

        if  x < 0 or  x >= self.lcd_width or y < 0 or y >= self.lcd_height:
            return

        x = int(x)
        y = int(y)
        index = x + (y//8)*self.lcd_width

        if mode == self.XOR:
            if color == self.WHITE:
                self._screenbuffer[index] ^= (1 << (y%8))

        else:
            if color == self.WHITE:
                self._screenbuffer[index] |= (1 << (y%8))
            else:
                self._screenbuffer[index] &= (~(1 << (y%8)) & 0xff)

    #--------------------------------------------------------------------------
    #  Draw line using color and mode from x0,y0 to x1,y1 of the screen buffer.

    def line(self, x0, y0, x1, y1, color=None, mode=None):
        """!
            Draw a line starting at and ending at specified coordinates, with a given color. Pixel copy mode is either Normal (source copy) or XOR

            @param x0: The X starting position for the line
            @param y0: The Y starting position for the line.
            @param x1: The X ending position for the line
            @param y1: The Y ending position for the line.
            @param color: The color to draw. If not set, the default foreground color is used.
            @param mode: The mode to draw the pixl to the screen bufffer. Value can be either XOR or NORM. Default is NORM

            @return  No return value

        
            """

        if color is None:
            color = self.fore_color

        if mode is None:
            mode = self.draw_mode

        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            # swap
            (x0, y0) = (y0, x0)
            (x1, y1) = (y1, x1)

        if x0 > x1:
            # swap
            (x0, x1) = (x1, x0)
            (y0, y1) = (y1, y0)

        dx = x1 - x0
        dy = abs(y1 - y0)

        err = dx // 2

        ystep = 1 if y0 < y1 else -1


        while x0 < x1:

            if steep:
                self.pixel(y0, x0, color, mode)
            else:
                self.pixel(x0, y0, color, mode)

            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1

    #--------------------------------------------------------------------------
    # Draw horizontal line using color and mode from x,y to x+width,y of the screen buffer.

    def line_h(self, x, y, width, color=None, mode=None):
        """!
            Draw a horizontal line defined by a starting position and width. A color can be specified. Pixel copy mode is either Normal (source copy) or XOR

            @param x: The X starting position for the line
            @param y: The Y starting position for the line.
            @param width: The width (length) of the line
            @param color: The color to draw. If not set, the default foreground color is used.
            @param mode: The mode to draw the pixl to the screen bufffer. Value can be either XOR or NORM. Default is NORM

            @return  No return value

        
            """

        if color is None:
            color = self.fore_color

        if mode is None:
            mode = self.draw_mode

        self.line(x, y, x+width, y, color, mode)

    #--------------------------------------------------------------------------
    # Draw vertical line using color and mode from x,y to x,y+height of the screen buffer.

    def line_v(self, x, y, height, color=None, mode=None):
        """!
            Draw a vertical line defined by a starting position and width. A color can be specified.
            Pixel copy mode is either Normal (source copy) or XOR

            @param x: The X starting position for the line
            @param y: The Y starting position for the line.
            @param height: The height (length) of the line
            @param color: The color to draw. If not set, the default foreground color is used.
            @param mode: The mode to draw the pixl to the screen bufffer. Value can be either
                        XOR or NORM. Default is NORM

            @return  No return value

        
            """

        if color is None:
            color = self.fore_color

        if mode is None:
            mode = self.draw_mode

        self.line(x, y, x, y+height, color, mode)

    #--------------------------------------------------------------------------
    # Draw rectangle using color and mode from x,y to x+width,y+height of the screen buffer.

    def rect(self, x, y, width, height, color=None, mode=None):
        """!
            Draw a rectangle on the diplay. A color can be specified. Pixel copy mode is either Normal (source copy) or XOR

            @param x: The X starting position for the rectangle
            @param y: The Y starting position for the rectangle.
            @param width: The width of the rectangle
            @param height: The height of the rectangle
            @param color: The color to draw. If not set, the default foreground color is used.
            @param mode: The mode to draw the pixl to the screen bufffer.
                        Value can be either XOR or NORM. Default is NORM

            @return  No return value

        
            """

        if color is None:
            color = self.fore_color

        if mode is None:
            mode = self.draw_mode

        self.line_h(x, y, width, color, mode)
        self.line_h(x, y+height-1, width, color, mode)

        tempHeight = height-2

        # skip drawing vertical lines to aself overlapping of pixel that will
        # affect XOR plot if no pixel in between horizontal lines
        if tempHeight < 1:
            return

        self.line_v(x, y+1, tempHeight, color, mode)
        self.line_v(x+width-1, y+1, tempHeight, color, mode)

    #--------------------------------------------------------------------------
    #  Draw filled rectangle using color and mode from x,y to x+width,y+height of the screen buffer.

    def rect_fill(self, x, y, width, height, color=None, mode=None):
        """!
            Draw a filled rectangle on the diplay. A color can be specified. Pixel copy mode is either Normal (source copy) or XOR

            @param x: The X starting position for the rectangle
            @param y: The Y starting position for the rectangle.
            @param width: The width of the rectangle
            @param height: The height of the rectangle
            @param color: The color to draw. If not set, the default foreground color is used.
            @param mode: The mode to draw the pixl to the screen bufffer.
                        Value can be either XOR or NORM. Default is NORM

            @return  No return value

        
            """

        if color is None:
            color = self.fore_color

        if mode is None:
            mode = self.draw_mode

        # // TODO - need to optimise the memory map draw so that this function will not call pixel one by one
        for i in range(x, x+width):
            self.line_v(i, y, height, color, mode)

    #--------------------------------------------------------------------------
    # Draw circle with radius using color and mode at x,y of the screen buffer.

    def circle(self, x0, y0, radius, color=None, mode=None):
        """!
            Draw a circle on the diplay. A color can be specified. Pixel copy mode is either Normal (source copy) or XOR

            @param x0: The X center position for the circle
            @param y0: The Y center position for the circle.
            @param radius: The radius of the circle
            @param color: The color to draw. If not set, the default foreground color is used.
            @param mode: The mode to draw the pixl to the screen bufffer. Value can be either XOR or NORM. Default is NORM

            @return  No return value

        
            """

        if color is None:
            color = self.fore_color

        if mode is None:
            mode = self.draw_mode

        # in the future- find a way to check for no overlapping of pixels so that XOR draw mode will work perfectly
        f = 1 - radius
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius

        self.pixel(x0, y0+radius, color, mode)
        self.pixel(x0, y0-radius, color, mode)
        self.pixel(x0+radius, y0, color, mode)
        self.pixel(x0-radius, y0, color, mode)

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y

            x += 1
            ddF_x += 2
            f += ddF_x

            self.pixel(x0 + x, y0 + y, color, mode)
            self.pixel(x0 - x, y0 + y, color, mode)
            self.pixel(x0 + x, y0 - y, color, mode)
            self.pixel(x0 - x, y0 - y, color, mode)

            self.pixel(x0 + y, y0 + x, color, mode)
            self.pixel(x0 - y, y0 + x, color, mode)
            self.pixel(x0 + y, y0 - x, color, mode)
            self.pixel(x0 - y, y0 - x, color, mode)

    # The height of the LCD return as byte.

    def get_lcd_height(self):
        """!
            The height of the display in pixels

            @return  height of the display
            :rvalue: integer

        
            """
        return self.lcd_height


    # The width of the LCD return as byte.
    def get_lcd_width(self):
        """!
            The width of the display in pixels

            @return  width of the display
            :rvalue: integer

        
            """
        return self.lcd_width


    # The cucrrent font's width return as byte.

    def get_font_width(self):
        """!
            The width of the current font

            @return  width of the font
            :rvalue: integer

        
            """
        return self._font.width


    # The current font's height return as byte.

    def get_font_height(self):
        """!
            The height of the current font

            @return  height of the font
            :rvalue: integer

        
            """
        return self._font.height

    # Return the starting ASCII character of the currnet font, not all fonts start with ASCII character 0. Custom fonts can start from any ASCII character.

    def get_font_start_char(self):
        """!
            Return the starting ASCII character of the currnet font, not all fonts start with ASCII character 0.
            Custom fonts can start from any ASCII character.

            @return  Starting character of the current font.
            :rvalue: integer

        
            """
        return self._font.start_char

    # Return the total characters of the current font.

    def get_font_total_char(self):
        """!
            The total number of characters in the current font.

            @return  Total number of characters
            :rvalue: integer

        
            """
        return self._font.total_char


    # Return the total number of fonts loaded into the OLED's flash memory.

    def get_total_fonts(self):
        """!
            Return the total number of fonts loaded into the OLED's flash memory.

            @return  Total number of fonts available
            :rvalue: integer

        
            """
        return self.n_fonts

    # Return the font type number of the current font.
    def get_font_type(self):
        """!
            Return the font type number of the current font.

            @return  Font type number.
            :rvalue: integer

        
            """
        return self.font_type

    # Set the current font type number, ie changing to different fonts base on the type provided.

    def set_font_type(self, font_type):
        """!
            Set the current font type number, ie changing to different fonts base on the type provided.

            @param font_type: The type to set the font to.

            @return **bool** True if the font was loaded, otherwise False

        
            """

        if font_type >= self.n_fonts or font_type < 0:
            return False

        self.font_type = font_type
        self._font = oled_fonts.get_font(font_type)
        if self._font is None:
            return False

        return True

    # Set the current draw's color. Only WHITE and BLACK available.

    def set_color(self, color):
        """!
            Set the current draw's color. Only WHITE and BLACK available.

            @param color: Color Value

            @return  No return value

        
            """
        self.fore_color = color

    # Set current draw mode with NORM or XOR.

    def set_draw_mode(self, mode):
        """!
            Set current draw mode with NORM or XOR.

            @param mode: Draw Mode

            @return  No return value

        
            """
        self.draw_mode = mode

    # Draw character c using color and draw mode at x,y.
    # pylint: disable=too-many-locals
    def draw_char(self, x, y, c, color=None, mode=None):
        """!
            Draw character c using color and draw mode at x,y. Pixel copy mode is either Normal (source copy) or XOR

            @param x: The X position on the display
            @param y: The Y position on the display
            @param c: The character to draw
            @param color: The color to draw. If not set, the default foreground color is used.
            @param mode: The mode to draw the pixl to the screen bufffer. Value can be either XOR or NORM. Default is NORM

            @return  No return value

        
            """

        if color is None:
            color = self.fore_color

        if mode is None:
            mode = self.draw_mode

        if self._font is None:
            return

        if c < self._font.start_char or c > (self._font.start_char + self._font.total_char - 1): # no bitmap for the required c
            return

        tempC = c - self._font.start_char

        # // each row (in datasheet is call page) is 8 bits high, 16 bit high character will have 2 rows to be drawn
        rowsToDraw = self._font.height//8   # 8 is LCD's page size, see SSD1306 datasheet

        if rowsToDraw <= 1:
            rowsToDraw = 1

        # figure out position of the character in the font map. integer math is key here
        charPerRow = self._font.map_width // self._font.width

        rowPos = tempC // charPerRow  # the number of full rows to skip
        colPos = tempC % charPerRow # the number of chars into the last
        iStart = rowPos * charPerRow * self._font.height//8 + colPos

        # each row on LCD is 8 bit height (see datasheet for explanation)
        for row in range(rowsToDraw):

            # load in the current character block.
            #pylint: disable=consider-using-enumerate, invalid-unary-operand-type
            fBuffer = self._font[iStart + row * charPerRow]
            for i in range(len(fBuffer)):

                for j in range(8):  # 8 is the LCD's page height (see datasheet for explanation)

                    self.pixel(x+i, y+j + (row*8), \
                        color if fBuffer[i] & 0x01 << j else (~color & 0xFF), \
                        mode)
            #pylint: enable=consider-using-enumerate, invalid-unary-operand-type

    
    def scroll_stop(self):
        """!
            Stop scrolling operation.

            @return  No return value

        
            """

        self._i2c.write_byte(self.address, I2C_COMMAND, DEACTIVATESCROLL)


    # Set row start to row stop on the OLED to scroll.
    def scroll (self, start, stop, scroll_command = RIGHTHORIZONTALSCROLL, vert_offset = 0):
        """!
            Set row start to row stop on the OLED to scroll.
            Refer to http://learn.microview.io/intro/general-overview-of-microview.html for explanation of the rows.

            @param start: The staring position on the display
            @param stop: The stopping position on the display
            @param scroll_command: The scroll command, for example RIGHTHORIZONTALSCROLL
            @param vert_offset: Vertical rows per step for the vertical scroll commands (0 means 1)

            @return  No return value
        
            """
        if stop < start:        # stop must be larger or equal to start
            return

        if scroll_command in [VERTICALRIGHTHORIZONTALSCROLL, VERTICALLEFTHORIZONTALSCROLL]:
            self._i2c.write_byte(self.address, I2C_COMMAND, SETVERTICALSCROLLAREA)
            self._i2c.write_byte(self.address, I2C_COMMAND, 0x00)
            self._i2c.write_byte(self.address, I2C_COMMAND, self.lcd_height)
            if vert_offset == 0:
                vert_offset = 1
        
        self.scroll_stop()       # need to disable scrolling before starting to avoid memory corrupt

        self._i2c.write_byte(self.address, I2C_COMMAND, scroll_command)
        self._i2c.write_byte(self.address, I2C_COMMAND, 0x00)
        self._i2c.write_byte(self.address, I2C_COMMAND, start)
        self._i2c.write_byte(self.address, I2C_COMMAND, 0x7)     # scroll speed frames , TODO
        self._i2c.write_byte(self.address, I2C_COMMAND, stop)
        self._i2c.write_byte(self.address, I2C_COMMAND, vert_offset)
        if vert_offset == 0: # Horizontal scroll
            self._i2c.write_byte(self.address, I2C_COMMAND, 0xFF)
        self._i2c.write_byte(self.address, I2C_COMMAND, ACTIVATESCROLL)
    
    # Refer to http://learn.microview.io/intro/general-overview-of-microview.html for explanation of the rows.

    def scroll_right(self, start, stop):
        """!
            Set row start to row stop on the OLED to scroll right.
            Refer to http://learn.microview.io/intro/general-overview-of-microview.html for explanation of the rows.

            @param start: The staring position on the display
            @param stop: The stopping position on the display

            @return  No return value

        
            """
        self.scroll(start, stop, RIGHTHORIZONTALSCROLL)

    def scroll_left(self, start, stop):
        """!
            Set row start to row stop on the OLED to scroll right.
            Refer to http://learn.microview.io/intro/general-overview-of-microview.html for explanation of the rows.

            @param start: The staring position on the display
            @param stop: The stopping position on the display

            @return  No return value

        
            """
        self.scroll(start, stop, LEFT_HORIZONTALSCROLL)

    def scroll_vert_left(self,start,stop, vert_offset = 1):
        """!
            Set row start to row stop on the OLED to scroll vertical right (Diagonally).
            Refer to http://learn.microview.io/intro/general-overview-of-microview.html for explanation of the rows.

            @param start: The staring position on the display
            @param stop: The stopping position on the display
            @param vert_offset: The vertical offset

            @return  No return value

        
            """
        self.scroll(start, stop, VERTICALLEFTHORIZONTALSCROLL, vert_offset)
    
    def scroll_vert_right(self, start, stop, vert_offset = 1):
        """!
            Set row start to row stop on the OLED to scroll vertical right (Diagonally).
            Refer to http://learn.microview.io/intro/general-overview-of-microview.html for explanation of the rows.

            @param start: The staring position on the display
            @param stop: The stopping position on the display
            @param vert_offset: The vertical offset

            @return  No return value

        
            """
        self.scroll(start, stop, VERTICALRIGHTHORIZONTALSCROLL, vert_offset)

    # Flip the graphics on the OLED vertically.
    def flip_vertical(self, flip):
        """!
            Flip the graphics on the OLED vertically.

            @return  No return value

        
            """

        self._i2c.write_byte(self.address, I2C_COMMAND, COMSCANINC if flip else COMSCANDEC)

    # Flip the graphics on the OLED horizontally.
    def flip_horizontal(self, flip):
        """!
            Flip the graphics on the OLED horizontally.

            @return  No return value

        
            """
        self._i2c.write_byte(self.address, I2C_COMMAND, SEGREMAP | ( 0x0 if flip else 0x1))
        self.clear(self.ALL)
        self.display()

    # Return a pointer to the start of the RAM screen buffer for direct access.
    def get_screenbuffer(self):
        """!
            Return a pointer to the start of the RAM screen buffer for direct access.

            @return **integer array** The internal screen buffer
            """
        return self._screenbuffer


    # Draw Bitmap image on screen. The array for the bitmap can be stored in the Arduino file, so user don't have to mess with the library files.
    # To use, create uint8_t array that is 64x48 pixels (384 bytes). Then call .draw_bitmap and pass it the array.

    def draw_bitmap(self, bit_array):
        """!
            Draw Bitmap image on screen.
            To use, create int array that is 64x48 pixels (384 bytes). Then call .draw_bitmap and pass it the array.

            @param bit_array: The bitmap to draw

            @return  No return value

        
            """

        if len(bit_array) != len(self._screenbuffer):
            raise ValueError("draw_bitmap: the bitmap must be %d bytes" % len(self._screenbuffer))

        self._screenbuffer[:] = bit_array
