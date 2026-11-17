#-----------------------------------------------------------------------------
# qwiic_pir.py
#
# Python library for the SparkFun qwiic PIR.
#   https://www.sparkfun.com/products/16407
#
#------------------------------------------------------------------------
#
# Written by Andy England and Priyanka Makin @ SparkFun Electronics, January 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
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
qwiic_pir
============
Python module for the Qwiic PIR.
This python package is a port of the exisiting [SparkFun Qwiic PIR Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_PIR_Arduino_Library)
This package can be used in conjunction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to qwiic? Take a look at the entire [SparkFun Qwiic Ecosystem](https://www.sparkfun.com/qwiic).
"""
#-----------------------------------------------------------------------------------

import math
import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class definition
# as class variables, making them available without having to create a class instance.
# This allows higher level logic to rapidly create an index of qwiic devices at runtime.

# This is the name of the device
_DEFAULT_NAME = "Qwiic PIR"

# Some devices have  multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the 
# device.
_QWIIC_PIR_DEFAULT_ADDRESS = 0x12
_FULL_ADDRESS_LIST = list(range(0x08, 0x77+1))  # Full address list (excluding reserved addresses)
_FULL_ADDRESS_LIST.remove(_QWIIC_PIR_DEFAULT_ADDRESS >> 1)  # Remove default address from list
_AVAILABLE_I2C_ADDRESS = [_QWIIC_PIR_DEFAULT_ADDRESS]  # Initialize with default address
_AVAILABLE_I2C_ADDRESS.extend(_FULL_ADDRESS_LIST)   # Add full range of I2C addresses

# Define the class that encapsulates the device being created. All information associated 
# with this device is encapsulated by this class. The device class should be the only value
# exported from this module.

class QwiicPIR(object):
    """"
    QwiicPIR
        
        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The GPIO device object.
        :rtype: Object
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Device ID for all Qwiic PIRs
    DEV_ID = 0x72

    # Registers
    ID = 0x00
    FIRMWARE_MINOR = 0x01
    FIRMWARE_MAJOR = 0x02
    EVENT_STATUS = 0x03
    INTERRUPT_CONFIG = 0x04
    EVENT_DEBOUNCE_TIME = 0x05
    DETECTED_QUEUE_STATUS = 0x07
    DETECTED_QUEUE_FRONT = 0x08
    DETECTED_QUEUE_BACK = 0x0C
    REMOVED_QUEUE_STATUS = 0x10
    REMOVED_QUEUE_FRONT = 0x11
    REMOVED_QUEUE_BACK = 0x15
    I2C_ADDRESS = 0x19

    # Status Flags
    event_available = 0
    object_remove = 0
    object_detect = 0
    raw_object_detected = 0

    # Interrupt Configuration Flags
    interrupt_enable = 0

    # Detected Queue Status Flags
    detected_pop_request = 0
    detected_is_empty = 0
    detected_is_full = 0
    
    # Removed Queue Status Flags
    removed_pop_request = 0
    removed_is_empty = 0 
    removed_is_full = 0

    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self.address = address if address != None else self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
        else: 
            self._i2c = i2c_driver

    # -----------------------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?
    def is_connected(self):
        """
            Determine if a Qwiic PIR device is connected to the system.
            
            :return: True if the device is connected, otherwise False.
            :rtype: bool
        """
        return qwiic_i2c.isDeviceConnected(self.address)
    
    # ------------------------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """
            Initialize the operation of the Qwiic PIR
            Run is_connected() and check the ID in the ID register
            
            :return: Returns true if the intialization was successful, otherwise False.
            :rtype: bool
        """
        if self.is_connected() == True:
            id = self._i2c.readByte(self.address, self.ID)
            
            if id == self.DEV_ID:
                return True
        
        return False
    
    # ------------------------------------------------
    # get_firmware_version()
    #
    # Returns the firmware version of the attached devie as a 16-bit integer.
    # The leftmost (high) byte is the major revision number, 
    # and the rightmost (low) byte is the minor revision number.
    def get_firmware_version(self):
        """
            Read the register and get the major and minor firmware version number.
            
            :return: 16 bytes version number
            :rtype: int
        """
        version = self._i2c.readByte(self.address, self.FIRMWARE_MAJOR) << 8
        version |= self._i2c.readByte(self.address, self.FIRMWARE_MINOR)
        return version

    # -------------------------------------------------
    # set_I2C_address(new_address)
    #
    # Configures the attached device to attach to the I2C bus using the specified address
    def set_I2C_address(self, new_address):
        """
            Change the I2C address of the Qwiic PIR
            
            :param new_address: the new I2C address to set the Qwiic PIR to
            :return: True if the change was successful, false otherwise.
            :rtype: bool
        """
        # First, check if the specified address is valid
        if new_address < 0x08 or new_address > 0x77:
            return False
        
        # Write new address to the I2C address register of the Qwiic PIR
        self._i2c.writeByte(self.address, self.I2C_ADDRESS, new_address)

        # Check if the write was successful
        self.address = new_address
    
    # ---------------------------------------------------
    # get_I2C_address()
    #
    # Returns the I2C address of the device
    def get_I2C_address(self):
        """
            Returns the current I2C address of the Qwiic PIR
            
            :return: current I2C address
            :rtype: int
        """
        return self.address

    # ---------------------------------------------------
    # raw_reading()
    #
    # Returns 1 if the PIR is detecting an object, 0 otherwise
    def raw_reading(self):
        """
            Returns the value of the raw_reading status bit of the EVENT_STATUS register
            
            :return: raw_object_detected bit
            :rtype: bool
        """
        # Read the PIR status register
        pir_status = self._i2c.readByte(self.address, self.EVENT_STATUS)
        # Convert to binary and clear all bits but raw_object_detected
        self.raw_object_detected = int(pir_status) & ~(0xFE) 
        # Return raw_object_detected as a bool
        return bool(self.raw_object_detected)


    # ---------------------------------------------------
    # object_detected()
    #
    # Returns 1 if the PIR has a debounced detect object event
    def object_detected(self):
        """
            Returns the value of the object_detect status bit of the EVENT_STATUS register
            
            :return: object_detect bit
            :rtype: bool
        """
        # Read the PIR status register
        pir_status = self._i2c.readByte(self.address, self.EVENT_STATUS)
        # Convert to binary and clear all bits but object_detect
        self.object_detect = int(pir_status) & ~(0xF7)
        # Shift object_detect bit to zero position
        self.object_detect = self.object_detect >> 3
        # Return object_detect as a bool
        return bool(self.object_detect)
    
    # ----------------------------------------------------
    # object_removed()
    #
    # Returns 1 if the object in front of the PIR is removed, and 0 otherwise
    def object_removed(self):
        """
            Returns the value of the object_remove status bit of the EVENT_STATUS register
            
            :return: object_remove bit
            :rtype: bool
        """
        # Read the PIR status register
        pir_status = self._i2c.readByte(self.address, self.EVENT_STATUS)
        # Convert to binary and clear all bits but object_remove
        self.object_remove = int(pir_status) & ~(0xFB)
        # Shift object_remove to the zero bit
        self.object_remove = self.object_remove >> 2
        # Return object_remove as a bool
        return bool(self.object_remove)
    
    # ------------------------------------------------------
    # get_debounce_time()
    #
    # Returns the time that the PIR is using to debounce events
    def get_debounce_time(self):
        """
            Returns the value in the EVENT_DEBOUNCE_TIME register
            
            :return: debounce time in milliseconds
            :rtype: int
        """
        time_list = self._i2c.readBlock(self.address, self.EVENT_DEBOUNCE_TIME, 2)
        # Convert list of bytes to time in milliseconds
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2)
        return time
    
    # -------------------------------------------------------
    # set_debounce_time(time)
    #
    # Sets the time that the PIR is using to debounce events
    def set_debounce_time(self, time):
        """
            Write two bytes into the EVENT_DEBOUNCE_TIME register
            
            :param time: the time in milliseconds to set debounce time to
                The max deounce time is 0xFFFF milliseconds, but the function
                checks if the entered parameter is valid
            :return: Nothing
            :rtype: void
        """
        # First check that time is not too big
        if time > 0xFFFF:
            time = 0xFFFF
        # Then write two bytes
        self._i2c.writeWord(self.address, self.EVENT_DEBOUNCE_TIME, time)

    # -------------------------------------------------------
    # enable_interrupt()
    #
    # The interrupt will be configured to trigger when the PIR
    # detects an object.
    def enable_interrupt(self):
        """
            Set interrupt_enable bit of the INTERRUPT_CONFIG register to a 1
            
            :return: Nothing
            :rtype: Void
        """
        self.interrupt_enable = 1
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, self.interrupt_enable)
    
    # -------------------------------------------------------
    # disable_interrupt()
    # 
    # Interrupt will no longer be configured to trigger when the
    # PIR is detecting.
    def disable_interrupt(self):
        """
            Clear the interrupt_enable bit of the INTERRUPT_CONFIG register
            
            :return: Nothing
            :rtype: Void
        """
        self.interrupt_enable = 0
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, self.interrupt_enable)

    # -------------------------------------------------------
    # available()
    #
    # Returns the event_availble bit. This bit is set to 1 if a
    # PIR detect or remove event occurred
    def available(self):
        """
            Return the event_available bit of the EVENT_STATUS register
            
            :return: event_available bit
            :rtye: bool
        """
        # First, read EVENT_STATUS register
        pir_status = self._i2c.readByte(self.address, self.EVENT_STATUS)
        # Convert to binary and clear all bits but the event_available bit
        self.event_available = int(pir_status) & ~(0xFD)
        # Shift event_availble to the zero bit
        self.event_available = self.event_available >> 1
        # Return event_available bit as a bool
        return bool(self.event_available)
    
    # -------------------------------------------------------
    # clear_event_bits()
    # 
    # Sets all PIR status bits (raw_object_detected, object_removed, 
    # and event_available) to zero.
    def clear_event_bits(self):
        """
            Clear the object_remove, object_detect, and event_available
            bits of the EVENT_STATUS register
            
            :return: Nothing
            :rtype: Void
        """
        # First, read EVENT_STATUS register
        pir_status = self._i2c.readByte(self.address, self.EVENT_STATUS)
        # Convert to binary and clear bits 1, 2, and 3
        pir_status = int(pir_status) & ~(0x0E)
        # Write to EVENT_STATUS register
        self._i2c.writeByte(self.address, self.EVENT_STATUS, pir_status)
        # Update variables
        self.object_remove = 0
        self.objected_detect = 0
        self.event_available = 0
    
    # -------------------------------------------------------
    # reset_interrupt_config()
    #
    # Resets the interrupt configuration back to defaults.
    def reset_interrupt_config(self):
        """
            Enable detect interrupt and clear the
            event_available bit of EVENT_STATUS register
            
            :return: Nothing
            :rtype: Void
        """
        # Enable interrupts on PIR detection
        self.enable_interrupt()
        # Clear the event bits
        self.clear_event_bits()
    
    # -------------------------------------------------------
    # is_detected_queue_full()
    #
    # Returns true if queue of PIR detect timestamps is full,
    # and false otherwise.
    def is_detected_queue_full(self):
        """
            Returns the is_full bit of the DETECTED_QUEUE_STATUS register
            
            :return: detected_is_full
            :rtype: bool
        """
        # First, read the DETECTED_QUEUE_STATUS register
        detected_queue_stat = self._i2c.readByte(self.address, self.DETECTED_QUEUE_STATUS)
        # Convert to binary and clear all bits but is_full
        self.detected_is_full = int(detected_queue_stat) & ~(0xFB)
        # Shift detected_is_full bit to zero position
        self.detected_is_full = self.detected_is_full >> 2
        # Return detected_is_full as a bool
        return bool(self.detected_is_full)
    
    # -------------------------------------------------------
    # is_detected_queue_empty()
    #
    # Returns true if the queue of PIR detect timestamps is
    # empty, and false otherwise.
    def is_detected_queue_empty(self):
        """
            Returns the is_empty bit of the DETECTED_QUEUE_STATUS register
            
            :return: detected_is_empty
            :rtype: bool
        """
        # First, read the DETECTED_QUEUE_STATUS register
        detected_queue_stat = self._i2c.readByte(self.address, self.DETECTED_QUEUE_STATUS)
        # Convert to binary and clear all bits but is_empty
        self.detected_is_empty = int(detected_queue_stat) & ~(0xFD)
        # Shift detected_is_empty to the zero bit
        self.detected_is_empty = self.detected_is_empty >> 1
        # Return is_empty as a bool
        return bool(self.detected_is_empty)

    # ------------------------------------------------------
    # time_since_last_detect()
    #
    # Returns how many milliseconds it has been since the last
    # detect event. Since this returns a 32-bit int, it will 
    # roll over about every 50 days.
    def time_since_last_detect(self):
        """
            Returns the four bytes of DETECTED_QUEUE_FRONT.
            Time in milliseconds.
            
            :return: DETECTED_QUEUE_FRONT
            :rtype: int
        """
        time_list = self._i2c.readBlock(self.address, self.DETECTED_QUEUE_FRONT, 4)
        # Convert list of bytes to a time in milliseconds
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2) + int(time_list[2]) * 16 ** (4) + int(time_list[3]) * 16 ** (6)
        return time
        
    # -------------------------------------------------------
    # time_since_first_detect()
    #
    # Returns how many milliseconds it has been since the first 
    # detect event. Since this returns a 32-bit int, it will 
    # roll over about every 50 days.
    def time_since_first_detect(self):
        """
            Returns the four bytes of DETECTED_QUEUE_BACK.
            Time in milliseconds
            
            :return: DETECTED_QUEUE_BACK
            :rtype: int
        """
        time_list = self._i2c.readBlock(self.address, self.DETECTED_QUEUE_BACK, 4)
        # Convert the list of bytes into milliseconds
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2) + int(time_list[2]) * 16 ** (4) + int(time_list[3]) * 16 ** (6)
        return time
        
    # -------------------------------------------------------
    # pop_detected_queue()
    #
    # Returns the oldest value in the queue (milliseconds since 
    # first PIR detect event), and then removes it.
    def pop_detected_queue(self):
        """
            Returns contents of DETECTED_QUEUE_BACK register and 
            writes a 1 to pop_request bit of DETECTED_QUEUE_STATUS
            register.
            
            :return: DETECTED_QUEUE_BACK
            :rtype: int
        """
        # Get the time in milliseconds since the PIR was first detect
        temp_data = self.time_since_first_detect()
        # Read DETECTED_QUEUE_STATUS register
        detected_queue_stat = self._i2c.readByte(self.address, self.DETECTED_QUEUE_STATUS)
        # Set detected_pop_request bit to 1
        self.detected_pop_request = 1
        detected_queue_stat = detected_queue_stat | (self.detected_pop_request)
        self._i2c.writeByte(self.address, self.DETECTED_QUEUE_STATUS, detected_queue_stat)
        return temp_data
    
    # -------------------------------------------------------
    # is_removed_queue_full()
    #
    # Returns true if queue of PIR remove timestamps is full,
    # and false otherwise.
    def is_removed_queue_full(self):
        """
            Returns the is_full bit of the REMOVED_QUEUE_STATUS register
            
            :return: removed_is_full
            :rtype: bool
        """
        # First, read the REMOVED_QUEUE_STATUS register
        removed_queue_stat = self._i2c.readByte(self.address, self.REMOVED_QUEUE_STATUS)
        # Convert to binary and clear all bits but is_full
        self.removed_is_full = int(removed_queue_stat) & ~(0xFB)
        # Shift removed_is_full to the zero bit
        self.removed_is_full = self.removed_is_full >> 2
        # Return removed_is_full as a bool
        return bool(self.removed_is_full)
    
    # -------------------------------------------------------
    # is_removed_queue_empty()
    #
    # Returns true if the queue of PIR remove timestamps is
    # empty, and false otherwise.
    def is_removed_queue_empty(self):
        """
            Returns the is_empty bit of the REMOVED_QUEUE_STATUS register
            
            :return: removed_is_empty
            :rtype: bool
        """
        # First, read the REMOVED_QUEUE_STATUS register
        removed_queue_stat = self._i2c.readByte(self.address, self.REMOVED_QUEUE_STATUS)
        # Convert to binary and clear all bits but is_empty
        self.removed_is_empty = int(removed_queue_stat) & ~(0xFD)
        # Shift removed_is_empty to the zero bit
        self.removed_is_empty = self.removed_is_empty >> 1
        # Return removed_is_empty as a bool
        return bool(self.removed_is_empty)

    # ------------------------------------------------------
    # time_since_last_remove()
    #
    # Returns how many milliseconds it has been since the last
    # remove event. Since this returns a 32-bit int, it will 
    # roll over about every 50 days.
    def time_since_last_remove(self):
        """
            Returns the four bytes of REMOVED_QUEUE_FRONT.
            Time in milliseconds.
            
            :return: REMOVED_QUEUE_FRONT
            :rtype: int
        """
        time_list = self._i2c.readBlock(self.address, self.REMOVED_QUEUE_FRONT, 4)
        # Convert list of bytes to time in milliseconds
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2) + int(time_list[2]) * 16 ** (4) + int(time_list[3]) * 16 ** (6)
        return time
        
    # -------------------------------------------------------
    # time_since_first_remove()
    #
    # Returns how many milliseconds it has been since the first 
    # remove event. Since this returns a 32-bit int, it will 
    # roll over about every 50 days.
    def time_since_first_remove(self):
        """
            Returns the four bytes of REMOVED_QUEUE_BACK.
            Time in milliseconds
            
            :return: REMOVED_QUEUE_BACK
            :rtype: int
        """
        time_list = self._i2c.readBlock(self.address, self.REMOVED_QUEUE_BACK, 4)
        # Convert list of bytes into time in milliseconds
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2) + int(time_list[2]) * 16 ** (4) + int(time_list[3]) * 16 ** (6)
        return time

    # -------------------------------------------------------
    # pop_removed_queue()
    #
    # Returns the oldest value in the queue (milliseconds since 
    # first PIR remove event), and then removes it.
    def pop_removed_queue(self):
        """
            Returns contents of REMOVED_QUEUE_BACK register and 
            writes a 1 to pop_request bit of REMOVED_QUEUE_STATUS
            register.
            
            :return: REMOVED_QUEUE_BACK
            :rtype: int
        """
        # Get the time in milliseconds since the PIR was first remove
        temp_data = self.time_since_first_remove()
        # Read REMOVED_QUEUE_STATUS register
        removed_queue_stat = self._i2c.readByte(self.address, self.REMOVED_QUEUE_STATUS)
        # Set removed_pop_request bit to 1
        self.removed_pop_request = 1
        removed_queue_stat = removed_queue_stat | (self.removed_pop_request)
        self._i2c.writeByte(self.address, self.REMOVED_QUEUE_STATUS, removed_queue_stat)
        return temp_data
