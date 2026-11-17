#!/usr/bin/env python
#-----------------------------------------------------------------------------
# top_phat_button_ex4_pwm.py
#
# Example that shows how to set and get the slow PWM value
#------------------------------------------------------------------------
#
# Written by SparkFun Electronics, November 2023
# 
# This python library supports the SparkFun Electronics qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatible) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2023 SparkFun Electronics
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
# Example 4 - PWM

import qwiic_relay
import time
import sys

# Be sure to initialize your relay with the proper address.
# Note - PWM is only supported for the solid state relays
myRelays = qwiic_relay.QwiicRelay(qwiic_relay.QUAD_RELAY_DEFUALT_ADDR)
# myRelays = qwiic_relay.QwiicRelay(qwiic_relay.QUAD_RELAY_JUMPER_CLOSE_ADDR)
# myRelays = qwiic_relay.QwiicRelay(qwiic_relay.DUAL_SOLID_STATE_RELAY_DEFUALT_ADDR)
# myRelays = qwiic_relay.QwiicRelay(qwiic_relay.DUAL_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR)

def runExample():

    print("\nSparkFun Qwiic Relay Example 4 - PWM\n")

    if myRelays.begin() == False:
        print("The Qwiic Relay isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    # Set PWM on each relay. All relays can be set independently, uncomment
    # lines below to activate them. Note that our range is 0-120 for setting a
    # PWM value as there are only 120 times where the zero crossing relay can
    # switch in one second
    myRelays.set_slow_pwm(1, 30) # 25% duty cycle
    # myRelays.set_slow_pwm(2, 60) # 50% duty cycle
    # myRelays.set_slow_pwm(3, 90) # 75% duty cycle
    # myRelays.set_slow_pwm(4, 120) # 100% duty cycle
    
    # Print the status of all relays
    print("Relay 1 PWM: " + str(myRelays.get_slow_pwm(1)))
    # print("Relay 2 PWM: " + str(myRelays.get_slow_pwm(2)))
    # print("Relay 3 PWM: " + str(myRelays.get_slow_pwm(3)))
    # print("Relay 4 PWM: " + str(myRelays.get_slow_pwm(4)))
    print()

    # Let the slow PWM run for a while
    time.sleep(10)
    
    # Set all relays off 
    myRelays.set_slow_pwm(1, 0)
    # myRelays.set_slow_pwm(2, 0)
    # myRelays.set_slow_pwm(3, 0)
    # myRelays.set_slow_pwm(4, 0)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 4")
        sys.exit(0)