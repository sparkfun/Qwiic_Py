# !/usr/bin/env python
# ---------------------------------------------------------------------------------
# qwiic_led_stick_ex10_change_address.py
#
# This example changes the address of the LED stick and shows the results by writing
# the whole strip white. Address will not reset on restart. Change the address back 
# to default with my_stick.change_address(0x23).
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
# Example 10

import qwiic_led_stick
import time
import sys

def run_example():
    # Change this to whatever the i2c address currently is
    old_address = qwiic_led_stick._QWIIC_LED_STICK_DEFAULT_ADDRESS

    print("\nSparkFun Qwiic LED Stick Example 10")
    my_stick = qwiic_led_stick.QwiicLEDStick(old_address)

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")

    print("\nEnter a new I2C address for the Qwiic LED Stick to use.")
    print("\nDon't use the 0x prefix. For instance, if you wanted to")
    print("\nchange the address to 0x5B, you would type 5B and hit enter.")

    new_address = input("\nNew address: ")
    new_address = int(new_address, 16)

    # Check if the user entered a valid address
    if new_address > 0x08 and new_address < 0x77:
        print("\nCharacters received and new address is valid!")
        print("\nAttempting to set Qwiic LED Stick address...")

        if my_stick.change_address(new_address) == True:
            print("\nAddress successfully changed!")
        # Check that the Qwiic LED Stick acknowledges on the new address
        time.sleep(0.02)
        if my_stick.begin() == False:
            print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        else:
            print("\nLED Stick acknowledged on new address!")
    else:
        print("\nAddress entered not a valid I2C address.")

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 10")
        sys.exit(0)
