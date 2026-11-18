#-----------------------------------------------------------------------------
# SparkFun qwiic proximity sensor
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
#
# More information on qwiic is at https:www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
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
#
# This is mostly a port of existing Arduino functionaly, so pylint is sad.
# The goal is to keep the public interface pthonic, but internal is internal
#
# pylint: disable=line-too-long, bad-whitespace, invalid-name
# pylint: disable=too-many-public-methods, too-many-instance-attributes
#

"""
qwiic_proximity
================

Python module for the [SparkFun Qwiic Proximity Sensor Breakout](https://www.sparkfun.com/products/15177)

This python package is a port of the existing [SparkFun VCNL4040 Proximity Sensor Arduino Library](https://github.com/sparkfun/SparkFun_VCNL4040_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""

# load the i2c bus driver package
import qwiic_i2c

__version__ = "3.0.0"

#
# The name of this device
_DEFAULT_NAME = "Qwiic Proximity Sensor"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x60]


# Used to select between upper and lower byte of command register
LOWER = True
UPPER = False

# VCNL4040 Command Codes
VCNL4040_ALS_CONF = 0x00
VCNL4040_ALS_THDH = 0x01
VCNL4040_ALS_THDL = 0x02
VCNL4040_PS_CONF1 = 0x03 #Lower
VCNL4040_PS_CONF2 = 0x03 #Upper
VCNL4040_PS_CONF3 = 0x04 #Lower
VCNL4040_PS_MS = 0x04  #Upper
VCNL4040_PS_CANC = 0x05
VCNL4040_PS_THDL = 0x06
VCNL4040_PS_THDH = 0x07
VCNL4040_PS_DATA = 0x08
VCNL4040_ALS_DATA = 0x09
VCNL4040_WHITE_DATA = 0x0A
VCNL4040_INT_FLAG = 0x0B #Upper
VCNL4040_ID = 0x0C


class QwiicProximity(object):
    """
    QwiicProximity

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.
        :return: The Proximity device object.
        :rtype: Object
    """

    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Flags exposed in userspace - make these class vars
    VCNL4040_PS_INT_MASK = (~((1 << 1) | (1 << 0))) & 0xff
    VCNL4040_PS_INT_DISABLE = 0
    VCNL4040_PS_INT_CLOSE = (1 << 0)
    VCNL4040_PS_INT_AWAY = (1 << 1)
    VCNL4040_PS_INT_BOTH = (1 << 1) | (1 << 0)

    # Define commands/commandwords for the sensor
    VCNL4040_ALS_IT_MASK = (~((1 << 7) | (1 << 6))) & 0xff #uint8
    VCNL4040_ALS_IT_80MS = 0
    VCNL4040_ALS_IT_160MS = (1 << 7)
    VCNL4040_ALS_IT_320MS = (1 << 6)
    VCNL4040_ALS_IT_640MS = (1 << 7) | (1 << 6)

    VCNL4040_ALS_PERS_MASK = (~((1 << 3) | (1 << 2))) & 0xff
    VCNL4040_ALS_PERS_1 = 0
    VCNL4040_ALS_PERS_2 = (1 << 2)
    VCNL4040_ALS_PERS_4 = (1 << 3)
    VCNL4040_ALS_PERS_8 = (1 << 3) | (1 << 2)

    VCNL4040_ALS_INT_EN_MASK = (~(1 << 1)) & 0xff
    VCNL4040_ALS_INT_DISABLE = 0
    VCNL4040_ALS_INT_ENABLE = (1 << 1)

    VCNL4040_ALS_SD_MASK = (~(1 << 0)) & 0xff
    VCNL4040_ALS_SD_POWER_ON = 0
    VCNL4040_ALS_SD_POWER_OFF = (1 << 0)

    VCNL4040_PS_DUTY_MASK = (~((1 << 7) | (1 << 6))) & 0xff
    VCNL4040_PS_DUTY_40 = 0
    VCNL4040_PS_DUTY_80 = (1 << 6)
    VCNL4040_PS_DUTY_160 = (1 << 7)
    VCNL4040_PS_DUTY_320 = (1 << 7) | (1 << 6)

    VCNL4040_PS_PERS_MASK = (~((1 << 5) | (1 << 4))) & 0xff
    VCNL4040_PS_PERS_1 = 0
    VCNL4040_PS_PERS_2 = (1 << 4)
    VCNL4040_PS_PERS_3 = (1 << 5)
    VCNL4040_PS_PERS_4 = (1 << 5) | (1 << 4)

    VCNL4040_PS_IT_MASK = (~((1 << 3) | (1 << 2) | (1 << 1))) & 0xff
    VCNL4040_PS_IT_1T = 0
    VCNL4040_PS_IT_15T = (1 << 1)
    VCNL4040_PS_IT_2T = (1 << 2)
    VCNL4040_PS_IT_25T = (1 << 2) | (1 << 1)
    VCNL4040_PS_IT_3T = (1 << 3)
    VCNL4040_PS_IT_35T = (1 << 3) | (1 << 1)
    VCNL4040_PS_IT_4T = (1 << 3) | (1 << 2)
    VCNL4040_PS_IT_8T = (1 << 3) | (1 << 2) | (1 << 1)

    VCNL4040_PS_SD_MASK = (~(1 << 0)) & 0xff
    VCNL4040_PS_SD_POWER_ON = 0
    VCNL4040_PS_SD_POWER_OFF = (1 << 0)

    VCNL4040_PS_HD_MASK = (~(1 << 3)) & 0xff
    VCNL4040_PS_HD_12_BIT = 0
    VCNL4040_PS_HD_16_BIT = (1 << 3)

    VCNL4040_PS_SMART_PERS_MASK = (~(1 << 4)) & 0xff
    VCNL4040_PS_SMART_PERS_DISABLE = 0
    VCNL4040_PS_SMART_PERS_ENABLE = (1 << 1)

    VCNL4040_PS_AF_MASK = (~(1 << 3)) & 0xff
    VCNL4040_PS_AF_DISABLE = 0
    VCNL4040_PS_AF_ENABLE = (1 << 3)

    VCNL4040_PS_TRIG_MASK = (~(1 << 3)) & 0xff
    VCNL4040_PS_TRIG_TRIGGER = (1 << 2)

    VCNL4040_WHITE_EN_MASK = (~(1 << 7)) & 0xff
    VCNL4040_WHITE_ENABLE = 0
    VCNL4040_WHITE_DISABLE = (1 << 7)

    VCNL4040_PS_MS_MASK = (~(1 << 6)) & 0xff
    VCNL4040_PS_MS_DISABLE = 0
    VCNL4040_PS_MS_ENABLE = (1 << 6)

    VCNL4040_LED_I_MASK = (~((1 << 2) | (1 << 1) | (1 << 0))) & 0xff
    VCNL4040_LED_50MA = 0
    VCNL4040_LED_75MA = (1 << 0)
    VCNL4040_LED_100MA = (1 << 1)
    VCNL4040_LED_120MA = (1 << 1) | (1 << 0)
    VCNL4040_LED_140MA = (1 << 2)
    VCNL4040_LED_160MA = (1 << 2) | (1 << 0)
    VCNL4040_LED_180MA = (1 << 2) | (1 << 1)
    VCNL4040_LED_200MA = (1 << 2) | (1 << 1) | (1 << 0)

    VCNL4040_INT_FLAG_ALS_LOW = (1 << 5)
    VCNL4040_INT_FLAG_ALS_HIGH = (1 << 4)
    VCNL4040_INT_FLAG_CLOSE = (1 << 1)
    VCNL4040_INT_FLAG_AWAY = (1 << 0)

    def __init__(self, address=None, i2c_bus=None):


        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address?
        self.address = address if address is not None else self.available_addresses[0]

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

    #----------------------------------------------
    def is_connected(self):
        """
            Determine if a Proximity device is connected to the system.

            :return: True if the device is connected, otherwise False.
            :rtype: bool

        """
        return qwiic_i2c.is_device_connected(self.address)

    #----------------------------------------------
    # //Check comm with sensor and set it to default init settings
    def begin(self):
        """
            Initialize the operation of the Proximity module

            :return: Returns true of the initializtion was successful, otherwise False.
            :rtype: bool

        """
        # //Check connection
        if not self.is_connected():
            return False  # I2C comm failure

        if self.get_id() != 0x0186:
            return False  # Check default ID value

        # //Configure the various parts of the sensor
        self.set_led_current(200) # Max IR LED current

        self.set_ir_dutycycle(40) # Set to highest duty cycle

        self.set_prox_integration_time(8) # Set to max integration

        self.set_prox_resolution(16) # Set to 16-bit output

        self.enable_smart_persistence() #Turn on smart persistence

        self.power_on_proximity() #Turn on prox sensing

        self.set_ambient_integration_time(self.VCNL4040_ALS_IT_80MS) #Keep it short
        self.power_on_ambient() #Turn on ambient sensing

        return True

    #----------------------------------------------
    # //Set the duty cycle of the IR LED. The higher the duty
    # //ratio, the faster the response time achieved with higher power
    # //consumption. For example, PS_Duty = 1/320, peak IRED current = 100 mA,
    # //averaged current consumption is 100 mA/320 = 0.3125 mA.
    def set_ir_dutycycle(self, duty_value):
        """
            Set the duty cycle of the IR LED. The higher the duty
            ratio, the faster the response time achieved with higher power
            consumption. For example, PS_Duty = 1/320, peak IRED current = 100 mA,
            averaged current consumption is 100 mA/320 = 0.3125 mA.

            :param duty_value: The duty cycle value for the IR LED on the sensor
            :return: No return value

        """
        if duty_value > 320 - 1:
            duty_value = self.VCNL4040_PS_DUTY_320
        elif duty_value > 160 - 1:
            duty_value = self.VCNL4040_PS_DUTY_160
        elif duty_value > 80 - 1:
            duty_value = self.VCNL4040_PS_DUTY_80
        else:
            duty_value = self.VCNL4040_PS_DUTY_40

        self._bit_mask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_DUTY_MASK, duty_value)


    #----------------------------------------------
    # //Set the Prox interrupt persistence value
    # //The PS persistence function (PS_PERS, 1, 2, 3, 4) helps to avoid
    # //false trigger of the PS INT. It defines the amount of
    # //consecutive hits needed in order for a PS interrupt event to be triggered.
    def set_prox_interrupt_persistence(self, pers_value):
        """
            Set the Prox interrupt persistence value
            The PS persistence function (PS_PERS, 1, 2, 3, 4) helps to avoid
            false trigger of the PS INT. It defines the amount of
            consecutive hits needed in order for a PS interrupt event to be triggered.

            :param pers_value: The persistence value
            :return: No return value

        """
        self._bit_mask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_PERS_MASK, pers_value)

    #----------------------------------------------
    # //Set the Ambient interrupt persistence value
    # //The ALS persistence function (ALS_PERS, 1, 2, 4, 8) helps to avoid
    # //false trigger of the ALS INT. It defines the amount of
    # //consecutive hits needed in order for a ALS interrupt event to be triggered.
    def set_ambient_interrupt_persistence(self, pers_value):
        """
            Set the Ambient interrupt persistence value
            The ALS persistence function (ALS_PERS, 1, 2, 4, 8) helps to avoid
            false trigger of the ALS INT. It defines the amount of
            consecutive hits needed in order for a ALS interrupt event to be triggered.

            :param pers_value: The ambient interrupt persistence value
            :return: No return value

        """
        self._bit_mask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_PERS_MASK, pers_value)

    def enable_ambient_interrupts(self):
        """
            Enable Ambient Interrupts

            :return: No return value
        """
        self._bit_mask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_INT_EN_MASK, self.VCNL4040_ALS_INT_ENABLE)

    def disable_ambient_interrupts(self):
        """
            Disable Ambient Interrupts

            :return: No return value
        """
        self._bit_mask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_INT_EN_MASK, self.VCNL4040_ALS_INT_DISABLE)

    # Power on or off the ambient light sensing portion of the sensor
    def power_on_ambient(self):
        """
            Power on the ambient light sensing portion of the sensor

            :return: No return value
        """
        self._bit_mask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_SD_MASK, self.VCNL4040_ALS_SD_POWER_ON)

    def power_off_ambient(self):
        """
            Power off the ambient light sensing portion of the sensor

            :return: No return value
        """
        self._bit_mask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_SD_MASK, self.VCNL4040_ALS_SD_POWER_OFF)

    # Sets the integration time for the ambient light sensor
    def set_ambient_integration_time(self, time_value):
        """
            Sets the integration time for the ambient light sensor

            :param time_value: The integration time
            :return: No return value
        """

        if time_value > 640 - 1:
            time_value = self.VCNL4040_ALS_IT_640MS
        elif time_value > 320 - 1:
            time_value = self.VCNL4040_ALS_IT_320MS
        elif time_value > 160 - 1:
            time_value = self.VCNL4040_ALS_IT_160MS
        else:
            time_value = self.VCNL4040_ALS_IT_80MS

        self._bit_mask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_IT_MASK, time_value)


    # Sets the integration time for the proximity sensor
    def set_prox_integration_time(self, time_value):
        """
            Sets the integration time for the proximity sensor

            :param time_value: The integration time
            :return: No return value
        """
        if time_value > 8 - 1:
            time_value = self.VCNL4040_PS_IT_8T
        elif time_value > 4 - 1:
            time_value = self.VCNL4040_PS_IT_4T
        elif time_value > 3 - 1:
            time_value = self.VCNL4040_PS_IT_3T
        elif time_value > 2 - 1:
            time_value = self.VCNL4040_PS_IT_2T
        else:
            time_value = self.VCNL4040_PS_IT_1T

        self._bit_mask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_IT_MASK, time_value)


    # Power on the prox sensing portion of the device
    def power_on_proximity(self):
        """
            Power on the prox sensing portion of the device

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_SD_MASK, self.VCNL4040_PS_SD_POWER_ON)

    # Power off the prox sensing portion of the device
    def power_off_proximity(self):
        """
            Power off the prox sensing portion of the device

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_SD_MASK, self.VCNL4040_PS_SD_POWER_OFF)

    # Sets the proximity resolution
    def set_prox_resolution(self, resolution_value):
        """
            Sets the proximity resolution

            :param resolution_value: The resolution time
            :return: No return value
        """
        if resolution_value > 16 - 1:
            resolution_value = self.VCNL4040_PS_HD_16_BIT
        else:
            resolution_value = self.VCNL4040_PS_HD_12_BIT

        self._bit_mask(VCNL4040_PS_CONF2, UPPER, self.VCNL4040_PS_HD_MASK, resolution_value)


    # Sets the proximity interrupt type
    def set_prox_interrupt_type(self, interrupt_value):
        """
            Sets the proximity interrupt type

            :param interrupt_value: The interupt type
            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_CONF2, UPPER, self.VCNL4040_PS_INT_MASK, interrupt_value)


    # Enable smart persistence
    # To accelerate the PS response time, smart
    # persistence prevents the misjudgment of proximity sensing
    # but also keeps a fast response time.
    def enable_smart_persistence(self):
        """
            Enable smart persistence
            To accelerate the PS response time, smart
            persistence prevents the misjudgment of proximity sensing
            but also keeps a fast response time.

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_CONF3, LOWER, self.VCNL4040_PS_SMART_PERS_MASK, self.VCNL4040_PS_SMART_PERS_ENABLE)

    def disable_smart_persistence(self):
        """
            Disable smart persistence

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_CONF3, LOWER, self.VCNL4040_PS_SMART_PERS_MASK, self.VCNL4040_PS_SMART_PERS_DISABLE)

    # Enable active force mode
    # An extreme power saving way to use PS is to apply PS active force mode.
    # Anytime host would like to request one proximity measurement,
    # enable the active force mode. This
    # triggers a single PS measurement, which can be read from the PS result registers.
    # VCNL4040 stays in standby mode constantly.
    def enable_active_force_mode(self):
        """
            Enable active force mode
            An extreme power saving way to use PS is to apply PS active force mode.
            Anytime host would like to request one proximity measurement,
            enable the active force mode. This
            triggers a single PS measurement, which can be read from the PS result registers.
            VCNL4040 stays in standby mode constantly.

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_CONF3, LOWER, self.VCNL4040_PS_AF_MASK, self.VCNL4040_PS_AF_ENABLE)

    def disable_active_force_mode(self):
        """
            Disable active force mode

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_CONF3, LOWER, self.VCNL4040_PS_AF_MASK, self.VCNL4040_PS_AF_DISABLE)

    # Set trigger bit so sensor takes a force mode measurement and returns to standby
    def take_single_prox_measurement(self):
        """
            Set trigger bit so sensor takes a force mode measurement and returns to standby

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_CONF3, LOWER, self.VCNL4040_PS_TRIG_MASK, self.VCNL4040_PS_TRIG_TRIGGER)

    # Enable the white measurement channel
    def enable_white_channel(self):
        """
            Enable the white measurement channel

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_MS, UPPER, self.VCNL4040_WHITE_EN_MASK, self.VCNL4040_WHITE_ENABLE)

    def disable_white_channel(self):
        """
            Disable the white measurement channel

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_MS, UPPER, self.VCNL4040_WHITE_EN_MASK, self.VCNL4040_WHITE_ENABLE)

    # Enable the proximity detection logic output mode
    # When this mode is selected, the INT pin is pulled low when an object is
    # close to the sensor (value is above high
    # threshold) and is reset to high when the object moves away (value is
    # below low threshold). Register: PS_THDH / PS_THDL
    # define where these threshold levels are set.
    def enable_prox_logic_mode(self):
        """
            Enable the proximity detection logic output mode
            When this mode is selected, the INT pin is pulled low when an object is
            close to the sensor (value is above high
            threshold) and is reset to high when the object moves away (value is
            below low threshold). Register: PS_THDH / PS_THDL
            define where these threshold levels are set.

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_MS, UPPER, self.VCNL4040_PS_MS_MASK, self.VCNL4040_PS_MS_ENABLE)

    def disable_prox_logic_mode(self):
        """
            Disable the proximity detection logic output mode

            :return: No return value
        """
        self._bit_mask(VCNL4040_PS_MS, UPPER, self.VCNL4040_PS_MS_MASK, self.VCNL4040_PS_MS_DISABLE)


    # Set the IR LED sink current to one of 8 settings
    def set_led_current(self, current_value):
        """
            Set the IR LED sink current to one of 8 settings

            :param current_value: The new current value. Valid values are VCNL4040_LED_50MA thru VCNL4040_LED_200MA at 25MA increments
            :return: No return value
        """

        if current_value > 200 - 1:
            current_value = self.VCNL4040_LED_200MA
        elif current_value > 180 - 1:
            current_value = self.VCNL4040_LED_180MA
        elif current_value > 160 - 1:
            current_value = self.VCNL4040_LED_160MA
        elif current_value > 140 - 1:
            current_value = self.VCNL4040_LED_140MA
        elif current_value > 120 - 1:
            current_value = self.VCNL4040_LED_120MA
        elif current_value > 100 - 1:
            current_value = self.VCNL4040_LED_100MA
        elif current_value > 75 - 1:
            current_value = self.VCNL4040_LED_75MA
        else:
            current_value = self.VCNL4040_LED_50MA

        self._bit_mask(VCNL4040_PS_MS, UPPER, self.VCNL4040_LED_I_MASK, current_value)


    # Set the proximity sensing cancelation value - helps reduce cross talk
    # with ambient light
    def set_prox_cancellation(self, cancel_value):
        """
            Set the proximity sensing cancelation value - helps reduce cross talk with ambient light

            :param cancel_value: the new cancelation value
            :return: No return value
        """
        self._i2c.write_word(self.address, VCNL4040_PS_CANC, cancel_value)


    # Value that ALS must go above to trigger an interrupt
    def set_als_high_threshold(self, threshold):
        """
            Value that ALS must go above to trigger an interrupt

            :param threshold: the new trigger threshold value for ALS
            :return: No return value
        """
        self._i2c.write_word(self.address, VCNL4040_ALS_THDH, threshold)


    # Value that ALS must go below to trigger an interrupt
    def set_als_low_threshold(self, threshold):
        """
            Value that ALS must go below to trigger an interrupt

            :param threshold: the new trigger threshold value for ALS
            :return: No return value
        """
        self._i2c.write_word(self.address, VCNL4040_ALS_THDL, threshold)


    # Value that Proximity Sensing must go above to trigger an interrupt
    def set_prox_high_threshold(self, threshold):
        """
            Value that Proximity Sensing must go above to trigger an interrupt

            :param threshold: The new Proximity High Value
            :return: No return value
        """
        self._i2c.write_word(self.address, VCNL4040_PS_THDH, threshold)


    # Value that Proximity Sensing must go below to trigger an interrupt
    def set_prox_low_threshold(self, threshold):
        """
            Value that Proximity Sensing must go below to trigger an interrupt

            :param threshold: The new Proximity Low Value
            :return: No return value
        """
        self._i2c.write_word(self.address, VCNL4040_PS_THDL, threshold)

    #--------------------------------------------------------------------------
    # Read Value methods
    #--------------------------------------------------------------------------
    # get_proximity()
    #
    # Read the Proximity value
    def get_proximity(self):
        """
            Get the current proximity value

            :return: The current proximity value
            :rtype: integer
        """
        return self._i2c.read_word(self.address, VCNL4040_PS_DATA)


    # Read the Ambient light value
    def get_ambient(self):
        """
            Read the Ambient light value

            :return: The current ambient value value
            :rtype: integer
        """
        return self._i2c.read_word(self.address, VCNL4040_ALS_DATA)


    # Read the Whilte light value
    def get_white(self):
        """
            Read the White light value

            :return: The current white value value
            :rtype: integer
        """
        return self._i2c.read_word(self.address, VCNL4040_WHITE_DATA)


    # Read the sensors ID
    def get_id(self):
        """
            Read the sensor ID

            :return: The sensor ID
            :rtype: integer
        """
        return self._i2c.read_word(self.address, VCNL4040_ID)


    # Returns true if the prox value rises above the upper threshold
    def is_close(self):
        """
            Returns true if the prox value rises above the upper threshold

            :return: True if close
            :rtype: boolean
        """
        interrupt_flags = self._read_command_upper(VCNL4040_INT_FLAG)
        return (interrupt_flags & self.VCNL4040_INT_FLAG_CLOSE) != 0


    # Returns true if the prox value drops below the lower threshold
    def is_away(self):
        """
            Returns true if the prox value drops below the lower threshold

            :return: True if away
            :rtype: boolean
        """
        interrupt_flags = self._read_command_upper(VCNL4040_INT_FLAG)
        return (interrupt_flags & self.VCNL4040_INT_FLAG_AWAY) != 0

    # Returns true if the prox value rises above the upper threshold
    def is_light(self):
        """
            Returns true if the prox value rises above the upper threshold

            :return: True if value light
            :rtype: boolean
        """
        interrupt_flags = self._read_command_upper(VCNL4040_INT_FLAG)
        return (interrupt_flags & self.VCNL4040_INT_FLAG_ALS_HIGH) != 0

    #Returns true if the ALS value drops below the lower threshold
    def is_dark(self):
        """
            Returns true if the prox value drops below the lower threshold

            :return: True if dark
            :rtype: boolean
        """
        interrupt_flags = self._read_command_upper(VCNL4040_INT_FLAG)
        return (interrupt_flags & self.VCNL4040_INT_FLAG_ALS_LOW) != 0

    #--------------------------------------------------------------------------
    # internal I2C Utility Routines
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    # _write_command_lower()
    #
    # Given a command code (address) write to the upper byte without affecting the upper byte
    def _write_command_lower(self, command_code, new_value):

        command_value = self._i2c.read_word(self.address, command_code)
        command_value &= 0xFF00    #Remove lower 8 bits
        command_value |= new_value    #Mask in

        return self._i2c.write_word(self.address, command_code, command_value)
    #--------------------------------------------------------------------------
    # _write_command_upper()
    #
    # Given a command code (address) write to the upper byte without affecting the lower byte
    def _write_command_upper(self, command_code, new_value):

        command_value = self._i2c.read_word(self.address, command_code)
        command_value &= 0x00FF    #Remove upper 8 bits
        command_value |= new_value << 8   #Mask in

        return self._i2c.write_word(self.address, command_code, command_value)
    #--------------------------------------------------------------------------
    # _read_command_lower()
    #
    # Given a command code (address) read the lower byte
    def _read_command_lower(self, command_code):

        command_value = self._i2c.read_word(self.address, command_code)

        return command_value & 0xFF

    #--------------------------------------------------------------------------
    # _read_command_upper()
    #
    # Given a command code (address) read the upper byte
    def _read_command_upper(self, command_code):

        command_value = self._i2c.read_word(self.address, command_code)

        return command_value >> 8

    #--------------------------------------------------------------------------
    # _bit_mask()
    #
    # Given a register, read it, mask it, and then set the thing
    # command_height is used to select between the upper or lower byte of command register
    # Example:
    # Write duty_value into PS_CONF1, lower byte, using the Duty_Mask
    # _bit_mask(VCNL4040_PS_CONF1, LOWER, VCNL4040_PS_DUTY_MASK, duty_value);
    def _bit_mask(self, command_address, command_height, mask, thing):

        # Grab current register context
        if command_height == LOWER:
            register_contents = self._read_command_lower(command_address)
        else:
            register_contents = self._read_command_upper(command_address)

        # Zero-out the portions of the register we're interested in
        register_contents &= mask

        # Mask in new thing
        register_contents |= thing

        # Change contents
        if command_height == LOWER:
            self._write_command_lower(command_address, register_contents)
        else:
            self._write_command_upper(command_address, register_contents)
