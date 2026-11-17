#-----------------------------------------------------------------------------
# qwiic_gpio.py
#
# Python library for the SparkFun qwiic gpio sensor.
#
# This sensor is available on the SparkFun Environmental Combo Breakout board.
#   https://www.sparkfun.com/products/14348
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
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

"""!
qwiic_gpio
============
Python module for the Qwiic GPIO.

This python package is a port of the existing [SparkFun GPIO Arduino Library](https://github.com/sparkfun/SparkFun_gpio_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""
#-----------------------------------------------------------------------------

import math
import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class defintion 
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at 
# runtine
#
# The name of this device 
_DEFAULT_NAME = "Qwiic GPIO"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the 
# device.
_AVAILABLE_I2C_ADDRESS = [0x27, 0x26, 0x25, 0x24, 0x23, 0x22, 0x21, 0x20]

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported 
# from this module.

class QwiicGPIO(object):
    """!
    QwiicGPIO

    @param address: The I2C address to use for the device. 
                    If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided 
                    a driver object is created.

    @return **Object** The GPIO device object.
    """
    # Constructor
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Registers
    REG_INPUT_PORT = 0x00
    REG_OUTPUT_PORT = 0x01
    REG_INVERSION = 0x02
    REG_CONFIGURATION = 0x03

    # Status/Configuration Flags
    GPIO_OUT = 0
    GPIO_IN = 1

    GPIO_LO = 0
    GPIO_HI = 1
    
    INVERT = True
    NO_INVERT = False

    NUM_GPIO = 8

    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self.address = address if address != None else self.available_addresses[0]

        # load the I2C driver if one isn't provided

        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

        # This list will hold the inversion status of each pin
        self.inversions = [self.NO_INVERT] * self.NUM_GPIO 
        self.modes = [self.GPIO_OUT] * self.NUM_GPIO # These are the mode settings for each pin
        self.out_statuses = [self.GPIO_LO] * self.NUM_GPIO  # These are the output settings for each pin
        self.in_statuses = [self.GPIO_LO] * self.NUM_GPIO # These are the input settings for each pin

    # ----------------------------------
    # isConnected()
    #
    # Is an actual board connected to our system?

    def isConnected(self):
        """!
        Determine if a Qwiic GPIO device is connected to the system..

        @return **bool** True if the device is connected, otherwise False.
        """
        return qwiic_i2c.isDeviceConnected(self.address)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board. 
    def begin(self):
        """!
        Initialize the operation of the Qwiic GPIO

        @return **bool** Returns true of the initializtion was successful, otherwise False.
        """
        
        return self.isConnected()

    #----------------------------------------------------------------
    # setMode()
    #
    # Set the mode (input/output) for all GPIO
    def setMode(self):
        """!
        Sends all 8 pin modes (input or output) to the GPIO to set all 8 pins. Setting the value to input or output is done using myGPIO.modes[0] = myGPIO.GPIO_OUT

        @return  No return value
        """
        tempData = 0

        for i in range (self.NUM_GPIO):
            tempData |= self.modes[i] << i

        self._i2c.writeByte(self.address, self.REG_CONFIGURATION, tempData)

    #----------------------------------------------------------------
    # getMode()
    #
    # Get the mode (input/output) for all GPIO
    def getMode(self):
        """!
        Updates mode_X variables with values from Qwiic GPIO

        @return **8 bit unsigned integer** The value of the mode register.
        """
        tempData = self._i2c.readByte(self.address, self.REG_CONFIGURATION)

        for i in range(self.NUM_GPIO):
            self.modes[i] = (tempData & (1 << i)) >> i
        
        return tempData

    #----------------------------------------------------------------
    # setInversion()
    # 
    # Set whether a GPIO will invert an incoming signal

    def setInversion(self):
        """!
        Send the inversion modes of all pins. This function must be called after editing modes using myGPIO.inversions[0] = myGPIO.INVERT

        @return  No return value
        """
        tempData = 0

        for i in range(self.NUM_GPIO):
            tempData |= self.inversions[i] << i

        self._i2c.writeByte(self.address, self.REG_INVERSION, tempData)

    #----------------------------------------------------------------
    # getInversion()
    # 
    # Get inversion settings from each GPIO.

    def getInversion(self):
        """!
        Updates inversion_X variables with values from Qwiic GPIO

        @return **8 bit unsigned integer** The value of the inversion register.
        """
        tempData = self._i2c.readByte(self.address, self.REG_INVERSION)

        for i in range(self.NUM_GPIO):
            self.inversions[i] = (tempData & (1 << i)) >> i

        return tempData

    #----------------------------------------------------------------
    # setGPIO()
    # 
    # Sends all GPIO outputs to the Qwiic GPIO 

    def setGPIO(self):
        """!
        Send all current output settings to the GPIO. This should be called after calling myGPIO.out_statuses[0] = myGPIO.GPIO_HI to set the GPIO.

        @return  No return value
        """
        tempData = 0

        for i in range(self.NUM_GPIO):
            tempData |= self.out_statuses[i] << i

        self._i2c.writeByte(self.address, self.REG_OUTPUT_PORT, tempData)

    def getGPIO(self):
        """!
        Updates mode_X variables with values from Qwiic GPIO

        @return **8 bit unsigned integer** The value of the mode register.
        """
        tempData = self._i2c.readByte(self.address, self.REG_INPUT_PORT)

        for i in range(self.NUM_GPIO):
            self.in_statuses[i] = (tempData & (1 << i)) >> i

        return tempData
    
    def pinMode (self, pin, mode):
        """!
        Set the mode of a single pin.

        @param pin: The pin number to set the mode of.
        @param mode: The mode to set the pin to.

        @return  No return value
        """
        if mode != self.GPIO_IN and mode != self.GPIO_OUT:
            return
        
        if pin < 0 or pin > 7:
            return
        
        self.modes[pin] = mode
        self.setMode()
    
    def pinModePort (self, gpioPinModeList):
        """!
        Set the mode of a list of pins.

        @param gpioPinModeList: A list of boolean modes to set the pins at each index to.

        @return  No return value
        """

        if len(gpioPinModeList) != 8:
            return
        
        self.modes = gpioPinModeList
        self.setMode()
    
    def invertPin(self, pin, invert):
        """!
        Set the inversion of a single pin.

        @param pin: The pin number to set the inversion of.
        @param invert: The inversion to set the pin to.

        @return  No return value
        """
        if pin < 0 or pin > 7:
            return
        
        self.inversions[pin] = invert
        self.setInversion()
    
    def invertPinPort (self, gpioInversionList):
        """!
        Set the inversion of a list of pins.

        @param gpioInversionList: A list of boolean inversions to set the pins at each index to.

        @return  No return value
        """

        if len(gpioInversionList) != 8:
            return
        
        self.inversions = gpioInversionList
        self.setInversion()
    
    def digitalWrite(self, pin, value):
        """!
        Set the output value of a single pin.

        @param pin: The pin number to set the output value of.
        @param value: The value to set the pin to.

        @return  No return value
        """
        if pin < 0 or pin > 7:
            return
        
        self.out_statuses[pin] = value
        self.setGPIO()
    
    def digitalWritePort (self, gpioOutputList):
        """!
        Set the output value of a list of pins.

        @param gpioOutputList: A list of boolean output values to set the pins at each index to.

        @return  No return value
        """

        if len(gpioOutputList) != 8:
            return
        
        self.out_statuses = gpioOutputList
        self.setGPIO()

    def digitalRead(self, pin):
        """!
        Get the input value of a single pin.

        @param pin: The pin number to get the input value of.

        @return **bool** The value of the pin.
        """
        if pin < 0 or pin > 7:
            return
        
        self.getGPIO()
        return self.in_statuses[pin]
    
    def digitalReadPort (self):
        """!
        Get the input value of all pins.

        @return  A list of boolean input values of all pins.
        """
        self.getGPIO()
        return self.in_statuses