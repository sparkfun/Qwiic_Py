#-------------------------------------------------------------------------------
# qwiic_tmp117.py
#
# Python library for the SparkFun Qwiic TMP117, available here:
# https://www.sparkfun.com/products/15805
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
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
qwiic_template
============
Python module for the [SparkFun Qwiic TMP117 High Precision Temperature Sensor](https://www.sparkfun.com/products/15805)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_TMP117_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic TMP117"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x48, 0x49, 0x4A, 0x4B]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicTMP117(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Register Addresses:
    kRegTempResult = 0x00
    kRegConfiguration = 0x01
    kRegTHighLimit = 0x02
    kRegTLowLimit = 0x03
    kRegEepromUl = 0x04
    kRegEeprom1 = 0x05
    kRegEeprom2 = 0x06
    kRegTempOffset = 0x07
    kRegEeprom3 = 0x08
    kRegDeviceId = 0x0F

    # Configuration Register Masks and Shifts:
    kConfigSoftResetShift = 1
    kConfigSoftResetMask  = 0b1 << kConfigSoftResetShift

    kConfigDrAlertShift = 2
    kConfigDrAlertMask = 0b1 << kConfigDrAlertShift

    kConfigPolShift = 3
    kConfigPolMask = 0b1 << kConfigPolShift

    kConfigTNaShift = 4
    kConfigTNaMask = 0b1 << kConfigTNaShift
    
    kConfigAvgShift = 5
    kConfigAvgMask = 0b11 << kConfigAvgShift

    kConfigConvShift = 7
    kConfigConvMask = 0b111 << kConfigConvShift

    kConfigModShift = 10
    kConfigModMask = 0b11 << kConfigModShift

    kConfigEepromBusyShift = 12
    kConfigEepromBusyMask = 0b1 << kConfigEepromBusyShift

    kConfigDataReadyShift = 13
    kConfigDataReadyMask = 0b1 << kConfigDataReadyShift

    kConfigLowAlertShift = 14
    kConfigLowAlertMask = 0b1 << kConfigLowAlertShift

    kConfigHighAlertShift = 15
    kConfigHighAlertMask = 0b1 << kConfigHighAlertShift
    
    # Device ID Register Masks and Shifts:
    kConfigDeviceIdShift = 0
    kConfigDeviceIdMask = 0xFFF

    kConfigRevShift = 12
    kConfigRevMask = 0xF << kConfigRevShift

    # Conversion Modes
    kContinuousConversionMode = 0b00  # Continuous Conversion Mode
    kOneShotMode = 0b11  # One Shot Conversion Mode
    kShutdownMode = 0b01  # Shutdown Conversion Mode

    # Therm/alert Modes
    kThermMode = 1
    kAlertMode = 0

    # Conversion Averaging Modes
    kConvAvgNone = 0b00  # No Averaging
    kConvAvg8 = 0b01  # 8 Averaged Conversions
    kConvAvg32 = 0b10  # 32 Averaged Conversions
    kConvAvg64 = 0b11  # 64 Averaged Conversions

    # Constants to index into the Return Value of get_high_low_alert()
    kLowAlertIdx = 0
    kHighAlertIdx = 1

    # Misc Constants:
    kDeviceIdValue = 0x0117  # Value found in the device ID register on reset (page 24 Table 3 of datasheet)
    kTmp117Resolution = 0.0078125  # Resolution of the device, found on (page 1 of datasheet)


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

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received

        if not self._i2c.isDeviceConnected(self.address):
            return False

        # Check the device has a product ID register
        deviceId = self.read_register(self.kRegDeviceId)

        return deviceId == self.kDeviceIdValue

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """

        # Confirm device is connected before doing anything
        return self.is_connected()
    
    def get_address(self):
        """!
        Returns the I2C address of the device

        @return **int** The I2C address of the device
        """
        return self.address
    
    def read_temp_c(self):
        """!
        This function reads the temperature reading from the sensor
	    and returns the value in degrees celsius.

        @return **float** The temperature in degrees celsius
        """
        rawTemp = self.read_register(self.kRegTempResult)
        
        # Convert to signed 16-bit value
        if rawTemp > 32767:
            rawTemp -= 65536

        return rawTemp * self.kTmp117Resolution
    
    def read_temp_f(self):
        """!
        This function calculates the fahrenheit reading from the
	    celsius reading initially found.

        @return **float** The temperature in degrees fahrenheit
        """
        return self.read_temp_c() * 1.8 + 32

    def get_temperature_offset(self):
        """!
        This function reads the temperature offset value from the device

        @return **float** The temperature offset value
        """
        offset = self.read_register(self.kRegTempOffset)
        
        # Convert to signed 16-bit value
        if offset > 32767:
            offset -= 65536
        return offset * self.kTmp117Resolution

    def set_temperature_offset(self, offset):
        """!
        This function sets the temperature offset value on the device

        @param float offset: The offset value to set
        """
        # Convert to 16-bit value
        offset = int(offset / self.kTmp117Resolution)
        
        # Write the offset to the device
        self.write_register(self.kRegTempOffset, offset)

    def get_low_limit(self):
        """!
        This function reads the low limit register that is set by the user.

        @return **float** The low limit temperature in degrees celsius
        """
        lowLimit = self.read_register(self.kRegTLowLimit)
        
        # Convert to signed 16-bit value
        if lowLimit > 32767:
            lowLimit -= 65536

        return lowLimit * self.kTmp117Resolution
    
    def set_low_limit(self, lowLimit):
        """!
        This function allows the user to set the low limit register to whatever
        specified value, as long as in the range for the temperature sensor. This
        function can be used as a threshold for Therm mode and or Alert mode.

        @param float lowLimit: The low limit temperature in degrees celsius
        """
        scaledLimit = int(lowLimit / self.kTmp117Resolution)
        self.write_register(self.kRegTLowLimit, scaledLimit)

    def get_high_limit(self):
        """!
        This function reads the high limit register that is set by the user.

        @return **float** The high limit temperature in degrees celsius
        """
        highLimit = self.read_register(self.kRegTHighLimit)
        
        # Convert to signed 16-bit value
        if highLimit > 32767:
            highLimit -= 65536

        return highLimit * self.kTmp117Resolution
    
    def set_high_limit(self, highLimit):
        """!
        This function allows the user to set the high limit register to whatever
	    specified value, as long as in the range for the temperature sensor. This
	    function can be used as a threshold for Therm mode and or Alert mode

        @param float highLimit: The high limit temperature in degrees celsius
        """
        scaledLimit = int(highLimit / self.kTmp117Resolution)
        self.write_register(self.kRegTHighLimit, scaledLimit)

    def get_configuration_register(self):
        """!
        This function reads configuration register. Use this function if you need to read
        certain flags before they are cleared. This can be found on page 25 of the
        datasheet.

        @return **int** The configuration register value
        """
        return self.read_register(self.kRegConfiguration)
    
    def get_high_low_alert(self):
        """!
        This function reads configuration register and saves the high and low alert flags. 
	    Use this function if you need to read the alert flags before they are cleared.

        @return **list of bool** The high and low alert flags in a list [low, high]

        Index into the list with the kLowAlertIdx and kHighAlertIdx constants
        """
        configReg = self.read_register(self.kRegConfiguration)
        highAlert = ( (configReg & self.kConfigHighAlertMask) == self.kConfigHighAlertMask )
        lowAlert = ( (configReg & self.kConfigLowAlertMask) == self.kConfigLowAlertMask )
        return [lowAlert, highAlert]
    
    def get_high_alert(self):
        """!
        This function reads the 15th bit of the configuration register to
        tell if the conversion result is higher than the high limit. This
        is set as a High Alert flag.

        @return **bool** `True` if the high alert flag is set, otherwise `False`
        """
        configReg = self.read_register(self.kRegConfiguration)
        return ( (configReg & self.kConfigHighAlertMask) == self.kConfigHighAlertMask )

    def get_low_alert(self):
        """!
        This function reads the 14th bit of the configuration register to
        tell if the conversion result is lower than the low limit. This
        is set as a Low Alert flag.

        @return **bool** `True` if the low alert flag is set, otherwise `False`
        """
        configReg = self.read_register(self.kRegConfiguration)
        return ( (configReg & self.kConfigLowAlertMask) == self.kConfigLowAlertMask )
    
    def set_alert_function_mode(self, setAlertMode):
        """!
        This function sets the alert function mode to either "alert" or
        "therm" mode

        @param bool setAlertMode: The alert mode to set

        Allowable setAlertMode values are:
            kThermMode
            kAlertMode

        @return **bool** `True` if successful, otherwise `False`
        """
        if setAlertMode not in [self.kThermMode, self.kAlertMode]:
            return False

        configReg = self.read_register(self.kRegConfiguration)

        if setAlertMode == self.kThermMode:
            configReg |= self.kConfigTNaMask
        else:
            configReg &= ~self.kConfigTNaMask

        self.write_register(self.kRegConfiguration, configReg)

        return True

    def get_alert_function_mode(self):
        """!
        This function gets the alert function mode to either "alert" or 
	    "therm" mode.

        @return **int** The alert mode

        Allowable return values are:
            kThermMode
            kAlertMode
        """
        configReg = self.read_register(self.kRegConfiguration)
        return (configReg & self.kConfigTNaMask) >> self.kConfigTNaShift
    
    def soft_reset(self):
        """!
        This function performs a software reset, loading all the default
	    values into the configuration register
        """
        configReg = self.read_register(self.kRegConfiguration)
        configReg |= self.kConfigSoftResetMask
        self.write_register(self.kRegConfiguration, configReg)

    # TODO: could combine all of the below functions into one function that takes a mode parameter, 
    # but since Arduino library has them separate, kept them separate for now
    def set_continuous_conversion_mode(self):
        """!
        This function sets the conversion mode of the sensor to be 
        continuous. The TMP117 defaults to Continuous Conversion Mode on reset.
        """
        configReg = self.read_register(self.kRegConfiguration)
        configReg &= ~self.kConfigModMask
        configReg |= (self.kContinuousConversionMode << self.kConfigModShift)

        self.write_register(self.kRegConfiguration, configReg)
    
    def set_shutdown_mode(self):
        """!
        This function sets the conversion mode of the sensor to be 
	    in shutdown mode. The TMP117 defaults to Continuous Conversion Mode 
	    on reset.
        """
        configReg = self.read_register(self.kRegConfiguration)
        configReg &= ~self.kConfigModMask
        configReg |= (self.kShutdownMode << self.kConfigModShift)

        self.write_register(self.kRegConfiguration, configReg)

    def set_one_shot_mode(self):
        """!
        This function sets the conversion mode of the sensor to be
        in one shot mode. The TMP117 defaults to Continuous Conversion Mode
        on reset.
        """
        configReg = self.read_register(self.kRegConfiguration)
        configReg &= ~self.kConfigModMask
        configReg |= (self.kOneShotMode << self.kConfigModShift)

        self.write_register(self.kRegConfiguration, configReg)

    def get_conversion_mode(self):
        """!
        This function reads the mode for the conversions.

        @return **int** The conversion mode

        Allowable return values are:
            kContinuousConversionMode
            kOneShotMode
            kShutdownMode
        """
        configReg = self.read_register(self.kRegConfiguration)
        return (configReg & self.kConfigModMask) >> self.kConfigModShift
    
    def set_conversion_average_mode(self, convMode):
        """!
        This function sets the conversion averaging mode of the device
	    when in Continuous Conversion Mode.

        @param int convMode: The conversion averaging mode to set

        Allowable convMode values are:
            kConvAvgNone
            kConvAvg8
            kConvAvg32
            kConvAvg64

        @return **bool** `True` if successful, otherwise `False`
        """
        if convMode not in [self.kConvAvgNone, self.kConvAvg8, self.kConvAvg32, self.kConvAvg64]:
            return False

        configReg = self.read_register(self.kRegConfiguration)
        configReg &= ~self.kConfigAvgMask
        configReg |= (convMode << self.kConfigAvgShift)

        self.write_register(self.kRegConfiguration, configReg)

        return True

    def get_conversion_average_mode(self):
        """!
        This function reads the conversion averaging mode

        @return **int** The conversion averaging mode

        Allowable return values are:
            kConvAvgNone
            kConvAvg8
            kConvAvg32
            kConvAvg64
        """
        configReg = self.read_register(self.kRegConfiguration)
        return (configReg & self.kConfigAvgMask) >> self.kConfigAvgShift

    def set_conversion_cycle_bit(self, conv):
        """!
        This function sets the conversion cycle time bit in 
        Continuous Conversion mode. The times for the conversions
        can be found below. The user puts in 0-7 and it will
	    return the cycle time accoring to the values in the chart.

        Conversion Cycle Time in CC Mode (found on the datasheet page 27 table 7)
               AVG       0       1       2       3
       CONV  averaging  (0)     (8)     (32)   (64)
         0             15.5ms  125ms   500ms    1s     
         1             125ms   125ms   500ms    1s     
         2             250ms   250ms   500ms    1s     
         3             500ms   500ms   500ms    1s     
         4             1s      1s      1s       1s     
         5             4s      4s      4s       4s     
         6             8s      8s      8s       8s     
         7             16s     16s     16s      16s

        @param int conv: The conversion cycle time bit to set

        Allowable conv values are 0-7

        @return **bool** `True` if successful, otherwise `False`
        """
        if conv < 0 or conv > 7:
            return False

        configReg = self.read_register(self.kRegConfiguration)
        configReg &= ~self.kConfigConvMask
        configReg |= (conv << self.kConfigConvShift)

        self.write_register(self.kRegConfiguration, configReg)
    
    def get_conversion_cycle_bit(self):
        """!
        This function returns the Conversion Cycle Bit value that the 
	    device is currently in at the time. This bit can help determine
	    the conversion cycle time that the device is in while being in
	    continuous conversion mode. (See table in set_conversion_cycle_bit, or page 27 of datasheet)

        @return **int** The conversion cycle bit value

        Allowable return values are 0-7
        """
        configReg = self.read_register(self.kRegConfiguration)
        return (configReg & self.kConfigConvMask) >> self.kConfigConvShift

    def data_ready(self):
        """!
        This function checks to see if there is data ready to be sent
	    from the TMP117.

        @return **bool** `True` if the data is ready, otherwise `False`
        """
        configReg = self.read_register(self.kRegConfiguration)
        return ( (configReg & self.kConfigDataReadyMask) == self.kConfigDataReadyMask )

    def read_register(self, register):
        """!
        Reads a register from the device

        @param int register: The register to read

        @return **int** The 16-bit value read from the register

        Used because the device returns bytes as big-endian
        """
        data = self._i2c.read_block(self.address, register, 2)
        return (data[0] << 8) | data[1]
    
    def write_register(self, register, value):
        """!
        Writes a value to a register on the device

        @param int register: The register to write to
        @param int value: The 16-bit value to write to the register

        Used because the device expects bytes as big-endian
        """
        self._i2c.write_block(self.address, register, [(value >> 8) & 0xFF, value & 0xFF])
