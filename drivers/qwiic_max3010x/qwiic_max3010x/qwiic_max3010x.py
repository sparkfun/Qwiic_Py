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
import time

from . import heart_rate
hr = heart_rate.HeartRate()

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

class QwiicMax3010x(object):
    """!
    QwiicMax3010x

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.

    @return The QwiicMax3010x device object.
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS
    
    # activeLEDs is the number of channels turned on, and can be 1 to 3. 2 is common for Red+IR.
    activeLEDs = 0 # Gets set during setup. Allows check() to calculate how many bytes to read from FIFO
    
    # Storage size
    # (This is "left over" from the arduino library, but needed for rollovers) 
    # Each long is 4 bytes so limit this to fit on your micro
    STORAGE_SIZE = 4

    # Circular buffer of readings from the sensor
    red = [0,0,0,0] # place holders to make this list 4 spaces long (to mimic previous struct arrays in arduino library)
    IR = [0,0,0,0]
    green = [0,0,0,0]
    head = 0
    tail = 0

    readPointer = 0
    writePointer = 0
    numberOfSamples = 0

    # Constructor

    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # load the I2C driver if one isn't provided

        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    # ----------------------------------
    # isConnected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """!
        Determine if a device is conntected to the system..

        @return **bool** True if the device is connected, otherwise False.
        """
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

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
        temp_reg = self._i2c.readByte(self.address, reg)

        # Zero-out the portions of the register we're interested in
        temp_reg &= mask

        # Change contents
        temp_reg |= thing

        return self._i2c.writeByte(self.address, reg, temp_reg)

    # ----------------------------------
    # millis()
    #
    # Returns the current time in milliseconds

    def millis(self):

        """!
        Returns the current time in milliseconds

        @return **int32_t** Returns current system time in milliseconds
        """        
        return int(round(time.time() * 1000))

    # ----------------------------------
    # softReset()
    #
    # Command a soft reset

    def softReset(self):
        """!
        Command a soft reset

        @return **bool** Returns true of the soft reset was successful, otherwise False.
        """
        self.bit_mask(MAX30105_MODECONFIG, MAX30105_RESET_MASK, MAX30105_RESET)

        # Poll for bit to clear, reset is then complete
        # Timeout after 100ms
        timeout = 100
        while (timeout):
            response = self._i2c.readByte(self.address, MAX30105_MODECONFIG)
            if ((response & MAX30105_RESET) == 0):
                return True # We're done!
            time.sleep(0.001) # Let's not over burden the I2C bus
            timeout -= 1
        return False # soft reset failure

    # 
    #  Configuration
    # 

    # Begin Interrupt configuration

    # ----------------------------------
    # getINT1()
    #
    # Returns the value of the INTSTAT1 Register

    def getINT1(self):
        """!
        Returns the value of the INTSTAT1 Register

        @return **integer** value of the INTSTAT1 Register
        """
        return self._i2c.readByte(self.address, MAX30105_INTSTAT1)

    # ----------------------------------
    # getINT2()
    #
    # Returns the value of the INTSTAT2 Register

    def getINT2(self):
        """!
        Returns the value of the INTSTAT2 Register

        @return **integer** value of the INTSTAT2 Register
        """
        return self._i2c.readByte(self.address, MAX30105_INTSTAT2)

    # ----------------------------------
    # enableAFULL()
    #
    # Enable AFULL Interrupt

    def enableAFULL(self):
        """!
        Enable AFULL Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_A_FULL_MASK, MAX30105_INT_A_FULL_ENABLE)

    # ----------------------------------
    # disableAFULL()
    #
    # Disable AFULL Interrupt

    def disableAFULL(self):
        """!
        Disable AFULL Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_A_FULL_MASK, MAX30105_INT_A_FULL_DISABLE)

    # ----------------------------------
    # enableDATARDY()
    #
    # Enable DATARDY Interrupt

    def enableDATARDY(self):
        """!
        Enable DATARDY Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_DATA_RDY_MASK, MAX30105_INT_DATA_RDY_ENABLE)

    # ----------------------------------
    # disableDATARDY()
    #
    # Disable DATARDY Interrupt

    def disableDATARDY(self):
        """!
        Disable DATARDY Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_DATA_RDY_MASK, MAX30105_INT_DATA_RDY_DISABLE)

    # ----------------------------------
    # enableALCOVF()
    #
    # Enable ALCOVF Interrupt

    def enableALCOVF(self):
        """!
        Enable ALCOVF Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_ALC_OVF_MASK, MAX30105_INT_ALC_OVF_ENABLE)

    # ----------------------------------
    # disableALCOVF()
    #
    # Disable ALCOVF Interrupt

    def disableALCOVF(self):
        """!
        Disable ALCOVF Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_ALC_OVF_MASK, MAX30105_INT_ALC_OVF_DISABLE)

    # ----------------------------------
    # enablePROXINT()
    #
    # Enable PROXINT Interrupt

    def enablePROXINT(self):
        """!
        Enable PROXINT Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_PROX_INT_MASK, MAX30105_INT_PROX_INT_ENABLE)

    # ----------------------------------
    # disablePROXINT()
    #
    # Disable PROXINT Interrupt

    def disablePROXINT(self):
        """!
        Disable PROXINT Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE1, MAX30105_INT_PROX_INT_MASK, MAX30105_INT_PROX_INT_DISABLE)

    # ----------------------------------
    # enableDIETEMPRDY()
    #
    # Enable DIETEMPRDY Interrupt

    def enableDIETEMPRDY(self):
        """!
        Enable DIETEMPRDY Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE2, MAX30105_INT_DIE_TEMP_RDY_MASK, MAX30105_INT_DIE_TEMP_RDY_ENABLE)

    # ----------------------------------
    # disableDIETEMPRDY()
    #
    # Disable DIETEMPRDY Interrupt

    def disableDIETEMPRDY(self):
        """!
        Disable DIETEMPRDY Interrupt

        @return no return value
        """
        self.bit_mask(MAX30105_INTENABLE2, MAX30105_INT_DIE_TEMP_RDY_MASK, MAX30105_INT_DIE_TEMP_RDY_DISABLE)

    # End Interrupt configuration        

    # ----------------------------------
    # shutDown()
    #
    # Put IC into low power mode (datasheet pg. 19)
    # During shutdown the IC will continue to respond to I2C commands but will
    # not update with or take new readings (such as temperature)

    def shutDown(self):
        """!
        Put IC into low power mode

        @return no return value
        """
        self.bit_mask(MAX30105_MODECONFIG, MAX30105_SHUTDOWN_MASK, MAX30105_SHUTDOWN)

    # ----------------------------------
    # wakeUp()
    #
    # Pull IC out of low power mode (datasheet pg. 19)

    def wakeUp(self):
        """!
        Pull IC out of low power mode

        @return no return value
        """
        self.bit_mask(MAX30105_MODECONFIG, MAX30105_SHUTDOWN_MASK, MAX30105_WAKEUP)

    # ----------------------------------
    # setLEDMode()
    #
    # Set which LEDs are used for sampling - Red only, RED+IR only, or custom.
    # See datasheet, page 19

    def setLEDMode(self, mode):
        """!
        Set which LEDs are used for sampling - Red only, RED+IR only, or custom

        @param mode: Red only, RED+IR only, or custom

        @return no return value
        """
        self.bit_mask(MAX30105_MODECONFIG, MAX30105_MODE_MASK, mode)

    # ----------------------------------
    # setADCRange()
    #
    # Set adcRange: one of MAX30105_ADCRANGE_2048, _4096, _8192, _16384

    def setADCRange(self, adcRange):
        """!
        Set adcRange: one of MAX30105_ADCRANGE_2048, _4096, _8192, _16384

        @param adcRange: MAX30105_ADCRANGE_2048, _4096, _8192, _16384

        @return no return value
        """
        self.bit_mask(MAX30105_PARTICLECONFIG, MAX30105_ADCRANGE_MASK, adcRange)

    # ----------------------------------
    # setSampleRate()
    #
    # Set sampleRate: one of MAX30105_SAMPLERATE_50, _100, _200, _400, _800, _1000, _1600, _3200

    def setSampleRate(self, sampleRate):
        """!
        Set sampleRate: one of MAX30105_SAMPLERATE_50, _100, _200, _400, _800, _1000, _1600, _3200

        @param sampleRate: MAX30105_SAMPLERATE_50, _100, _200, _400, _800, _1000, _1600, _3200

        @return no return value
        """
        self.bit_mask(MAX30105_PARTICLECONFIG, MAX30105_SAMPLERATE_MASK, sampleRate)

    # ----------------------------------
    # setPulseWidth()
    #
    # Set pulseWidth: one of MAX30105_PULSEWIDTH_69, _188, _215, _411

    def setPulseWidth(self, pulseWidth):
        """!
        Set pulseWidth: one of MAX30105_PULSEWIDTH_69, _188, _215, _411

        @param pulseWidth: MAX30105_PULSEWIDTH_69, _188, _215, _411

        @return no return value
        """
        self.bit_mask(MAX30105_PARTICLECONFIG, MAX30105_PULSEWIDTH_MASK, pulseWidth)

    # ----------------------------------
    # setPulseAmplitudeRed()
    #
    # Set pulse amplitude (mA) of red LED
    # 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)
    # See datasheet, page 21

    def setPulseAmplitudeRed(self, amplitude):
        """!
        Set pulse amplitude (mA) of red LED

        @param amplitude: 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)

        @return no return value
        """
        self._i2c.writeByte(self.address, MAX30105_LED1_PULSEAMP, amplitude)

    # ----------------------------------
    # setPulseAmplitudeIR()
    #
    # Set pulse amplitude (mA) of IR LED
    # 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)
    # See datasheet, page 21

    def setPulseAmplitudeIR(self, amplitude):
        """!
        Set pulse amplitude (mA) of IR LED

        @param amplitude: 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)

        @return no return value
        """
        self._i2c.writeByte(self.address, MAX30105_LED2_PULSEAMP, amplitude)

    # ----------------------------------
    # setPulseAmplitudeGreen()
    #
    # Set pulse amplitude (mA) of green LED
    # 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)
    # See datasheet, page 21

    def setPulseAmplitudeGreen(self, amplitude):
        """!
        Set pulse amplitude (mA) of green LED

        @param amplitude: 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA (typical)

        @return no return value
        """
        self._i2c.writeByte(self.address, MAX30105_LED3_PULSEAMP, amplitude)

    # ----------------------------------
    # setPulseAmplitudeProximity()
    #
    # Set pulse aplitude while in proximity mode (only MAX30105)
    # Note, this is specific to the MAX30105, and not included in the MAX30101

    def setPulseAmplitudeProximity(self, amplitude):
        """!
        Set pulse aplitude while in proximity mode (only MAX30105)
            Note, this is specific to the MAX30105, and not included in the MAX30101

        @param amplitude: amplitude

        @return no return value
        """
        self._i2c.writeByte(self.address, MAX30105_LED_PROX_AMP, amplitude)

    # ----------------------------------
    # setProximityThreshold()
    #
    # Set the IR ADC count that will trigger the beginning of particle-sensing mode.
    # The threshMSB signifies only the 8 most significant-bits of the ADC count.
    # Note, this is specific to the MAX30105, and not included in the MAX30101
    # See datasheet, page 24.

    def setProximityThreshold(self, threshMSB):
        """!
        Set the IR ADC count that will trigger the beginning of particle-sensing mode.
            The threshMSB signifies only the 8 most significant-bits of the ADC count.
            Note, this is specific to the MAX30105, and not included in the MAX30101

        @param threshMSB: threshold of ADC count to cause trigger

        @return no return value
        """
        self._i2c.writeByte(self.address, MAX30105_PROXINTTHRESH, threshMSB)     

    #
    # enableSlot()
    #
    # Given a slot number assign a thing to it
    # Devices are SLOT_RED_LED or SLOT_RED_PILOT (proximity)
    # Assigning a SLOT_RED_LED will pulse LED
    # Assigning a SLOT_RED_PILOT will ??

    def enableSlot(self, slotNumber, device):
        """!
        Given a slot number assign a thing to it
            Devices are SLOT_RED_LED or SLOT_RED_PILOT (proximity)
            Assigning a SLOT_RED_LED will pulse LED
            Assigning a SLOT_RED_PILOT will ??

        @param slotNumber: slot number as int 1,2,3,4
        @param device: which device (aka led) you'd like to assign to the given slot

        @return **bool** Whether or not the configuration write was successful
        """
        if slotNumber == 1:
            return self.bit_mask(MAX30105_MULTILEDCONFIG1, MAX30105_SLOT1_MASK, device)
        elif slotNumber == 2:
            return self.bit_mask(MAX30105_MULTILEDCONFIG1, MAX30105_SLOT2_MASK, device << 4)
        elif slotNumber == 3:
            return self.bit_mask(MAX30105_MULTILEDCONFIG2, MAX30105_SLOT3_MASK, device)
        elif slotNumber == 4:
            return self.bit_mask(MAX30105_MULTILEDCONFIG2, MAX30105_SLOT4_MASK, device << 4)
        else:
            return False #Shouldn't be here!
  
    #
    # disableSlots()
    # 
    # Clears all slot assignments

    def disableSlots(self):
        """!
        Clears all slot assignments

        @return no return value
        """
        self._i2c.writeByte(self.address, MAX30105_MULTILEDCONFIG1, 0)
        self._i2c.writeByte(self.address, MAX30105_MULTILEDCONFIG2, 0)

    #
    # FIFO Configuration
    #

    # 
    # setFIFOAverage()
    #
    # Set sample average (Table 3, Page 18)

    def setFIFOAverage(self, numberOfSamples):
        """!
        Set sample average

        @param numberOfSamples: MAX30105_SAMPLEAVG_1, _2, _4, _8, _16, _32

        @return no return value
        """
        self.bit_mask(MAX30105_FIFOCONFIG, MAX30105_SAMPLEAVG_MASK, numberOfSamples)

    #
    # clearFIFO()
    #
    # Resets all points to start in a known state
    # Page 15 recommends clearing FIFO before beginning a read

    def clearFIFO(self):
        """!
        Resets all points to start in a known state

        @return no return value
        """
        self._i2c.writeByte(self.address, MAX30105_FIFOWRITEPTR, 0)
        self._i2c.writeByte(self.address, MAX30105_FIFOOVERFLOW, 0)
        self._i2c.writeByte(self.address, MAX30105_FIFOREADPTR, 0)

    # 
    # enableFIFORollover()
    # 
    # Enable roll over if FIFO over flows

    def enableFIFORollover(self):
        """!
        Enable roll over if FIFO over flows

        @return no return value
        """
        self.bit_mask(MAX30105_FIFOCONFIG, MAX30105_ROLLOVER_MASK, MAX30105_ROLLOVER_ENABLE)

    # 
    # disableFIFORollover()
    # 
    # Disable roll over if FIFO over flows

    def disableFIFORollover(self):
        """!
        Disable roll over if FIFO over flows

        @return no return value
        """
        self.bit_mask(MAX30105_FIFOCONFIG, MAX30105_ROLLOVER_MASK, MAX30105_ROLLOVER_DISABLE)

    # 
    # setFIFOAlmostFull()
    # 
    # Set number of samples to trigger the almost full interrupt (Page 18)
    # Power on default is 32 samples
    # Note it is reverse: 0x00 is 32 samples, 0x0F is 17 samples

    def setFIFOAlmostFull(self, numberOfSamples):
        """!
        Set number of samples to trigger the almost full interrupt

        @param numberOfSamples: default is 32 samples. Note it's reverse (0x00 is 32 samples, 0x0F is 17 samples)

        @return no return value
        """
        self.bit_mask(MAX30105_FIFOCONFIG, MAX30105_A_FULL_MASK, numberOfSamples)

    # 
    # getWritePointer()
    # 
    # Read the FIFO Write Pointer

    def getWritePointer(self):
        """!
        Read the FIFO Write Pointer

        @return **integer** FIFO write pointer value
        """
        return self._i2c.readByte(self.address, MAX30105_FIFOWRITEPTR)

    # 
    # getReadPointer()
    # 
    # Read the FIFO Read Pointer
    
    def getReadPointer(self):
        """!
        Read the FIFO Read Pointer

        @return **integer** FIFO read pointer value
        """
        return self._i2c.readByte(self.address, MAX30105_FIFOREADPTR)

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

    def setup(self, powerLevel = 0x1F, sampleAverage = 4, ledMode = 3, sampleRate = 400, pulseWidth = 411, adcRange = 4096):
        """!
        Setup the MAX3010x with default or custom settings

        @param powerLevel: 0x00 = 0mA, 0x7F = 25.4mA, 0xFF = 50mA
        @param sampleAverage: int, 1,2,4,8,16,32, default is 4
        @param ledMode: 1 = RED, 2=RED+IR , 3=RED+IR+GREEN
        @param sampleRate: 0-3200
        @param pulseWidth: 0-411 (microseconds)
        @param adcRange: 2048,4096,8192,16384

        @return no return value
        """
        self.softReset() # Reset all configuration, threshold, and data registers to POR values

        # FIFO Configuration
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # The chip will average multiple samples of same type together if you wish
        if sampleAverage == 1:
            self.setFIFOAverage(MAX30105_SAMPLEAVG_1) # No averaging per FIFO record
        elif sampleAverage == 2:
            self.setFIFOAverage(MAX30105_SAMPLEAVG_2)
        elif sampleAverage == 4:
            self.setFIFOAverage(MAX30105_SAMPLEAVG_4)
        elif sampleAverage == 8:
            self.setFIFOAverage(MAX30105_SAMPLEAVG_8)
        elif sampleAverage == 16:
            self.setFIFOAverage(MAX30105_SAMPLEAVG_16)
        elif sampleAverage == 32:
            self.setFIFOAverage(MAX30105_SAMPLEAVG_32)
        else:
            self.setFIFOAverage(MAX30105_SAMPLEAVG_4)

        # setFIFOAlmostFull(2) # Set to 30 samples to trigger an 'Almost Full' interrupt
        self.enableFIFORollover() # Allow FIFO to wrap/roll over
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # Mode Configuration
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        if ledMode == 3:
            self.setLEDMode(MAX30105_MODE_MULTILED) # Watch all three LED channels
        elif ledMode == 2:
            self.setLEDMode(MAX30105_MODE_REDIRONLY) # Red and IR
        else:
            self.setLEDMode(MAX30105_MODE_REDONLY) # Red only
        self.activeLEDs = ledMode # Used to control how many bytes to read from FIFO buffer
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # Particle Sensing Configuration
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        if adcRange < 4096:
            self.setADCRange(MAX30105_ADCRANGE_2048) # 7.81pA per LSB
        elif adcRange < 8192:
            self.setADCRange(MAX30105_ADCRANGE_4096) # 15.63pA per LSB
        elif adcRange < 16384:
            self.setADCRange(MAX30105_ADCRANGE_8192) # 31.25pA per LSB
        elif adcRange == 16384:
            self.setADCRange(MAX30105_ADCRANGE_16384) # 62.5pA per LSB
        else:
            self.setADCRange(MAX30105_ADCRANGE_2048)

        if sampleRate < 100:
            self.setSampleRate(MAX30105_SAMPLERATE_50) # Take 50 samples per second
        elif sampleRate < 200:
            self.setSampleRate(MAX30105_SAMPLERATE_100)
        elif sampleRate < 400:
            self.setSampleRate(MAX30105_SAMPLERATE_200)
        elif sampleRate < 800:
            self.setSampleRate(MAX30105_SAMPLERATE_400)
        elif sampleRate < 1000:
            self.setSampleRate(MAX30105_SAMPLERATE_800)
        elif sampleRate < 1600:
            self.setSampleRate(MAX30105_SAMPLERATE_1000)
        elif sampleRate < 3200:
            self.setSampleRate(MAX30105_SAMPLERATE_1600)
        elif sampleRate == 3200:
            self.setSampleRate(MAX30105_SAMPLERATE_3200)
        else:
            self.setSampleRate(MAX30105_SAMPLERATE_50)

        # The longer the pulse width the longer range of detection you'll have
        # At 69us and 0.4mA it's about 2 inches
        # At 411us and 0.4mA it's about 6 inches
        if pulseWidth < 118:
            self.setPulseWidth(MAX30105_PULSEWIDTH_69) # Page 26, Gets us 15 bit resolution
        elif pulseWidth < 215:
            self.setPulseWidth(MAX30105_PULSEWIDTH_118) # 16 bit resolution
        elif pulseWidth < 411:
            self.setPulseWidth(MAX30105_PULSEWIDTH_215) # 17 bit resolution
        elif pulseWidth == 411:
            self.setPulseWidth(MAX30105_PULSEWIDTH_411) # 18 bit resolution
        else:
            self.setPulseWidth(MAX30105_PULSEWIDTH_69)
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # LED Pulse Amplitude Configuration
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Default is 0x1F which gets us 6.4mA
        # powerLevel = 0x02, 0.4mA - Presence detection of ~4 inch
        # powerLevel = 0x1F, 6.4mA - Presence detection of ~8 inch
        # powerLevel = 0x7F, 25.4mA - Presence detection of ~8 inch
        # powerLevel = 0xFF, 50.0mA - Presence detection of ~12 inch

        self.setPulseAmplitudeRed(powerLevel)
        self.setPulseAmplitudeIR(powerLevel)
        self.setPulseAmplitudeGreen(powerLevel)
        self.setPulseAmplitudeProximity(powerLevel)
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        # Multi-LED Mode Configuration, Enable the reading of the three LEDs
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.enableSlot(1, SLOT_RED_LED)
        if ledMode > 1:
            self.enableSlot(2, SLOT_IR_LED)
        if ledMode > 2:
            self.enableSlot(3, SLOT_GREEN_LED)
        # self.enableSlot(1, SLOT_RED_PILOT)
        # self.nableSlot(2, SLOT_IR_PILOT)
        # self.enableSlot(3, SLOT_GREEN_PILOT)
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        self.clearFIFO() # Reset the FIFO before we begin checking the sensor


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
        numberOfSamples = self.head - self.tail
        if numberOfSamples < 0:
            numberOfSamples += self.STORAGE_SIZE
        return numberOfSamples

    # 
    # nextSample()
    # 
    # Advance the tail

    def nextSample(self):
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

        readPointer = self.getReadPointer()
        writePointer = self.getWritePointer()
        numberOfSamples = 0

        #Do we have new data?
        if readPointer != writePointer:
            #Calculate the number of samples we need to get from sensor
            numberOfSamples = (writePointer - readPointer)
            if (numberOfSamples < 0):
                numberOfSamples += 32 #Wrap condition
                
            #We now have the number of samples, now calc bytes to read
            bytesToRead = numberOfSamples * self.activeLEDs * 3

            # We may need to read as many as 288 bytes (32 * 3 * 3), but not all
            # platforms can read that much in one go. So we read in blocks until
            # we reach the end.
            maxReadSize = 32
            buff = []
            while bytesToRead > 0:
                # Compute how many bytes we need to read in this loop iteration
                bytesToReadThisTime = bytesToRead
                if bytesToReadThisTime > maxReadSize:
                    bytesToReadThisTime = maxReadSize
                
                # Update number of bytes remaining
                bytesToRead -= bytesToReadThisTime

                # Read from FIFO and append to buffer
                buff += self._i2c.readBlock(self.address, MAX30105_FIFODATA, bytesToReadThisTime)
            
            # Grab all the bytes we just read into buff, and plug them into the correct local variables.
            # Note, we need to keep track of where we are in the buff (using sampleNumber and buffIndex "i")
            # Also, the bytes in buff will mean different things,
            # according to which LEDs are active (Red, IR, and/or Green)

            # for loop through the entire buff list,
            # using sampleNumber to "jump" buffIndex as necessary to each sample start within buff
            for sampleNumber in range(0, numberOfSamples):
                buffIndex = sampleNumber * self.activeLEDs * 3 # move index to the start of the next sample
                self.head += 1 # Advance the head of the storage list
                self.head %= self.STORAGE_SIZE # Wrap condition

                # First 3 bytes in buff will always be RED
                tempByte2 = buff[buffIndex+0]
                tempByte1 = buff[buffIndex+1]
                tempByte0 = buff[buffIndex+2]

                #also copy to varaibles for testing
                #self.byte0 = tempByte0
                #self.byte1 = tempByte1
                #self.byte2 = tempByte2

                # Combine bytes into single 32 bit integer variable
                tempLong = 0
                tempLong |= tempByte0
                tempLong |= (tempByte1 << 8) 
                tempLong |= (tempByte2 << 16)
                tempLong &= 0x3FFFF # Zero out all but 18 bits
                self.red[self.head] = tempLong # Store this reading into the red list at head
                #self.red[self.head] = tempByte0 # Store this reading into the red list at head

                if (self.activeLEDs > 1):
                    # Next 3 bytes in buff will be IR
                    tempByte2 = buff[buffIndex+3]
                    tempByte1 = buff[buffIndex+4]
                    tempByte0 = buff[buffIndex+5]

                    # Combine bytes into single 32 bit integer variable
                    tempLong = 0
                    tempLong |= tempByte0
                    tempLong |= (tempByte1 << 8) 
                    tempLong |= (tempByte2 << 16)
                    tempLong &= 0x3FFFF # Zero out all but 18 bits
                    self.IR[self.head] = tempLong # Store this reading into the IR list at head                    

                if (self.activeLEDs > 2):
                    # Next 3 bytes in buff will be GREEN
                    tempByte2 = buff[buffIndex+6]
                    tempByte1 = buff[buffIndex+7]
                    tempByte0 = buff[buffIndex+8]

                    # Combine bytes into single 32 bit integer variable
                    tempLong = 0
                    tempLong |= tempByte0
                    tempLong |= (tempByte1 << 8) 
                    tempLong |= (tempByte2 << 16)
                    tempLong &= 0x3FFFF # Zero out all but 18 bits
                    self.green[self.head] = tempLong # Store this reading into the IR list at head          

        return numberOfSamples #Let the world know how much new data we found

    # 
    # safeCheck()
    # 
    # Check for new data but give up after a certain amount of time
    # Returns true if new data was found
    # Returns false if new data was not found

    def safeCheck(self, maxTimeToCheck):
        """!
        Check for new data but give up after a certain amount of time
            Returns true if new data was found
            Returns false if new data was not found

        @param maxTimeToCheck: milliseconds to timeout

        @return **boolean** True if new data was found, otherwise False
        """
        timeout = maxTimeToCheck
        while(timeout):
            if(self.check() > 0): #We found new data!
                return True
            time.sleep(0.001)
            timeout -= 1
        return False

    # 
    # getRed()
    # 
    # Report the most recent red value

    def getRed(self):
        """!
        Report the most recent red value

        @return **integer** value of RED light sensor from most recent sample
        """
        #Check the sensor for new data for 250ms
        if self.safeCheck(250):
            return self.red[self.head]
        else:
            return 0 #Sensor failed to find new data

    # 
    # getIR()
    # 
    # Report the most recent IR value

    def getIR(self):
        """!
        Report the most recent IR value

        @return **integer** value of IR light sensor from most recent sample
        """
        #Check the sensor for new data for 250ms
        if self.safeCheck(250):
            return (self.IR[self.head])
        else:
            return 0 #Sensor failed to find new data

    # 
    # getGreen()
    # 
    # Report the most recent Green value

    def getGreen(self):
        """!
        Report the most recent GREEN value

        @return **integer** value of GREEN light sensor from most recent sample
        """
        #Check the sensor for new data for 250ms
        if self.safeCheck(250):
            return self.green[self.head]
        else:
            return 0 #Sensor failed to find new data

    # 
    # getFIFORed()
    # 
    # Report the next Red value in the FIFO

    def getFIFORed(self):
        """!
        Report the next Red value in the FIFO

        @return **integer** the next Red value in the FIFO
        """
        return self.red[self.tail]

    # 
    # getFIFOIR()
    # 
    # Report the next IR value in the FIFO

    def getFIFOIR(self):
        """!
        Report the next IR value in the FIFO

        @return **integer** the next IR value in the FIFO
        """
        return self.IR[self.tail]

    # 
    # getFIFOGreen()
    # 
    # Report the next Green value in the FIFO

    def getFIFOGreen(self):
        """!
        Report the next Green value in the FIFO

        @return **integer** the next Green value in the FIFO
        """
        return self.green[self.tail]

    #
    # Device ID and Revision
    #

    # 
    # readPartID()
    #
    # Report Part ID from the sensor

    def readPartID(self):
        """!
        Report Part ID from the sensor

        @return **integer** Part ID
        """
        return self._i2c.readByte(self.address, MAX30105_PARTID)

    # 
    # readRevisionID()
    #
    # Report Revision ID from the sensor

    def readRevisionID(self):
        """!
        Report Revision ID from the sensor

        @return **integer** Revision ID
        """
        self.revisionID = self._i2c.readByte(self.address, MAX30105_REVISIONID)

    # 
    # getRevisionID()
    #
    # Report Revision ID from current variable in this class

    def getRevisionID(self):
        """!
        Report Revision ID from current variable in this class

        @return **integer** Revision ID
        """
        return self.revisionID

    #
    # readTemperature()
    #
    # Read Die Temperature in C
    #

    def readTemperature(self):
        """!
        Report Die Temperature in C

        @return **float** die temp in C
        """

        # DIE_TEMP_RDY interrupt must be enabled
        # See issue 19: https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library/issues/19
        
        # Step 1: Config die temperature register to take 1 temperature sample
        self._i2c.writeByte(self.address, MAX30105_DIETEMPCONFIG, 0x01)

        # Poll for bit to clear, reading is then complete
        # Timeout after 100ms
        startTime = self.millis()
        while ( ( self.millis() - startTime ) < 100 ):
            # Check to see if DIE_TEMP_RDY interrupt is set
            response = self._i2c.readByte(self.address, MAX30105_INTSTAT2)
            if ((response & MAX30105_INT_DIE_TEMP_RDY_ENABLE) > 0):
                break # We're done!
            time.sleep(0.001) # Let's not over burden the I2C bus

        # Step 2: Read die temperature register (integer)
        tempInt = self._i2c.readByte(self.address, MAX30105_DIETEMPINT)
        tempFrac = self._i2c.readByte(self.address, MAX30105_DIETEMPFRAC) # Causes the clearing of the DIE_TEMP_RDY interrupt

        tempInt = float(tempInt)
        tempFrac = float(tempFrac)

        # Step 3: Calculate temperature (datasheet pg. 23)
        return (tempInt + (tempFrac * 0.0625))

    #
    # readTemperatureF()
    #
    # Returns die temp in F
    #

    def readTemperatureF(self):
        """!
        Returns die temp in F

        @return **float** die temp in F
        """
        temp = self.readTemperature()
        if (temp != -999.0):
            temp = ( (temp * 1.8) + 32.0 )
        return temp

    #
    # checkForBeat()
    #
    # Wrapper function to allow access to function within supporting heart_rate.py file
    #

    def checkForBeat(self, sample):
        """!
        Wrapper function to allow access to function within supporting heart_rate.py file

        @param sample: IR sample

        @return **boolean** True if a beat is detected, otherwise False
        """
        return hr.checkForBeat(sample)
