#-------------------------------------------------------------------------------
# qwiic_ens160.py
#
# Python library for the SparkFun Qwiic ENS160, available here:
# https://www.sparkfun.com/products/20844
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, October 2024
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
qwiic_ens160
============
Python module for the [SparkFun Qwiic ENS160](https://www.sparkfun.com/products/20844)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_Indoor_Air_Quality_Sensor-ENS160_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic ENS160" 

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x53, 0x52]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicENS160(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # ENS160 register map
    kRegPartId = 0x00
    kRegOpMode = 0x10
    kRegConfig = 0x11
    kRegCommand = 0x12
    kRegTempIn = 0x13
    kRegRhIn = 0x15
    kRegDeviceStatus = 0x20
    kRegDataAqi = 0x21
    kRegDataTvoc = 0x22
    kRegDataEtoh = 0x22 
    kRegDataEco2 = 0x24
    kRegDataT = 0x30
    kRegDataRh = 0x32
    kRegDataMisr = 0x38
    kRegGPRWrite0 = 0x40
    kRegGPRWrite1 = 0x41
    kRegGPRWrite2 = 0x42
    kRegGPRWrite3 = 0x43
    kRegGPRWrite4 = 0x44
    kRegGPRWrite5 = 0x45
    kRegGPRWrite6 = 0x46
    kRegGPRWrite7 = 0x47
    kRegGPRRead0 = 0x48
    kRegGPRRead1 = 0x49
    kRegGPRRead2 = 0x4A
    kRegGPRRead3 = 0x4B
    kRegGPRRead4 = 0x4C 
    kRegGPRRead5 = 0x4D
    kRegGPRRead6 = 0x4E
    kRegGPRRead7 = 0x4F

    # ENS160 defines and masks
    kPartId = 0x0160

    # Possible Operating Mode defines/masks
    # Default = 0x00
    kOpModeDeepSleep = 0x00
    kOpModeIdle = 0x01
    kOpModeStandard = 0x02
    kOpModeReset = 0xF0
    
    # Config defines/masks
    # Default = 0x00
    kShiftConfigIntPol = 6  # INTn pin polarity 0: active low, 1: active high
    kShiftConfigIntCfg = 5  # INTn Pin Drive (INT_CFG) 0: open drain, 1: push/pull
    kShiftConfigIntGPR = 3  # INTn assert on new data in GPR reg (INTGPR)
    kShiftConfigIntDat = 1  # INTn pin assert on new data in DATA reg (INTDAT)
    kShiftConfigIntEn = 0   # INTn enable
    
    kMaskConfigIntPol = 0b1 << kShiftConfigIntPol
    kMaskConfigIntCfg = 0b1 << kShiftConfigIntCfg
    kMaskConfigIntGPR = 0b1 << kShiftConfigIntGPR
    kMaskConfigIntDat = 0b1 << kShiftConfigIntDat
    kMaskConfigIntEn = 0b1 << kShiftConfigIntEn

    # Command defines/masks
    # All commands must be issued when device is idle.
    kCommandNop = 0x00
    # Get Firwmware App Version - version is placed in General Purpose Read Registers as follows:
    # GPR_READ04 - Version (Major)
    # GPR_READ05 - Version (Minor)
    # GPR_READ06 - Version (Release)
    kCommandGetAppVer = 0x0E
    kCommandClearGPR = 0xCC

    # DeviceStatus defines/masks
    kShiftDeviceStatusStatAs = 7 # indicates an OPMODE is running
    kShiftDeviceStatusStatEr = 6 # indicates an error
    kShiftDeviceStatusValidityFlag = 2 # 0: normal, 1: warm-up, 2: initial start-up, 3: invalid
    kShiftDeviceStatusNewDat = 1 # new data available on DATA_x regs
    kShiftDeviceStatusNewGpr = 0  # new data available on GPR_READx regs

    kMaskDeviceStatusStatAs = 0b1 << kShiftDeviceStatusStatAs
    kMaskDeviceStatusStatEr = 0b1 << kShiftDeviceStatusStatEr
    kMaskDeviceStatusValidityFlag = 0b11 << kShiftDeviceStatusValidityFlag
    kMaskDeviceStatusNewDat = 0b1 << kShiftDeviceStatusNewDat
    kMaskDeviceStatusNewGpr = 0b1 << kShiftDeviceStatusNewGpr

    kValidityFlagNormal = 0
    kValidityFlagWarmUp = 1
    kValidityFlagStartUp = 2
    kValidityFlagInvalid = 3

    # DataAqi defines/masks
    kShiftDataAqiUba = 0 # Air quality index according to UBA

    kMaskDataAqiUba = 0b11 << kShiftDataAqiUba

    # DataMisr defines/masks
    # Gives calculated checksum of "DATA_" registers
    kPoly = 0x1D #  0b00011101 = x^8+x^4+x^3+x^2+x^0 (x^8 is implicit)

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
        if(self._i2c.isDeviceConnected(self.address) == False):
            return False

        prodid = self.get_unique_id()

        return prodid == self.kPartId

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        return self.is_connected()

    # ////////////////////////////////////////////////////////////////////////////////
    # General Operation
    # 

    def set_operating_mode(self, val):
        """!
        Sets the operating mode: Deep Sleep (0x00), Idle (0x01), Standard (0x02),
        Reset (0xF0)

        @param int val: The desired operating mode to set
        """
        if (val > self.kOpModeReset) or (val < self.kOpModeDeepSleep):
            return False
        
        self._i2c.write_byte(self.address, self.kRegOpMode, val)

        return True
    
    def get_operating_mode(self):
        """!
        Gets the current operating mode: Deep Sleep (0x00), Idle (0x01), Standard
        (0x02), Reset (0xF0)

        @return **int** The current operating mode
        """
        return self._i2c.read_byte(self.address, self.kRegOpMode)
    
    def get_app_ver(self):
        """!
        Retrieves the 24 bit application version of the device

        @return **int** Application version
        """

        old_mode = self.get_operating_mode()
        self.set_operating_mode(self.kOpModeIdle)
        self._i2c.write_byte(self.address, self.kRegCommand, self.kCommandClearGPR)
        self._i2c.write_byte(self.address, self.kRegCommand, self.kCommandGetAppVer)

        while not self.check_gpr_status():
            pass

        version_bytes = self._i2c.read_block(self.address, self.kRegGPRRead4, 3)

        version = version_bytes[0]
        version |= version_bytes[1] << 8
        version |= version_bytes[2] << 16

        self.set_operating_mode(old_mode)

        return version
    
    def get_unique_id(self):
        """!
        Retrieves the 16 bit id of the device

        @return **int** Part Id
        """
        id_bytes = self._i2c.read_block(self.address, self.kRegPartId, 2) 

        id = id_bytes[0]
        id |= id_bytes[1] << 8

        return id
    
    def configure_interrupt(self, val):
        """!
        Changes all of the settings within the interrupt configuration register

        @param int val: The desired configuration settings.
        """

        self._i2c.write_byte(self.address, self.kRegConfig, val)

    def enable_interrupt(self, enable=True):
        """!
        Enables the interrupt.

        @param bool enable: Turns on or off the interrupt
        """

        newConfig = self._i2c.read_byte(self.address, self.kRegConfig)

        newConfig &= ~self.kMaskConfigIntEn

        if enable:
            newConfig |= self.kMaskConfigIntEn

        self._i2c.write_byte(self.address, self.kRegConfig, newConfig)

    def set_interrupt_polarity(self, activeHigh = True):
        """!
        Changes the polarity of the interrupt: active high or active low. By default
        this value is set to zero or active low.

        @param bool activeHigh: Changes active state of interrupt from high to low.
        """
        newConfig = self._i2c.read_byte(self.address, self.kRegConfig)

        newConfig &= ~self.kMaskConfigIntPol

        if activeHigh:
            newConfig |= self.kMaskConfigIntPol
        
        self._i2c.write_byte(self.address, self.kRegConfig, newConfig)
    
    def get_interrupt_polarity(self):
        """!
        Retrieves the Retrieves the polarity of the physical interrupt.

        @return **int** Interrupt polarity (0: active low, 1: active high)
        """
        currentConfig = self._i2c.read_byte(self.address, self.kRegConfig)

        intPol = currentConfig & self.kMaskConfigIntPol

        return (intPol >> self.kShiftConfigIntPol)
    
    def set_interrupt_drive(self, pushPull = True):
        """!
        Changes the pin drive of the interrupt: open drain (default) to push/pull

        @param bool pushPull: Changes the drive of the pin.
        """
        newConfig = self._i2c.read_byte(self.address, self.kRegConfig)
        
        newConfig &= ~self.kMaskConfigIntCfg

        if pushPull:
            newConfig |= self.kMaskConfigIntCfg
        
        self._i2c.write_byte(self.address, self.kRegConfig, newConfig)

    def set_data_interrupt(self, enable):
        """!
        Routes the data ready signal to the interrupt pin.

        @param bool enable: enables or disables data ready on
        """
        newConfig = self._i2c.read_byte(self.address, self.kRegConfig)
        
        newConfig &= ~self.kMaskConfigIntDat

        if enable:
            newConfig |= self.kMaskConfigIntDat
        
        self._i2c.write_byte(self.address, self.kRegConfig, newConfig)
    
    def set_gpr_interrupt(self, enable):
        """!
        Routes the general purporse read register signal to the interrupt pin.

        @param bool enable: whether to turn on or off general purpose read
        """
        newConfig = self._i2c.read_byte(self.address, self.kRegConfig)

        newConfig &= ~self.kMaskConfigIntGPR

        if enable:
            newConfig |= self.kMaskConfigIntGPR

        self._i2c.write_byte(self.address, self.kRegConfig, newConfig)
    
    # ////////////////////////////////////////////////////////////////////////////////
    # Temperature and Humidity Compensation
    #

    def set_temp_compensation(self, tempKelvin):
        """!
        The ENS160 can use temperature data to help give more accurate sensor data.

        @param float tempKelvin: The given temperature in Kelvin
        """
        
        tempVal = [None] * 2
        kelvinConversion = int(tempKelvin * 64); # convert value - fixed equation pg. 29 of datasheet
        tempVal[0] = (kelvinConversion & 0x00FF)
        tempVal[1] = ( (kelvinConversion & 0xFF00) >> 8)

        self._i2c.write_block(self.address, self.kRegTempIn, tempVal)

    def set_temp_compensation_celsius(self, tempCelsius):
        """!
        The ENS160 can use temperature data to help give more accurate sensor data.

        @param float tempCelsius: The given temperature in Celsius
        """

        kelvinConversion = tempCelsius + 273.15
        self.set_temp_compensation(kelvinConversion)

    def set_rh_compensation(self, humidity):
        """!
        The ENS160 can use relative Humidiy data to help give more accurate sensor data.

        @param float humidity: The given relative humidity
        """
        
        humidityConversion = int(humidity * 512) # convert value - fixed equation pg. 29 in datasheet.
        
        tempVal = [None] * 2
        tempVal[0] = (humidityConversion & 0x00FF)
        tempVal[1] = ( (humidityConversion & 0xFF00) >> 8)

        self._i2c.write_block(self.address, self.kRegRhIn, tempVal)

    # ////////////////////////////////////////////////////////////////////////////////
    # Device Status
    # 

    def check_data_status(self):
        """!
        This checks the if the NEWDAT bit is high indicating that new data is ready
        to be read. The bit is cleared when data has been read from their registers.

        @return **bool** Whether NEWDAT bit is high
        """

        currentStatus = self._i2c.read_byte(self.address, self.kRegDeviceStatus)
        
        currentStatus &= self.kMaskDeviceStatusNewDat

        if currentStatus == self.kMaskDeviceStatusNewDat:
            return True

        return False

    def check_gpr_status(self):
        """!
        This checks the if the NEWGPR bit is high indicating that there is data in
        the general purpose read registers. The bit is cleared the relevant registers
        have been read.

        @return **bool** Whether NEWGPR bit is high
        """
        currentStatus = self._i2c.read_byte(self.address, self.kRegDeviceStatus)
        
        currentStatus &= self.kMaskDeviceStatusNewGpr

        if currentStatus == self.kMaskDeviceStatusNewGpr:
            return True

        return False

    def get_flags(self):
        """!
        This checks the status "flags" of the device (0-3).

        @return **int** The current status flag (0: normal, 1: warm-up, 2: initial start-up, 3: invalid)
        """
        
        currentStatus = self._i2c.read_byte(self.address, self.kRegDeviceStatus)

        flags = (currentStatus & self.kMaskDeviceStatusValidityFlag) >> self.kShiftDeviceStatusValidityFlag
        
        return flags

    def check_operation_status(self):
        """!
        Checks the bit that indicates if an operation mode is running i.e. the device
        is not off.

        @return **bool** Whether NEWGPR bit is high
        """
        currentStatus = self._i2c.read_byte(self.address, self.kRegDeviceStatus)
        
        currentStatus &= self.kMaskDeviceStatusStatAs

        if currentStatus == self.kMaskDeviceStatusStatAs:
            return True

        return False

    def get_operation_error(self):
        """!
        Checks the bit that indicates if an invalid operating mode has been selected.

        @return **bool** Whether an OpMode error is selected
        """
        currentStatus = self._i2c.read_byte(self.address, self.kRegDeviceStatus)
        
        currentStatus &= self.kMaskDeviceStatusStatEr

        if currentStatus == self.kMaskDeviceStatusStatEr:
            return True

        return False

    # ////////////////////////////////////////////////////////////////////////////////
    # Data Registers
    # 

    def get_aqi(self):
        """!
        This reports the calculated Air Quality Index according to UBA which is a
        value between 1-5. The AQI-UBA is a guideline developed by the German Federal
        Environmental Agency and is widely referenced and adopted by many countries
        and organizations.
        
        1 - Excellent, 2 - Good, 3 - Moderate, 4 - Poor, 5 - Unhealthy.

        @return **int** Qir Quality Index
        """
        currentDataAqi = self._i2c.read_byte(self.address, self.kRegDataAqi)
        
        aqiUba = currentDataAqi & self.kMaskDataAqiUba

        return (aqiUba >> self.kShiftDataAqiUba)


    def get_tvoc(self):
        """!
        This reports the Total Volatile Organic Compounds in ppb (parts per billion)

        @return **int** Total Volatile Organic Compounds in ppb
        """
        
        tvocBytes = self._i2c.read_block(self.address, self.kRegDataTvoc, 2)

        tvoc = tvocBytes[0]
        tvoc |= tvocBytes[1] << 8

        return tvoc

    def get_etoh(self):
        """!
        This reports the ehtanol concentration in ppb (parts per billion). According
        to the datasheet this is a "virtual mirror" of the ethanol-calibrated TVOC
        register, which is why they share the same register.

        @return **int** Ethanol concentration in ppb
        """
        
        ethanolBytes = self._i2c.read_block(self.address, self.kRegDataEtoh, 2)

        ethanol = ethanolBytes[0]
        ethanol |= ethanolBytes[1] << 8

        return ethanol

    def get_eco2(self):
        """!
        This reports the CO2 concentration in ppm (parts per million) based on the
        detected VOCs and hydrogen.

        @return **int** CO2 concentration in ppm
        """
        
        ecoBytes = self._i2c.read_block(self.address, self.kRegDataEco2, 2)

        eco = ecoBytes[0]
        eco |= ecoBytes[1] << 8

        return eco
        
    def get_temp_kelvin(self):
        """!
        This reports the temperature compensation value given to the sensor in
        Kelvin.

        @return **float** Temperature compensation in Kelvin
        """
        
        tempBytes = self._i2c.read_block(self.address, self.kRegDataT, 2)

        tempConversion = tempBytes[0]
        tempConversion |= tempBytes[1] << 8

        temperature = float(tempConversion) / 64.0 # Formula as described on pg. 32 of datasheet.

        return temperature

    def get_temp_celsius(self):
        """!
        This reports the temperature compensation value given to the sensor in
        Celsius.

        @return **float** Temperature compensation in Celsius
        """

        temperature = self.get_temp_kelvin()

        return (temperature - 273.15)

    def get_rh(self):
        """!
        This reports the relative humidity compensation value given to the sensor.

        @return **float** Relative Humidty
        """

        rhBytes = self._i2c.read_block(self.address, self.kRegDataRh, 2)

        rh = rhBytes[0]
        rh |= rhBytes[1] << 8

        return rh / 512.0 # Formula as described on pg. 33 of datasheet.
    
    def get_raw_resistance(self):
        """!
        For certain gases the raw resistance values of the hot plates can be 
        used for post processing. More information can be found within the datasheet.

        @return **float** Raw Resistance
        """

        resBytes = self._i2c.read_block(self.address, self.kRegGPRRead6, 2)

        res = resBytes[0]
        res |= resBytes[1] << 8

        resistance = 2 ** (res / 2048) # Formula as described on page 13 of datasheet.

        return resistance

