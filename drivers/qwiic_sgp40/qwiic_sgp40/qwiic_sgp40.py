#-----------------------------------------------------------------------------
# qwiic_sgp40.py
#
# Python library for the SparkFun Air Quality Sensor - SGP40 (Qwiic).
#   https://www.sparkfun.com/products/18345
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
# This python module heavily is heavily based on the driver written by 
# DFRobot and leverages its VOC algorithm. It can be found here:
# https://github.com/DFRobot/DFRobot_SGP40/tree/master/Python/raspberrypi
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
qwiic_sgp40
===========
Python module for the SparkFun Air Quality Sensor - SGP40 (Qwiic).

This package is a port of the existing [SparkFun SGP40 Arduino Library](https://github.com/sparkfun/SparkFun_SGP40_Arduino_Library) and is heavily based on the driver written by [DFRobot](https://github.com/DFRobot/DFRobot_SGP40/tree/master/Python/raspberrypi).

This package can be used in conjunction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun Qwiic Ecosystem](https://www.sparkfun.com/qwiic).
"""
# ----------------------------------------------------------------------

import time
import qwiic_i2c
from . import DFRobot_SGP40_VOCAlgorithm

_DEFAULT_NAME = "Qwiic SGP40"

_AVAILABLE_I2C_ADDRESS = [0x59]

class QwiicSGP40(object):
    """!
    QwiicSGP40

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided a
                        a driver object is created.

    @return **Object** The GPIO device object.
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS
  
    # SGP40 I2C commands
    SGP40_MEASURE_RAW = [0x26, 0x0F]
    SGP40_MEASURE_TEST = [0x28, 0x0E]
    SGP40_HEATER_OFF = [0x36, 0x15]
    SGP40_SOFT_RESET = [0x00, 0x06]
  
    # SGP40 Measure Test Results
    SGP40_MEASURE_TEST_PASS = [0xD4, 0x00]
    SGP40_MEASURE_TEST_FAIL = [0x4B, 0x00]
  
    DURATION_WAIT_MEASURE_TEST = 0.25
    DURATION_READ_RAW_VOC = 0.03
  
    # Constructor
    def __init__(self, address=None, i2c_driver=None):
    
        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]
    
        # Load the I2C driver is one isn't provided
        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver
                
        self.__my_vocalgorithm = DFRobot_SGP40_VOCAlgorithm.DFRobot_VOCAlgorithm()
        self.__rh = 0
        self.__temc = 0
        self.__rh_h = 0
        self.__rh_l = 0
        self.__temc_h = 0
        self.__temc_l = 0
        self.__temc__crc = 0
        self.__rh__crc = 0

    # --------------------------------------------------------------------
    # is_connected()
    #
    # Is an actual board connected to our sysem?
    def is_connected(self):
        """!
        Determine if a Qwiic SGP40 device is connected to the system.

        @return **bool** True if the device is connected, false otherwise.
        """
        return self._i2c.isDeviceConnected(self.address)

    # --------------------------------------------------------------------
    # begin()
    # 
    # Initialize I2C communication and wait through warm-up time.
    def begin(self, warm_up_time = 10):
        """!
        Initialize the operation of the Qwiic SGP40 and wait through warm-
            up time. Run is_connected() and measure_test().

        @return **bool** Returns true if the intialization was successful, false otherwise.
        """
        if self.is_connected() == True:
            
            print("\nWaiting " + str(warm_up_time) + " seconds for the SGP40 to warm-up.")
            
            self.__my_vocalgorithm.vocalgorithm_init()
            start_time = int(time.time())
            while(int(time.time()) - start_time < warm_up_time):
                self.get_VOC_index()
            return self.measure_test()
        
        return False

    # --------------------------------------------------------------------
    # measure_test()
    #
    # Sensor runs chip self test
    def measure_test(self):
        """!
        Sensor runs chip self test.

        @return **int** Returns 0 if the self-test succeeded and 1 if it failed.
        """
        temp0 = self.SGP40_MEASURE_TEST[0]
        temp1 = self.SGP40_MEASURE_TEST[1]
        
        self._i2c.writeByte(self.address, temp0, temp1)
        time.sleep(self.DURATION_WAIT_MEASURE_TEST)
        result = self._i2c.readBlock(self.address, 0, 3)
        
        if result[0] == self.SGP40_MEASURE_TEST_PASS[0] and result[1] == self.SGP40_MEASURE_TEST_PASS[1]:
            return 0
        else:
            return 1

    # --------------------------------------------------------------------
    # soft_reset()
    #
    # Performs a soft reset
    def soft_reset(self, ignore_error = True):
        """!
        Sensor reset

        @param bool, optional ignore_error: Whether to ignore exception that can be raised
            due to no ACK after reset command, defaults to True
        """
        temp0 = self.SGP40_SOFT_RESET[0]
        temp1 = self.SGP40_SOFT_RESET[1]

        # Attempt to reset the sensor. The SGP40 does not send back an ACK, so
        # an error is expected. If ignore_error is False, the error is raised.
        try:
            self._i2c.writeByte(self.address, temp0, temp1)
        except:
            if ignore_error == False:
                raise

    # --------------------------------------------------------------------
    # heater_off()
    #
    # Turns the heater off
    def heater_off(self):
        """!
        Turns the hotplate off and puts sensor in idle mode.
        """
        temp0 = self.SGP40_HEATER_OFF[0]
        temp1 = self.SGP40_HEATER_OFF[1]
        self._i2c.writeByte(self.address, temp0, temp1)

    # --------------------------------------------------------------------
    # measure_raw(__relative_humidity, __temperature_c)
    #
    # The raw signal is returned in SRAW_ticks. The user can provide relative
    # humidity or temperature parameters if desired.
    def measure_raw(self, __relative_humidity = 50, __temperature_c = 25):
        """!
        Returns the raw data. See the SGP40 datasheet for more info.

        @param SRAW_ticks: variable to assign raw measurement to
        @param __relative_humidity: float relative humidity between 0 and 100%.
        @param __temperature_c: float temperature in celcius between -45 and 130 degrees.

        @return **int** 0 if CRC checks out, -1 otherwise
        """
        # Check boundaries of relative humidity and temperature
        if __relative_humidity < 0:
            __relative_humidity = 0
        if __relative_humidity > 100:
            __relative_humidity = 100
        if __temperature_c < -45:
            __temperature_c = -45
        if __temperature_c > 130:
            __temperature_c = 130

        
        # Calculate relative humidity and temperature ticks
        self.__rh = int(((__relative_humidity*65535)/100+0.5))
        self.__temc = int(((__temperature_c+45)*(65535/175)+0.5))
        # Break it into bytes and calculate CRC
        self.__rh_h = int(self.__rh)>>8
        self.__rh_l = int(self.__rh)&0xFF
        self.__rh__crc = self.__crc(self.__rh_h, self.__rh_l)
        self.__temc_h = int(self.__temc)>>8
        self.__temc_l = int(self.__temc)&0xFF
        self.__temc__crc = self.__crc(self.__temc_h, self.__temc_l)
        
        temp0 = int(self.SGP40_MEASURE_RAW[0])
        temp1 = int(self.SGP40_MEASURE_RAW[1])
        write_bytes = [temp1, int(self.__rh_h), int(self.__rh_l), int(self.__rh__crc), int(self.__temc_h), int(self.__temc_l), int(self.__temc__crc)]
        
        self._i2c.writeBlock(self.address, temp0, write_bytes)

        time.sleep(self.DURATION_READ_RAW_VOC)
        
        # Data is read back in 3 bytes: data (MSB) / data (LSB) / Cecksum
        result = self._i2c.readBlock(self.address, 0, 3)
        
        if self.__check_crc(result) == 0:
            return result[0]<<8 | result[1]
        else:
            return -1
    
    # --------------------------------------------------------------------
    # __check__crc(raw)
    #
    # Verify the calibration value of the sensor
    def __check_crc(self, raw):
        """!
        Verify the calibration value of the sensor

        @param raw: list parameter to check

        @return **int** -1 if the check failed, 0 if it succeeded
        """
        assert (len(raw) == 3)
        if self.__crc(raw[0], raw[1]) != raw[2]:
            return -1
        return 0
    
    # --------------------------------------------------------------------
    # __crc(data_1, data_2)
    #
    # CRC calculation
    def __crc(self, data_1, data_2):
        """!
        CRC calculation

        @param data_1: high 8 bits of data
        @param data_2: low 8 bits of data

        @return **int** calibration value
        """
        crc = 0xff
        list = [data_1, data_2]
        for i in range(0, 2):
            crc = crc ^ list[i]
            for bit in range(0, 8):
                if (crc & 0x80):
                    crc = ((crc << 1) ^ 0x31)
                else:
                    crc = (crc << 1)
            
            # TODO: not sure if this line is necessary.
            # It is not in the datasheet sample code pg 12
            crc = crc & 0xFF
        return crc
            
    # --------------------------------------------------------------------
    # get_VOC_index(self.__relative_humidity, self.__tempertature_c)
    #
    # Get VOC index
    def get_VOC_index(self, __relative_humidity = 50, __temperature_c = 25):
        """!
        Get VOC index

        @param __relative_humidity: float relative humidity between 0 and 100%.
        @param __temperature_c: float temperature in celcius between -45 and 130 degrees.

        @return **int** VOC index
        """
        raw = self.measure_raw(__relative_humidity, __temperature_c)

        if raw < 0:
            return -1
        else:
            voc_index = self.__my_vocalgorithm.vocalgorithm_process(raw)
            return voc_index 