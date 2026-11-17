#-----------------------------------------------------------------------------
# qwiic_titan_gps.py
#
# Python library for the SparkFun's GPS Breakout - XA1110. 
#
# SparkFun GPS Breakout - XA1110
#   https://www.sparkfun.com/products/14414
#
#------------------------------------------------------------------------
#
# Written by SparkFun Electronics, November 2019
#
# This python library supports the SparkFun Electroncis Qwiic sensor/board
# ecosystem.
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
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
# The goal of this is to keep the public interface pythonic, but internal is
# internal and code is kept as close to its Arduino source library as possible.
#
# pylint: disable=line-too-long, bad-whitespace, invalid-name, too-many-public-methods
#

"""!
qwiic_titan_gps
===============
Python library for `SparkFun GPS Breakout -
XA1110 <https://www.sparkfun.com/products/14414>`_

This python package is a port of the existing `SparkFun GPS Arduino Library <https://github.com/sparkfun/SparkFun_I2C_GPS_Arduino_Library>`_.

This package can be used in conjunction with the overall `SparkFun Qwiic Python Package <https://github.com/sparkfun/Qwiic_Py>`_

New to Qwiic? Take a look at the entire `SparkFun Qwiic ecosystem <https://www.sparkfun.com/qwiic>`_.
"""

import sys
import qwiic_i2c
from .micropyGPS import MicropyGPS

#======================================================================
# NOTE: For Raspberry Pi
#======================================================================
# For this sensor to work on the Raspberry Pi, I2C clock stretching
# must be enabled.
#
# To do this:
#   - Login as root to the target Raspberry Pi
#   - Open the file /boot/config.txt in your favorite editor (vi, nano ...etc)
#   - Scroll down until the block that contains the following is found:
#           dtparam=i2c_arm=on
#           dtparam=i2s=on
#           dtparam=spi=on
#   - Add the following line:
#           # Enable I2C clock stretching
#           dtparam=i2c_arm_baudrate=10000
#
#   - Save the file
#   - Reboot the Raspberry Pi
#======================================================================

def __checkIsOnRPi():

    # Are we on a Pi or Linux?

    if sys.platform not in ('linux', 'linux2'):
        return False

    # we can find out if we are on a RPI by looking at the contents
    # of /proc/device-tree/compatible

    try:
        with open('/proc/device-tree/compatible', 'r') as fCompat:

            systype = fCompat.read()

            return systype.find('raspberrypi') != -1
    except IOError:
        return False

# check if stretching is set if on a Raspberry Pi. 
#
def _checkForRPiI2CClockStretch():

    # Check if we're on a Raspberry Pi first.
    if not __checkIsOnRPi():
        return

    # read the boot config file and see if the clock stretch parameter is set
    try:
        with open('/boot/config.txt') as fConfig:

            strConfig = fConfig.read()
            for line in strConfig.split('\n'):
                if line.find('i2c_arm_baudrate') == -1:
                    continue

                # start with a comment?
                if line.strip().startswith('#'):
                    break

                # is the value less <= 10000
                params = line.split('=')
                if int(params[-1]) <= 10000:
                    # Stretching is enabled and set correctly.
                    return

                break
    except IOError:
        pass

    # if we are here, then we are on a Raspberry Pi and Clock Stretching isn't
    # set correctly.
    # Print out a message!

    print("""!
        ============================================================================
 NOTE:

 For the SparkFun GPS Breakout to work on the Raspberry Pi, I2C clock stretching
 must be enabled.

 The following line must be added to the file /boot/config.txt

    dtparam=i2c_arm_baudrate=10000

 For more information, see the note at:
          https://github.com/sparkfun/qwiic_ublox_gps_py
============================================================================
        """)

# Define the device name and I2C addresses. These are set in the class definition
# as class variables, making them available without having to create a class instance.
# This allows higher level logic to rapidly create a index of Qwiic devices at
# runtime.
#
# The name of this device
_DEFAULT_NAME = "Qwiic Titan GPS"

# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x10]

class QwiicTitanGps(object):
    """!
    QwiicTitanGps

    @param address: The I2C address to use for the device.
                    If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided
                    a driver object is created.

    @return **Object** The Qwiic Titan GPS device object.
    """

    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    MAX_I2C_BUFFER = 32
    MAX_GPS_BUFFER = 255

    _RPiCheck = False

    gnss_messages = {
        'Time'           : 0,
        'Latitude'       : 0,
        'Lat_Direction'  : "",
        'Longitude'      : 0,
        'Long_Direction' : "",
        'Altitude'       : 0,
        'Sat_Number'     : 0,
        'Geo_Separation' : 0,
    }

    def __init__(self, address=None, i2c_driver=None):


        # As noted above, to run this device on a Raspberry Pi,
        # clock stretching is needed.
        #
        # Lets check if it's enabled. This is done only once in
        # the session
        if not QwiicTitanGps._RPiCheck:
            _checkForRPiI2CClockStretch()
            QwiicTitanGps._RPiCheck = True

        # Did the user specify an I2C address?

        self.address = address if address is not None else self.available_addresses[0]

        # load the I2C driver if one isn't provided

        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

        self.gps = MicropyGPS(location_formatting='dd')

    # ----------------------------------

    def is_connected(self):

        """!
        Determine if a GPS device is connected to the system..

        @return **bool** True if the device is connected, otherwise False.
        """
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):

        """!
        Initialize the data transmission lines.

        @return **boolean** Returns True on success, False on failure
        """
        return self.is_connected()

    def get_raw_data(self):
        """!
        This function pulls GPS data from the module 255 bytes at a time.

        @return **String** A string of all the GPS data.
        """
        raw_sentences = ""
        buffer_tracker = self.MAX_GPS_BUFFER
        raw_data = []

        while buffer_tracker != 0:

            if buffer_tracker > self.MAX_I2C_BUFFER:
                raw_data.extend(self._i2c.readBlock(self.address, 0x00,
                                                    self.MAX_I2C_BUFFER))
                buffer_tracker = buffer_tracker - self.MAX_I2C_BUFFER
                if raw_data[0] == 0x0A:
                    break

            elif buffer_tracker < self.MAX_I2C_BUFFER:
                raw_data.extend(self._i2c.readBlock(self.address, 0x00,
                                                    buffer_tracker))
                buffer_tracker = 0
                if raw_data[0] == 0x0A:
                    break

            for raw_bytes in raw_data:
                raw_sentences = raw_sentences + chr(raw_bytes)

        return raw_sentences

    def prepare_data(self):

        """!
        This function seperates raw GPS data from the module into sentences
        of GNSS data.

        @return **List** A list of all the gathered GPS data.
        """
        sentences = self.get_raw_data()
        clean_gnss_list = []
        complete_sentence_list = []
        gnss_list = sentences.split('\n')

        for sentence in gnss_list:
            if sentence is not '':
                clean_gnss_list.append(sentence)

        for index,sentence in enumerate(clean_gnss_list):
            if not sentence.startswith('$') and index is not 0:
                joined = clean_gnss_list[index - 1] + sentence
                complete_sentence_list.append(joined)
            else:
                complete_sentence_list.append(sentence)

        return complete_sentence_list

    def get_nmea_data(self):

        """!
        This function takes a list of GNSS sentences and uses the pynmea2
        parser to parse the data.

        @return **Boolean** Returns True on success and False otherwise
        """
        gps_data = self.prepare_data()
        msg = ""
        for sentence in gps_data:
            self.feed_sentence(sentence)
            self.add_to_gnss_messages()

        return True
    
    def feed_sentence(self, sentence):
        """!
        Feeds a NMEA sentence to the GPS parser one character at a time
        """
        for b in sentence:
            self.gps.update(b)

    def add_to_gnss_messages(self):
        """!
        This function takes parsed GNSS data and assigns them to the
        respective dictionary key.

        @return **Boolean** Returns True
        """
        try:
            self.gnss_messages['Time'] = self.gps.timestamp
            self.gnss_messages['Lat_Direction'] = self.gps.latitude[1]
            self.gnss_messages['Long_Direction'] = self.gps.longitude[1]
            self.gnss_messages['Latitude'] = self.gps.latitude[0]
            self.gnss_messages['Longitude'] = self.gps.longitude[0]
            self.gnss_messages['Altitude'] = self.gps.altitude
            self.gnss_messages['Sat_Number'] = self.gps.satellites_in_use
            self.gnss_messages['Geo_Separation'] = self.gps.geoid_height
        except KeyError:
            pass
        except AttributeError:
            pass

        return True
