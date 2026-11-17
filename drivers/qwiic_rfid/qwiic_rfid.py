#-----------------------------------------------------------------------------
# qwiic_rfid.py
#
# Python library for the SparkFun qwiic rfid reader.
#   https://www.sparkfun.com/products/15191
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, December 2020
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
qwiic_rfid
============
Python module for the Qwiic RFID Reader.

This python package is a port of the existing [SparkFun Qwiic RFID Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_RFID_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""
#-----------------------------------------------------------------------------

import qwiic_i2c

# Define the device name and I2C addresses. These are set in teh class definition
# as class variables, making them available without having to create a class instance.
# This allows higher level logic to rapidly create an index of qwiic devices at
# runtime.
#
# The name of this device
_DEFAULT_NAME = "Qwiic RFID"

# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x13, 0x14] # Default I2C Address

_AVAILABLE_I2C_ADDRESS += range(0x07, 0x78) # Additional addresses

# QUESTION: what do you do if the i2c address is software configurable?!

# define the class that enxapsulates the device being created. All information associated with this
# device is enxapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicRFID(object):
    """!
    QwiicRFID

    @param address: The I2C address to use for the device.
                        If not provied, the default address is  used.
    @param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.

    @return **Object** The RFID device object.
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Global variables
    ALTERNATE_ADDR = 0x7C
    ADDRESS_LOCATION = 0xC7

    TAG_AND_TIME_REQUEST = 10
    MAX_TAG_STORAGE = 20
    BYTES_IN_BUFFER = 4

    RFID_TAG = None
    RFID_TIME = None
    TAG_ARRAY = [None] * MAX_TAG_STORAGE
    TIME_ARRAY = [None] * MAX_TAG_STORAGE

    # Constructor
    def __init__(self, address=None, i2c_driver=None):
        
        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    # ------------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?
    def is_connected(self):
        """!
        Determine if a Qwiic RFID device is connected to the system.

        @return **void** True if the device is connected, otherwise False.
        """
        return self._i2c.isDeviceConnected(self.address)

    # -------------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """!
        Initialize the operation of the Qwiic GPIO

        @return **void** Returns true if the initialization was successful, otherwise False.
        """
        return self.is_connected()

    # --------------------------------------
    # get_tag()
    #
    # This function gets the RFID tag from the Qwiic RFID Reader. If there is not
    # a tag then it will return an empty string. When the function is called the tag
    # is retrieved but saved to a global struct variable set within the _read_tag_time
    # function. The tag is saved to a local variable, wiped from the global variable, and
    # local variable is returned. This allows me to get both the tag and the
    # associated time the tag was scanned at the same time, while keeping the 
    # function simple.
    def get_tag(self):
        """!
        Gets the current RFID tag

        @return **string** Returns the RFID tag
        """
        # Call the read command that will fill the global struct variable: rfidData
        self._read_tag_time()

        temp_tag = self.RFID_TAG  # Assign the tag to our local variable
        self.RFID_TAG = None   # Clear the global variable
        return temp_tag  # Return the local variable

    # --------------------------------------
    # get_req_time()
    # 
    # This funtion gets the time in seconds of the latest RFID tag was scanned from the Qwiic
    # RFID reader. If there is no tag then the time that is returned will be zero.
    # The information is received in the call to get_tag() above.
    def get_req_time(self):
        """!
        Gets the time when when RFID tag was last scanned

        @return **int** Returns time in seconds
        """
        # Global variable is loaded from get_tag function. 
        # There is no time without a tag scan.
        temp_time = self.RFID_TIME   # Assign the time to the local variable
        self.RFID_TIME = 0   # Clear the global variable
        return temp_time/1000    # Return the local variable in seconds

    # --------------------------------------------
    # get_prec_req_time()
    #
    # This function gets the precise time in seconds of the latest RFID tag was scanned from the Qwiic 
    # RFID reader. If there is no tag then the time that is returned will be zero.
    # The information is received in the call to get_tag() above.
    def get_prec_req_time(self):
        """!
        Gets the time when the RFID tag was last scanned

        @return **int** Returns time in seconds
        """
        # Global variable is loaded from get_tag function. 
        # There is no time without a tag scan.
        temp_time = float(self.RFID_TIME)/1000   # Assign the time to the local variable
        self.RFID_TIME = 0   # Clear the global variable
        return temp_time # Return the local variable in seconds
    
    # ---------------------------------------------
    # clear_tags()
    #
    # This function clears the buffer from the Qwiic RFID reader by reading them
    # but not storing them.
    def clear_tags(self):
        """!
        Reads and clears the tags from the buffer
        """
        self._read_all_tags_times(self.MAX_TAG_STORAGE)

    # --------------------------------------------
    # get_all_tags(tagArray[MAX_TAG_STORAGE])
    #
    # This function gets all the available tags on the Qwiic RFID reader's buffer.
    # The buffer on the Qwiic RFID holds 20 tags and their scan time. Not knowing
    # how many are available until the i2c buffer is read, the parameter is a full
    # 20 element array.
    def get_all_tags(self, tag_array):
        """!
        Gets all the tags in the buffer

        @param tag_array: list of upto 20 RFID tag numbers
        """
        # Load up the global struct variables
        self._read_all_tags_times(self.MAX_TAG_STORAGE)

        for i in range(0, self.MAX_TAG_STORAGE):
            tag_array[i] = self.TAG_ARRAY[i]  # Load up passed array with tag
            self.TAG_ARRAY[i] = ""   # Clear global variable

    # ---------------------------------------------
    # get_all_prec_times(time_array)
    # 
    # This function gets all the available precise scan times associated with the scanned RFID tags.
    # The buffer on the Qwiic RFID holds 20 tags and their scan time. Not knowing
    # how many are available until the I2C buffer is read, the parameter is a full 20 element
    # array.
    # A note on the time: the time is not the time of the day when the tage was scanned
    # but actually the time between when the tag was scanned and when it was read from the I2C bus.
    def get_all_prec_times(self, time_array):
    
        """!
        Gets all times in the buffer

        @param time_array: list of upto 20 times the RFID tag was read from the I2C bus
        """
        for i in range(0, self.MAX_TAG_STORAGE):
            time_array[i] = self.TIME_ARRAY[i]    # Load up passed array with time in seconds
            time_array[i] = float(time_array[i])/1000
            self.TIME_ARRAY[i] = 0   # Clear global variable

    # ----------------------------------------------
    # change_address(new_address)
    #
    # This function changes the I2C address of the Qwiic RFID. The address
    # is written to the memory location in EEPROM that determines its address.
    def change_address(self, new_address):
        """!
        Changes the I2C address of the Qwiic RFID reader

        @param new_address: the new address to set the RFID reader to
        
        @return **bool** False if the address is out of range
        """
        if new_address < 0x07 or new_address > 0x78:
            return False
        
        self._i2c.writeByte(self.address, self.ADDRESS_LOCATION, new_address)
        
        self.address = new_address

    # ------------------------------------------------
    # _read_tag_time()
    # 
    # This function handles the I2C transaction to get the RFID tag and 
    # time from the Qwiic RFID reader. What comes in from the RFID reader is a 
    # number that was converted from a string to its direct numerical
    # representation which is then converted back to its original state. The tag
    # and the time is saves to the global variables.
    def _read_tag_time(self):
        """!
        Handles the I2C transaction to get the RFID tag and time
        """
        _temp_tag_str = ""  
        _temp_time = 0

        # What is read from the buffer is immediately converted to a string and 
        # concatenated onto the temporary variable.
        _temp_tag_list = self._i2c.readBlock(self.address, 0, 10)
        
        for i in range(0, 6):
            _temp_tag_str += str(_temp_tag_list[i])
        
        # The tag is copied to the global variable
        self.RFID_TAG = _temp_tag_str
        
        # Bring in the time
        if self.RFID_TAG == "000000":    # If the tag is blank

            # Time is zero if there is not a tag
            _temp_time = 0
        
        else:
            _temp_time = int(_temp_tag_list[6]) * 16 ** (6) + int(_temp_tag_list[7]) * 16 ** (4) + int(_temp_tag_list[8]) * 16 ** (2) + int(_temp_tag_list[9])
            
        # Time is copied to the global variable
        self.RFID_TIME = _temp_time   # Time in milliseconds

    # ----------------------------------------------------
    # _read_all_tags_times(_num_of_reads)
    #
    # This function differs from the above by populating an array of 20 elements that
    # drains the entire available rfid buffer on the Qwiic RFID Reader. Similar to the
    # function above it handles the I2C transaction to get the RFID tags time from the 
    # Qwiic RFID Reader. What comes in the form of the RFID reader is a number that was
    # converted from a string to it's direct numerical representation which is then 
    # converted back to its' original state.
    def _read_all_tags_times(self, _num_of_reads):
        """!
        Populates an array of 20 RFID tags/times and drains available RFID buffer on the Reader.

        @param _num_of_reads: int number of bytes to read
        """        
        for i in range(0, _num_of_reads):
            _temp_tag_str = ""
            _temp_time = 0
        
            # What is read from the buffer is immediately converted to a string and 
            # concatenated onto the temporary variable.
            _temp_tag_list = self._i2c.readBlock(self.address, 0, 10)
        
            for j in range(0, 6):
                _temp_tag_str += str(_temp_tag_list[j])
        
            # The tag is copied to the global array
            self.TAG_ARRAY[i] = _temp_tag_str
            
            # Bring in the time but only if there is a tag
            if self.TAG_ARRAY[i] == "000000":    # Blank tag

                # Time is zero since there is no tag
                _temp_time = 0
            
            else:
                _temp_time = int(_temp_tag_list[6]) * 16 ** (6) + int(_temp_tag_list[7]) * 16 ** (4) + int(_temp_tag_list[8]) * 16 ** (2) + int(_temp_tag_list[9])
            
            # Time is copied to the global array
            self.TIME_ARRAY[i] = _temp_time   # Convert to seconds            
