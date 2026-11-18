# !/usr/bin/env python
# ---------------------------------------------------------------------------------
# qwiic_led_stick_ex7_cycle_rainbow.py
#
# This example ake the LED Stick smoothly change through the colors of the rainbow.
# --------------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
# 
# This python library supports the SpakrFun Electronics qwiic sensor/
# board ecosystem on a Raspberry Pi (and compatible) board computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun by buying a board!
#
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
# Example 7

import qwiic_led_stick
import qwiic_i2c
import sys

def cycle_rainbow(led_stick, delay_ms):
    # Red to yellow
    for g in range(0, 255):
        led_stick.set_all_led_color(255, g, 0)
        qwiic_i2c.delay_ms(delay_ms)
    
    # Yellow to green
    for r in range(255, 0, -1):
        led_stick.set_all_led_color(r, 255, 0)
        qwiic_i2c.delay_ms(delay_ms)
    
    # Green to cyan
    for b in range(0, 255):
        led_stick.set_all_led_color(0, 255, b)
        qwiic_i2c.delay_ms(delay_ms)
    
    # Cyan to blue
    for g in range(255, 0, -1):
        led_stick.set_all_led_color(0, g, 255)
        qwiic_i2c.delay_ms(delay_ms)
    
    # Blue to magenta
    for r in range(0, 255):
        led_stick.set_all_led_color(r, 0, 255)
        qwiic_i2c.delay_ms(delay_ms)
    
    # Magenta to red
    for b in range(255, 0, -1):
        led_stick.set_all_led_color(255, 0, b)
        qwiic_i2c.delay_ms(delay_ms)


print("\nSparkFun Qwiic LED Stick Example 7")
my_stick = qwiic_led_stick.QwiicLEDStick()

if my_stick.begin() == False:
    print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    sys.exit(1)
print("\nLED Stick ready!")

while True:
    cycle_rainbow(my_stick, 10)
