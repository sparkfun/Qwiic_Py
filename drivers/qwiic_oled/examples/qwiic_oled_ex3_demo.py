#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_oled_ex3_demo.py
#
# An example showing various features of the display driver for Qwiic OLED displays
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2021
#
# This python library supports the SparkFun Electroncis qwiic
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers.
#
# More information on qwiic is at https:# www.sparkfun.com/qwiic
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

import qwiic_oled
import qwiic_i2c
import sys
import math
from random import randint

# --------- SET YOUR OLED DISPLAY TYPE HERE ----------------
# The library supports three different types of SparkFun boards. The demo uses the following
# variables to determine which device is being used. Uncomment the device being used for this demo.

userOLED = qwiic_oled.QwiicMicroOLED()   # Micro OLED             https://www.sparkfun.com/products/14532
# userOLED = qwiic_oled.QwiicOLEDDisplay() # "Narrow" OLED          https://www.sparkfun.com/products/24606
# userOLED = qwiic_oled.QwiicLargeOLED()  # Qwiic OLED 1.3in        https://www.sparkfun.com/products/23453

#-------------------------------------------------------------------
def pixel_example(my_oled):

    print("Pixels!")

    lWidth = my_oled.get_lcd_width()
    lHeight = my_oled.get_lcd_height()
    for i in range(128):
        my_oled.pixel(randint(0, lWidth), randint(0, lHeight))
        my_oled.display()

    my_oled.clear(my_oled.PAGE)
#-------------------------------------------------------------------
def line_example(my_oled):

    middleX = my_oled.get_lcd_width() // 2
    middleY = my_oled.get_lcd_height() // 2

    lineWidth = min(middleX, middleY)

    print("Lines!")

    for i in range(2):

        for deg in range(0, 360, 15):

            xEnd = lineWidth * math.cos(deg * math.pi / 180.0)
            yEnd = lineWidth * math.sin(deg * math.pi / 180.0)

            my_oled.line(middleX, middleY, middleX + xEnd, middleY + yEnd)
            my_oled.display()
            qwiic_i2c.delay_ms(50)

        for deg in range(0, 360, 15):

            xEnd = lineWidth * math.cos(deg * math.pi / 180.0)
            yEnd = lineWidth * math.sin(deg * math.pi / 180.0)

            my_oled.line(middleX, middleY, middleX + xEnd, middleY + yEnd, my_oled.BLACK, my_oled.NORM)
            my_oled.display()
            qwiic_i2c.delay_ms(50)
#-------------------------------------------------------------------
def shape_example(my_oled):

    print("Shapes!")

    # Silly pong demo. It takes a lot of work to fake pong...
    paddleW = 3  # Paddle width
    paddleH = 15  # Paddle height

    lWidth = my_oled.get_lcd_width()
    lHeight = my_oled.get_lcd_height()

    # Paddle 0 (left) position coordinates
    paddle0_Y = (lHeight // 2) - (paddleH // 2)
    paddle0_X = 2

    # Paddle 1 (right) position coordinates
    paddle1_Y = (lHeight // 2) - (paddleH // 2)
    paddle1_X = lWidth - 3 - paddleW

    ball_rad = 2  #Ball radius
    # // Ball position coordinates
    ball_X = paddle0_X + paddleW + ball_rad
    ball_Y = randint(1 + ball_rad, lHeight - ball_rad) #paddle0_Y + ball_rad
    ballVelocityX = 1  # Ball left/right velocity
    ballVelocityY = 1  # Ball up/down velocity
    paddle0Velocity = -1  # Paddle 0 velocity
    paddle1Velocity = 1  # Paddle 1 velocity


    while (ball_X - ball_rad > 1) and (ball_X + ball_rad < lWidth - 2):

        # // Increment ball's position
        ball_X += ballVelocityX
        ball_Y += ballVelocityY
        # // Check if the ball is colliding with the left paddle
        if ball_X - ball_rad < paddle0_X + paddleW:

            # // Check if ball is within paddle's height
            if (ball_Y > paddle0_Y)  and (ball_Y < paddle0_Y + paddleH):

                ball_X +=1  # Move ball over one to the right
                ballVelocityX = -ballVelocityX # Change velocity

        # Check if the ball hit the right paddle
        if ball_X + ball_rad > paddle1_X:

            # Check if ball is within paddle's height
            if (ball_Y > paddle1_Y) and (ball_Y < paddle1_Y + paddleH):

                ball_X -= 1  # Move ball over one to the left
                ballVelocityX = -ballVelocityX # change velocity

        # // Check if the ball hit the top or bottom
        if (ball_Y <= ball_rad) or (ball_Y >= (lHeight - ball_rad - 1)):

            # Change up/down velocity direction
            ballVelocityY = -ballVelocityY

        # // Move the paddles up and down
        paddle0_Y += paddle0Velocity
        paddle1_Y += paddle1Velocity

        # // Change paddle 0's direction if it hit top/bottom
        if (paddle0_Y <= 1) or (paddle0_Y > lHeight - 2 - paddleH):

            paddle0Velocity = -paddle0Velocity

        # // Change paddle 1's direction if it hit top/bottom
        if (paddle1_Y <= 1) or (paddle1_Y > lHeight - 2 - paddleH):

            paddle1Velocity = -paddle1Velocity

        # Draw the Pong Field
        my_oled.clear(my_oled.PAGE)  # Clear the page

        # Draw an outline of the screen:
        my_oled.rect(0, 0, lWidth - 1, lHeight)

        # Draw the center line
        my_oled.rect_fill(lWidth//2 - 1, 0, 2, lHeight)

        # Draw the Paddles:
        my_oled.rect_fill(paddle0_X, paddle0_Y, paddleW, paddleH)
        my_oled.rect_fill(paddle1_X, paddle1_Y, paddleW, paddleH)

        # # Draw the ball:
        my_oled.circle(ball_X, ball_Y, ball_rad)

        # Actually draw everything on the screen:
        my_oled.display()
        qwiic_i2c.delay_ms(10)  # Delay for visibility

    qwiic_i2c.delay_ms(200)

def show_done(my_oled):
    my_oled.set_font_type(1)
    my_oled.clear(my_oled.PAGE)
    my_oled.set_cursor(0, 0)
    my_oled.print("DONE!")
    my_oled.display()
    qwiic_i2c.delay_ms(1000)

#-------------------------------------------------------------------
def text_examples(my_oled):

    print("Text!")

    # Demonstrate font 0. 5x8 font
    my_oled.clear(my_oled.PAGE)     # Clear the screen
    my_oled.set_font_type(0)  # Set font to type 0
    my_oled.set_cursor(0, 0) # Set cursor to top-left
    # There are 255 possible characters in the font 0 type.
    # Lets run through all of them and print them out!
    for i in range(256):

        # You can write byte values and they'll be mapped to
        # their ASCII equivalent character.
        my_oled.write(i)  # Write a byte out as a character
        my_oled.display() # Draw on the screen
        # qwiic_i2c.delay_ms(50)

        # We can only display 60 font 0 characters at a time.
        # Every 60 characters, pause for a moment. Then clear
        # the page and start over.
        if (i%60 == 0) and (i != 0):

            qwiic_i2c.delay_ms(100)
            my_oled.clear(my_oled.PAGE)     # Clear the page
            my_oled.set_cursor(0, 0) # Set cursor to top-left

    qwiic_i2c.delay_ms(500) # Wait 500ms before next example

    # Demonstrate font 1. 8x16. Let's use the print function
    # to display every character defined in this font.
    my_oled.set_font_type(1)  # Set font to type 1
    my_oled.clear(my_oled.PAGE)     # Clear the page
    my_oled.set_cursor(0, 0) # Set cursor to top-left
    # Print can be used to print a string to the screen:
    my_oled.print(" !\"#$%&'()*+,-./01234")
    my_oled.display()       # Refresh the display
    qwiic_i2c.delay_ms(1000)

    my_oled.clear(my_oled.PAGE)
    my_oled.set_cursor(0, 0)
    my_oled.print("56789:<=>?@ABCDEFGHI")
    my_oled.display()
    qwiic_i2c.delay_ms(1000)

    my_oled.clear(my_oled.PAGE)
    my_oled.set_cursor(0, 0)
    my_oled.print("JKLMNOPQRSTUVWXYZ[\\]^")
    my_oled.display()
    qwiic_i2c.delay_ms(1000)

    my_oled.clear(my_oled.PAGE)
    my_oled.set_cursor(0, 0)
    my_oled.print("_`abcdefghijklmnopqrs")
    my_oled.display()
    qwiic_i2c.delay_ms(1000)

    my_oled.clear(my_oled.PAGE)
    my_oled.set_cursor(0, 0)
    my_oled.print("tuvwxyz{|}~")
    my_oled.display()
    qwiic_i2c.delay_ms(1000)

    # Demonstrate font 2. 10x16. Only numbers and '.' are defined.
    # This font looks like 7-segment displays.
    # Lets use this big-ish font to display readings from the
    # analog pins.
    for i in range(25):

        my_oled.clear(my_oled.PAGE)            # Clear the display
        my_oled.set_cursor(0, 0)        # Set cursor to top-left
        my_oled.set_font_type(0)         # Smallest font
        my_oled.print("A0: ")          # Print "A0"
        my_oled.set_font_type(2)         # 7-segment font
        my_oled.print("%.3d" % randint(0,255))

        my_oled.set_cursor(0, 16)       # Set cursor to top-middle-left
        my_oled.set_font_type(0)         # Repeat
        my_oled.print("A1: ")
        my_oled.set_font_type(2)

        # Note: For the "narrow" display, we can only fit the above two lines, so A2 will not be seen.
        my_oled.print("%.3d" % randint(0,255))
        my_oled.set_cursor(0, 32)
        my_oled.set_font_type(0)
        my_oled.print("A2: ")
        my_oled.set_font_type(2)
        my_oled.print("%.3d" % randint(0,255))

        my_oled.display()
        qwiic_i2c.delay_ms(100)

    # Demonstrate font 3. 12x48. Stopwatch demo.
    if my_oled.get_lcd_height() < 48:
        # The "narrow" display doesn't have enough height to fully display font 3 or 4 so we'll end the demo here.
        show_done(my_oled)
        return
    
    my_oled.set_font_type(3)  # Use the biggest font
    ms = 0
    s = 0

    while s <= 5:

        my_oled.clear(my_oled.PAGE)     # Clear the display
        my_oled.set_cursor(0, 0) # Set cursor to top-left
        if s < 10:
            my_oled.print("00")   # Print "00" if s is 1 digit
        elif s < 100:
            my_oled.print("0")    # Print "0" if s is 2 digits

        my_oled.print(s)        # Print s's value
        my_oled.print(":")      # Print ":"
        my_oled.print(ms)       # Print ms value
        my_oled.display()       # Draw on the screen
        ms +=1         # Increment ms
        if ms >= 10 : #If ms is >= 10
            ms = 0     # Set ms back to 0
            s +=1        # and increment s

    # Demonstrate font 4. 31x48. Let's use the print function
    # to display some characters defined in this font.
    my_oled.set_font_type(4)  # Set font to type 4
    my_oled.clear(my_oled.PAGE)     #Clear the page
    my_oled.set_cursor(0, 0) #Set cursor to top-left

    # Print can be used to print a string to the screen:
    my_oled.print("OL")
    my_oled.display()       # Refresh the display
    qwiic_i2c.delay_ms(1000)

    my_oled.clear(my_oled.PAGE)
    my_oled.set_cursor(0, 0)
    my_oled.print("ED")
    my_oled.display()
    qwiic_i2c.delay_ms(1000)

    show_done(my_oled)

#-------------------------------------------------------------------

def run_example():
    #  Before you can start using the OLED, call begin() to init
    #  all of the pins and configure the OLED.

    print("\nOLED Display - Everything Example\n")
    my_oled = userOLED

    if not my_oled.is_connected():
        print("The OLED Display isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    my_oled.begin()
    #  clear(ALL) will clear out the OLED's graphic memory.
    #  clear(PAGE) will clear the Arduino's display buffer.
    my_oled.clear(my_oled.ALL)  #  Clear the display's memory (gets rid of artifacts)
    #  To actually draw anything on the display, you must call the
    #  display() function.
    my_oled.display()
    qwiic_i2c.delay_ms(1000)

    my_oled.clear(my_oled.PAGE)

    print("-"*30)
    pixel_example(my_oled)
    print("-"*30)
    line_example(my_oled)
    print("-"*30)
    shape_example(my_oled)
    print("-"*30)
    text_examples(my_oled)
    print("-"*30)
    print("DONE")

#-------------------------------------------------------------------

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding OLED Everything Example")
        sys.exit(0)
