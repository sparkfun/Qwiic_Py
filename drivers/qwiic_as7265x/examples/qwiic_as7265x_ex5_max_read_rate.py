#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_as7265x_ex5_max_read_rate.py
#
# This example shows how to setup the sensor for max, calibrated read rate.
# Printing floats is the greatest bottleneck so we increase it to 115200.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
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
#===============================================================================

import qwiic_as7265x
import sys

def runExample():
    print("\nQwiic Spectral Triad Example 5 - Max Read Rate\n")

    # Create instance of device
    myAS7265x = qwiic_as7265x.QwiicAS7265x()

    # Check if it's connected
    if myAS7265x.is_connected() == False:
        print("The device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    # Initialize the device
    if myAS7265x.begin() == False:
        print("Unable to initialize the AS7265x. Please check your connection", file = sys.stderr)
        return
    
    # All 6 channels on all devices
    myAS7265x.set_measurement_mode(myAS7265x.kMeasurementMode6ChanContinuous)

    # 0 seems to cause the sensors to read very slowly
    # 1 is the fastest
    # 1*2.8ms = 5.6ms per reading
    # But we need two integration cycles so 89Hz is aproximately the fastest read rate
    myAS7265x.set_integration_cycles(1)

    myAS7265x.disable_indicator()

    # Rather than toggle the LEDs with each measurment, turn all on all the time
    myAS7265x.enable_bulb(myAS7265x.kLedWhite)
    myAS7265x.enable_bulb(myAS7265x.kLedIr)
    myAS7265x.enable_bulb(myAS7265x.kLedUv)

    print("A,B,C,D,E,F,G,H,R,I,S,J,T,U,V,W,K,L")

    while True:
        # Must wait two integration cycles to get all values
        while myAS7265x.data_available() == False:
            pass
        
        # Notice that we don't explicitly call take_measurements since we are in continuous mode
        
        print(str(myAS7265x.get_calibrated_a()) + ",", end="")  # 410nm
        print(str(myAS7265x.get_calibrated_b()) + ",", end="")  # 435nm
        print(str(myAS7265x.get_calibrated_c()) + ",", end="")  # 460nm
        print(str(myAS7265x.get_calibrated_d()) + ",", end="")  # 485nm
        print(str(myAS7265x.get_calibrated_e()) + ",", end="")  # 510nm
        print(str(myAS7265x.get_calibrated_f()) + ",", end="")  # 535nm

        print(str(myAS7265x.get_calibrated_g()) + ",", end="")  # 560nm
        print(str(myAS7265x.get_calibrated_h()) + ",", end="")  # 585nm
        print(str(myAS7265x.get_calibrated_r()) + ",", end="")  # 610nm
        print(str(myAS7265x.get_calibrated_i()) + ",", end="")  # 645nm
        print(str(myAS7265x.get_calibrated_s()) + ",", end="")  # 680nm
        print(str(myAS7265x.get_calibrated_j()) + ",", end="")  # 705nm

        print(str(myAS7265x.get_calibrated_t()) + ",", end="")  # 730nm
        print(str(myAS7265x.get_calibrated_u()) + ",", end="")  # 760nm
        print(str(myAS7265x.get_calibrated_v()) + ",", end="")  # 810nm
        print(str(myAS7265x.get_calibrated_w()) + ",", end="")  # 860nm
        print(str(myAS7265x.get_calibrated_k()) + ",", end="")  # 900nm
        print(str(myAS7265x.get_calibrated_l()))  # 940nm	

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)