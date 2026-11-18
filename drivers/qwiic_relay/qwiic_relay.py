#-----------------------------------------------------------------------------
# qwiic_relay.py
#
# Python library for the SparkFun Qwiic Relays
#
#   https://www.sparkfun.com/products/15168
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, July 2019
#
# This python library supports the SparkFun Electronics qwiic
# qwiic sensor/board ecosystem
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
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
# This is mostly a port of existing Arduino functionality, so pylint is sad.
# The goal is to keep the public interface pthonic, but internal is internal
#
# pylint: disable=line-too-long, bad-whitespace, invalid-name
#
"""!
qwiic_relay
===============
Python module for the `SparkFun Qwiic Single Relay <https://www.sparkfun.com/products/15093>`_, `SparkFun Qwiic Quad Relay <https://www.sparkfun.com/products/15102>`_, `SparkFun Qwiic Dual Solid State Relay <https://www.sparkfun.com/products/16810>`_, `SparkFun Qwiic Quad Solid State Relay <https://www.sparkfun.com/products/16796>`_

This package can be used in conjunction with the overall `SparkFun qwiic Python Package <https://github.com/sparkfun/Qwiic_Py>`_

New to qwiic? Take a look at the entire `SparkFun qwiic ecosystem <https://www.sparkfun.com/qwiic>`_.
"""
#-----------------------------------------------------------------------------

import qwiic_i2c

__version__ = "3.0.0"

# Define the device name and I2C addresses. These are set in the class definition
# as class variables, making them available without having to create a class instance.
# This allows higher level logic to rapidly create an index of qwiic devices at
# runtime
#
# The name of this device
_DEFAULT_NAME = "SparkFun Qwiic Relay"

# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
SINGLE_RELAY_DEFAULT_ADDR                = 0x18
SINGLE_RELAY_JUMPER_CLOSE_ADDR           = 0x19
QUAD_RELAY_DEFAULT_ADDR                  = 0x6D
QUAD_RELAY_JUMPER_CLOSE_ADDR             = 0x6C
DUAL_SOLID_STATE_RELAY_DEFAULT_ADDR      = 0x0A
DUAL_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR = 0x0B
QUAD_SOLID_STATE_RELAY_DEFAULT_ADDR      = 0x08
QUAD_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR = 0x09

_AVAILABLE_I2C_ADDRESSES = [
    SINGLE_RELAY_DEFAULT_ADDR,
    SINGLE_RELAY_JUMPER_CLOSE_ADDR,
    QUAD_RELAY_DEFAULT_ADDR,
    QUAD_RELAY_JUMPER_CLOSE_ADDR,
    DUAL_SOLID_STATE_RELAY_DEFAULT_ADDR,
    DUAL_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR,
    QUAD_SOLID_STATE_RELAY_DEFAULT_ADDR,
    QUAD_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR]

# Define commands for changing i2c address to
SINGLE_CHANGE_ADDRESS = 0x03
QUAD_CHANGE_ADDRESS   = 0xC7

# Define the register offsets of each relay
RELAY_ONE   = 1
RELAY_TWO   = 2
RELAY_THREE = 3
RELAY_FOUR  = 4

# Define register start positions
DUAL_QUAD_TOGGLE_BASE = 0x00
STATUS_BASE           = 0x04
DUAL_QUAD_PWM_BASE    = 0x0F
TURN_ALL_OFF          = 0x0A
TURN_ALL_ON           = 0x0B
TOGGLE_ALL            = 0x0C

# Special values for single relay
SINGLE_OFF              = 0x00
SINGLE_ON               = 0x01
SINGLE_FIRMWARE_VERSION = 0x04
SINGLE_STATUS           = 0x05

# Define the value of an "Off" relay
STATUS_OFF = 0

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicRelay(object):
    """!
    QwiicRelay

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.

    @return **Object** The Qwiic Relay device object.
    """
    # Constructor
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESSES
    
    # Constructor
    def __init__(self, address=None, i2c_bus=None):

        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address? Any address is accepted, so a
        # board moved with change_address() can be opened again.
        self.address = address if address is not None else self.available_addresses[0]

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """!
        Determine if the Qwiic Relay is connected to the system.

        @return **bool** True if the device is connected, otherwise False.
        """
        return self._i2c.is_device_connected(self.address)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    
    def begin(self):
        """!
        Initialize the operation of the relay

        @return **bool** Returns true of the initialization was successful, otherwise False.
        """

        # Basically return True if we are connected...

        return self.is_connected()
    
    #----------------------------------------------------------------
    # set_relay_on(relay_num)
    #
    # Turn's on a specific relay number, if we're using a single relay, do not pass in a relay number.
    
    def set_relay_on(self, relay_num=None):
        """!
        Turn's on a relay,if we're using a single relay, do not pass in a relay number

        @param relay_num: The relay to turn on

        @return **bool** successful I2C transaction
        """
        if relay_num is None:
            return self._i2c.write_byte(self.address, None, SINGLE_ON)
        else:
            temp = self._i2c.read_byte(self.address, STATUS_BASE + relay_num)

            if temp == STATUS_OFF:
                return self._i2c.write_byte(self.address, None, DUAL_QUAD_TOGGLE_BASE + relay_num)

    #----------------------------------------------------------------
    # set_relay_off(relay_num)
    #
    # Turn's off a specific relay number, if we're using a single relay, do not pass in a relay number.

    def change_address(self, new_address, single_relay=True):
        """!
        Change the I2C address of the relay

        @param new_address: The new address to change to (0x07 to 0x78)
        @param single_relay: True for the single relay, False for the
                        dual and quad relays

        @return **bool** True if the address was changed, False if
                        new_address is out of range
        """
        if (new_address < 0x07) or (new_address > 0x78):
            return False
        
        if single_relay:
            self._i2c.write_byte(self.address, SINGLE_CHANGE_ADDRESS, new_address)
        else:
            self._i2c.write_byte(self.address, QUAD_CHANGE_ADDRESS, new_address)

        # Talk to the board at its new address from now on
        self.address = new_address
        return True
    
    def set_relay_off(self, relay_num=None):
        """!
        Turn's off a relay,if we're using a single relay, do not pass in a relay number

        @param relay_num: The relay to turn off

        @return **bool** successful I2C transaction
        """
        
        if relay_num is None:
            return self._i2c.write_byte(self.address, None, SINGLE_OFF)
        else:
            temp = self._i2c.read_byte(self.address, STATUS_BASE + relay_num)

            if temp != STATUS_OFF:
                return self._i2c.write_byte(self.address, None, DUAL_QUAD_TOGGLE_BASE + relay_num)   

    #----------------------------------------------------------------
    # set_all_relays_on(relay_num)
    #
    # Turn's on all relays. This command does nothing for the single relay    
    def set_all_relays_on(self):
        """!
        Turn's on all relays. This command does nothing for the single relay

        @return **bool** successful I2C transaction
        """
        
        return self._i2c.write_byte(self.address, None, TURN_ALL_ON)
    
    #----------------------------------------------------------------
    # set_all_relays_off(relay_num)
    #
    # Turn's off all relays. This command does nothing for the single relay
    
    def set_all_relays_off(self):
        """!
        Turn's off all relays. This command does nothing for the single relay

        @return **bool** successful I2C transaction
        """
        
        return self._i2c.write_byte(self.address, None, TURN_ALL_OFF)
    
    #----------------------------------------------------------------
    # set_slow_pwm(relay_num, pwm_value)
    #
    # Sets the value for the slow PWM signal. Can be anywhere from 0 (off) to 120 (on).
    # A full cycle takes 1 second
    
    def set_slow_pwm(self, relay_num, pwm_value):
        """!
        Sets the value for the slow PWM signal. Can be anywhere from 0 (off) to 120 (on).
            A full cycle takes 1 second.

        @param relay_num: The relay to set the PWM signal of
        @param pwm_value: The value of the PWM signal, a value between 0 and 120

        @return **bool** successful I2C transaction
        """
        for i in range(4):
            if self.address == self.available_addresses[i]:
                # Slow PWM does not work for the mechanical relays
                return False
        return self._i2c.write_byte(self.address, DUAL_QUAD_PWM_BASE + relay_num, pwm_value)
        
    #----------------------------------------------------------------
    # get_slow_pwm(relay_num)
    #
    # Gets the value for the slow PWM signal. Can be anywhere from 0 (off) to 120 (on).
  
    def get_slow_pwm(self, relay_num):
        """!
        Gets the value for the slow PWM signal. Can be anywhere from 0 (off) to 120 (on).

        @param relay_num: The relay to get the PWM signal of

        @return **bool** The value of the PWM signal, a value between 0 and 120
        """
        for i in range(4):
            if self.address == self.available_addresses[i]:
                # Slow PWM does not work for the mechanical relays
                return False
        return self._i2c.read_byte(self.address, DUAL_QUAD_PWM_BASE + relay_num)
    
    #----------------------------------------------------------------
    # get_relay_state(relay_num)
    #
    # Returns the status of the relay_num you pass to it. Do not pass in a relay number if you are using a single relay.
    
    def get_relay_state(self, relay_num=None):
        """!
        Returns true if the relay is currently on, and false if it is off.

        @return **bool** Status of the relay
        """
        
        if relay_num is None:
            relay_num = 1
        
        if self._i2c.read_byte(self.address, STATUS_BASE + relay_num) == STATUS_OFF:
            return False
        else:
            return True

    #----------------------------------------------------------------
    # get_version()
    #
    # Returns the firmware version for the Single Relay

    def get_version(self):
        """!
        Returns the firmware version for the Single Relay

        @return **string** The firmware version
        """

        return self._i2c.read_byte(self.address, SINGLE_FIRMWARE_VERSION)
