#-------------------------------------------------------------------------------
# qwiic_ads1015.py
#
# Python library for the SparkFun Qwiic ADS1015, available here:
# https://www.sparkfun.com/products/15334
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
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
qwiic_ads1015
============
Python module for the [SparkFun Qwiic ADS1015](https://www.sparkfun.com/products/15334)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_ADS1015_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c

__version__ = "3.0.0"

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic ADS1015"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x48, 0x49, 0x4A, 0x4B]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicADS1015(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Register addresses
    ADS1015_DELAY = 1

    # TODO: potentially we could delete some of the below constants to save space if we don't think we'll use them in 

    # Pointer Register
    POINTER_CONVERT = 0x00
    POINTER_CONFIG = 0x01
    POINTER_LOW_THRESH = 0x02
    POINTER_HI_THRESH = 0x03

    # Config Register

    # Operational status or single-shot conversion start
    # This bit determines the operational status of the device. OS can only be written
    # when in power-down state and has no effect when a conversion is ongoing.

    CONFIG_OS_NO = 0x0000
    CONFIG_OS_SINGLE = 0x8000  # 1 : Start a single conversion (when in power-down state)
    CONFIG_OS_NOT_READY = 0x0000  # 0 : Device is currently performing a conversion
    CONFIG_OS_READY = 0x8000  # 1 : Device is not currently performing a conversion

    CONFIG_MODE_CONT = 0x0000
    CONFIG_MODE_SINGLE = 0x0100

    CONFIG_MUX_SINGLE_0 = 0x4000
    CONFIG_MUX_SINGLE_1 = 0x5000
    CONFIG_MUX_SINGLE_2 = 0x6000
    CONFIG_MUX_SINGLE_3 = 0x7000
    CONFIG_MUX_DIFF_P0N1 = 0x0000
    CONFIG_MUX_DIFF_P0N3 = 0x1000
    CONFIG_MUX_DIFF_P1N3 = 0x2000
    CONFIG_MUX_DIFF_P2N3 = 0x3000

    CONFIG_RATE_MASK = 0x00E0
    CONFIG_RATE_128HZ = 0x0000
    CONFIG_RATE_250HZ = 0x0020
    CONFIG_RATE_490HZ = 0x0040
    CONFIG_RATE_920HZ = 0x0060
    CONFIG_RATE_1600HZ = 0x0080
    CONFIG_RATE_2400HZ = 0x00A0
    CONFIG_RATE_3300HZ = 0x00C0

    CONFIG_PGA_MASK = 0x0E00
    CONFIG_PGA_TWO_THIRDS = 0x0000  # +/- 6.144v
    CONFIG_PGA_1 = 0x0200  # +/- 4.096v
    CONFIG_PGA_2 = 0x0400  # +/- 2.048v
    CONFIG_PGA_4 = 0x0600  # +/- 1.024v
    CONFIG_PGA_8 = 0x0800  # +/- 0.512v
    CONFIG_PGA_16 = 0x0A00  # +/- 0.256v

    CONFIG_CMODE_TRAD = 0x0000  # Traditional comparator with hysteresis (default)
    CONFIG_CMODE_WINDOW = 0x0010  # Window comparator
    CONFIG_CPOL_ACTV_LOW = 0x0000  # ALERT/RDY pin is low when active (default)
    CONFIG_CPOL_ACTV_HI = 0x0008  # ALERT/RDY pin is high when active
    CONFIG_CLAT_NON_LAT = 0x0000  # Non-latching comparator (default)
    CONFIG_CLAT_LATCH = 0x0004  # Latching comparator
    CONFIG_CQUE_1_CONV = 0x0000  # Assert ALERT/RDY after one conversion
    CONFIG_CQUE_2_CONV = 0x0001  # Assert ALERT/RDY after two conversions
    CONFIG_CQUE_4_CONV = 0x0002  # Assert ALERT/RDY after four conversions
    CONFIG_CQUE_NONE = 0x0003  # Disable the comparator and put ALERT/RDY in high state (default)

    def __init__(self, address=None, i2c_bus=None):
        """!
        Constructor

        @param address: **int, optional** The I2C address to use for the device
            If not provided, the default address is used
        @param i2c_bus: **I2CBus, optional** A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.
        """
        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

        self._sampleRate = self.CONFIG_RATE_1600HZ
        self._gain = self.CONFIG_PGA_2
        self._useConversionReady = False # Default to disabled, allowing continous mode to be used
        self._mode = self.CONFIG_MODE_CONT # Default to continuous mode
        self._multiplierToVolts = 1.0

        # Array is structured as calibrationValues[finger][lo/hi]
        self._calibrationValues = [[0,0],[0,0]]

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        # TODO: If the device has a product ID register, that should be
        # checked in addition to the ACK
        return self._i2c.is_device_connected(self.address)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        return True


    def get_single_ended(self, channel):
        """!
        Returns the decimal value of sensor channel single-ended input

        @param channel: **int** The channel to read

        @return **int** The decimal value of the sensor channel
        """
        if channel > 3:
            return 0

        config = self.CONFIG_OS_SINGLE | self.CONFIG_CQUE_NONE | self._sampleRate

        config |= self._gain

        if self._useConversionReady:
            config |= self.CONFIG_MODE_SINGLE
        else:
            config |= self._mode

        if channel == 0:
            config |= self.CONFIG_MUX_SINGLE_0
        elif channel == 1:
            config |= self.CONFIG_MUX_SINGLE_1
        elif channel == 2:
            config |= self.CONFIG_MUX_SINGLE_2
        elif channel == 3:
            config |= self.CONFIG_MUX_SINGLE_3

        bytes_to_write = [config >> 8, config & 0xFF]
        self._i2c.write_block(self.address, self.POINTER_CONFIG, bytes_to_write)

        if self._useConversionReady:
            while not self.available():
                pass
            else:
                self.conversion_delay()

        result_bytes = self._i2c.read_block(self.address, self.POINTER_CONVERT, 2)
        result = (result_bytes[0] << 8) | result_bytes[1]

        return result >> 4
    
    def get_single_ended_signed(self, channel):
        """!
        Returns the signed value of sensor channel single-ended input

        @param channel: **int** The channel to read

        @return **int** The signed value of the sensor channel
        """
        value = self.get_single_ended(channel)

        # Check for sign bit in the 12-bit result and turn into a negative number if needed
        if result > 0x07FF:  # noqa: F821
            result -= 1 << 12  # noqa: F821

        return value
    
    def get_single_ended_millivolts(self, channel):
        """!
        Returns the millivolt value of sensor channel single-ended input

        @param channel: **int** The channel to read

        @return **float** The millivolt value of the sensor channel
        """
        return self.get_single_ended(channel) * self.get_multiplier()
    
    def get_differential(self, config_mux_diff=CONFIG_MUX_DIFF_P0N1):
        """!
        Returns the signed decimal value of sensor differential input
        Note, there are 4 possible differential pin setups:
        CONFIG_MUX_DIFF_P0N1
        CONFIG_MUX_DIFF_P0N3
        CONFIG_MUX_DIFF_P1N3
        CONFIG_MUX_DIFF_P2N3

        @param config_mux_diff: **int** The differential pin set up from the list above

        @return **int** The signed value of the sensor differential input channel
        """
        if config_mux_diff not in [
            self.CONFIG_MUX_DIFF_P0N1,
            self.CONFIG_MUX_DIFF_P0N3,
            self.CONFIG_MUX_DIFF_P1N3,
            self.CONFIG_MUX_DIFF_P2N3,
        ]:
            return 0  # received invalid argument

        config = self.CONFIG_OS_SINGLE | self.CONFIG_CQUE_NONE | self._sampleRate
        config |= self._gain

        if self._useConversionReady:
            config |= self.CONFIG_MODE_SINGLE
        else:
            config |= self._mode
        
        config |= config_mux_diff

        bytes_to_write = [config >> 8, config & 0xFF]
        self._i2c.write_block(self.address, self.POINTER_CONFIG, bytes_to_write)

        if self._useConversionReady:
            while not self.available():
                pass
        else:
            self.conversion_delay()

        result_bytes = self._i2c.read_block(self.address, self.POINTER_CONVERT, 2)
        result = ( (result_bytes[0] << 8) | result_bytes[1]) >> 4

        # Check for sign bit in the 12-bit result and turn into a negative number if needed
        if result > 0x07FF:
            result -= 1 << 12
        
        return result

    def get_differential_millivolts(self, config_mux_diff=CONFIG_MUX_DIFF_P0N1):
        """!
        Returns the millivolt value of sensor differential input
        Note, there are 4 possible differential pin setups:
        CONFIG_MUX_DIFF_P0N1
        CONFIG_MUX_DIFF_P0N3
        CONFIG_MUX_DIFF_P1N3
        CONFIG_MUX_DIFF_P2N3

        @param config_mux_diff: **int** The differential pin set up from the list above

        @return **float** The millivolt value of the sensor differential input channel
        """
        value = self.get_differential(config_mux_diff)
        return value * self.get_multiplier()
    
    def mapf(self, val, in_min, in_max, out_min, out_max):
        """!
        Maps a value from one range to another

        @param val: **float** The value to map
        @param in_min: **float** The minimum value of the input range
        @param in_max: **float** The maximum value of the input range
        @param out_min: **float** The minimum value of the output range
        @param out_max: **float** The maximum value of the output range

        @return **float** The mapped value
        """
        return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def get_scaled_analog_data(self, channel):
        """!
        Returns a value between 0 and 1 based on how bent the finger is. This function will not work with an uncalibrated sensor

        @param channel: **int** The channel to read

        @return **float** The scaled value of the sensor
        """
        if channel > 3:
            return 0
        
        data = self.mapf(self.get_single_ended(channel), self._calibrationValues[channel][0], self._calibrationValues[channel][1], 0, 1)

        if data > 1:
            return 1
        elif data < 0:
            return 0
        else:
            return data

    def calibrate(self):
        """!
        Perform calibration on the sensor. This function will set the calibration values for each finger
        """
        for finger in range(2):
            value = self.get_single_ended(finger)
            if (value > self._calibrationValues[finger][1] or self._calibrationValues[finger][1] == 0) and value < 1085:
                self._calibrationValues[finger][1] = value
            elif (value < self._calibrationValues[finger][0] or self._calibrationValues[finger][0] == 0):
                self._calibrationValues[finger][0] = value
    
    def get_calibration(self, channel, hi_lo):
        """!
        Returns the calibration value for the specified channel and hi_lo

        @param channel: **int** The channel to read
        @param hi_lo: **int** The hi_lo to read

        @return **int** The calibration value
        """
        return self._calibrationValues[channel][hi_lo]
    
    def set_calibration(self, channel, hi_lo, value):
        """!
        Sets the calibration value for the specified channel and hi_lo

        @param channel: **int** The channel to read
        @param hi_lo: **int** The hi_lo to read
        @param value: **int** The value to set
        """
        self._calibrationValues[channel][hi_lo] = value
    
    def reset_calibration(self):
        """!
        Resets the calibration values to 0
        """
        self._calibrationValues = [[0,0],[0,0]]
    
    def set_mode(self, mode):
        """!
        Sets the mode of the device. Continuous mode 0 is favored

        @param mode: **int** The mode to set
        """
        mode &= self.CONFIG_MODE_SINGLE
        self._mode = mode

    def get_mode(self):
        """!
        Returns the mode of the device. get_mode will return 0 for continuous and CONFIG_MODE_SINGLE for single shot

        @return **int** The mode of the device
        """
        return self._mode

    def set_gain(self, gain):
        """!
        Sets the gain of the device. 
        Valid values are: 
            CONFIG_PGA_TWO_THIRDS,
            CONFIG_PGA_1,
            CONFIG_PGA_2,
            CONFIG_PGA_4,
            CONFIG_PGA_8,
            CONFIG_PGA_16

        @param gain: **int** The gain to set
        """
        gain &= self.CONFIG_PGA_MASK
        self._gain = gain
        self.update_multiplier_to_volts() # each new gain setting changes how we convert to volts
    
    def get_gain(self):
        """!
        Returns the gain of the device
            Will return a differnet hex value of each gain setting:
            0x0E00: +/- 0.256V
            0X0000: +/- 6.144V
            0X0200: +/- 4.096V
            0X0400: +/- 2.048V
            0X0600: +/- 1.024V
            0X0800: +/- 0.512V
            0X0A00: +/- 0.256V

        @return **int** The gain of the device
        """
        return self._gain
    
    def update_multiplier_to_volts(self):
        """!
        Updates the multiplier to convert to volts
        """
        if self._gain == self.CONFIG_PGA_TWO_THIRDS:
            self._multiplierToVolts = 3.0
        elif self._gain == self.CONFIG_PGA_1:
            self._multiplierToVolts = 2.0
        elif self._gain == self.CONFIG_PGA_2:
            self._multiplierToVolts = 1.0
        elif self._gain == self.CONFIG_PGA_4:
            self._multiplierToVolts = 0.5
        elif self._gain == self.CONFIG_PGA_8:
            self._multiplierToVolts = 0.25
        elif self._gain == self.CONFIG_PGA_16:
            self._multiplierToVolts = 0.125
        else:
            self._multiplierToVolts = 1.0

    def get_multiplier(self):
        """!
        Returns the multiplier to convert to volts

        @return **float** The multiplier to convert to volts
        """
        return self._multiplierToVolts

    def set_sample_rate(self, rate):
        """!
        Sets the sample rate of the device

        @param rate: **int** The sample rate to set
        """
        rate &= self.CONFIG_RATE_MASK
        self._sampleRate = rate
    
    def get_sample_rate(self):
        """!
        Will return a different hex value for each sample rate
        Possible Values:
            0x0000: 128 Hz
            0X0020: 250 Hz
            0X0040: 490 Hz
            0X0060: 920 Hz
            0X0080: 1600 Hz
            0X00A0: 2400 Hz
            0X00C0: 3300 Hz

        @return **int** The sample rate of the device
        """
        return self._sampleRate
    
    def available(self):
        """!
        Checks to see if the Operational Status (OS) flag is set in the status register

        @return **bool** True if the OS flag is set, otherwise False
        """
        value_bytes = self._i2c.read_block(self.address, self.POINTER_CONFIG, 2)
        value = (value_bytes[0] << 8) | value_bytes[1]

        return (value & self.CONFIG_OS_READY > 0)
    
    def set_comparator_single_ended(self, channel, threshold):
        """!
        Sets up the comparator to operate in basic mode, causing the
            ALERT/RDY pin to assert (go from high to low) when the ADC
            value exceeds the specified threshold.

            This will also set the ADC in continuous conversion mode.

        Note, this function was adapted from the Adafruit Industries
        located here:
        https://github.com/adafruit/Adafruit_ADS1X15

        @param channel: **int** The channel to read
        @param threshold: **int** The threshold value to compare
        """
        if channel > 3:
            return 0

        config = (
            self.CONFIG_MODE_CONT |
            self._sampleRate |
            self.CONFIG_CQUE_1_CONV |   # Comparator enabled and asserts on 1 match
            self.CONFIG_CLAT_LATCH |   # Latching mode
            self.CONFIG_CPOL_ACTV_LOW | # Alert/Rdy active low (default val)
            self.CONFIG_CMODE_TRAD    # Traditional comparator (default val)
        )

        config |= self._gain

        if channel == 0:
            config |= self.CONFIG_MUX_SINGLE_0
        elif channel == 1:
            config |= self.CONFIG_MUX_SINGLE_1
        elif channel == 2:
            config |= self.CONFIG_MUX_SINGLE_2
        elif channel == 3:
            config |= self.CONFIG_MUX_SINGLE_3

        # Set the high threshold register
        # Shift 12-bit results left 4 bits for the ADS1015
        threshold = threshold << 4

        bytes_to_write = [threshold >> 8, threshold & 0xFF]
        self._i2c.write_block(self.address, self.POINTER_CONFIG, bytes_to_write)


        # Write config register to the ADC
        bytes_to_write  = [config >> 8, config & 0xFF]
        self._i2c.write_block(self.address, self.POINTER_CONFIG, bytes_to_write)
    
    def get_last_conversion_results(self):
        """!
        In order to clear the comparator, we need to read the
            conversion results.  This function reads the last conversion
            results without changing the config value.

            Note, this function was adapted from the Adafruit Industries
            located here:
            https://github.com/adafruit/Adafruit_ADS1X15

        @return **int** The last conversion result
        """

        # Read the conversion results
        # Shift 12-bit results right 4 bits for the ADS1015,
        # making sure we keep the sign bit intact
        result_bytes = self._i2c.read_block(self.address, self.POINTER_CONFIG, 2)
        result = (result_bytes[0] << 8) | result_bytes[1]
        result = result >> 4

        # Check for sign bit in the 12-bit result and turn into a negative number if needed
        if result > 0x07FF:
            result -= 1 << 12
        
        return result

    def conversion_delay(self):
        """!
        Delay for experimentally-determined delay times based on sample rate.
        These were determined experimentally by using Example7
        """
        if self._sampleRate >= self.CONFIG_RATE_3300HZ:
            self._i2c.delay_us(400) # > 303 us + 10% + 25 us power-up
        elif self._sampleRate >= self.CONFIG_RATE_2400HZ:
            self._i2c.delay_us(500) # > (417us + 10% + 25us power-up)
        elif self._sampleRate >= self.CONFIG_RATE_1600HZ:
            self._i2c.delay_ms(1) # > (625us + 10% + 25us power-up)
        elif self._sampleRate >= self.CONFIG_RATE_920HZ:
            self._i2c.delay_ms(2)
        elif self._sampleRate >= self.CONFIG_RATE_490HZ:
            self._i2c.delay_ms(4)
        elif self._sampleRate >= self.CONFIG_RATE_250HZ:
            self._i2c.delay_ms(8)
        else:
            self._i2c.delay_ms(16) # 128Hz
    
    def use_conversion_ready(self, enable):
        """!
        Enables or disables the use of useConversionReady

        When useConversionReady is enabled:
        The Config Register OS bit is read to determine when the conversion is complete - instead of using conversionDelay.
        Single-shot mode is always selected. _mode is ignored.

        @param enable: **bool** True to enable, False to disable
        """
        self._useConversionReady = enable
