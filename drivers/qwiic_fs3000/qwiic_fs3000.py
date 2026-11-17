#-------------------------------------------------------------------------------
# qwiic_fs3000.py
#
# Python library for the SparkFun Qwiic FS3000, available here:
# https://www.sparkfun.com/products/18768A
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
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

"""!
qwiic_fs3000
============
Python module for the [SparkFun Qwiic FS300](https://www.sparkfun.com/products/18768A)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_FS3000_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic FS3000"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x28] # Note, the FS3000 does not have an adjustable address.

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicFS3000(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    kAirflowRange7Mps = 0 # FS3000-1005 has a range of 0-7.23 meters per second
    kAirflowRange15Mps = 1 # FS3000-1015 has a range of 0-15 meters per second

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

        self._range = self.kAirflowRange7Mps # defaults to FS3000-1005 range
        self._mps_data_point = [0, 1.07, 2.01, 3.00, 3.97, 4.96, 5.98, 6.99, 7.23] # defaults to FS3000-1005 datapoints
        self._raw_data_point = [409, 915, 1522, 2066, 2523, 2908, 3256, 3572, 3686] # defaults to FS3000-1005 datapoints

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        return self.is_connected()

    def set_range(self, range):
        """!
        There are two varieties of this sensor (1) FS3000-1005 (0-7.23 m/sec)
        and (2) FS3000-1015 (0-15 m/sec)

        Valid input arguments are:
        AIRFLOW_RANGE_7_MPS
        AIRPLOW_RANGE_15_MPS

        Note, this also sets the datapoints (from the graphs in the datasheet pages 6 and 7).
        These datapoints are used to convert from raw values to m/sec - and then mph.

        @param int range: The range of the sensor

        @return **bool** Returns `True` if successful, otherwise `False`
        """

        if range == self.kAirflowRange7Mps:
            self._mps_data_point = [0, 1.07, 2.01, 3.00, 3.97, 4.96, 5.98, 6.99, 7.23] # FS3000-1005 datapoints
            self._raw_data_point = [409, 915, 1522, 2066, 2523, 2908, 3256, 3572, 3686] # FS3000-1005 datapoints
        elif range == self.kAirflowRange15Mps:
            self._mps_data_point = [0, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00, 11.00, 13.00, 15.00] # FS3000-1015 datapoints
            self._raw_data_point = [409, 1203, 1597, 1908, 2187, 2400, 2629, 2801, 3006, 3178, 3309, 3563, 3686] # FS3000-1015 datapoints
        else:
            return False
        
        return True
        
    def checksum(self, data_in):
        """!
        CHECKSUM
        Check to see that the CheckSum is correct, and data is good
        Return true if all is good, return false if something is off   
        The entire response from the FS3000 is 5 bytes.
        [0]Checksum
        [1]data high
        [2]data low
        [3]generic checksum data
        [4]generic checksum data

        @param list data_in: The data to check

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        sum = 0
        for i in range (1,5):
            sum += data_in[i]
        
        sum = sum % 256
        crc_byte = data_in[0]
        overall = sum+crc_byte
        overall = overall % 256

        return overall == 0
    
    def read_raw(self):
        """!
        Read from sensor, checksum, return raw data (409-3686)

        @return **int** The raw value from the sensor (or -1 on error)
        """

        buff = self._i2c.read_block(self.address, None, 5) # Pass None for the command, this is a read not from a specific register. Will only work with newer versions of Qwiic_I2c_Py

        if not self.checksum(buff):
            return -1
        
        airflow_raw = 0
        data_high_byte = buff[1]
        data_low_byte = buff[2]

        # The flow data is a 12-bit integer. 
        # Only the least significant four bits in the high byte are valid.
        # clear out (mask out) the unnecessary bits
        data_high_byte = data_high_byte & 0x0F

        # combine the high and low bytes
        airflow_raw = (data_high_byte << 8) | data_low_byte

        return airflow_raw
    
    def read_meters_per_second(self):
        """!
        Read from sensor, checksum, return m/s (0-7.23)

        @return **float** The air velocity value in meters per second (or -1 on error)
        """

        airflow_raw = self.read_raw()

        if airflow_raw == -1:
            return -1

        # convert from Raw readings to m/s.
        # There is an output curve on datasheet page 8.
        # it has 9 data points, and it's not a perfectly straight line.
        # let's create two arrays to contain the conversion data.
        # Then we can find where our reading lives in the array, 
        # then we can consider it a straight line conversion graph between each data point.

        # find where our raw data fits in the arrays
        data_position = 0

        for i in range(len(self._raw_data_point)):
            if airflow_raw > self._raw_data_point[i]:
                data_position = i

        # set limits on min and max.
        # if we are at or below 409, we'll bypass conversion and report 0.
        # if we are at or above 3686, we'll bypass conversion and report max (7.23 or 15)
        if airflow_raw <= 409:
            return 0
        if airflow_raw >= 3686:
            return self._mps_data_point[-1]
        
        # look at where we are between the two data points in the array.
        # now use the percentage of that window to calculate m/s

        # calculate the percentage of the window we are at.
        # using the data_position, we can find the "edges" of the data window we are in
        # and find the window size

        window_size = self._raw_data_point[data_position + 1] - self._raw_data_point[data_position]

        # diff is the amount (difference) above the bottom of the window
        diff = airflow_raw - self._raw_data_point[data_position]

        percentage_of_window = diff / window_size

        # calculate window size from MPS data points
        mps_window_size = self._mps_data_point[data_position + 1] - self._mps_data_point[data_position]

        # add percentage of window_mps to mps
        airflowMps = self._mps_data_point[data_position] + (percentage_of_window * mps_window_size)

        return airflowMps
    
    def read_miles_per_hour(self):
        """!
        Read from sensor, checksum, return mph (0-33ish)

        @return **float** The air velocity value in miles per hour (or -1 on error)
        """

        airflowMps = self.read_meters_per_second()

        if airflowMps == -1:
            return -1

        # convert m/s to mph
        airflowMph = airflowMps * 2.2369362912

        return airflowMph