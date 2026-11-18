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

import qwiic_i2c

__version__ = "3.0.0"

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
    @param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.

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
    def __init__(self, address=None, i2c_bus=None):

        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address?
        self.address = address if address is not None else self.available_addresses[0]

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

        # This list will hold the inversion status of each pin
        self.inversions = [self.NO_INVERT] * self.NUM_GPIO 
        self.modes = [self.GPIO_OUT] * self.NUM_GPIO # These are the mode settings for each pin
        self.out_statuses = [self.GPIO_LO] * self.NUM_GPIO  # These are the output settings for each pin
        self.in_statuses = [self.GPIO_LO] * self.NUM_GPIO # These are the input settings for each pin

    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """!
        Determine if a Qwiic GPIO device is connected to the system.

        @return **bool** True if the device is connected, otherwise False.
        """
        return self._i2c.is_device_connected(self.address)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board. 
    def begin(self):
        """!
        Initialize the operation of the Qwiic GPIO

        @return **bool** Returns true of the initializtion was successful, otherwise False.
        """
        
        return self.is_connected()

    #----------------------------------------------------------------
    # set_mode()
    #
    # Set the mode (input/output) for all GPIO
    def set_mode(self):
        """!
        Sends all 8 pin modes (input or output) to the GPIO to set all 8 pins. Setting the value to input or output is done using my_gpio.modes[0] = my_gpio.GPIO_OUT

        @return  No return value
        """
        temp_data = 0

        for i in range (self.NUM_GPIO):
            temp_data |= self.modes[i] << i

        self._i2c.write_byte(self.address, self.REG_CONFIGURATION, temp_data)

    #----------------------------------------------------------------
    # get_mode()
    #
    # Get the mode (input/output) for all GPIO
    def get_mode(self):
        """!
        Updates mode_X variables with values from Qwiic GPIO

        @return **8 bit unsigned integer** The value of the mode register.
        """
        temp_data = self._i2c.read_byte(self.address, self.REG_CONFIGURATION)

        for i in range(self.NUM_GPIO):
            self.modes[i] = (temp_data & (1 << i)) >> i
        
        return temp_data

    #----------------------------------------------------------------
    # set_inversion()
    # 
    # Set whether a GPIO will invert an incoming signal

    def set_inversion(self):
        """!
        Send the inversion modes of all pins. This function must be called after editing modes using my_gpio.inversions[0] = my_gpio.INVERT

        @return  No return value
        """
        temp_data = 0

        for i in range(self.NUM_GPIO):
            temp_data |= self.inversions[i] << i

        self._i2c.write_byte(self.address, self.REG_INVERSION, temp_data)

    #----------------------------------------------------------------
    # get_inversion()
    # 
    # Get inversion settings from each GPIO.

    def get_inversion(self):
        """!
        Updates inversion_X variables with values from Qwiic GPIO

        @return **8 bit unsigned integer** The value of the inversion register.
        """
        temp_data = self._i2c.read_byte(self.address, self.REG_INVERSION)

        for i in range(self.NUM_GPIO):
            self.inversions[i] = (temp_data & (1 << i)) >> i

        return temp_data

    #----------------------------------------------------------------
    # set_gpio()
    # 
    # Sends all GPIO outputs to the Qwiic GPIO 

    def set_gpio(self):
        """!
        Send all current output settings to the GPIO. This should be called after calling my_gpio.out_statuses[0] = my_gpio.GPIO_HI to set the GPIO.

        @return  No return value
        """
        temp_data = 0

        for i in range(self.NUM_GPIO):
            temp_data |= self.out_statuses[i] << i

        self._i2c.write_byte(self.address, self.REG_OUTPUT_PORT, temp_data)

    def get_gpio(self):
        """!
        Updates mode_X variables with values from Qwiic GPIO

        @return **8 bit unsigned integer** The value of the mode register.
        """
        temp_data = self._i2c.read_byte(self.address, self.REG_INPUT_PORT)

        for i in range(self.NUM_GPIO):
            self.in_statuses[i] = (temp_data & (1 << i)) >> i

        return temp_data
    
    def pin_mode (self, pin, mode):
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
        self.set_mode()
    
    def pin_mode_port (self, gpio_pin_mode_list):
        """!
        Set the mode of a list of pins.

        @param gpio_pin_mode_list: A list of boolean modes to set the pins at each index to.

        @return  No return value
        """

        if len(gpio_pin_mode_list) != 8:
            return
        
        self.modes = gpio_pin_mode_list
        self.set_mode()
    
    def invert_pin(self, pin, invert):
        """!
        Set the inversion of a single pin.

        @param pin: The pin number to set the inversion of.
        @param invert: The inversion to set the pin to.

        @return  No return value
        """
        if pin < 0 or pin > 7:
            return
        
        self.inversions[pin] = invert
        self.set_inversion()
    
    def invert_pin_port (self, gpio_inversion_list):
        """!
        Set the inversion of a list of pins.

        @param gpio_inversion_list: A list of boolean inversions to set the pins at each index to.

        @return  No return value
        """

        if len(gpio_inversion_list) != 8:
            return
        
        self.inversions = gpio_inversion_list
        self.set_inversion()
    
    def digital_write(self, pin, value):
        """!
        Set the output value of a single pin.

        @param pin: The pin number to set the output value of.
        @param value: The value to set the pin to.

        @return  No return value
        """
        if pin < 0 or pin > 7:
            return
        
        self.out_statuses[pin] = value
        self.set_gpio()
    
    def digital_write_port (self, gpio_output_list):
        """!
        Set the output value of a list of pins.

        @param gpio_output_list: A list of boolean output values to set the pins at each index to.

        @return  No return value
        """

        if len(gpio_output_list) != 8:
            return
        
        self.out_statuses = gpio_output_list
        self.set_gpio()

    def digital_read(self, pin):
        """!
        Get the input value of a single pin.

        @param pin: The pin number to get the input value of.

        @return **bool** The value of the pin.
        """
        if pin < 0 or pin > 7:
            return
        
        self.get_gpio()
        return self.in_statuses[pin]
    
    def digital_read_port (self):
        """!
        Get the input value of all pins.

        @return  A list of boolean input values of all pins.
        """
        self.get_gpio()
        return self.in_statuses