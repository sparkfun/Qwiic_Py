#-------------------------------------------------------------------------------
# qwiic_cap1203.py
#
# Python library for the SparkFun Qwiic Capacitive Touch Slider, available here:
# https://www.sparkfun.com/products/15344
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2023
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
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
#===============================================================================
# This code was generated in part with ChatGPT, created by OpenAI. The code was
# reviewed and edited by the following human(s):
#
# Dryw Wade
#===============================================================================

"""!
qwiic_cap1203
============
Python module for the [SparkFun Qwiic Capacitive Touch Slider](https://www.sparkfun.com/products/15344)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_CAP1203_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c
import time

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic CAP1203"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x28]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicCAP1203(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # CAP1203 Registers as defined in Table 5-1 from datasheet (pg 20-21)
    MAIN_CONTROL = 0x00
    GENERAL_STATUS = 0x02
    SENSOR_INPUT_STATUS = 0x03
    NOISE_FLAG_STATUS = 0x0A
    SENSOR_INPUT_1_DELTA_COUNT = 0x10
    SENSOR_INPUT_2_DELTA_COUNT = 0X11
    SENSOR_INPUT_3_DELTA_COUNT = 0X12
    SENSITIVITY_CONTROL = 0x1F
    CONFIG = 0x20
    SENSOR_INPUT_ENABLE = 0x21
    SENSOR_INPUT_CONFIG = 0x22
    SENSOR_INPUT_CONFIG_2 = 0x23
    AVERAGING_AND_SAMPLE_CONFIG = 0x24
    CALIBRATION_ACTIVATE_AND_STATUS = 0x26
    INTERRUPT_ENABLE = 0x27
    REPEAT_RATE_ENABLE = 0x28
    MULTIPLE_TOUCH_CONFIG = 0x2A
    MULTIPLE_TOUCH_PATTERN_CONFIG = 0x2B
    MULTIPLE_TOUCH_PATTERN = 0x2D
    BASE_COUNT_OUT = 0x2E
    RECALIBRATION_CONFIG = 0x2F
    SENSOR_1_INPUT_THRESH = 0x30
    SENSOR_2_INPUT_THRESH = 0x31
    SENSOR_3_INPUT_THRESH = 0x32
    SENSOR_INPUT_NOISE_THRESH = 0x38
    STANDBY_CHANNEL = 0x40
    STANDBY_CONFIG = 0x41
    STANDBY_SENSITIVITY = 0x42
    STANDBY_THRESH = 0x43
    CONFIG_2 = 0x44
    SENSOR_INPUT_1_BASE_COUNT = 0x50
    SENSOR_INPUT_2_BASE_COUNT = 0x51
    SENSOR_INPUT_3_BASE_COUNT = 0x52
    POWER_BUTTON = 0x60
    POWER_BUTTON_CONFIG = 0x61
    SENSOR_INPUT_1_CALIBRATION = 0xB1
    SENSOR_INPUT_2_CALIBRATION = 0xB2
    SENSOR_INPUT_3_CALIBRATION = 0xB3
    SENSOR_INPUT_CALIBRATION_LSB_1 = 0xB9
    PROD_ID = 0xFD
    MANUFACTURE_ID = 0xFE
    REVISION = 0xFF

    # Product ID - always the same (pg. 22)
    PROD_ID_VALUE = 0x6D

    # Capacitive sensor input (pg. 23)
    OFF = 0x00  # No touch detected
    ON = 0x01   # Check capacitive sensor input (pg. 23)

    # Pads to be power button (pg. 43)
    PWR_CS1 = 0x00  # Pad 1 (Left)
    PWR_CS2 = 0x01  # Pad 2 (Middle)
    PWR_CS3 = 0x02  # Pad 3 (Right)

    PAD_LEFT = PWR_CS1
    PAD_MIDDLE = PWR_CS2
    PAD_RIGHT = PWR_CS3

    # Power button hold time to generate interrupt (pg. 44)
    PWR_TIME_280_MS = 0x00   # 280 ms
    PWR_TIME_560_MS = 0x01   # 560 ms
    PWR_TIME_1120_MS = 0x02  # 1.12 sec
    PWR_TIME_2240_MS = 0x03  # 2.24 sec

    # Sensitivity for touch detection (pg. 25)
    SENSITIVITY_128X = 0x00  # Most sensitive
    SENSITIVITY_64X = 0x01
    SENSITIVITY_32X = 0x02
    SENSITIVITY_16X = 0x03
    SENSITIVITY_8X = 0x04
    SENSITIVITY_4X = 0x05
    SENSITIVITY_2X = 0x06
    SENSITIVITY_1X = 0x07  # Least sensitive

    def __init__(self, address=None, i2c_driver=None):
        """!
        Constructor

        @param int, optional address: The I2C address to use for the device
            If not provided, the default address is used
        @param I2CDriver, optional i2c_driver: An existing i2c driver object
            If not provided, a driver object is created
        """

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

        # TODO: Initialize any variables used by this driver

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        if(not self._i2c.isDeviceConnected(self.address)):
            return False
        
        # Something ACK'd, check if the product ID is correct
        prodid = self._i2c.readByte(self.address, self.PROD_ID)
        return prodid == self.PROD_ID_VALUE

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        self.set_sensitivity(self.SENSITIVITY_2X) # Set sensitivity to 2x on startup - value calibrated for SparkFun CAP1203 Cap Touch Slider Board
        self.set_interrupt_enabled()              # Enable INT and LED as default
        self.clear_interrupt()                    # Clear interrupt on startup
        return True

    def check_main_control(self):
        """!
        Control the primary power state of the device. See data sheet
        on Main Control Register (pg. 22).

        @return **int** Main Control Register value
        """
        self._i2c.readByte(self.address, self.MAIN_CONTROL)

    def check_status(self):
        """!
        Checks inputs in the general status register to ensure program
        is set up correctly. See data sheet on Status Registers (pg. 23).

        @return **int** General Status Register value
        """
        self._i2c.readByte(self.address, self.GENERAL_STATUS)

    def clear_interrupt(self):
        """!
        Clears the interrupt (INT) bit by writing a logic 0 to it.
        This bit must be cleared in order to detec a new capacitive
        touch input. See datasheet on Main Control Register (pg. 22).
        """
        reg = self._i2c.readByte(self.address, self.MAIN_CONTROL)
        reg &= 0xFE
        self._i2c.writeByte(self.address, self.MAIN_CONTROL, reg)

    def set_interrupt_disabled(self):
        """!
        This disables all the interrupts, so the alert LED will not turn on
        when a sensor is touched. Set on default in begin function See data 
        sheet on Interrupt Enable Register (pg. 33).
        """
        reg = self._i2c.readByte(self.address, self.INTERRUPT_ENABLE)
        reg &= 0xF8
        self._i2c.writeByte(self.address, self.INTERRUPT_ENABLE, reg)

    def set_interrupt_enabled(self):
        """!
        This turns on all the interrupts, so the alert LED turns on when any 
        sensor is touched. See data sheet on Interrupt Enable Register (pg. 33).
        """
        reg = self._i2c.readByte(self.address, self.INTERRUPT_ENABLE)
        reg |= 0x07
        self._i2c.writeByte(self.address, self.INTERRUPT_ENABLE, reg)

    def is_interrupt_enabled(self):
        """!
        Returns state of intterupt pin. Returns true if all interrupts enabled 
        (0x07), otherwise returns false. When the interrupts are enabled, the 
        LED on the CAP1203 Touch Slider Board turns on when it detects a touch 
        (pg. 33).

        @return **bool** `True` if enabled, otherwise `False`
        """
        reg = self._i2c.readByte(self.address, self.INTERRUPT_ENABLE)
        if (reg & 0x07) == 0x07:
            return True
        return False

    def set_sensitivity(self, sensitivity):
        """!
        Sensitivity calibrated for SparkFun Capacitive Touch Slider. You may 
        want to change sensitivity settings if creating your own capacitive 
        touch pads. See datasheet on Sensitivity Control Register (pg. 25).

        @param int sensitivity: Sensitivity multiplier
        """
        reg = self._i2c.readByte(self.address, self.SENSITIVITY_CONTROL)
        reg &= 0x8F
        if sensitivity >= self.SENSITIVITY_128X and sensitivity <= self.SENSITIVITY_1X:
            reg |= sensitivity << 4
        else:
            # Default case: calibrated for CAP1203 touch sensor
            reg |= self.SENSITIVITY_2X << 4
        self._i2c.writeByte(self.address, self.SENSITIVITY_CONTROL, reg)

    def get_sensitivity(self):
        """!
        Returns the sensitivity multiplier for current sensitivity settings
        (pg. 25).

        @return **int** Sensitivity multiplier
        """
        reg = self._i2c.readByte(self.address, self.SENSITIVITY_CONTROL)
        sensitivity = (reg >> 4) & 0x07
        if sensitivity == self.SENSITIVITY_128X:
            return 128
        elif sensitivity == self.SENSITIVITY_64X:
            return 64
        elif sensitivity == self.SENSITIVITY_32X:
            return 32
        elif sensitivity == self.SENSITIVITY_16X:
            return 16
        elif sensitivity == self.SENSITIVITY_8X:
            return 8
        elif sensitivity == self.SENSITIVITY_4X:
            return 4
        elif sensitivity == self.SENSITIVITY_2X:
            return 2
        elif sensitivity == self.SENSITIVITY_1X:
            return 1
        else:
            # Error - no possible register value (pg. 25)
            return 0
        
    def is_left_touched(self):
        """!
        Checks if touch input detected on left sensor (pad 1). Need to clear
        interrupt pin after touch occurs. See datasheet on Sensor Interrupt 
        Status Reg (pg.23).

        @return **bool** `True` if left sensor is touched, otherwise `False`
        """
        reg = self._i2c.readByte(self.address, self.SENSOR_INPUT_STATUS)

        # Touch detected
        if ((reg >> 0) & 0x01) == self.ON:
            self.clear_interrupt()
            return True
        return False

    def is_middle_touched(self):
        """!
        Checks if touch input detected on left sensor (pad 2). Need to clear
        interrupt pin after touch occurs. See datasheet on Sensor Interrupt 
        Status Reg (pg.23).

        @return **bool** `True` if middle sensor is touched, otherwise `False`
        """
        reg = self._i2c.readByte(self.address, self.SENSOR_INPUT_STATUS)

        # Touch detected
        if ((reg >> 1) & 0x01) == self.ON:
            self.clear_interrupt()
            return True
        return False

    def is_right_touched(self):
        """!
        Checks if touch input detected on left sensor (pad 3). Need to clear
        interrupt pin after touch occurs. See datasheet on Sensor Interrupt 
        Status Reg (pg.23).

        @return **bool** `True` if right sensor is touched, otherwise `False`
        """
        reg = self._i2c.readByte(self.address, self.SENSOR_INPUT_STATUS)

        # Touch detected
        if ((reg >> 2) & 0x01) == self.ON:
            self.clear_interrupt()
            return True
        return False

    def is_touched(self):
        """!
        Checks if touch input detected on any sensor. Need to clear
        interrupt pin after touch occurs. See datasheet on Sensor Interrupt 
        Status (pg.23).

        @return **bool** `True` if any sensor is touched, otherwise `False`
        """
        reg = self._i2c.readByte(self.address, self.GENERAL_STATUS)

        # Touch detected
        if ((reg >> 0) & 0x01) == self.ON:
            self.clear_interrupt()
            return True
        return False

    def is_right_swipe_pulled(self):
        """!
        Checks if a right swipe occured on the board. This method
        takes up all functionality due to implementation of 
        while loop with millis().

        @return **bool** `True` if right swipe occured, otherwise `False`
        """
        swipe = False  # Tracks if conditions are being met
        start_time = self.millis()

        # LEFT TOUCH CONDITION
        while (self.millis() - start_time) < 100:
            if self.is_left_touched():
                swipe = True
                while self.is_left_touched():
                    pass  # Wait for user to remove their finger
                break  # Break out of loop

        # Return if left not touched
        if not swipe:
            return False

        start_time = self.millis()  # Reset start time
        swipe = False  # Reset check statement

        # MIDDLE TOUCH CONDITION
        while (self.millis() - start_time) < 100:
            if self.is_middle_touched():
                swipe = True
                while self.is_middle_touched():
                    pass  # Wait for user to remove their finger
                break  # Break out of loop

        # Return if middle not touched
        if not swipe:
            return False

        start_time = self.millis()  # Reset start time
        swipe = False  # Reset check statement

        # RIGHT TOUCH CONDITION
        while (self.millis() - start_time) < 100:
            if self.is_right_touched():
                return True

        return False

    def is_left_swipe_pulled(self):
        """!
        Checks if a left swipe occured on the board. This method
        takes up all functionality due to implementation of 
        while loop with millis().

        @return **bool** `True` if left swipe occured, otherwise `False`
        """
        swipe = False  # Tracks if conditions are being met
        start_time = self.millis()

        # RIGHT TOUCH CONDITION
        while (self.millis() - start_time) < 100:
            if self.is_right_touched():
                swipe = True
                while self.is_right_touched():
                    pass  # Wait for user to remove their finger
                break  # Break out of loop

        # Return if right not touched
        if not swipe:
            return False

        start_time = self.millis()  # Reset start time
        swipe = False  # Reset check statement

        # MIDDLE TOUCH CONDITION
        while (self.millis() - start_time) < 100:
            if self.is_middle_touched():
                swipe = True
                while self.is_middle_touched():
                    pass  # Wait for user to remove their finger
                break  # Break out of loop

        # Return if middle not touched
        if not swipe:
            return False

        start_time = self.millis()  # Reset start time
        swipe = False  # Reset check statement

        # LEFT TOUCH CONDITION
        while (self.millis() - start_time) < 100:
            if self.is_left_touched():
                return True

        return False

    def set_power_button_pad(self, pad):
        """!
        Sets a specific pad to act as a power button. Function takes in which 
        pad to set as power button. See datasheet on Power Button (pg. 16).

        @param int pad: Pad to be set as power button

        @return **bool** `True` if successful, otherwise `False`
        """
        reg = self._i2c.readByte(self.address, self.POWER_BUTTON)
        reg &= 0xF8

        # Set pad to act as power button (pg. 43)
        if pad == self.PAD_LEFT:
            reg |= self.PWR_CS1
        elif pad == self.PAD_MIDDLE:
            reg |= self.PWR_CS2
        elif pad == self.PAD_RIGHT:
            reg |= self.PWR_CS3
        else:
            # User input invalid pad number
            return False
        self._i2c.writeByte(self.address, self.POWER_BUTTON, reg)
        return True

    def get_power_button_pad(self):
        """!
        Returns which capacitive touch pad is currently set to act
        as a power button.
        
        Add 1 to return value so value matches pad number.
        See data sheet on Power Button (pg. 44)
            REG VALUE   PAD
            0x00        1
            0x01        2
            0x02        3

        @return **int** Pad number set as power button
        """
        reg = self._i2c.readByte(self.address, self.POWER_BUTTON)

        return (reg & 0x07) + 1

    def set_power_button_time(self, input_time):
        """!
        Configure the length of time that the designated power button
        must indicate a touch before an interrupt is generated and the
        power status indicator is set. See data sheet on Power Button
        Configuration Register (pg. 43). 
        
        Possible inputs (represent time in ms): 280, 560, 1120, 2240

        @param int input_time: Power button input time

        @return **bool** `True` if successful, otherwise `False`
        """
        reg = self._i2c.readByte(self.address, self.POWER_BUTTON_CONFIG)
        reg &= 0xFC
        if input_time >= self.PWR_TIME_280_MS and input_time <= self.PWR_TIME_2240_MS:
            reg |= input_time & 0x03
        else:
            # User input invalid time
            return False
        self._i2c.writeByte(self.address, self.POWER_BUTTON_CONFIG, reg)
        return True

    def get_power_button_time(self):
        """!
        Returns the length of the time designated time power button must 
        indicate a touch before an interrupt is generated. 
        
        See data sheet on Power Button Time (pg. 44)
            REG VALUE   TIME
            0x00        280 MS
            0x01        560 MS
            0x02        1120 MS
            0x03        2240 MS
        
        @return **int** Time in milliseconds
        """
        reg = self._i2c.readByte(self.address, self.POWER_BUTTON_CONFIG)
        if (reg & 0x03) == self.PWR_TIME_280_MS:
            return 280
        elif (reg & 0x03) == self.PWR_TIME_560_MS:
            return 560
        elif (reg & 0x03) == self.PWR_TIME_1120_MS:
            return 1120
        elif (reg & 0x03) == self.PWR_TIME_2240_MS:
            return 2240
        # Invalid data reading - check hook up
        return 0

    def set_power_button_enabled(self):
        """!
        Enables power button in active state. See data sheet on Power Button
        Configuration Register (pg. 43-44)
        """
        reg = self._i2c.readByte(self.address, self.POWER_BUTTON_CONFIG)
        reg |= 0x04
        self._i2c.writeByte(self.address, self.POWER_BUTTON_CONFIG, reg)

    def set_power_button_disabled(self):
        """!
        Disables power button in active state. See data sheet on Power Button
        Configuration Register (pg. 43-44)
        """
        reg = self._i2c.readByte(self.address, self.POWER_BUTTON_CONFIG)
        reg &= 0xFB
        self._i2c.writeByte(self.address, self.POWER_BUTTON_CONFIG, reg)

    def is_power_button_enabled(self):
        """!
        Returns state of power button. Returns true if enabled (reg. value is
        0x01), otherwise returns false. Power button must be ENABLED to use.
        See data sheet on Power Button Configuration Register (pg. 43-44).

        @return **bool** `True` if enabled, otherwise `False`
        """
        reg = self._i2c.readByte(self.address, self.POWER_BUTTON_CONFIG)
        if reg & 0x04 == 0x04:
            # Power button enabled
            return True
        # Power button disabled
        return False

    def is_power_button_touched(self):
        """!
        Once the power button has been held for designated time, an interrupt 
        is generated and PWR bit is set in the General Status Register. See 
        data sheet on Power Button (pg. 16), Power Button Register (pg. 43),
        and Power Button Configuration Register (pg. 43).

        @return **bool** `True` if power button is touched, otherwise `False`
        """
        reg = self._i2c.readByte(self.address, self.GENERAL_STATUS)
        if reg & 0x10 == 0x10:
            self.clear_interrupt()
            return True
        return False
    
    def millis(self):
        """!
        Get the current time in milliseconds

        @return **int** Current time in milliseconds
        """
        if hasattr(time, "ticks_ms"):
	        # MicroPython: time.time() gives an integer, instead use ticks_ms()
            return time.ticks_ms()
        else:
	        # Other platforms: time.time() gives a float
            return int(round(time.time() * 1000))