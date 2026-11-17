#!/usr/bin/env python
#-----------------------------------------------------------------------------
# top_phat_button_ex2.py
#
# Interrupt example for the Top pHAT Buttons
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, April 2020
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
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
# Example 2
#

from __future__ import print_function
import top_phat_button
import time
import sys
import RPi.GPIO as GPIO

INTERRUPT_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(INTERRUPT_PIN, GPIO.IN)

myButtons = top_phat_button.ToppHATButton()

def interruptCallback(channel):
    myButtons.button_pressed
    myButtons.button_clicked #Both interrupts are configured, so we need to read both registers to clear the interrupt and update our button data.   
    if myButtons.a_pressed == True:
        print("A Pressed")
    if myButtons.a_clicked == True:
        print("A Released")
    if myButtons.b_pressed == True:
        print("B Pressed")
    if myButtons.b_clicked == True:
        print("B Released")
    if myButtons.up_pressed == True:
        print("Up Pressed")
    if myButtons.up_clicked == True:
        print("Up Released")
    if myButtons.down_pressed == True:
        print("Down Pressed")
    if myButtons.down_clicked == True:
        print("Down Released")
    if myButtons.left_pressed == True:
        print("Left Pressed")
    if myButtons.left_clicked == True:
        print("Left Released")
    if myButtons.right_pressed == True:
        print("Right Pressed")
    if myButtons.right_clicked == True:
        print("Right Released")
    if myButtons.center_pressed == True:
        print("Center Pressed")
    if myButtons.center_clicked == True:
        print("Center Released")
    
GPIO.add_event_detect(INTERRUPT_PIN, GPIO.FALLING, callback=interruptCallback, bouncetime=5)

def runExample():

    print("\nSparkFun Top pHAT Button  Example 1\n")

    if myButtons.is_connected() == False:
        print("The Top pHAT Button device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
       
    myButtons.pressed_interrupt_enable = True
    myButtons.clicked_interrupt_enable = True #Enable both hardware interrupts
  
    while True:
        
        time.sleep(.1)


if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)


