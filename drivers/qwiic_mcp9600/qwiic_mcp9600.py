#-------------------------------------------------------------------------------
# qwiic_mcp9600.py
#
# Python library for the SparkFun Qwiic Awiic Thermocouple Amplifier - MCP9600, available here:
# https://www.sparkfun.com/products/16295
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
qwiic_mcp9600
============
Python module for the [SparkFun Qwiic MCP9600](https://www.sparkfun.com/products/16295)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_MCP9600_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic MCP9600"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x60]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicMCP9600(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    kDeviceIdUpper = 0x40 # value of the upper half of the device ID register. lower half is used for device revision
    kDeviceResolution = 0.0625 # device resolution (temperature in C that the LSB represents)
    kRetryAttempts = 3 # how many times to attempt to read a register from the thermocouple before giving up
    
    # TODO: We could potentially remove any of these that are not used in the library, but they are nice if users ever want to use them
    # MCP9600 Registers
    kRegisterHotJuncTemp = 0x00
    kRegisterDeltaJuncTemp = 0x01
    kRegisterColdJuncTemp = 0x02
    kRegisterRawAdc = 0x03
    kRegisterSensorStatus = 0x04
    kRegisterThermoSensorConfig = 0x05
    kRegisterDeviceConfig = 0x06
    kRegisterAlert1Config = 0x08
    kRegisterAlert2Config = 0x09
    kRegisterAlert3Config = 0x0A
    kRegisterAlert4Config = 0x0B
    kRegisterAlert1Hysteresis = 0x0C
    kRegisterAlert2Hysteresis = 0x0D
    kRegisterAlert3Hysteresis = 0x0E
    kRegisterAlert4Hysteresis = 0x0F
    kRegisterAlert1Limit = 0x10
    kRegisterAlert2Limit = 0x11
    kRegisterAlert3Limit = 0x12
    kRegisterAlert4Limit = 0x13
    kRegisterDeviceId = 0x20

    # Thermocouple Types
    kTypeK = 0b000
    kTypeJ = 0b001
    kTypeT = 0b010
    kTypeN = 0b011
    kTypeS = 0b100
    kTypeE = 0b101
    kTypeB = 0b110
    kTypeR = 0b111

    # Ambient Resolution
    kAmbientResolutionZeroPoint0625 = 0
    kAmbientResolutionZeroPoint25 = 1

    # Thermocouple Resolution
    kThermocoupleResolution18Bit = 0b00
    kThermocoupleResolution16Bit = 0b01
    kThermocoupleResolution14Bit = 0b10
    kThermocoupleResolution12Bit = 0b11

    # Burst Sample
    kBurstSample1 = 0b000
    kBurstSample2 = 0b001
    kBurstSample4 = 0b010
    kBurstSample8 = 0b011
    kBurstSample16 = 0b100
    kBurstSample32 = 0b101
    kBurstSample64 = 0b110
    kBurstSample128 = 0b111

    # Shutdown Mode
    kShutdownModeNormal = 0x00
    kShutdownModeShutdown = 0x01
    kShutdownModeBurst = 0x02

    # Status bits shifts and masks
    kStatusShiftAlert1 = 0
    kStatusShiftAlert2 = 1
    kStatusShiftAlert3 = 2
    kStatusShiftAlert4 = 3
    kShiftInputRange = 4
    kShiftDataReady = 6
    kShiftBurstComplete = 7

    kStatusMaskAlert1 = 0b1 << kStatusShiftAlert1
    kStatusMaskAlert2 = 0b1 << kStatusShiftAlert2
    kStatusMaskAlert3 = 0b1 << kStatusShiftAlert3
    kStatusMaskAlert4 = 0b1 << kStatusShiftAlert4
    kMaskInputRange = 0b11 << kShiftInputRange
    kMaskDataReady = 0b1 << kShiftDataReady
    kMaskBurstComplete = 0b1 << kShiftBurstComplete

    # Device Config bits shifts and masks
    kConfigShiftShutdownMode = 0
    kConfigShiftBurstModeSample = 2
    kConfigShiftADCResolution = 5
    kConfigShiftColdJuncRes = 7

    kConfigMaskShutdownMode = 0b11 << kConfigShiftShutdownMode
    kConfigMaskBurstModeSample = 0b111 << kConfigShiftBurstModeSample
    kConfigMaskADCResolution = 0b11 << kConfigShiftADCResolution
    kConfigMaskColdJuncRes = 0b1 << kConfigShiftColdJuncRes

    # Thermocouple Sensor Config bits shifts and masks
    kThermoSensorConfigShiftFilter = 0
    kThermoSensorConfigShiftType = 4

    kThermoSensorConfigMaskFilter = 0b111 << kThermoSensorConfigShiftFilter
    kThermoSensorConfigMaskType = 0b111 << kThermoSensorConfigShiftType

    # Alert Limit bits
    kAlertLimitShiftSignBit = 15
    kAlertLimitMaskSignBit = 0b1 << kAlertLimitShiftSignBit

    # Alert Config bits shifts and masks
    kAlertConfigShiftEnable = 0
    kAlertConfigShiftCompIntMode = 1
    kAlertConfigShiftActiveHigh = 2
    kAlertConfigShiftRising = 3
    kAlertConfigShiftJuncHot = 4
    kAlertConfigShiftIntClear = 7

    kAlertConfigMaskEnable = 0b1 << kAlertConfigShiftEnable
    kAlertConfigMaskCompIntMode = 0b1 << kAlertConfigShiftCompIntMode
    kAlertConfigMaskActiveHigh = 0b1 << kAlertConfigShiftActiveHigh
    kAlertConfigMaskRising = 0b1 << kAlertConfigShiftRising
    kAlertConfigMaskJuncHot = 0b1 << kAlertConfigShiftJuncHot
    kAlertConfigMaskIntClear = 0b1 << kAlertConfigShiftIntClear

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
    
    def available(self):
        """!
        Returns true if the thermocouple (hot) junction temperature has been updated since we last checked. Also referred to as the data ready bit.

        @return **bool** `True` if the data is ready, otherwise `False`
        """
        status = self.read_block_retry(self.kRegisterSensorStatus, 1)
        if status == -1:
            return False
        return (status[0] & self.kMaskDataReady) != 0

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

        From Arduino Lib:
        The MCP9600 is a fussy device. If we call isConnected twice in succession, the second call fails
        as the MCP9600 does not ACK on the second call. Only on the first.
        So we should not call is_connected here(). We should only call check_device_id().
        """
        return self.check_device_id()

    def check_device_id(self):
        """!
        Returns true if the constant upper 8 bits in the device ID register are what they should be according to the datasheet.

        @return **bool** `True` if the device ID is correct, otherwise `False`
        """
        
        # According to Arduino lib: this is here because the first read doesn't seem to work, but the second does. No idea why :/
        self.read_block_retry(self.kRegisterDeviceId, 2)

        device_id_upper = self.read_block_retry(self.kRegisterDeviceId, 2)

        if device_id_upper == -1: # We were unable to read the device ID successfully
            return False
        
        return device_id_upper[0] == self.kDeviceIdUpper

    def read_block_retry(self, register, num_bytes):
        """!
        Attempt to read the register until we exit with no error code
        This attempts to fix the bug where clock stretching sometimes failes, as
        described in the MCP9600 eratta. Maximum retries defined by kRetryAttempts.

        @param int register: The register to read
        @param int num_bytes: The number of bytes to read

        @return **int** The value of the register
        """

        for i in range(self.kRetryAttempts):
            try:
                # Read the register
                value = self._i2c.read_block(self.address, register, num_bytes)
            except:
                # If there's an error, try again
                continue
            else:
                # If no error, return the value
                return list(value)
        
        return -1
    
    def write_double_register(self, register, value):
        """!
        Writes a 16-bit value to a register

        @param int register: The register to write to
        @param int value: The value to write

        Necessary because we have to write with opposite endianness as write_word
        """
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF

        self._i2c.write_block(self.address, register, [high_byte, low_byte])
    
    def reset_to_defaults(self):
        """!
        Resets all device parameters to their default values.
        """
        self._i2c.write_byte(self.address, self.kRegisterSensorStatus, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterThermoSensorConfig, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterDeviceConfig, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterAlert1Config, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterAlert2Config, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterAlert3Config, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterAlert4Config, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterAlert1Hysteresis, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterAlert2Hysteresis, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterAlert3Hysteresis, 0x00)
        self._i2c.write_byte(self.address, self.kRegisterAlert4Hysteresis, 0x00)
        self.write_double_register(self.kRegisterAlert1Limit, 0x0000)
        self.write_double_register(self.kRegisterAlert2Limit, 0x0000)
        self.write_double_register(self.kRegisterAlert3Limit, 0x0000)
        self.write_double_register(self.kRegisterAlert4Limit, 0x0000)
    
    def get_thermocouple_temp(self, units = True):
        """!
        Returns the thermocouple temperature, and clears the data ready bit. Set units to true for Celcius, or false for freedom units (Fahrenheit)

        @param bool, optional units: The units to use for the temperature as specified above

        @return  The temperature of the thermocouple or -1 on error
        
        """
        raw = self.read_block_retry(self.kRegisterHotJuncTemp, 2)
        if raw == -1:
            return -1
        
        status = self.read_block_retry(self.kRegisterSensorStatus, 1)
        if status == -1:
            return -1
        
        # Clear the data ready bit
        status[0] &= ~self.kMaskDataReady
        self._i2c.write_byte(self.address, self.kRegisterSensorStatus, status[0])

        celcius = (raw[0] << 8 | raw[1])
        # convert from unsigned 16-bit value to a signed 16-bit value
        if celcius > 32767:
            celcius -= 65536

        celcius *= self.kDeviceResolution

        return celcius if units else celcius * 1.8 + 32

    def get_ambient_temp(self, units=True):
        """!
        Returns the ambient (IC die) temperature. Set units to true for Celsius, or false for Fahrenheit.

        @param bool, optional units: The units to use for the temperature as specified above

        @return  The temperature of the ambient sensor or -1 on error
        
        """
        raw = self.read_block_retry(self.kRegisterColdJuncTemp, 2)
        if raw == -1:
            return -1

        celcius = (raw[0] << 8 | raw[1])
        # convert from unsigned 16-bit value to a signed 16-bit value
        if celcius > 32767:
            celcius -= 65536

        celcius *= self.kDeviceResolution

        return celcius if units else celcius * 1.8 + 32
    
    def get_temp_delta(self, units=True):
        """!
        Returns the difference in temperature between the thermocouple and ambient junctions. Set units to true for Celsius, or false for Fahrenheit.

        @param bool, optional units: The units to use for the temperature as specified above

        @return  The temperature difference or -1 on error
        
        """
        raw = self.read_block_retry(self.kRegisterDeltaJuncTemp, 2)
        if raw == -1:
            return -1

        celcius = (raw[0] << 8 | raw[1])
        # convert from unsigned 16-bit value to a signed 16-bit value
        if celcius > 32767:
            celcius -= 65536

        celcius *= self.kDeviceResolution

        return celcius if units else celcius * 1.8 + 32
    
    def get_raw_adc(self):
        """!
        Returns the raw contents of the raw ADC register

        @return  The raw ADC value or -1 on error
        
        """

        raw = self.read_block_retry(self.kRegisterRawAdc, 3)
        if raw == -1:
            return -1
        
        return (raw[0] << 16 | raw[1] << 8 | raw[2])
    
    def is_input_range_exceeded(self):
        """!
        Returns true if the input range has been exceeded

        @return **bool** `True` if the input range has been exceeded, otherwise `False`
        """
        status = self.read_block_retry(self.kRegisterSensorStatus, 1)
        if status == -1:
            return False # TODO: We might want to return a third value here rather than true or false to indicate that we couldn't read the status register
        
        return (status[0] & self.kMaskInputRange) != 0
    
    # --------------------------- Measurement Configuration ---------------
    def set_ambient_resolution(self, res):
        """!
        Changes the resolution on the cold (ambient) junction, for either 0.0625 or 0.25 degree C resolution. Lower resolution reduces conversion time.
        Valid inputs are:
            kAmbientResolutionZeroPoint0625
            kAmbientResolutionZeroPoint25

        @param int res: The resolution to use for the ambient sensor

        @return **bool** `True` if the resolution was set successfully, otherwise `False`
        """
        if res not in [self.kAmbientResolutionZeroPoint0625, self.kAmbientResolutionZeroPoint25]:
            return False

        config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if config == -1:
            return False

        # Set the bit that controls the ambient (cold) junction resolution
        config[0] = (config[0] & ~self.kConfigMaskColdJuncRes) | (res << self.kConfigShiftColdJuncRes)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.kRegisterDeviceConfig, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_ambient_resolution(self):
        """!
        Returns the resolution on the cold (ambient) junction, for either 0.0625 or 0.25 degree C resolution. Lower resolution reduces conversion time.

        @return **int** The resolution of the ambient sensor or -1 on error
        """
        config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if config == -1:
            return -1
        
        return (config[0] >> self.kConfigShiftColdJuncRes) & 0x01
    
    def set_thermocouple_resolution(self, res):
        """!
        Changes the resolution on the hot (thermocouple) junction, for either 18, 16, 14, or 12-bit resolution. Lower resolution reduces conversion time.
        Valid inputs are:
            kThermocoupleResolution18Bit
            kThermocoupleResolution16Bit
            kThermocoupleResolution14Bit
            kThermocoupleResolution12Bit

        @param int res: The resolution to use for the thermocouple sensor

        @return **bool** `True` if the resolution was set successfully, otherwise `False`
        """
        if res not in [self.kThermocoupleResolution18Bit, self.kThermocoupleResolution16Bit, self.kThermocoupleResolution14Bit, self.kThermocoupleResolution12Bit]:
            return False

        config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if config == -1:
            return False

        # Set the bits that control the thermocouple resolution
        config[0] = (config[0] & ~self.kConfigMaskADCResolution) | (res << self.kConfigShiftADCResolution)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.kRegisterDeviceConfig, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_thermocouple_resolution(self):
        """!
        Returns the resolution on the hot (thermocouple) junction, for either 18, 16, 14, or 12-bit resolution. Lower resolution reduces conversion time.

        @return **int** The resolution of the thermocouple sensor or -1 on error

        Possible return values:
            kThermocoupleResolution18Bit
            kThermocoupleResolution16Bit
            kThermocoupleResolution14Bit
            kThermocoupleResolution12Bit
        """
        config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if config == -1:
            return -1

        return ((config[0] & self.kConfigMaskADCResolution ) >> self.kConfigShiftADCResolution)

    def set_thermocouple_type(self, type):
        """!
        Changes the type of thermocouple connected to the MCP9600. Supported types are:
            kTypeK
            kTypeJ
            kTypeT
            kTypeN
            kTypeS
            kTypeE
            kTypeB
            kTypeR

        @param int type: The type of thermocouple to use

        @return **bool** `True` if the type was set successfully, otherwise `False`
        """
        if type not in [self.kTypeK, self.kTypeJ, self.kTypeT, self.kTypeN, self.kTypeS, self.kTypeE, self.kTypeB, self.kTypeR]:
            return False

        config = self.read_block_retry(self.kRegisterThermoSensorConfig, 1)
        if config == -1:
            return False

        # Clear the bits that control the thermocouple type
        config[0] &= ~self.kThermoSensorConfigMaskType
        # Set the bits that control the thermocouple type
        config[0] |= (type << self.kThermoSensorConfigShiftType)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.kRegisterThermoSensorConfig, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.kRegisterThermoSensorConfig, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_thermocouple_type(self):
        """!
        Returns the type of thermocouple connected to the MCP9600 as found in its configuration register. 
        Supported types are:
            kTypeK
            kTypeJ
            kTypeT
            kTypeN
            kTypeS
            kTypeE
            kTypeB
            kTypeR

        @return **int** The type of thermocouple sensor or -1 on error
        """

        config = self.read_block_retry(self.kRegisterThermoSensorConfig, 1)
        if config == -1:
            return -1

        return ((config[0] & self.kThermoSensorConfigMaskType ) >> self.kThermoSensorConfigShiftType)
    
    def set_filter_coefficient(self, filter):
        """!
        Changes the weight of the on-chip exponential moving average filter. Set this to 0 for no filter, 1 for minimum filter, and 7 for maximum filter.

        @param int filter: The filter coefficient to use

        @return **bool** `True` if the filter coefficient was set successfully, otherwise `False`

        TODO: Arduino function for this looked a bit odd...it might need to be reworked
        """
        if filter > 7:
            return False  # return immediately if the value is too big

        config = self.read_block_retry(self.kRegisterThermoSensorConfig, 1)
        if config == -1:
            return False

        # Clear the bits that control the filter coefficient
        config[0] &= ~self.kThermoSensorConfigMaskFilter
        # Set the bits that control the filter coefficient
        config[0] |= (filter << self.kThermoSensorConfigShiftFilter)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.kRegisterThermoSensorConfig, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.kRegisterThermoSensorConfig, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_filter_coefficient(self):
        """!
        Returns the weight of the on-chip exponential moving average filter.

        @return **int** The filter coefficient or -1 on error
        """
        config = self.read_block_retry(self.kRegisterThermoSensorConfig, 1)
        if config == -1:
            return -1

        coeff = (config[0] & self.kThermoSensorConfigMaskFilter) >> self.kThermoSensorConfigShiftFilter

        return coeff

    def set_burst_samples(self, samples):
        """!
        Changes the amount of samples to take in burst mode.

        @param int samples: The number of samples to take in burst mode

        Available options are:
            kBurstSample1
            kBurstSample2
            kBurstSample4
            kBurstSample8
            kBurstSample16
            kBurstSample32
            kBurstSample64
            kBurstSample128

        @return **bool** `True` if the burst samples were set successfully, otherwise `False`
        """
        if samples not in [self.kBurstSample1, self.kBurstSample2, self.kBurstSample4, self.kBurstSample8, self.kBurstSample16, self.kBurstSample32, self.kBurstSample64, self.kBurstSample128]:
            return False

        config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if config == -1:
            return False

        # Clear the bits that control the burst samples
        config[0] &= ~self.kConfigMaskBurstModeSample
        # Set the bits that control the burst samples
        config[0] |= (samples << self.kConfigShiftBurstModeSample)

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.kRegisterDeviceConfig, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_burst_samples(self):
        """!
        Returns the amount of samples to take in burst mode, according to the device's configuration register.

        @return **int** The number of samples to take in burst mode or -1 on error

        Possible return values:
            kBurstSample1
            kBurstSample2
            kBurstSample4
            kBurstSample8
            kBurstSample16
            kBurstSample32
            kBurstSample64
            kBurstSample128
        """
        config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if config == -1:
            return -1

        samples = (config[0] & self.kConfigMaskBurstModeSample) >> self.kConfigShiftBurstModeSample
        return samples
    
    def burst_available(self):
        """!
        Checks if burst mode data is available.

        @return **bool** Returns `True` if all the burst samples have been taken and the results are ready. Returns `False` otherwise.
        """
        status = self.read_block_retry(self.kRegisterSensorStatus, 1)
        if status == -1:
            return False

        return (status[0] & self.kMaskBurstComplete) != 0
    
    def start_burst(self):
        """!
        Initiates a burst on the MCP9600.

        @return **bool** `True` if the burst was started successfully, otherwise `False`
        """
        status = self.read_block_retry(self.kRegisterSensorStatus, 1)
        if status == -1:
            return False

        # Clear the burst complete bit
        status[0] &= ~self.kMaskBurstComplete
        self._i2c.write_byte(self.address, self.kRegisterSensorStatus, status[0])

        # Set the device to burst mode
        return self.set_shutdown_mode(self.kShutdownModeBurst)

    def set_shutdown_mode(self, mode):
        """!
        Changes the shutdown "operating" mode of the MCP9600. Configurable to Normal, Shutdown, and Burst.

        @param int mode: The mode to set the device to

        Available options are:
            kShutdownModeNormal
            kShutdownModeShutdown
            kShutdownModeBurst

        @return **bool** `True` if the mode was set successfully, otherwise `False`
        """

        config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if config == -1:
            return False

        # Clear the last two bits of the device config register
        config[0] = (config[0] & ~self.kConfigMaskShutdownMode) | mode

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, self.kRegisterDeviceConfig, config[0])

        # Double check that it was set properly
        new_config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if new_config == -1 or new_config[0] != config[0]:
            return False

        return True
    
    def get_shutdown_mode(self, mode):
        """!
        Returns the shutdown "operating" mode of the MCP9600. Configurable to Normal, Shutdown, and Burst.

        @return **int** The current mode of the device or -1 on error

        Possible return values:
            kShutdownModeNormal
            kShutdownModeShutdown
            kShutdownModeBurst
        """

        config = self.read_block_retry(self.kRegisterDeviceConfig, 1)
        if config == -1:
            return -1

        return (config[0] & self.kConfigMaskShutdownMode) >> self.kConfigShiftShutdownMode
    
    #---------------------------- Temperature Alerts -------------------
    def config_alert_temp(self, number, temp):
        """!
        Configures the temperature at which to trigger the alert for a given alert number.

        @param int number: The alert number (1-4)
        @param float temp: The temperature at which to trigger the alert

        @return **bool** `True` if the alert temperature was set successfully, otherwise `False`
        """
        
        # Pick the right register to put the temp limit in
        if number == 1:
            temp_limit_register = self.kRegisterAlert1Limit
        elif number == 2:
            temp_limit_register = self.kRegisterAlert2Limit
        elif number == 3:
            temp_limit_register = self.kRegisterAlert3Limit
        elif number == 4:
            temp_limit_register = self.kRegisterAlert4Limit
        else:
            return False

        # Convert the temp limit from a float to actual bits in the register
        # See datasheet pg. 23 for the structure of this register
        unsigned_temp_limit = int(abs(temp) * 4)
        unsigned_temp_limit = (unsigned_temp_limit << 2) & 0xFFFC
        signed_temp_limit = unsigned_temp_limit 
        if temp < 0:
            signed_temp_limit |= self.kAlertLimitMaskSignBit   # if the original temp limit was negative we shifted away the sign bit, so reapply it if necessary

        # Write the new temp limit to the MCP9600, return if it was successful
        return self.write_double_register(temp_limit_register, signed_temp_limit)
    
    def config_alert_junction(self, number, junction):
        """!
        Configures the junction to monitor the temperature of to trigger the alert. Set to fALSE for the thermocouple (hot) junction, or True for the ambient (cold) junction.

        @param int number: The alert number (1-4)
        @param bool junction: The junction to monitor False for the hot junction, True for the cold junction

        @return **bool** `True` if the junction was set successfully, otherwise `False`
        """

        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.kRegisterAlert1Config
        elif number == 2:
            alert_config_register = self.kRegisterAlert2Config
        elif number == 3:
            alert_config_register = self.kRegisterAlert3Config
        elif number == 4:
            alert_config_register = self.kRegisterAlert4Config
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the junction
        config[0] = (config[0] & ~self.kAlertConfigMaskJuncHot)
        if junction:
            config[0] |= self.kAlertConfigMaskJuncHot 

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True
    
    def config_alert_hysteresis(self, number, hysteresis):
        """!
        Configures the hysteresis to use around the temperature set point, in degrees Celsius.

        @param int number: The alert number (1-4)
        @param float hysteresis: The hysteresis value to set

        @return **bool** `True` if the hysteresis was set successfully, otherwise `False`
        """
        
        # Pick the register that points to the right alert
        if number == 1:
            alert_hysteresis_register = self.kRegisterAlert1Hysteresis
        elif number == 2:
            alert_hysteresis_register = self.kRegisterAlert2Hysteresis
        elif number == 3:
            alert_hysteresis_register = self.kRegisterAlert3Hysteresis
        elif number == 4:
            alert_hysteresis_register = self.kRegisterAlert4Hysteresis
        else:
            return False

        # Write the new hysteresis value to the MCP9600
        self._i2c.write_byte(self.address, alert_hysteresis_register, hysteresis)
        return True
    
    def config_alert_edge(self, number, edge):
        """!
        Configures whether to trigger the alert on the rising (cold -> hot) or falling (hot -> cold) edge of the temperature change. Set to True for rising, False for falling.

        @param int number: The alert number (1-4)
        @param bool edge: The edge to trigger the alert on

        @return **bool** `True` if the edge was set successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.kRegisterAlert1Config
        elif number == 2:
            alert_config_register = self.kRegisterAlert2Config
        elif number == 3:
            alert_config_register = self.kRegisterAlert3Config
        elif number == 4:
            alert_config_register = self.kRegisterAlert4Config
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the edge
        config[0] &= ~self.kAlertConfigMaskRising
        if edge:
            config[0] |= self.kAlertConfigMaskRising
            
        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def config_alert_logic_level(self, number, level):
        """!
        Configures whether the hardware alert pin is active-high or active-low. Set to True for active-high, False for active-low.

        @param int number: The alert number (1-4)
        @param bool level: The logic level to set

        @return **bool** `True` if the logic level was set successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.kRegisterAlert1Config
        elif number == 2:
            alert_config_register = self.kRegisterAlert2Config
        elif number == 3:
            alert_config_register = self.kRegisterAlert3Config
        elif number == 4:
            alert_config_register = self.kRegisterAlert4Config
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the logic level
        config[0] &= ~self.kAlertConfigMaskActiveHigh
        if level:
            config[0] |= self.kAlertConfigMaskActiveHigh

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def config_alert_mode(self, number, mode):
        """!
        Configures whether the MCP9600 treats the alert like a comparator or an interrrupt. Set to True for interrupt, False for comparator. More information is on pg. 34 of the datasheet.

        @param int number: The alert number (1-4)
        @param bool mode: The mode to set the alert to

        @return **bool** `True` if the alert mode was set successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.kRegisterAlert1Config
        elif number == 2:
            alert_config_register = self.kRegisterAlert2Config
        elif number == 3:
            alert_config_register = self.kRegisterAlert3Config
        elif number == 4:
            alert_config_register = self.kRegisterAlert4Config
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the mode
        config[0] &= ~self.kAlertConfigMaskCompIntMode

        if mode:
            config[0] |= self.kAlertConfigMaskCompIntMode
        
        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def config_alert_enable(self, number, enable):
        """!
        Configures whether or not the interrupt is enabled or not. Set to True to enable, or False to disable.

        @param int number: The alert number (1-4)
        @param bool enable: Set to True to enable the alert, False to disable

        @return **bool** `True` if the alert was enabled/disabled successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.kRegisterAlert1Config
        elif number == 2:
            alert_config_register = self.kRegisterAlert2Config
        elif number == 3:
            alert_config_register = self.kRegisterAlert3Config
        elif number == 4:
            alert_config_register = self.kRegisterAlert4Config
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that controls the enable state
        config[0] &= ~self.kAlertConfigMaskEnable
        
        if enable:
            config[0] |= self.kAlertConfigMaskEnable

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def clear_alert_pin(self, number):
        """!
        Clears the interrupt on the specified alert channel, resetting the value of the pin.

        @param int number: The alert number (1-4)

        @return **bool** `True` if the alert pin was cleared successfully, otherwise `False`
        """
        # Pick the register that points to the right alert
        if number == 1:
            alert_config_register = self.kRegisterAlert1Config
        elif number == 2:
            alert_config_register = self.kRegisterAlert2Config
        elif number == 3:
            alert_config_register = self.kRegisterAlert3Config
        elif number == 4:
            alert_config_register = self.kRegisterAlert4Config
        else:
            return False

        # Grab the current value of the config register so we don't overwrite any other settings
        config = self.read_block_retry(alert_config_register, 1)
        if config == -1:
            return False

        # Set the bit that clears the alert pin
        config[0] |= self.kAlertConfigMaskIntClear

        # Write new config register to MCP9600
        self._i2c.write_byte(self.address, alert_config_register, config[0])

        return True

    def is_temp_greater_than_limit(self, number):
        """!
        Returns true if the interrupt has been triggered, false otherwise

        @param int number: The alert number (1-4)

        @return **bool** `True` if the temperature is greater than the limit, otherwise `False`
        """
        if number < 1 or number > 4:
            return False  # if a nonexistent alert number is given, return False

        status = self.read_block_retry(self.kRegisterSensorStatus, 1)
        if status == -1:
            return False

        return (status[0] & (1 << (number - 1))) != 0