#----------------------------------------------------------------------------------
# qwiic_max3010x.py
#
# Python library for the MAX3010x Particle Sensor
#
#----------------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2020
# Original Arduino Library written by Peter Jansen and Nathan Seidle (SparkFun)
# BSD license, all atribution text must be included in any redistribution.
# 
# These sensors use I2C to communicate, as well as a single (optional)
# interrupt line that is not currently supported in this driver.
#
# This python library supports the SparkFun Electroncis qwiic
# qwiic sensor/board ecosystem
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
# This sensor can easily protyped using the following:
# SparkFun Particle Sensor Breakout - MAX30101 (Qwiic)
# https://www.sparkfun.com/products/16474
# 
#==================================================================================
# Copyright (c) 2020 SparkFun Electronics
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
# pylint: disable=line-too-long, too-many-public-methods, invalid-name
#

"""!
qwiic_max3010x
============
Python module for the MAX3010x sensor as found on the [SparkFun Particle Sensor Breakout - MAX30101 (Qwiic)](https://www.sparkfun.com/products/16474)

This python package is a port of the existing [SparkFun MAX3010x Sensor Arduino Library](https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library)

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
_DEFAULT_NAME = "Qwiic MAX3010x"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x57] # 7-bit I2C Address
# Note that MAX30102 has the same I2C address and Part ID

# Status Registers
MAX30105_INTSTAT1 =		0x00 
MAX30105_INTSTAT2 =		0x01 
MAX30105_INTENABLE1 =		0x02 
MAX30105_INTENABLE2 =		0x03 

# FIFO Registers
MAX30105_FIFOWRITEPTR = 	0x04 
MAX30105_FIFOOVERFLOW = 	0x05 
MAX30105_FIFOREADPTR = 	0x06 
MAX30105_FIFODATA =		0x07 

# Configuration Registers
MAX30105_FIFOCONFIG = 		0x08 
MAX30105_MODECONFIG = 		0x09 
MAX30105_PARTICLECONFIG = 	0x0A     # Note, sometimes listed as "SPO2" config in datasheet (pg. 11)
MAX30105_LED1_PULSEAMP = 	0x0C 
MAX30105_LED2_PULSEAMP = 	0x0D 
MAX30105_LED3_PULSEAMP = 	0x0E 
MAX30105_LED_PROX_AMP = 	0x10 
MAX30105_MULTILEDCONFIG1 = 0x11 
MAX30105_MULTILEDCONFIG2 = 0x12 

# Die Temperature Registers
MAX30105_DIETEMPINT = 		0x1F 
MAX30105_DIETEMPFRAC = 	0x20 
MAX30105_DIETEMPCONFIG = 	0x21 

# Proximity Function Registers
MAX30105_PROXINTTHRESH = 	0x30 

# Part ID Registers
MAX30105_REVISIONID = 		0xFE 
MAX30105_PARTID = 			0xFF     # Should always be 0x15. Identical to MAX30102.

# MAX30105 Commands
# Interrupt configuration (pg 13, 14)
MAX30105_INT_A_FULL_MASK =		(~0b10000000)
MAX30105_INT_A_FULL_ENABLE = 	0x80 
MAX30105_INT_A_FULL_DISABLE = 	0x00 

MAX30105_INT_DATA_RDY_MASK = (~0b01000000)
MAX30105_INT_DATA_RDY_ENABLE =	0x40 
MAX30105_INT_DATA_RDY_DISABLE = 0x00 

MAX30105_INT_ALC_OVF_MASK = (~0b00100000)
MAX30105_INT_ALC_OVF_ENABLE = 	0x20 
MAX30105_INT_ALC_OVF_DISABLE = 0x00 

MAX30105_INT_PROX_INT_MASK = (~0b00010000)
MAX30105_INT_PROX_INT_ENABLE = 0x10 
MAX30105_INT_PROX_INT_DISABLE = 0x00 

MAX30105_INT_DIE_TEMP_RDY_MASK = (~0b00000010)
MAX30105_INT_DIE_TEMP_RDY_ENABLE = 0x02 
MAX30105_INT_DIE_TEMP_RDY_DISABLE = 0x00 

MAX30105_SAMPLEAVG_MASK =	(~0b11100000)
MAX30105_SAMPLEAVG_1 = 	0x00 
MAX30105_SAMPLEAVG_2 = 	0x20 
MAX30105_SAMPLEAVG_4 = 	0x40 
MAX30105_SAMPLEAVG_8 = 	0x60 
MAX30105_SAMPLEAVG_16 = 	0x80 
MAX30105_SAMPLEAVG_32 = 	0xA0 

MAX30105_ROLLOVER_MASK = 	0xEF 
MAX30105_ROLLOVER_ENABLE = 0x10 
MAX30105_ROLLOVER_DISABLE = 0x00 

MAX30105_A_FULL_MASK = 	0xF0 

# Mode configuration commands (page 19)
MAX30105_SHUTDOWN_MASK = 	0x7F 
MAX30105_SHUTDOWN = 		0x80 
MAX30105_WAKEUP = 			0x00 

MAX30105_RESET_MASK = 		0xBF 
MAX30105_RESET = 			0x40 

MAX30105_MODE_MASK = 		0xF8 
MAX30105_MODE_REDONLY = 	0x02 
MAX30105_MODE_REDIRONLY = 	0x03 
MAX30105_MODE_MULTILED = 	0x07 

# Particle sensing configuration commands (pgs 19-20)
MAX30105_ADCRANGE_MASK = 	0x9F 
MAX30105_ADCRANGE_2048 = 	0x00 
MAX30105_ADCRANGE_4096 = 	0x20 
MAX30105_ADCRANGE_8192 = 	0x40 
MAX30105_ADCRANGE_16384 = 	0x60 

MAX30105_SAMPLERATE_MASK = 0xE3 
MAX30105_SAMPLERATE_50 = 	0x00 
MAX30105_SAMPLERATE_100 = 	0x04 
MAX30105_SAMPLERATE_200 = 	0x08 
MAX30105_SAMPLERATE_400 = 	0x0C 
MAX30105_SAMPLERATE_800 = 	0x10 
MAX30105_SAMPLERATE_1000 = 0x14 
MAX30105_SAMPLERATE_1600 = 0x18 
MAX30105_SAMPLERATE_3200 = 0x1C 

MAX30105_PULSEWIDTH_MASK = 0xFC 
MAX30105_PULSEWIDTH_69 = 	0x00 
MAX30105_PULSEWIDTH_118 = 	0x01 
MAX30105_PULSEWIDTH_215 = 	0x02 
MAX30105_PULSEWIDTH_411 = 	0x03 

#Multi-LED Mode configuration (pg 22)
MAX30105_SLOT1_MASK = 		0xF8 
MAX30105_SLOT2_MASK = 		0x8F 
MAX30105_SLOT3_MASK = 		0xF8 
MAX30105_SLOT4_MASK = 		0x8F 

SLOT_NONE = 				0x00 
SLOT_RED_LED = 			0x01 
SLOT_IR_LED = 				0x02 
SLOT_GREEN_LED = 			0x03 
SLOT_NONE_PILOT = 			0x04 
SLOT_RED_PILOT =			0x05 
SLOT_IR_PILOT = 			0x06 
SLOT_GREEN_PILOT = 		0x07 

MAX_30105_EXPECTEDPARTID = 0x15

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

#-----------------------------------------------------------------------------
# Heart rate detection (formerly heart_rate.py)
#-----------------------------------------------------------------------------
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

class HeartRate(object):
    """
    HeartRate
    
        :return: The Heart Beat device object.
        :rtype: Object
    """
    def __init__(self):
        
        self.ir_ac_max = 20
        self.ir_ac_min = -20

        self.ir_ac_signal_current = 0
        self.ir_ac_signal_previous = 0
        self.ir_ac_signal_min = 0
        self.ir_ac_signal_max = 0
        self.ir_average_estimated = 0

        self.positive_edge = 0
        self.negative_edge = 0
        self.ir_avg_reg = 0

        self.cbuff = list(range(32))
        self.offset = 0

        self.fir_coeffs = [172, 321, 579, 927, 1360, 1858, 2390, 2916, 3391, 3768, 4012, 4096]

    # Average DC Estimator
    def average_dc_estimator(self,p, x):
        self.ir_avg_reg = p
        self.ir_avg_reg += ( ( (x << 15) - self.ir_avg_reg) >> 4)
        return (self.ir_avg_reg >> 15)

    # Integer multiplier
    def mul16(self,x, y):
        return (x * y)
        
    # Low Pass FIR Filter
    def low_pass_fir_filter(self,din):
        
        self.cbuff[self.offset] = din

        z = self.mul16(self.fir_coeffs[11], self.cbuff[(self.offset - 11) & 0x1F])
      
        for i in range(0,11):
            z += self.mul16(self.fir_coeffs[i], self.cbuff[(self.offset - i) & 0x1F] + self.cbuff[(self.offset - 22 + i) & 0x1F])

        self.offset += 1
        self.offset %= 32 #Wrap condition

        return (z >> 15)

    def get_dce(self):
        return self.ir_average_estimated

    #  Heart Rate Monitor functions takes a sample value
    #  Returns True if a beat is detected
    #  A running average of four samples is recommended for display on the screen.
    def check_for_beat(self, sample):
        beat_detected = False
        
        #  Save current state
        self.ir_ac_signal_previous = self.ir_ac_signal_current
      
        #This is good to view for debugging
        #Serial.print("Signal_Current: ")
        #Serial.println(self.ir_ac_signal_current)

        # Process next data sample
        self.ir_average_estimated = self.average_dc_estimator(self.ir_avg_reg, sample)
        self.ir_ac_signal_current = self.low_pass_fir_filter(sample - self.ir_average_estimated)

        # Detect positive zero crossing (rising edge)
        if ((self.ir_ac_signal_previous < 0) & (self.ir_ac_signal_current >= 0)):
            self.ir_ac_max = self.ir_ac_signal_max #Adjust our AC max and min
            self.ir_ac_min = self.ir_ac_signal_min

            self.positive_edge = 1
            self.negative_edge = 0
            self.ir_ac_signal_max = 0

            #if ((self.ir_ac_max - self.ir_ac_min) > 100 & (self.ir_ac_max - self.ir_ac_min) < 1000)
            if ((self.ir_ac_max - self.ir_ac_min) > 20 & (self.ir_ac_max - self.ir_ac_min) < 1000):
                #Heart beat!!!
                beat_detected = True

        # Detect negative zero crossing (falling edge)
        if ((self.ir_ac_signal_previous > 0) & (self.ir_ac_signal_current <= 0)):
            self.positive_edge = 0
            self.negative_edge = 1
            self.ir_ac_signal_min = 0

        # Find Maximum value in positive cycle
        if (self.positive_edge & (self.ir_ac_signal_current > self.ir_ac_signal_previous)):
            self.ir_ac_signal_max = self.ir_ac_signal_current

        # Find Minimum value in negative cycle
        if (self.negative_edge & (self.ir_ac_signal_current < self.ir_ac_signal_previous)):
            self.ir_ac_signal_min = self.ir_ac_signal_current
      
        return beat_detected

hr = HeartRate()


class QwiicMAX3010x(object):
    """!
    QwiicMAX3010x

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.

    @return The QwiicMAX3010x device object.
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS
    
    # active_leds is the number of channels turned on, and can be 1 to 3. 2 is common for Red+IR.
    active_leds = 0 # Gets set during setup. Allows check() to calculate how many bytes to read from FIFO
    
    # Storage size
    # (This is "left over" from the arduino library, but needed for rollovers) 
    # Each long is 4 bytes so limit this to fit on your micro
    STORAGE_SIZE = 4

    # Circular buffer of readings from the sensor
    red = [0,0,0,0] # place holders to make this list 4 spaces long (to mimic previous struct arrays in arduino library)
    ir = [0,0,0,0]
    green = [0,0,0,0]
    head = 0
    tail = 0

    read_pointer = 0
    write_pointer = 0
    number_of_samples = 0

    # Constructor

    def __init__(self, address=None, i2c_bus=None):

        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """!
        Determine if a device is connected to the system.

        @return **bool** True if the device is connected, otherwise False.
        """
        return self._i2c.is_device_connected(self.address)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.

    def begin(self):
        """!
        Initialize the operation of the Qwiic MAX3010x module

        @return **bool** Returns true of the initializtion was successful, otherwise False.
        """

        # Basically return True if we are connected...

        return self.is_connected()

    # ----------------------------------
    # bit_mask()
    #
    # Given a register, read it, mask it, and then set the thing

    def bit_mask(self, reg, mask, thing):
        """!
        Given a register, read it, mask it, and then set the thing

        @param reg: the register you'd like to effect
        @param mask: the mask needed to zero-out the portion of the register we're interested in
        @param thing: the thing we are affecting aka the control bits of the register

        @return **bool** Returns true of the register write was successful, otherwise False.
        """

        # Grab current register context, store it in local variable "temp_reg"
        temp_reg = self._i2c.read_byte(self.address, reg)

        # Zero-out the portions of the register we're interested in
        temp_reg &= mask

        # Change contents
        temp_reg |= thing

        return self._i2c.write_byte(self.address, reg, temp_reg)

    # ----------------------------------
    # millis()
    #
    # Returns the current time in milliseconds

    def millis(self):

        """!
        Returns a millisecond counter for measuring intervals. It may wrap, so
            compare values with qwiic_i2c.ticks_diff().

        @return **int** Millisecond counter
        """        
        return self._i2c.ticks_ms()

    # ----------------------------------
    # soft_reset()
    #
    # Command a soft reset

    def soft_reset(self):
        """!
        Command a soft reset

        @return **bool** Returns true of the soft reset was successful, otherwise False.
        """
        self.bit_mask(MAX30105_MODECONFIG, MAX30105_RESET_MASK, MAX30105_RESET)

        # Poll for bit to clear, reset is then complete
        # Timeout after 100ms
        timeout = 100
        while (timeout):
            response = self._i2c.read_byte(self.address, MAX30105_MODECONFIG)
            if ((response & MAX30105_RESET) == 0):
                return True # We're done!
            self._i2c.delay_ms(1) # Let's not over burden the I2C bus
            timeout -= 1
        return False # soft reset failure

    # 
    #  Configuration
    # 

    # Begin Interrupt configuration

    # ----------------------------------
    # get_int1()
    #
    # Returns the value of the INTSTAT1 Register

    def get_int1(self):
        """!
        Returns the value of the INTSTAT1 Register

        @return **integer** value of the INTSTAT1 Register
        """
        return self._i2c.read_byte(self.address, MAX30105_INTSTAT1)

    # ----------------------------------
    # get_int2()
    #
    # Returns the value of the INTSTAT2 Register

    def get_int2(self):
        """!
        Returns the value of the INTSTAT2 Register

        @return **integer** value of the INTSTAT2 Register
        """
        return self._i2c.read_byte(self.address, MAX30105_INTSTAT2)

    # ----------------------------------
    # enable_afull()
    #
    # Enable AFULL Interrupt

    def enable_afull(self):
        """!
        Enable AFULL Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_A_FULL_MASK, MAX30105_INT_A_FULL_ENABLE)

    # ----------------------------------
    # disable_afull()
    #
    # Disable AFULL Interrupt

    def disable_afull(self):
        """!
        Disable AFULL Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_A_FULL_MASK, MAX30105_INT_A_FULL_DISABLE)

    # ----------------------------------
    # enable_datardy()
    #
    # Enable DATARDY Interrupt

    def enable_datardy(self):
        """!
        Enable DATARDY Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_DATA_RDY_MASK, MAX30105_INT_DATA_RDY_ENABLE)

    # ----------------------------------
    # disable_datardy()
    #
    # Disable DATARDY Interrupt

    def disable_datardy(self):
        """!
        Disable DATARDY Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_DATA_RDY_MASK, MAX30105_INT_DATA_RDY_DISABLE)

    # ----------------------------------
    # enable_alcovf()
    #
    # Enable ALCOVF Interrupt

    def enable_alcovf(self):
        """!
        Enable ALCOVF Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_ALC_OVF_MASK, MAX30105_INT_ALC_OVF_ENABLE)

    # ----------------------------------
    # disable_alcovf()
    #
    # Disable ALCOVF Interrupt

    def disable_alcovf(self):
        """!
        Disable ALCOVF Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_ALC_OVF_MASK, MAX30105_INT_ALC_OVF_DISABLE)

    # ----------------------------------
    # enable_proxint()
    #
    # Enable PROXINT Interrupt

    def enable_proxint(self):
        """!
        Enable PROXINT Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_PROX_INT_MASK, MAX30105_INT_PROX_INT_ENABLE)

    # ----------------------------------
    # disable_proxint()
    #
    # Disable PROXINT Interrupt

    def disable_proxint(self):
        """!
        Disable PROXINT Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_PROX_INT_MASK, MAX30105_INT_PROX_INT_DISABLE)

    # ----------------------------------
    # enable_dietemprdy()
    #
    # Enable DIETEMPRDY Interrupt

    def enable_dietemprdy(self):
        """!
        Enable DIETEMPRDY Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE2, MAX30105_INT_DIE_TEMP_RDY_MASK, MAX30105_INT_DIE_TEMP_RDY_ENABLE)

    # ----------------------------------
    # disable_dietemprdy()
    #
    # Disable DIETEMPRDY Interrupt

    def disable_dietemprdy(self):
        """!
        Disable DIETEMPRDY Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE2, MAX30105_INT_DIE_TEMP_RDY_MASK, MAX30105_INT_DIE_TEMP_RDY_DISABLE)

    # End Interrupt configuration        

    # ----------------------------------
    # shut_down()
    #
    # Put IC into low power mode (datasheet pg. 19)
    # During shutdown the IC will continue to respond to I2C commands but will
    # not update with or take new readings (such as temperature)

    def shut_down(self):
        """!
        Put IC into low power mode

        @return no return value
        """
        self.bit_mask(MAX30105_MODECONFIG, MAX30105_SHUTDOWN_MASK, MAX30105_SHUTDOWN)

    # ----------------------------------
    # wake_up()
    #
    # Pull IC out of low power mode (datasheet pg. 19)

    def wake_up(self):
        """!
        Pull IC out of low power mode

        @return no return value
        """
        self.bit_mask(MAX30105_MODECONFIG, MAX30105_SHUTDOWN_MASK, MAX30105_WAKEUP)

    # ----------------------------------
    # set_led_mode()
    #
    # Set which LEDs are used for sampling - Red only, RED+IR only, or custom.
    # See datasheet, page 19

    def set_led_mode(self, mode):
        """!
        Set which LEDs are used for sampling - Red only, RED+IR only, or custom

        @param mode: Red only, RED+IR only, or custom

        @return no return value
        """
        self.bit_mask(MAX30105_MODECONFIG, MAX30105_MODE_MASK, mode)

    # ----------------------------------
    # set_adc_range()
    #
    # Set adc_range: one of MAX30105_ADCRANGE_2048, _4096, _8192, _16384

    def set_adc_range(self, adc_range):
        """!
        Set adc_range: one of MAX30105_ADCRANGE_2048, _4096, _8192, _16384

        @param adc_range: MAX30105_ADCRANGE_2048, _4096, _8192, _16384

        @return no return value
        """
        self.bit_mask(MAX30105_PARTICLECONFIG, MAX30105_ADCRANGE_MASK, adc_range)

    # ----------------------------------
    # set_sample_rate()
    #
    # Set sample_rate: one of MAX30105_SAMPLERATE_50, _100, _200, _400, _800, _1000, _1600, _3200

    def set_sample_rate(self, sample_rate):
        """!
        Set sample_rate: one of MAX30105_SAMPLERATE_50, _100, _200, _400, _800, _1000, _1600, _3200

        @param sample_rate: MAX30105_SAMPLERATE_50, _100, _200, _400, _800, _1000, _1600, _3200

        @return no return value
        """
        self.bit_mask(MAX30105_PARTICLECONFIG, MAX30105_SAMPLERATE_MASK, sample_rate)

    # ----------------------------------
    # set_pulse_width()
    #
    # Set pulse_width: one of MAX30105_PULSEWIDTH_69, _188, _215, _411

    def set_pulse_width(self, pulse_width):
        """!
        Set pulse_width: one of MAX30105_PULSEWIDTH_69, _188, _215, _411

        @param pulse_width: MAX30105_PULSEWIDTH_69, _188, _215, _411

        @return no return value
        """
        self.bit_mask(MAX30105_PARTICLECONFIG, MAX30105_PULSEWIDTH_MASK, pulse_width)

    # ----------------------------------
    # set_pulse_amplitude_red()
    #
    # Set pulse amplitude (mA) of red LED
    # 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)
    # See datasheet, page 21

    def set_pulse_amplitude_red(self, amplitude):
        """!
        Set pulse amplitude (mA) of red LED

        @param amplitude: 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)

        @return no return value
        """
        self._i2c.write_byte(self.address, MAX30105_LED1_PULSEAMP, amplitude)

    # ----------------------------------
    # set_pulse_amplitude_ir()
    #
    # Set pulse amplitude (mA) of IR LED
    # 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)
    # See datasheet, page 21

    def set_pulse_amplitude_ir(self, amplitude):
        """!
        Set pulse amplitude (mA) of IR LED

        @param amplitude: 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)

        @return no return value
        """
        self._i2c.write_byte(self.address, MAX30105_LED2_PULSEAMP, amplitude)

    # ----------------------------------
    # set_pulse_amplitude_green()
    #
    # Set pulse amplitude (mA) of green LED
    # 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)
    # See datasheet, page 21

    def set_pulse_amplitude_green(self, amplitude):
        """!
        Set pulse amplitude (mA) of green LED

        @param amplitude: 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)

        @return no return value
        """
        self._i2c.write_byte(self.address, MAX30105_LED3_PULSEAMP, amplitude)

    # ----------------------------------
    # set_pulse_amplitude_proximity()
    #
    # Set pulse aplitude while in proximity mode (only MAX30105)
    # Note, this is specific to the MAX30105, and not included in the MAX30101

    def set_pulse_amplitude_proximity(self, amplitude):
        """!
        Set pulse aplitude while in proximity mode (only MAX30105)
            Note, this is specific to the MAX30105, and not included in the MAX30101

        @param amplitude: amplitude

        @return no return value
        """
        self._i2c.write_byte(self.address, MAX30105_LED_PROX_AMP, amplitude)

    # ----------------------------------
    # set_proximity_threshold()
    #
    # Set the IR ADC count that will trigger the beginning of particle-sensing mode.
    # The thresh_msb signifies only the 8 most significant-bits of the ADC count.
    # Note, this is specific to the MAX30105, and not included in the MAX30101
    # See datasheet, page 24.

    def set_proximity_threshold(self, thresh_msb):
        """!
        Set the IR ADC count that will trigger the beginning of particle-sensing mode.
            The thresh_msb signifies only the 8 most significant-bits of the ADC count.
            Note, this is specific to the MAX30105, and not included in the MAX30101

        @param thresh_msb: threshold of ADC count to cause trigger

        @return no return value
        """
        self._i2c.write_byte(self.address, MAX30105_PROXINTTHRESH, thresh_msb)     

    #
    # enable_slot()
    #
    # Given a slot number assign a thing to it
    # Devices are SLOT_RED_LED or SLOT_RED_PILOT (proximity)
    # Assigning a SLOT_RED_LED will pulse LED
    # Assigning a SLOT_RED_PILOT will ??

    def enable_slot(self, slot_number, device):
        """!
        Given a slot number assign a thing to it
            Devices are SLOT_RED_LED or SLOT_RED_PILOT (proximity)
            Assigning a SLOT_RED_LED will pulse LED
            Assigning a SLOT_RED_PILOT will ??

        @param slot_number: slot number as int 1,2,3,4
        @param device: which device (aka led) you'd like to assign to the given slot

        @return **bool** Whether or not the configuration write was successful
        """
        if slot_number == 1:
            return self.bit_mask(MAX30105_MULTILEDCONFIG1, MAX30105_SLOT1_MASK, device)
        elif slot_number == 2:
            return self.bit_mask(MAX30105_MULTILEDCONFIG1, MAX30105_SLOT2_MASK, device << 4)
        elif slot_number == 3:
            return self.bit_mask(MAX30105_MULTILEDCONFIG2, MAX30105_SLOT3_MASK, device)
        elif slot_number == 4:
            return self.bit_mask(MAX30105_MULTILEDCONFIG2, MAX30105_SLOT4_MASK, device << 4)
        else:
            return False #Shouldn't be here!
  
    #
    # disable_slots()
    # 
    # Clears all slot assignments

    def disable_slots(self):
        """!
        Clears all slot assignments

        @return no return value
        """
        self._i2c.write_byte(self.address, MAX30105_MULTILEDCONFIG1, 0)
        self._i2c.write_byte(self.address, MAX30105_MULTILEDCONFIG2, 0)

    #
    # FIFO Configuration
    #

    # 
    # set_fifo_average()
    #
    # Set sample average (Table 3, Page 18)

    def set_fifo_average(self, number_of_samples):
        """!
        Set sample average

        @param number_of_samples: MAX30105_SAMPLEAVG_1, _2, _4, _8, _16, _32

        @return no return value
        """
        self.bit_mask(MAX30105_FIFOCONFIG, MAX30105_SAMPLEAVG_MASK, number_of_samples)

    #
    # clear_fifo()
    #
    # Resets all points to start in a known state
    # Page 15 recommends clearing FIFO before beginning a read

    def clear_fifo(self):
        """!
        Resets all points to start in a known state

        @return no return value
        """
        self._i2c.write_byte(self.address, MAX30105_FIFOWRITEPTR, 0)
        self._i2c.write_byte(self.address, MAX30105_FIFOOVERFLOW, 0)
        self._i2c.write_byte(self.address, MAX30105_FIFOREADPTR, 0)

    # 
    # enable_fifo_rollover()
    # 
    # Enable roll over if FIFO over flows

    def enable_fifo_rollover(self):
        """!
        Enable roll over if FIFO over flows

        @return no return value
        """
        self.bit_mask(MAX30105_FIFOCONFIG, MAX30105_ROLLOVER_MASK, MAX30105_ROLLOVER_ENABLE)

    # 
    # disable_fifo_rollover()
    # 
    # Disable roll over if FIFO over flows

    def disable_fifo_rollover(self):
        """!
        Disable roll over if FIFO over flows

        @return no return value
        """
        self.bit_mask(MAX30105_FIFOCONFIG, MAX30105_ROLLOVER_MASK, MAX30105_ROLLOVER_DISABLE)

    # 
    # set_fifo_almost_full()
    # 
    # Set number of samples to trigger the almost full interrupt (Page 18)
    # Power on default is 32 samples
    # Note it is reverse: 0x00 is 32 samples, 0x0F is 17 samples

    def set_fifo_almost_full(self, number_of_samples):
        """!
        Set number of samples to trigger the almost full interrupt

        @param number_of_samples: default is 32 samples. Note it's reverse (0x00 is 32 samples, 0x0F is 17 samples)

        @return no return value
        """
        self.bit_mask(MAX30105_FIFOCONFIG, MAX30105_A_FULL_MASK, number_of_samples)

    # 
    # get_write_pointer()
    # 
    # Read the FIFO Write Pointer

    def get_write_pointer(self):
        """!
        Read the FIFO Write Pointer

        @return **integer** FIFO write pointer value
        """
        return self._i2c.read_byte(self.address, MAX30105_FIFOWRITEPTR)

    # 
    # get_read_pointer()
    # 
    # Read the FIFO Read Pointer
    
    def get_read_pointer(self):
        """!
        Read the FIFO Read Pointer

        @return **integer** FIFO read pointer value
        """
        return self._i2c.read_byte(self.address, MAX30105_FIFOREADPTR)

    # ----------------------------------
    # setup()
    #
    # Setup the MAX3010x with default settings

    # Setup the sensor
    # The MAX30105 has many settings. By default we select:
    #  Sample Average = 4
    #  Mode = MultiLED
    #  ADC Range = 16384 (62.5pA per LSB)
    #  Sample rate = 50
    # Use the default setup if you are just getting started with the MAX30105 sensor

    def setup(self, power_level = 0x1F, sample_average = 4, led_mode = 3, sample_rate = 400, pulse_width = 411, adc_range = 4096):
        """!
        Setup the MAX3010x with default or custom settings

        @param power_level: 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA
        @param sample_average: int, 1,2,4,8,16,32, default is 4
        @param led_mode: 1 = RED, 2=RED+IR , 3=RED+IR+GREEN
        @param sample_rate: 0-3200
        @param pulse_width: 0-411 (microseconds)
        @param adc_range: 2048,4096,8192,16384

        @return no return value
        """
        self.soft_reset() # Reset all configuration, threshold, and data registers to POR values

        # FIFO Configuration
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # The chip will average multiple samples of same type together if you wish
        if sample_average == 1:
            self.set_fifo_average(MAX30105_SAMPLEAVG_1) # No averaging per FIFO record
        elif sample_average == 2:
            self.set_fifo_average(MAX30105_SAMPLEAVG_2)
        elif sample_average == 4:
            self.set_fifo_average(MAX30105_SAMPLEAVG_4)
        elif sample_average == 8:
            self.set_fifo_average(MAX30105_SAMPLEAVG_8)
        elif sample_average == 16:
            self.set_fifo_average(MAX30105_SAMPLEAVG_16)
        elif sample_average == 32:
            self.set_fifo_average(MAX30105_SAMPLEAVG_32)
        else:
            self.set_fifo_average(MAX30105_SAMPLEAVG_4)

        # set_fifo_almost_full(2) # Set to 30 samples to trigger an 'Almost Full' interrupt
        self.enable_fifo_rollover() # Allow FIFO to wrap/roll over
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # Mode Configuration
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        if led_mode == 3:
            self.set_led_mode(MAX30105_MODE_MULTILED) # Watch all three LED channels
        elif led_mode == 2:
            self.set_led_mode(MAX30105_MODE_REDIRONLY) # Red and IR
        else:
            self.set_led_mode(MAX30105_MODE_REDONLY) # Red only
        self.active_leds = led_mode # Used to control how many bytes to read from FIFO buffer
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # Particle Sensing Configuration
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        if adc_range < 4096:
            self.set_adc_range(MAX30105_ADCRANGE_2048) # 7.81pA per LSB
        elif adc_range < 8192:
            self.set_adc_range(MAX30105_ADCRANGE_4096) # 15.63pA per LSB
        elif adc_range < 16384:
            self.set_adc_range(MAX30105_ADCRANGE_8192) # 31.25pA per LSB
        elif adc_range == 16384:
            self.set_adc_range(MAX30105_ADCRANGE_16384) # 62.5pA per LSB
        else:
            self.set_adc_range(MAX30105_ADCRANGE_2048)

        if sample_rate < 100:
            self.set_sample_rate(MAX30105_SAMPLERATE_50) # Take 50 samples per second
        elif sample_rate < 200:
            self.set_sample_rate(MAX30105_SAMPLERATE_100)
        elif sample_rate < 400:
            self.set_sample_rate(MAX30105_SAMPLERATE_200)
        elif sample_rate < 800:
            self.set_sample_rate(MAX30105_SAMPLERATE_400)
        elif sample_rate < 1000:
            self.set_sample_rate(MAX30105_SAMPLERATE_800)
        elif sample_rate < 1600:
            self.set_sample_rate(MAX30105_SAMPLERATE_1000)
        elif sample_rate < 3200:
            self.set_sample_rate(MAX30105_SAMPLERATE_1600)
        elif sample_rate == 3200:
            self.set_sample_rate(MAX30105_SAMPLERATE_3200)
        else:
            self.set_sample_rate(MAX30105_SAMPLERATE_50)

        # The longer the pulse width the longer range of detection you'll have
        # At 69us and 0.4mA it's about 2 inches
        # At 411us and 0.4mA it's about 6 inches
        if pulse_width < 118:
            self.set_pulse_width(MAX30105_PULSEWIDTH_69) # Page 26, Gets us 15 bit resolution
        elif pulse_width < 215:
            self.set_pulse_width(MAX30105_PULSEWIDTH_118) # 16 bit resolution
        elif pulse_width < 411:
            self.set_pulse_width(MAX30105_PULSEWIDTH_215) # 17 bit resolution
        elif pulse_width == 411:
            self.set_pulse_width(MAX30105_PULSEWIDTH_411) # 18 bit resolution
        else:
            self.set_pulse_width(MAX30105_PULSEWIDTH_69)
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # LED Pulse Amplitude Configuration
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Default is 0x1F which gets us 6.4mA
        # power_level = 0x02, 0.4mA - Presence detection of ~4 inch
        # power_level = 0x1F, 6.4mA - Presence detection of ~8 inch
        # power_level = 0x7F, 25.4mA - Presence detection of ~8 inch
        # power_level = 0xFF, 50.0mA - Presence detection of ~12 inch

        self.set_pulse_amplitude_red(power_level)
        self.set_pulse_amplitude_ir(power_level)
        self.set_pulse_amplitude_green(power_level)
        self.set_pulse_amplitude_proximity(power_level)
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # Multi-LED Mode Configuration, Enable the reading of the three LEDs
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.enable_slot(1, SLOT_RED_LED)
        if led_mode > 1:
            self.enable_slot(2, SLOT_IR_LED)
        if led_mode > 2:
            self.enable_slot(3, SLOT_GREEN_LED)
        # self.enable_slot(1, SLOT_RED_PILOT)
        # self.enable_slot(2, SLOT_IR_PILOT)
        # self.enable_slot(3, SLOT_GREEN_PILOT)
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        self.clear_fifo() # Reset the FIFO before we begin checking the sensor


    #
    # Data Collection
    #

    # 
    # available()
    # 
    # Tell caller how many samples are available

    def available(self):
        """!
        Tell caller how many samples are available

        @return **integer** number of samples available
        """
        number_of_samples = self.head - self.tail
        if number_of_samples < 0:
            number_of_samples += self.STORAGE_SIZE
        return number_of_samples

    # 
    # next_sample()
    # 
    # Advance the tail

    def next_sample(self):
        """!
        Advance the tail

        @return no return value
        """
        if self.available(): #Only advance the tail if new data is available
            self.tail += 1
            self.tail %= self.STORAGE_SIZE #Wrap condition

    # 
    # check()
    # 
    # Polls the sensor for new data
    # Call regularly
    # If new data is available, it updates the head and tail in the main lists of data
    # Returns number of new samples obtained

    def check(self):
        """!
        Polls the sensor for new data
            Call regularly
            If new data is available, it updates the head and tail in the main lists of data

        @return **integer** number of new samples obtained
        """

        # Read register FIDO_DATA (3-byte * number of active LED)
        # Until FIFO_RD_PTR = FIFO_WR_PTR

        read_pointer = self.get_read_pointer()
        write_pointer = self.get_write_pointer()
        number_of_samples = 0

        #Do we have new data?
        if read_pointer != write_pointer:
            #Calculate the number of samples we need to get from sensor
            number_of_samples = (write_pointer - read_pointer)
            if (number_of_samples < 0):
                number_of_samples += 32 #Wrap condition
                
            #We now have the number of samples, now calc bytes to read
            bytes_to_read = number_of_samples * self.active_leds * 3

            # We may need to read as many as 288 bytes (32 * 3 * 3), but not all
            # platforms can read that much in one go. So we read in blocks until
            # we reach the end.
            max_read_size = 32
            buff = []
            while bytes_to_read > 0:
                # Compute how many bytes we need to read in this loop iteration
                bytes_to_read_this_time = bytes_to_read
                if bytes_to_read_this_time > max_read_size:
                    bytes_to_read_this_time = max_read_size
                
                # Update number of bytes remaining
                bytes_to_read -= bytes_to_read_this_time

                # Read from FIFO and append to buffer
                buff += self._i2c.read_block(self.address, MAX30105_FIFODATA, bytes_to_read_this_time)
            
            # Grab all the bytes we just read into buff, and plug them into the correct local variables.
            # Note, we need to keep track of where we are in the buff (using sample_number and buff_index "i")
            # Also, the bytes in buff will mean different things,
            # according to which LEDs are active (Red, IR, and/or Green)

            # for loop through the entire buff list,
            # using sample_number to "jump" buff_index as necessary to each sample start within buff
            for sample_number in range(0, number_of_samples):
                buff_index = sample_number * self.active_leds * 3 # move index to the start of the next sample
                self.head += 1 # Advance the head of the storage list
                self.head %= self.STORAGE_SIZE # Wrap condition

                # First 3 bytes in buff will always be RED
                temp_byte2 = buff[buff_index+0]
                temp_byte1 = buff[buff_index+1]
                temp_byte0 = buff[buff_index+2]

                #also copy to varaibles for testing
                #self.byte0 = temp_byte0
                #self.byte1 = temp_byte1
                #self.byte2 = temp_byte2

                # Combine bytes into single 32 bit integer variable
                temp_long = 0
                temp_long |= temp_byte0
                temp_long |= (temp_byte1 << 8) 
                temp_long |= (temp_byte2 << 16)
                temp_long &= 0x3FFFF # Zero out all but 18 bits
                self.red[self.head] = temp_long # Store this reading into the red list at head
                #self.red[self.head] = temp_byte0 # Store this reading into the red list at head

                if (self.active_leds > 1):
                    # Next 3 bytes in buff will be IR
                    temp_byte2 = buff[buff_index+3]
                    temp_byte1 = buff[buff_index+4]
                    temp_byte0 = buff[buff_index+5]

                    # Combine bytes into single 32 bit integer variable
                    temp_long = 0
                    temp_long |= temp_byte0
                    temp_long |= (temp_byte1 << 8) 
                    temp_long |= (temp_byte2 << 16)
                    temp_long &= 0x3FFFF # Zero out all but 18 bits
                    self.ir[self.head] = temp_long # Store this reading into the IR list at head                    

                if (self.active_leds > 2):
                    # Next 3 bytes in buff will be GREEN
                    temp_byte2 = buff[buff_index+6]
                    temp_byte1 = buff[buff_index+7]
                    temp_byte0 = buff[buff_index+8]

                    # Combine bytes into single 32 bit integer variable
                    temp_long = 0
                    temp_long |= temp_byte0
                    temp_long |= (temp_byte1 << 8) 
                    temp_long |= (temp_byte2 << 16)
                    temp_long &= 0x3FFFF # Zero out all but 18 bits
                    self.green[self.head] = temp_long # Store this reading into the IR list at head          

        return number_of_samples #Let the world know how much new data we found

    # 
    # safe_check()
    # 
    # Check for new data but give up after a certain amount of time
    # Returns true if new data was found
    # Returns false if new data was not found

    def safe_check(self, max_time_to_check):
        """!
        Check for new data but give up after a certain amount of time
            Returns true if new data was found
            Returns false if new data was not found

        @param max_time_to_check: milliseconds to timeout

        @return **boolean** True if new data was found, otherwise False
        """
        timeout = max_time_to_check
        while(timeout):
            if(self.check() > 0): #We found new data!
                return True
            self._i2c.delay_ms(1)
            timeout -= 1
        return False

    # 
    # get_red()
    # 
    # Report the most recent red value

    def get_red(self):
        """!
        Report the most recent red value

        @return **integer** value of RED light sensor from most recent sample
        """
        #Check the sensor for new data for 250ms
        if self.safe_check(250):
            return self.red[self.head]
        else:
            return 0 #Sensor failed to find new data

    # 
    # get_ir()
    # 
    # Report the most recent IR value

    def get_ir(self):
        """!
        Report the most recent IR value

        @return **integer** value of IR light sensor from most recent sample
        """
        #Check the sensor for new data for 250ms
        if self.safe_check(250):
            return (self.ir[self.head])
        else:
            return 0 #Sensor failed to find new data

    # 
    # get_green()
    # 
    # Report the most recent Green value

    def get_green(self):
        """!
        Report the most recent GREEN value

        @return **integer** value of GREEN light sensor from most recent sample
        """
        #Check the sensor for new data for 250ms
        if self.safe_check(250):
            return self.green[self.head]
        else:
            return 0 #Sensor failed to find new data

    # 
    # get_fifo_red()
    # 
    # Report the next Red value in the FIFO

    def get_fifo_red(self):
        """!
        Report the next Red value in the FIFO

        @return **integer** the next Red value in the FIFO
        """
        return self.red[self.tail]

    # 
    # get_fifo_ir()
    # 
    # Report the next IR value in the FIFO

    def get_fifo_ir(self):
        """!
        Report the next IR value in the FIFO

        @return **integer** the next IR value in the FIFO
        """
        return self.ir[self.tail]

    # 
    # get_fifo_green()
    # 
    # Report the next Green value in the FIFO

    def get_fifo_green(self):
        """!
        Report the next Green value in the FIFO

        @return **integer** the next Green value in the FIFO
        """
        return self.green[self.tail]

    #
    # Device ID and Revision
    #

    # 
    # read_part_id()
    #
    # Report Part ID from the sensor

    def read_part_id(self):
        """!
        Report Part ID from the sensor

        @return **integer** Part ID
        """
        return self._i2c.read_byte(self.address, MAX30105_PARTID)

    # 
    # read_revision_id()
    #
    # Report Revision ID from the sensor

    def read_revision_id(self):
        """!
        Report Revision ID from the sensor

        @return **integer** Revision ID
        """
        self.revision_id = self._i2c.read_byte(self.address, MAX30105_REVISIONID)

    # 
    # get_revision_id()
    #
    # Report Revision ID from current variable in this class

    def get_revision_id(self):
        """!
        Report Revision ID from current variable in this class

        @return **integer** Revision ID
        """
        return self.revision_id

    #
    # read_temperature()
    #
    # Read Die Temperature in C
    #

    def read_temperature(self):
        """!
        Report Die Temperature in C

        @return **float** die temp in C
        """

        # DIE_TEMP_RDY interrupt must be enabled
        # See issue 19: https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library/issues/19
        
        # Step 1: Config die temperature register to take 1 temperature sample
        self._i2c.write_byte(self.address, MAX30105_DIETEMPCONFIG, 0x01)

        # Poll for bit to clear, reading is then complete
        # Timeout after 100ms
        start_time = self.millis()
        while self._i2c.ticks_diff(self.millis(), start_time) < 100:
            # Check to see if DIE_TEMP_RDY interrupt is set
            response = self._i2c.read_byte(self.address, MAX30105_INTSTAT2)
            if ((response & MAX30105_INT_DIE_TEMP_RDY_ENABLE) > 0):
                break # We're done!
            self._i2c.delay_ms(1) # Let's not over burden the I2C bus

        # Step 2: Read die temperature register (integer)
        temp_int = self._i2c.read_byte(self.address, MAX30105_DIETEMPINT)
        temp_frac = self._i2c.read_byte(self.address, MAX30105_DIETEMPFRAC) # Causes the clearing of the DIE_TEMP_RDY interrupt

        temp_int = float(temp_int)
        temp_frac = float(temp_frac)

        # Step 3: Calculate temperature (datasheet pg. 23)
        return (temp_int + (temp_frac * 0.0625))

    #
    # read_temperature_f()
    #
    # Returns die temp in F
    #

    def read_temperature_f(self):
        """!
        Returns die temp in F

        @return **float** die temp in F
        """
        temp = self.read_temperature()
        if (temp != -999.0):
            temp = ( (temp * 1.8) + 32.0 )
        return temp

    #
    # check_for_beat()
    #
    # Wrapper function to allow access to function within supporting heart_rate.py file
    #

    def check_for_beat(self, sample):
        """!
        Wrapper function to allow access to function within supporting heart_rate.py file

        @param sample: IR sample

        @return **boolean** True if a beat is detected, otherwise False
        """
        return hr.check_for_beat(sample)
