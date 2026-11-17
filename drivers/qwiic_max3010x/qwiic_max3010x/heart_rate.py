#  Optical Heart Rate Detection (PBA Algorithm)
#
#  By: Pete Lewis
#  SparkFun Electronics
#  Date: May 20th, 2020
#
#  Ported to Python from a previous CPP version
#  By: Nathan Seidle
#  SparkFun Electronics
#  Date: October 2nd, 2016
#
#  Given a series of IR samples from the MAX30105 we discern when a heart beat is occurring
#
#  Let's have a brief chat about what this code does. We're going to try to detect
#  heart-rate optically. This is tricky and prone to give false readings. We really don't
#  want to get anyone hurt so use this code only as an example of how to process optical
#  data. Build fun stuff with our MAX30105 breakout board but don't use it for actual
#  medical diagnosis.
#
#  Excellent background on optical heart rate detection:
#  http:#www.ti.com/lit/an/slaa655/slaa655.pdf
#
#  Good reading:
#  http:#www.techforfuture.nl/fjc_documents/mitrabaratchi-measuringheartratewithopticalsensor.pdf
#  https:#fruct.org/publications/fruct13/files/Lau.pdf
#
#  This is an implementation of Maxim's PBA (Penpheral Beat Amplitude) algorithm. It's been 
#  converted to work within the Arduino framework, and then to Python.
#
#
# Copyright (C) 2016 Maxim Integrated Products, Inc., All Rights Reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL MAXIM INTEGRATED BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# Except as contained in this notice, the name of Maxim Integrated
# Products, Inc. shall not be used except as stated in the Maxim Integrated
# Products, Inc. Branding Policy.
# 
# The mere transfer of this software does not imply any licenses
# of trade secrets, proprietary technology, copyrights, patents,
# trademarks, maskwork rights, or any other form of intellectual
# property whatsoever. Maxim Integrated Products, Inc. retains all
# ownership rights.
#  
# 

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class HeartRate(object):
    """
    HeartRate
    
        :return: The Heart Beat device object.
        :rtype: Object
    """
    def __init__(self):
        
        self.IR_AC_Max = 20
        self.IR_AC_Min = -20

        self.IR_AC_Signal_Current = 0
        self.IR_AC_Signal_Previous = 0
        self.IR_AC_Signal_min = 0
        self.IR_AC_Signal_max = 0
        self.IR_Average_Estimated = 0

        self.positiveEdge = 0
        self.negativeEdge = 0
        self.ir_avg_reg = 0

        self.cbuff = list(range(32))
        self.offset = 0

        self.FIRCoeffs = [172, 321, 579, 927, 1360, 1858, 2390, 2916, 3391, 3768, 4012, 4096]

    # Average DC Estimator
    def averageDCEstimator(self,p, x):
        self.ir_avg_reg = p
        self.ir_avg_reg += ( ( (x << 15) - self.ir_avg_reg) >> 4)
        return (self.ir_avg_reg >> 15)

    # Integer multiplier
    def mul16(self,x, y):
        return (x * y)
        
    # Low Pass FIR Filter
    def lowPassFIRFilter(self,din):
        
        self.cbuff[self.offset] = din

        z = self.mul16(self.FIRCoeffs[11], self.cbuff[(self.offset - 11) & 0x1F])
      
        for i in range(0,11):
            z += self.mul16(self.FIRCoeffs[i], self.cbuff[(self.offset - i) & 0x1F] + self.cbuff[(self.offset - 22 + i) & 0x1F])

        self.offset += 1
        self.offset %= 32 #Wrap condition

        return (z >> 15)

    def getDCE(self):
        return self.IR_Average_Estimated

    #  Heart Rate Monitor functions takes a sample value
    #  Returns True if a beat is detected
    #  A running average of four samples is recommended for display on the screen.
    def checkForBeat(self, sample):
        beatDetected = False
        
        #  Save current state
        self.IR_AC_Signal_Previous = self.IR_AC_Signal_Current
      
        #This is good to view for debugging
        #Serial.print("Signal_Current: ")
        #Serial.println(self.IR_AC_Signal_Current)

        # Process next data sample
        self.IR_Average_Estimated = self.averageDCEstimator(self.ir_avg_reg, sample)
        self.IR_AC_Signal_Current = self.lowPassFIRFilter(sample - self.IR_Average_Estimated)

        # Detect positive zero crossing (rising edge)
        if ((self.IR_AC_Signal_Previous < 0) & (self.IR_AC_Signal_Current >= 0)):
            self.IR_AC_Max = self.IR_AC_Signal_max #Adjust our AC max and min
            self.IR_AC_Min = self.IR_AC_Signal_min

            self.positiveEdge = 1
            self.negativeEdge = 0
            self.IR_AC_Signal_max = 0

            #if ((self.IR_AC_Max - self.IR_AC_Min) > 100 & (self.IR_AC_Max - self.IR_AC_Min) < 1000)
            if ((self.IR_AC_Max - self.IR_AC_Min) > 20 & (self.IR_AC_Max - self.IR_AC_Min) < 1000):
                #Heart beat!!!
                beatDetected = True

        # Detect negative zero crossing (falling edge)
        if ((self.IR_AC_Signal_Previous > 0) & (self.IR_AC_Signal_Current <= 0)):
            self.positiveEdge = 0
            self.negativeEdge = 1
            self.IR_AC_Signal_min = 0

        # Find Maximum value in positive cycle
        if (self.positiveEdge & (self.IR_AC_Signal_Current > self.IR_AC_Signal_Previous)):
            self.IR_AC_Signal_max = self.IR_AC_Signal_Current

        # Find Minimum value in negative cycle
        if (self.negativeEdge & (self.IR_AC_Signal_Current < self.IR_AC_Signal_Previous)):
            self.IR_AC_Signal_min = self.IR_AC_Signal_Current
      
        return beatDetected
