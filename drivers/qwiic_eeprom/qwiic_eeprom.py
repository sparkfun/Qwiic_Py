#-----------------------------------------------------------------------
# qwiic_eeprom.py
#
# Python library for the SparkFun Qwiic EEPROM Breakout - 512Kbit.
#   https://www.sparkfun.com/products/18355
#
#-----------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#=======================================================================
# Copyright (c) 2020 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#=======================================================================

"""
qwiic_eeprom
============
Python module for the SparkFun Qwiic EEPROM Breakout - 512Kbit.

This package is a port of the exisiting [SparkFun External EEPROM Arduino Library](https://github.com/sparkfun/SparkFun_External_EEPROM_Arduino_Library).

This package can be used in conjuction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py).

New to qwiic? Take a look at the entire [SparkFun Qwiic Ecosystem](https://www.sparkfun.com/qwiic).
"""
# ----------------------------------------------------------------------

import math
import time
import qwiic_i2c
import smbus2
import struct

_DEFAULT_NAME = "Qwiic EEPROM"

_AVAILABLE_I2C_ADDRESS = [0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57]

class QwiicEEPROM(object):
    """
    Qwiic EEPROM

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided a
                        a driver object is created.
        :return: The GPIo device object.
        :rtype: Object
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Variables
    
    memory_size_bytes = int(512 * 1024 / 8)  # kBytes to kbits / 8 bits
    page_size_bytes = 128
    page_write_time_ms = 5
    poll_for_write_complete = True

    I2C_BUFFER_LENGTH = 32

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

    # ------------------------------------------------------------------
    # is_connected(i2c_address)
    #
    # Is an actual board connected to our system?
    def is_connected(self, i2c_address = 255):
        """
            Determine if a Qwiic EEPROM device is connected to the system

            :param i2c_address: I2C address of EEPROM. Larger EEPROMs have two addresses.
            :return: True if the device is connected, false otherwise.
            :rtype: bool
        """
        if i2c_address == 255:
            i2c_address = self.address       
        return qwiic_i2c.isDeviceConnected(i2c_address)
    
    # ------------------------------------------------------------------
    # begin()
    #
    # Initialize the system and validate the board.
    def begin(self):
        """
            Initialize the operation of the Qwiic EEPROM.
            Run is_connected().

            :return: Returns true if the initialization was successful, false otherwise.
            :rtype: bool
        """
        if self.is_connected() == True:
            return True
        return False

    # ------------------------------------------------------------------
    # erase(to_write)
    #
    # Erase entire EEPROM
    def erase(self, to_write = 0x00):
        """
            Erase entire EEPROM.
            
            :param to_write: byte to write into each spot of EEPROM 
            :return: Nothing
            :rtype: void
        """
        temp_buffer = []

        for x in range(0, self.page_size_bytes):
            temp_buffer.append(to_write)
        
        for addr in range(0, int(self.length()), self.page_size_bytes):
            self.write(addr, temp_buffer)
    
    # ------------------------------------------------------------------
    # length()
    #
    # Returns the memory size of the EEPROM
    def length(self):
        """
            Returns the memory size of the EEPROM

            :return: memory_size_bytes
            :rtype: int
        """
        return self.memory_size_bytes
    
    # ------------------------------------------------------------------
    # is_busy(i2c_address)
    #
    # Returns true if the device is not answering (currently writing).
    def is_busy(self, i2c_address = 255):
        """
            Returns true if the device is not answering (currently writing).

            :param i2c_address: I2C address of EEPROM. Larger EEPROMs have two addresses.
            :return: True if the IC is busy, false otherwise
            :rtype: bool
        """
        if i2c_address == 255:
            i2c_address = self.address

        if self.is_connected(i2c_address) == True:
            return False
        return True

    # ------------------------------------------------------------------
    # set_memory_size(mem_size)
    #
    # Set the size of memory in bytes
    def set_memory_size(self, mem_size):
        """
            Set the size of memory in bytes

            :param mem_size: memory size in bytes
            :return: Nothing
            :rtype: void
        """
        self.memory_size_bytes = mem_size

    # ------------------------------------------------------------------
    # get_memory_size()
    #
    # Return the size of EEPROM
    def get_memory_size(self):
        """
            Return the size of EEPROM

            :return: memory_size_bytes
            :rtype: int
        """
        return self.memory_size_bytes
    
    # ------------------------------------------------------------------
    # set_page_size(page_size)
    #
    # Set the size of the page we can write at a time
    def set_page_size(self, page_size):
        """
            Set the size of the page we can write at a time

            :param page_size: new page size in bytes
            :return: Nothing
            :rtype: void
        """
        self.page_size_bytes = page_size
    
    # ------------------------------------------------------------------
    # get_page_size()
    #
    # Return the current page size of EEPROM in bytes
    def get_page_size(self):
        """
            Get the page size

            :return: Current page size off EEPROM in bytes
            :rtype: int
        """
        return self.page_size_bytes
    
    # ------------------------------------------------------------------
    # set_page_write_time(write_time_ms)
    #
    # Set the number of ms required per page write
    def set_page_write_time(self, write_time_ms):
        """
            Set the number of ms required per page write

            :param write_time_ms: write time in ms
            :return: Nothing
            :rtype: Void
        """
        self.page_write_time_ms = write_time_ms
    
    # ------------------------------------------------------------------
    # get_page_write_time()
    #
    # Get the current time required per page write
    def get_page_write_time(self):
        """
            Get the current time required per page write

            :return: Time required per page write
            :rtype: int
        """
        return self.page_write_time_ms
    
    # ------------------------------------------------------------------
    # enable_poll_for_write_complete()
    #
    # Most EEPROMs allow I2C polling of when a write has completed
    def enable_poll_for_write_complete(self):
        """
            Enable I2C polling of when a write has completed

            :return: Nothing
            :rtype: Void
        """
        self.poll_for_write_complete = True

    # ------------------------------------------------------------------
    # disable_poll_for_write_complete()
    #
    # Disable polling of when a write has completed
    def disable_poll_for_write_complete(self):
        """
            Disable polling of when a write has completed

            :return: Nothing
            :rtype: Void
        """
        self.poll_for_write_complete = False

    # ------------------------------------------------------------------
    # set_I2C_buffer_size(buff_size)
    #
    # Set the size of the TX buffer
    def set_I2C_buffer_size(self, buff_size):
        """
            Set the size of the TX buffer
            
            :param buff_size: the size of the I2C buffer
            :return: nothing
            :rtype: Void
        """
        self.I2C_BUFFER_LENGTH = buff_size
        
    # ------------------------------------------------------------------
    # get_I2C_buffer_size()
    #
    # Return the size of the TX buffer
    def get_I2C_buffer_size(self):
        """
            Return the size of the TX buffer

            :return: I2C_BUFFER_LENGTH_TX
            :rtype: int
        """
        return self.I2C_BUFFER_LENGTH
    
    # ------------------------------------------------------------------
    # read_byte(eeprom_location)
    #
    # Read a byte from a given EEPROM location
    def read_byte(self, eeprom_location):
        """
            Read exactly one byte from EEPROM at a given address location
            
            :param eeprom_location: location in EEPROM to read byte from
            :return: byte read from EEPROM
            :rtype: byte
        """
        read_list = self.read(eeprom_location, 1)
        
        return read_list[0]
    
    # ------------------------------------------------------------------
    # read_int(eeprom_location)
    # 
    # Read a 32-bit signed int from a given EEPROM location
    def read_int(self, eeprom_location):
        """
            Read a 32-bit signed int from a given EEPROM location
            
            :param eeprom_location: location in EEPROM to read int from
            :return: int read from EEPROM
            :rtype: int
        """
        num_bytes = 4   # Default to 32-bit integer
        read_list = self.read(eeprom_location, num_bytes) 
        
        # Convert list of bytes into one big int
        # First, cast list into "bytes" type
        int_bytes = bytes(read_list)
        # Then, conver to int
        int_val = int.from_bytes(int_bytes, "big", signed=True)
        
        return int_val
    
    # ------------------------------------------------------------------
    # read_float(eeprom_location)
    #
    # Read 32-bit float from given EEPROM location
    def read_float(self, eeprom_location):
        """
            Read a 32-bit float from a given EEPROM location
            
            :param eeprom_location: location in EEPROM to read float from 
            :return: float read from EEPROM
            :rtype: float
        """
        num_bytes = 4
        read_list = self.read(eeprom_location, num_bytes)
        
        # Convert list of bytes into a float
        # Use bytearrays as we did in the write_float() function
        byte_float = bytearray(read_list)
        float_tuple = struct.unpack('f', byte_float)
        
        # Extract float value from the tuple returned by the unpack() function
        float_val = float_tuple[0]
                
        return float_val
        
    # ------------------------------------------------------------------
    # read_string(eeprom_location, string_length)
    #
    # Read string of given length from EEPROM
    def read_string(self, eeprom_location, string_length):
        """
            Read a stromg of given length from any address of EEPROM
            
            :param: eeprom_location: location in EEPROM to read string from
            :param string_length: number of chars to read from EEPROM
            :return: string read from EEPROM
            :rtype: string
        """
        read_list = self.read(eeprom_location, string_length)
        
        # Convert a list of byte back into the string
        byte_string = bytearray(read_list)
        decoded_string = byte_string.decode()
        
        return decoded_string
    
    # ------------------------------------------------------------------
    # read(eeprom_location, amt_to_read)
    #
    # Bulk read from EEPROM.
    # Handles breaking up read amt into 32 byte chunks (can be overidden with set_I2C_buffer_size())
    # Handles a read that straddles the 512kbit barrier    
    def read(self, eeprom_location, num_bytes):
        """
            Bulk read from EEPROM.
            Handles breaking up read amt into 32 byte chunks (can be 
            overidden with set_I2C_buffer_size()
            Handles a read that straddles the 512kbit barrier
            
            :param eeprom_location: address of EEPROM to start reading from
            :param num_bytes: number of bytes to be read from external EEPROM
            :return: a list of bytes read from EEPROM
            :rtype: list
        """
        received = 0
        data_list = []

        while received < num_bytes:

            # Limit the amount to write to a page size
            amt_to_read = num_bytes - received
            if amt_to_read > self.I2C_BUFFER_LENGTH:
                amt_to_read = self.I2C_BUFFER_LENGTH
            
            # Check if we are dealing with large (>512kbit) EEPROMs
            i2c_address = self.address
            
            # if self.memory_size_bytes > 0xFFFF:
                # # Figure out if we are going to cross the barrier with this read
                # if eeprom_location + received < 0xFFFF:
                    # if 0xFFFF - (eeprom_location + received) < amt_to_read:   # 0xFFFF - 0xFFFA < 32
                        # amt_to_read = 0xFFFF - (eeprom_location + received) # Limit the read amt to right up to edge of barrier
                    
                # # Figure out if we are accessing the lower half or the upper half
                # if eeprom_location + received > 0xFFFF:
                    # i2c_address |= 0b100    # Set the block bit to 1
              
            # See if EEPROM is available or still writing to a previous request
            if self.poll_for_write_complete == True:
                while self.is_busy(i2c_address) == True:
                    time.sleep(0.001) # This shortens the amount of time waiting between writes but hammers the I2C bus
            
            eeprom_address_MSB = (eeprom_location + received) >> 8
            eeprom_address_LSB = (eeprom_location + received) & 0xFF
        
            write_list = [eeprom_address_MSB, eeprom_address_LSB]
            read_list = list(self._i2c.__i2c_rdwr__(i2c_address, write_list, amt_to_read))
            
            data_list.extend(read_list)
            
            received = received + amt_to_read
        
        return data_list
        
    # ------------------------------------------------------------------
    # write_byte(eeprom_location, byte_to_write)
    #
    # Write a single byte to a given EEPROM location
    def write_byte(self, eeprom_location, byte_to_write):
        """
            Write a single byte to given EEPROM location

            :param eeprom_location: location in EEPROM to byte to 
            :param byte_to_write: byte to write to EEPROM
            :return: Nothing
            :rtype: Void
        """
        byte_list = [byte_to_write]
        self.write(eeprom_location, byte_list)
    
    # ------------------------------------------------------------------
    # write_int()
    #
    # Write a signed 32-bit int to a given EEPROM location
    def write_int(self, eeprom_location, int_to_write):
        """
            Write a signed 32-bit int to a given EEPROM location
            
            :param eeprom_location: location in EEPROM to write int to 
            :param int_to_write: int to write to EEPROM
            :return: Nothing
            :rtype: Void
        """
        # Convert int to a list of bytes
        num_bytes = 4 # Defaulting to 32-bit int
        list_int = list(int_to_write.to_bytes(num_bytes, "big", signed=True))
        
        self.write(eeprom_location, list_int)
    
    # ------------------------------------------------------------------
    # write_float()
    #
    # Write a 32-bit float to a given EEPROM location
    def write_float(self, eeprom_location, float_to_write):
        """
            Write a 32-bit float to a given EEPROM location
            
            :param eeprom_location: location in EEPROM to write float to 
            :param float_to_write: float to write to EEPROM
            :return: Nothing
            :rtype: Void
        """
        # Convert float into a bytearray
        byte_float = bytearray(struct.pack('f', float_to_write))
        # Convert bytearray to list
        list_float = list(byte_float)
        
        self.write(eeprom_location, list_float)
    
    # ------------------------------------------------------------------
    # write_string()
    #
    # Write a string to a given EEPROM location
    def write_string(self, eeprom_location, string_to_write):
        """
            Write a stirng to a given EEPROM location
            
            :param eeprom_location: location in EEPROM to write string to
            :param string_to_write: string to write to EEPROM
            :return: Nothing
            :rtype: Void
        """
        # Encode string to ASCII representation
        encoded_string = string_to_write.encode()
        byte_string = bytearray(encoded_string)
        # Convert bytearray to list
        list_string = list(byte_string)
        
        self.write(eeprom_location, list_string)
        
    # ------------------------------------------------------------------
    # write
    #
    # Write large bulk amounts to EEPROM. Limits writes to the I2C buffer size
    # (default is 32 bytes).
    def write(self, eeprom_location, data_list):
        """
            Write large bulk amounts to EEPROM. Limits write to the I2C buffer size
            (default is 32 bytes).
            
            :param eeprom_location: 2-byte EEPROM address to write to 
            :param data_list: list of data bytes to be written to EEPROM 
                sequentially, starting at the EEPROM address
            :rtype: Void
            :return: nothing
        """
        buffer_size = len(data_list)
        
        # Error check
        if eeprom_location + buffer_size >= self.memory_size_bytes:
            buffer_size = self.memory_size_bytes - eeprom_location
        
        max_write_size = self.page_size_bytes
        if max_write_size > self.I2C_BUFFER_LENGTH - 2:
            max_write_size = self.I2C_BUFFER_LENGTH - 2 # We loose two bytes to the EEPROM address
        
        # Break the buffer into page sized chunks
        recorded = 0
        while recorded < buffer_size:
            
            # Limit the amount to write to either the page size or the Rasp Pi limit
            amt_to_write = buffer_size - recorded
            if amt_to_write > max_write_size:
                amt_to_write = max_write_size
            
            if amt_to_write > 1:
                # check for crossing of a page line. Writes cannot cross a page line.
                page_number_1 = int((eeprom_location + recorded) / self.page_size_bytes)
                page_number_2 = int((eeprom_location + recorded + amt_to_write - 1) / self.page_size_bytes)
                if page_number_2 > page_number_1:
                    amt_to_write = (page_number_2 * self.page_size_bytes) - (eeprom_location + recorded) # Limit the read amt to go right up to edge of page barrier
                    
            i2c_address = self.address
            # # Check if we are dealing with large (>512kbit) EEPROMs
            # if self.memory_size_bytes > 0xFFFF:
                # # Figure out if we are accessing the lower half or the upper half
                # if eeprom_location + recorded > 0xFFFF:
                    # i2c_address |= 0b100    # Set the block bit to 1
            
            # See if EEPROM is available or still writing a previous request
            if self.poll_for_write_complete == True:
                while self.is_busy(i2c_address) == True:   # Poll device
                    time.sleep(0.001) # This shortens the amount of time waiting between writes but hammers the I2C bus
            
            eeprom_address_MSB = (eeprom_location + int(recorded)) >> 8
            eeprom_address_LSB = (eeprom_location + int(recorded)) & 0xFF
            temp_write_list = [eeprom_address_LSB]
            
            for x in range(0, int(amt_to_write)):
                temp_write_list.append(int(data_list[int(recorded) + x]))
            
            # Now, set up the full write
            self._i2c.writeBlock(i2c_address, eeprom_address_MSB, temp_write_list)
                
            # Increment "recorded" counter
            recorded = recorded + amt_to_write

            if self.poll_for_write_complete == False:
                time.sleep(self.page_write_time_ms / 1000) # Delay the amount of time to record a page
            
            # Need to hard-code this delay in because if code falls into the is_busy() call above
            # error messages are printed to the command line when pinging the i2c address when it's busy
            time.sleep(0.005)
