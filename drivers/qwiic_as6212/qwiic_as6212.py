#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_as6212.py
#
# Python module for the AS6212 Digital Temperature Sensor Qwiic
# 
#------------------------------------------------------------------------
#
# Written by Pete Lewis, SparkFun Electronics, Aug 2021
# 
# Thanks to Alex Wende and Lori Croster @ SparkFun Electronics
# for code examples from TMP102 Python Package, May 2021
# (https://github.com/sparkfun/Qwiic_TMP102_Py)
#
# Thanks to Brandon Williams. This library was based off his 
# original library created 07/15/2020 and can be found here:
# https://github.com/will2055/AS6212-Arduino-Library/
#
# Thanks to Madison Chodikov @ SparkFun Electronics
# for code examples from TMP117 Arduino Library
# (https://github.com/sparkfun/SparkFun_TMP117_Arduino_Library)
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
# Copyright (c) 2021 SparkFun Electronics
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

"""
qwiic_as6212
============
Python module for the [SparkFun Digital Temperature Sensor Breakout - AS6212 (Qwiic)](https://www.sparkfun.com/products/18521)

This python package is a port of the existing [SparkFun AS6212 Qwiic Arduino Library](https://github.com/sparkfun/SparkFun_AS6212_Qwiic_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""
import qwiic_i2c

__version__ = "3.0.0"

#======================================================================
# Basic setup of I2C commands and available I2C Addresses
#
#
# The name of this device - note this is private
_DEFAULT_NAME = "Qwiic AS6212 Sensor"

AS6212_DEFAULT_ADDRESS = 0x48

#Internal Register Addresses
TVAL_REG      =       0x0    #Temperature Register
CONFIG_REG    =       0x1    #Configuration Register
TLOW_REG      =       0x2    #Low Temperature Threshold
THIGH_REG     =       0x3    #High Temperature Threshold

#Helpful preset definitions for configuration register
DEFAULTM  =       0x40A0   #Default state
SLEEPMODE =       0x41A0   #Sleep Mode
SLEEPSS   =       0xC1A0   #Sleep Mode Single Shot

# Register values (MSB -> LSB)
SINGLESHOT	=	0x8000	#15
CFAULT_1		=	0x0800	#12
CFAULT_0		=	0x0400	#11
POLARITY		=	0x0200	#10
INTERRUPT		=	0x0100	#9
SLEEP			=	0x0080	#8
CONVER_RATE_1 =	0x0040	#7
CONVER_RATE_0 =	0x0020	#6
ALERT			=	0x0010	#5

AS6212_RESOLUTION = 0.0078125

AS6212_CONFIG_BIT_ALERT = 5
AS6212_CONFIG_BIT_CONVERSION_RATE_0 = 6
AS6212_CONFIG_BIT_CONVERSION_RATE_1 = 7
AS6212_CONFIG_BIT_SLEEP_MODE = 8
AS6212_CONFIG_BIT_INTERRUPT_MODE = 9
AS6212_CONFIG_BIT_ALERT_POL = 10
AS6212_CONFIG_BIT_CONSECUTIVE_FAULTS_0 = 11
AS6212_CONFIG_BIT_CONSECUTIVE_FAULTS_1 = 12
AS6212_CONFIG_BIT_SINGLE_SHOT = 15

#Address can be set using jumpers on bottom of board (default: 0x48)
_AVAILABLE_I2C_ADDRESS = [0x48, 0x44, 0x45, 0x46, 0x47, 0x49, 0x4A, 0x4B]

###############################################################################
###############################################################################
# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.

class QwiicAS6212(object):
    """
    QwiicAS6212

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.
        :return: The AS6212 Sensor device object.
        :rtype: Object
    """
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    AS6212_MODE_COMPARATOR = 0
    AS6212_MODE_INTERRUPT = 1

    AS6212_CONVERSION_CYCLE_TIME_125MS = 3
    AS6212_CONVERSION_CYCLE_TIME_250MS = 2
    AS6212_CONVERSION_CYCLE_TIME_1000MS = 1
    AS6212_CONVERSION_CYCLE_TIME_4000MS = 0

    AS6212_ALERT_ACTIVE_HIGH = 1
    AS6212_ALERT_ACTIVE_LOW = 0

    # Constructor
    def __init__(self, address=None, i2c_bus=None):

        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address?
        self.address = self.available_addresses[0] if address is None else address

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """
            Determine if an AS6212 device is connected to the system.
            :return: True if the device is connected, otherwise False.
            :rtype: bool
        """        
        return qwiic_i2c.is_device_connected(self.address)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """
            Initialize the operation of the AS6212 module
            :return: Returns true of the initialization was successful, otherwise False.
            :rtype: bool
        """
        # Set variables
        self.temp_c = 0
        self.temp_f = 0

        # Basically return True if we are connected...
        return self.is_connected()

    #****************************************************************************#
    #
    #   Sensor functions
    #
    # ****************************************************************************#
    def get_address(self):
        """
        Returns the device address
        """
        return self.address

    def read_2_byte_register(self, register_to_read):
        """
        Reads two bytes of data from a desired register.
        Combines them into a single 16 bit value
        Returns single value
        """
        data = self._i2c.read_block(self.address, register_to_read, 2)

        #Combine bytes to create a single signed int
        return ( (data[0] << 8 ) | data[1] )

    def write_register(self, reg, data):
        data_bytes = [0,0]
        data_bytes[1] |= (data & 0xFF)
        data_bytes[0] |= data >> 8
        self._i2c.write_block(self.address, reg, data_bytes)

    def read_config(self):
        return self.read_2_byte_register(CONFIG_REG)

    def write_config(self, target_state):
        self.write_register(CONFIG_REG, target_state)
        
    def read_temp_c(self):
        """
        Reads the results from the sensor
        :return: The temperature in degrees Celsius
        :rtype: float
        """
        digital_temp_c = self.read_2_byte_register(TVAL_REG)

        if (digital_temp_c < 32768):
                final_temp_c = digital_temp_c * 0.0078125
        if (digital_temp_c >= 32768):
                final_temp_c = ((digital_temp_c - 1) * 0.0078125) * -1

        self.temp_c = final_temp_c
        return self.temp_c
        
    def read_temp_f(self):
        """
        Reads the results from the sensor
        :return: The temperature in degrees Fahrenheit
        :rtype: float
        """

        self.temp_f = self.read_temp_c() * 9.0 / 5.0 + 32.0
        return self.temp_f

    def set_alert_polarity(self, polarity):
        """
        Set the polarity of Alert
        AS6212_ALERT_ACTIVE_HIGH (1)
        AS6212_ALERT_ACTIVE_LOW (0)
        """
        config_reg = self.read_config()
        config_reg = self.bit_write(config_reg, AS6212_CONFIG_BIT_ALERT_POL, polarity)        
        self.write_config(config_reg)
        
    def get_alert_polarity(self):
        """
        Get the polarity of Alert
        AS6212_ALERT_ACTIVE_HIGH (1)
        AS6212_ALERT_ACTIVE_LOW (0)
        """
        config_reg = self.read_config()
        return self.bit_read(config_reg, AS6212_CONFIG_BIT_ALERT_POL)            

    def set_interrupt_mode(self, mode):
        """
        sets the interrupt mode bits in the config register

        valid options are:
        AS6212_MODE_COMPARATOR (0)
        AS6212_MODE_INTERRUPT (1)
        """
        config_reg = self.read_config()
        config_reg = self.bit_write(config_reg, AS6212_CONFIG_BIT_INTERRUPT_MODE, mode)        
        self.write_config(config_reg)

    def get_interrupt_mode(self):
        """
        Get the interrupt mode bit
        AS6212_MODE_COMPARATOR (0)
        AS6212_MODE_INTERRUPT (1)
        """
        config_reg = self.read_config()
        return self.bit_read(config_reg, AS6212_CONFIG_BIT_INTERRUPT_MODE)

    def get_alert_status(self):
        """
        Get the status of the alert bit (0 or 1)
        """
        config_reg = self.read_config()
        return self.bit_read(config_reg, AS6212_CONFIG_BIT_ALERT)              

    def set_consecutive_faults(self, faults):
        """
	    Set the number of consecutive faults
	    1 - 1 fault
	    2 - 2 faults
	    3 - 3 faults
	    4 - 4 faults
        """
        if (faults > 4) or (faults < 1):
            return NaN  # noqa: F821
        faults = faults - 1 # consecutive faults value is stored in just 2 bits in the config reg,
        # so we must convert from "human readable" ints 1-4 to stored values (0-3).
        config_reg = self.read_config()
        config_bit_11 = self.bit_read(faults, 0)
        config_bit_12 = self.bit_read(faults, 1)
        config_reg = self.bit_write(config_reg, AS6212_CONFIG_BIT_CONSECUTIVE_FAULTS_0, config_bit_11)
        config_reg = self.bit_write(config_reg, AS6212_CONFIG_BIT_CONSECUTIVE_FAULTS_1, config_bit_12)
        self.write_config(config_reg)

    def get_consecutive_faults(self):
        """
                Gets the number of consecutive faults that need to happen in a row before alert is changed.
                valid settings are 1,2,3 or 4 but this correspond to other bit values
                in the configuration register bits 11 and 12
        """
        config_reg = self.read_config()
        consecutive_faults_bit_0 = self.bit_read(config_reg, AS6212_CONFIG_BIT_CONSECUTIVE_FAULTS_0)
        consecutive_faults_bit_1 = self.bit_read(config_reg, AS6212_CONFIG_BIT_CONSECUTIVE_FAULTS_1)
        faults = 0
        faults = self.bit_write(faults, 0, consecutive_faults_bit_0)
        faults = self.bit_write(faults, 1, consecutive_faults_bit_1)
        faults = ( faults + 1 ) # consecutive faults is stored in just two bits in teh config reg
        # so we must +1 to make it the stored values (0-3) human readable (1-4)
        return faults

    def set_conversion_cycletime(self, cycletime):
        """
        sets the conversion cylce time (aka convertion rate) in the config register
        valid settings are:
        
        AS6212_CONVERSION_CYCLE_TIME_125MS
        AS6212_CONVERSION_CYCLE_TIME_250MS
        AS6212_CONVERSION_CYCLE_TIME_1000MS
        AS6212_CONVERSION_CYCLE_TIME_4000MS
        """
        #discard out of range values
        if cycletime > 3 or cycletime < 0:
            return nan  # noqa: F821
        config_reg = self.read_config()
        config_bit_6 = self.bit_read(cycletime, 0)
        config_bit_7 = self.bit_read(cycletime, 1)
        config_reg = self.bit_write(config_reg, AS6212_CONFIG_BIT_CONVERSION_RATE_0, config_bit_6)
        config_reg = self.bit_write(config_reg, AS6212_CONFIG_BIT_CONVERSION_RATE_1, config_bit_7)
        self.write_config(config_reg)
        
    def get_conversion_cycletime(self):
        """
                Gets the conversion cycle time (aka conversion rate) in teh config reg
                Returns the cycle time in milliseconds: (125/250/1000/4000)
        """
        config_reg = self.read_config()
        conversion_rate_bit_0 = self.bit_read(config_reg, AS6212_CONFIG_BIT_CONVERSION_RATE_0)
        conversion_rate_bit_1 = self.bit_read(config_reg, AS6212_CONFIG_BIT_CONVERSION_RATE_1)
        cycletime_val = 0
        cycletime_val = self.bit_write(cycletime_val, 0, conversion_rate_bit_0)
        cyceltime_val = self.bit_write(cycletime_val, 1, conversion_rate_bit_1)
        if cycletime_val == AS6212_CONVERSION_CYCLE_TIME_125MS:  # noqa: F821
            return 125
        if cycletime_val == AS6212_CONVERSION_CYCLE_TIME_250MS:  # noqa: F821
            return 250
        if cycletime_val == AS6212_CONVERSION_CYCLE_TIME_1000MS:  # noqa: F821
            return 1000
        if cycletime_val == AS6212_CONVERSION_CYCLE_TIME_4000MS:  # noqa: F821
            return 4000
      
    def set_sleep_mode(self, mode):
        """
                sets the sleep mode bit (on or off) in the config register

                valid options are:
                0 = SLEEP MODE OFF
                1 = SLEEP MODE ON
        """
        config_reg = self.read_config()
        config_reg = self.bit_write(config_reg, AS6212_CONFIG_BIT_SLEEP_MODE, mode)
        if mode == 1: # as recommended in datasheet section 6.2.4
            config_reg = self.bit_write(config_reg, AS6212_CONFIG_BIT_SINGLE_SHOT, 1)
        self.write_config(config_reg)

    def get_sleep_mode(self):
        """
        gets the status of the sleep mode bit from the config register
        """
        config_reg = self.read_config()
        return self.bit_read(config_reg, AS6212_CONFIG_BIT_SLEEP_MODE)

    def trigger_single_shot_conversion(self):
        """
                Sets the SS mode bit in the config register
                Note, you must be in sleep mode for this to work
        """
        config_reg = self.read_config()
        if self.bit_read(config_reg, AS6212_CONFIG_BIT_SLEEP_MODE) == 1:
            config_reg = self.bit_write(config_reg, AS6212_CONFIG_BIT_SINGLE_SHOT, 1)
            self.write_config(config_reg)

    def get_single_shot_status(self):
        """
        gets the status of the single shot bit from the config register
        0 = No conversion ongoing / conversion finished
        1 = Start single shot conversion / conversion ongoing
        """
        config_reg = self.read_config()
        return self.bit_read(config_reg, AS6212_CONFIG_BIT_SINGLE_SHOT)

    def set_low_temp_c(self, temperature):
        """
        Sets T_LOW (degrees C) alert threshold
        """
        if temperature >= 0: # positive number or zero
            low_temp = int(temperature / 0.0078125)
        if temperature < 0: #negative number
            temperature /= 0.0078125
            temp_int = int(temperature)
            temp_int &= 0xFFFF
            low_temp = ( ~(temp_int) + 1 ) * -1
        self.write_register(TLOW_REG, low_temp)
        

    def set_high_temp_c(self, temperature):
        """
        Sets THIGH (degrees C) alert threshold
        """
        if temperature >= 0: # positive number or zero
            high_temp = int(temperature / 0.0078125)
        if temperature < 0: #negative number
            temperature /= 0.0078125
            temp_int = int(temperature)
            temp_int &= 0xFFFF
            high_temp = ( ~(temp_int) + 1 ) * -1
        self.write_register(THIGH_REG, high_temp)
        
    def set_low_temp_f(self, temperature):
        """
        Sets T_LOW (degrees F) alert threshold
        """
        new_temp = (temperature - 32)*5/9    # Convert temperature to C
        self.set_low_temp_c(new_temp)           # Set T_LOW

        
    def set_high_temp_f(self, temperature):
        """
        Sets T_HIGH (degrees F) alert threshold
        """
        new_temp = (temperature - 32)*5/9    # Convert temperature to C
        self.set_high_temp_c(new_temp)           # Set T_HIGH

    def read_low_temp_c(self):
        """
        Gets T_LOW (degrees C) alert threshold
        """
        digital_temp = self.read_2_byte_register(TLOW_REG)
        if (digital_temp < 32768):
                final_temp_c = float(digital_temp) * 0.0078125
        if (digital_temp >= 32768):
                digital_temp = ~digital_temp
                digital_temp &= 0xFFFF
                final_temp_c = (( digital_temp + 1 ) * 0.0078125) * -1
        return final_temp_c       
         
    def read_high_temp_c(self):
        """
        Gets T_HIGH (degrees C) alert threshold
        """
        digital_temp = self.read_2_byte_register(THIGH_REG)
        if (digital_temp < 32768):
                final_temp_c = digital_temp * 0.0078125
        if (digital_temp >= 32768):
                digital_temp = ~digital_temp
                digital_temp &= 0xFFFF
                final_temp_c = (( digital_temp + 1 ) * 0.0078125) * -1
        return final_temp_c  

    def read_low_temp_f(self):
        """
        Reads T_LOW register in F
        """
        return self.read_low_temp_c()*9.0/5.0 + 32.0
        
    def read_high_temp_f(self):
        """
        Reads T_HIGH register in F		
        """
        
        return self.read_high_temp_c()*9.0/5.0 + 32.0

    def bit_read(self, value, bit):
        return (((value) >> (bit)) & 0x01)

    def bit_set(self, value, bit):
        return ((value) | (1 << (bit)))

    def bit_clear(self, value, bit):
        return ((value) & ~(1 << (bit)))

    def bit_write(self, value, bit, bitvalue):
        if (bitvalue == 1):
            return self.bit_set(value, bit)
        if (bitvalue == 0):
            return self.bit_clear(value, bit)
    
    def get_config_binary(self):
        """
        Returns the configuration register as a binary string, MSB first,
        with a space between the two bytes (for example "01000000 10100000")
        """
        return self.format_binary(self.read_config())

    def format_binary(self, data):
        """
        Returns a 16-bit value as a binary string, MSB first,
        with a space between the two bytes
        """
        data_bin = ""
        for i in range(15, -1, -1):
            data_bin += str(self.bit_read(data, i))
            if i == 8:
                data_bin += " "
        return data_bin        