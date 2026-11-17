#-------------------------------------------------------------------------------
# qwiic_bmp581.py
#
# Python library for the SparkFun Qwiic BMP581, available here:
# https://www.sparkfun.com/products/20170
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2023 SparkFun Electronics
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
qwiic_bmp581
============
Python module for the [SparkFun Qwiic BMP581](https://www.sparkfun.com/products/20170)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_BMP581_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c
import time

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic BMP581"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x47, 0x46]

# TODO: Made these helper structs from the Arduino lib into their own classes here,
#       so their would be a direct mapping between the Arduino lib and this Python lib.
#       We can rework this if necessary.

# OSR, ODR and pressure configuration structure
class OsrOdrPressConfig(object):
    # Oversampling for temperature and pressure
    kOversampling1x = 0x00
    kOversampling2x = 0x01
    kOversampling4x = 0x02
    kOversampling8x = 0x03
    kOversampling16x = 0x04
    kOversampling32x = 0x05
    kOversampling64x = 0x06
    kOversampling128x = 0x07

    def __init__(self):
        # Oversampling 
        # Temperature and Pressure oversampling respectively
        self.osrT = self.kOversampling1x
        self.osrP = self.kOversampling1x

        # Enable Pressure (1 - enabled, 0 - disabled)
        self.pressEn = 0

        # Output data rate
        self.odr = 0

# OSR, ODR and pressure configuration structure
class IirConfig(object):
    # IIR filter for temperature and pressure
    kIirFilterBypass = 0x00
    kIirFilterCoeff1 = 0x01
    kIirFilterCoeff3 = 0x02
    kIirFilterCoeff7 = 0x03
    kIirFilterCoeff15 = 0x04
    kIirFilterCoeff31 = 0x05
    kIirFilterCoeff63 = 0x06
    kIirFilterCoeff127 = 0x07

    def __init__(self):
        # Temperature IIR
        self.setIirT = self.kIirFilterBypass
        
        # Pressure IIR
        self.setIirP = self.kIirFilterBypass
        
        # Shadow IIR selection for temperature (1 - enabled, 0 - disabled)
        self.shdwSetIirT = 0

        # Shadow IIR selection for pressure (1 - enabled, 0 - disabled)
        self.shdwSetIirP = 0

        # IIR Flush in forced mode (1 - enabled, 0 - disabled)
        self.iirFlushForcedEn = 0

# Effective OSR configuration and ODR valid status structure
class SensorData(object):
    def __init__(self):
        self.temperature = 0
        self.pressure = 0

# Effective OSR configuration and ODR valid status structure
class OsrOdrEff(object):
    def __init__(self):
        self.osrTEff = 0
        self.osrPEff = 0
        self.odrIsValid = 0

# BMP5 interrupt source selection.
class intSourceSelect(object):
    def __init__(self):
        # All of these are enables for the corresponding interrupt, (1 - enabled, 0 - disabled)
        self.intDrdy = 0
        self.intFifoFull = 0
        self.intFifoThres = 0
        self.intOorPress = 0

# BMP5 Out-of-range pressure configuration.
class OorPressConfiguration(object):
    # Pressure Out-of-range count limit
    kOorCountLimit1 = 0x00
    kOorCountLimit3 = 0x01
    kOorCountLimit7 = 0x02
    kOorCountLimit15 = 0x03

    def __init__(self):
        self.oorThrP = 0
        self.oorRangeP = 0

        # Out of range pressure count limit
        self.oorCntLim = 0

        # Out-of-range pressure IIR (1 - enabled, 0 - disabled)
        self.oorSeliirP = 0

# BMP5 fifo configurations.
class FifoConfig(object):
    # Possible fifo frame selections
    kFifoNotEnabled = 1
    kFifoTemperatureData = 2
    kFifoPressureData = 3
    kFifoPressTempData = 4
    
    # Possible fifo decimation(downsampling) selection
    kFifoNoDownsampling = 0
    kFifoDownsampling2x = 1
    kFifoDownsampling4x = 2
    kFifoDownsampling8x = 3
    kFifoDownsampling16x = 4
    kFifoDownsampling32x = 5
    kFifoDownsampling64x = 6
    kFifoDownsampling128x = 7

    # Possible fifo mode selection
    kFifoModeStreaming = 0
    kFifoModeStopOnFull = 1

    def __init__(self):
        self.data = []
        self.length = 0
        self.frameSel = self.kFifoNotEnabled
        self.decSel = self.kFifoNoDownsampling
        self.fifoCount = 0 # frame count
        self.mode = self.kFifoModeStreaming
        self.threshold = 0
        self.setFifoIirT = 0 # Fifo IIR for temperature (1 - enabled, 0 - disabled)
        self.setFifoIirP = 0 # Fifo IIR for pressure (1 - enabled, 0 - disabled)

class QwiicBMP581(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Register definitions
    kRegChipId = 0x01
    kRegRevId = 0x02
    kRegChipStatus = 0x11
    kRegDriveConfig = 0x13
    kRegIntConfig = 0x14
    kRegIntSource = 0x15
    kRegFifoConfig = 0x16
    kRegFifoCount = 0x17
    kRegFifoSel = 0x18
    kRegTempDataXlsb = 0x1D
    kRegTempDataLsb = 0x1E
    kRegTempDataMsb = 0x1F
    kRegPressDataXlsb = 0x20
    kRegPressDataLsb = 0x21
    kRegPressDataMsb = 0x22
    kRegIntStatus = 0x27
    kRegStatus = 0x28
    kRegFifoData = 0x29
    kRegNvmAddr = 0x2B
    kRegNvmDataLsb = 0x2C
    kRegNvmDataMsb = 0x2D
    kRegDspConfig = 0x30
    kRegDspIir = 0x31
    kRegOorThrPLsb = 0x32
    kRegOorThrPMsb = 0x33
    kRegOorRange = 0x34
    kRegOorConfig = 0x35
    kRegOsrConfig = 0x36
    kRegOdrConfig = 0x37
    kRegOsrEff = 0x38
    kRegCmd = 0x7E

    # Power mode definitions
    kPowerModeStandby = 0
    kPowerModeNormal = 1
    kPowerModeForced = 2
    kPowerModeContinuous = 3
    kPowerModeDeepStandby = 4

    # Masks and Shifts
    # Interrupt configurations
    kIntModeMask = 0x01
    kIntModeShift = 0
    
    kIntPolMask = 0x02
    kIntPolShift = 1

    kIntOdMask = 0x04
    kIntOdShift = 2

    kIntEnMask = 0x08
    kIntEnShift = 3

    kIntDrdyEnMask = 0x01
    kIntDrdyEnShift = 0

    kIntFifoFullEnMask = 0x02
    kIntFifoFullEnShift = 1

    kIntFifoThresEnMask = 0x04
    kIntFifoThresEnShift = 2

    kIntOorPressEnMask = 0x08
    kIntOorPressEnShift = 3

    # ODR configuration
    kOdrMask = 0x7C
    kOdrShift = 2

    # OSR configurations
    kTempOsMask = 0x07
    kTempOsShift = 0

    kPressOsMask = 0x38
    kPressOsShift = 3

    # Pressure enable
    kPressEnMask = 0x40
    kPressEnShift = 6

    # IIR configurations
    kSetIirTempMask = 0x07
    kSetIirTempShift = 0

    kSetIirPressMask = 0x38
    kSetIirPressShift = 3

    kOorSelIirPressMask = 0x80
    kOorSelIirPressShift = 7

    kShdwSetIirTempMask = 0x08
    kShdwSetIirTempShift = 3

    kShdwSetIirPressMask = 0x20
    kShdwSetIirPressShift = 5

    kSetFifoIirTempMask = 0x10
    kSetFifoIirTempShift = 4

    kSetFifoIirPressMask = 0x40
    kSetFifoIirPressShift = 6

    kIirFlushForcedEnMask = 0x04
    kIirFlushForcedEnShift = 2

    # Effective OSR configurations and ODR valid status
    kOsrTempEffMask = 0x07
    kOsrTempEffShift = 0

    kOsrPressEffMask = 0x38
    kOsrPressEffShift = 3

    kOdrIsValidMask = 0x80
    kOdrIsValidShift = 7

    # Powermode
    kPowermodeMask = 0x03
    kPowermodeShift = 0

    kDeepDisableMask = 0x80
    kDeepDisableShift = 7

    # Fifo configurations
    kFifoThresholdMask = 0x1F
    kFifoThresholdShift = 0

    kFifoModeMask = 0x20
    kFifoModeShift = 5

    kFifoDecSelMask = 0x1C
    kFifoDecSelShift = 2

    kFifoCountMask = 0x3F
    kFifoCountShift = 0

    kFifoFrameSelMask = 0x03
    kFifoFrameSelShift = 0

    # Out-of-range configuration
    kOorThrPLsbMask = 0x0000FF
    kOorThrPLsbShift = 0

    kOorThrPMsbMask = 0x00FF00
    kOorThrPMsbShift = 0

    kOorThrPXmsbMask = 0x010000
    kOorThrPXmsbShift = 16

    # Macro to mask xmsb value of oor threshold from register(0x35) value
    kOorThrPXmsbRegMask = 0x01
    kOorThrPXmsbRegShift = 0

    kOorCountLimitMask = 0xC0
    kOorCountLimitShift = 6

    # NVM configuration
    kNvmAddrMask = 0x3F
    kNvmAddrShift = 0

    kNvmProgEnMask = 0x40
    kNvmProgEnShift = 6

    kNvmDataLsbMask = 0x00FF
    kNvmDataLsbShift = 0

    kNvmDataMsbMask = 0xFF00
    kNvmDataMsbShift = 0

    # Constant Value definitions
    # Delay definitions
    kDelayUsSoftReset = 2000
    kDelayUsStandby = 2500
    kDelayUsNvmReadyRead = 800
    kDelayUsNvmReadyWrite = 10000

    # Soft reset command
    kSoftResetCmd = 0xB6

    # NVM command
    kNvmFirstCmd = 0x5D
    kNvmReadEnableCmd = 0xA5
    kNvmWriteEnableCmd = 0xA0

    # Deepstandby enable/disable
    kDeepEnabled = 0
    kDeepDisabled = 1

    # General enable/disable
    kEnable = 1
    kDisable = 0
    kError = -1
    kNoError = 0

    # ODR settings
    kOdr240Hz = 0x00
    kOdr218_5Hz = 0x01
    kOdr199_1Hz = 0x02
    kOdr179_2Hz = 0x03
    kOdr160Hz = 0x04
    kOdr149_3Hz = 0x05
    kOdr140Hz = 0x06
    kOdr129_8Hz = 0x07
    kOdr120Hz = 0x08
    kOdr110_1Hz = 0x09
    kOdr100_2Hz = 0x0A
    kOdr89_6Hz = 0x0B
    kOdr80Hz = 0x0C
    kOdr70Hz = 0x0D
    kOdr60Hz = 0x0E
    kOdr50Hz = 0x0F
    kOdr45Hz = 0x10
    kOdr40Hz = 0x11
    kOdr35Hz = 0x12
    kOdr30Hz = 0x13
    kOdr25Hz = 0x14
    kOdr20Hz = 0x15
    kOdr15Hz = 0x16
    kOdr10Hz = 0x17
    kOdr05Hz = 0x18
    kOdr04Hz = 0x19
    kOdr03Hz = 0x1A
    kOdr02Hz = 0x1B
    kOdr01Hz = 0x1C
    kOdr0_5Hz = 0x1D
    kOdr0_250Hz = 0x1E
    kOdr0_125Hz = 0x1F

    # Fifo frame configuration
    kFifoEmpty = 0x7F
    kFifoMaxThresholdPTMode = 0x0F
    kFifoMaxThresholdPMode = 0x1F

    # Macro to bypass both iir_t and iir_p together
    kIirBypass = 0xC0

    # Interrupt configurations
    kIntModePulsed = 0
    kIntModeLatched = 1

    kIntPolActiveLow = 0
    kIntPolActiveHigh = 1

    kIntOdPushPull = 0
    kIntOdOpenDrain = 1

    # NVM and Interrupt status asserted macros
    kIntAssertedDrdy = 0x01
    kIntAssertedFifoFull = 0x02
    kIntAssertedFifoThres = 0x04
    kIntAssertedPressureOor = 0x08
    kIntAssertedPorSoftresetComplete = 0x10
    kIntNvmRdy = 0x02
    kIntNvmErr = 0x04
    kIntNvmCmdErr = 0x08

    # NVM addresses
    kNvmStartAddr = 0x20
    kNvmEndAddr = 0x22

    # Chip ID
    kChipId = 0x50

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
        
        self.osrOdrConfig = OsrOdrPressConfig()
        self.fifo = FifoConfig()

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        # Reset the sensor
        self.soft_reset()
        
        chipId = self._i2c.read_byte(self.address, self.kRegChipId)

        if self._power_up_check() == False:
            return False
        if self._validate_chip_id(chipId) == False:
            return False
        
        # Enable both pressure and temperature sensors
        self.enable_press(self.kEnable)

        # Set to normal mode
        self.set_power_mode(self.kPowerModeNormal)
        return True
    
    def enable_press(self, enable):
        """!
        Enables or disables the pressure sensor.

        @param int enable: The value to set

        Allowable values:
            - `kEnable`
            - `kDisable`
        """
        self.osrOdrConfig.pressEn = enable
        self.set_osr_odr_press_config()
    
    def set_odr_frequency(self, odr):
        """!
        Sets the output data rate of the sensor.

        @param int odr: The output data rate to set
        """
        # check whether ODR is valid
        if odr > self.kOdr0_125Hz:
            return self.kError

        self.osrOdrConfig.odr = odr
        self.set_osr_odr_press_config()

    def set_osr_multipliers(self, config):
        """!
        Set the temperature and pressure oversampling multipliers.

        @param OsrOdrPressConfig config: The configuration to set
        """
        # check whether OSR multipliers are valid
        if config.osrT > config.kOversampling128x or config.osrP > config.kOversampling128x:
            return self.kError
        
        self.osrOdrConfig.osrT = config.osrT
        self.osrOdrConfig.osrP = config.osrP
        self.set_osr_odr_press_config()

    def soft_reset(self):
        """!
        This API performs the soft reset of the sensor.
        """
        self._i2c.write_byte(self.address, self.kRegCmd, self.kSoftResetCmd)
        time.sleep(1e-6 * self.kDelayUsSoftReset)

    def get_osr_odr_press_config(self):
        """!
        Gets the current oversampling and output data rate configuration

        @return **OsrOdrPressConfig** The current oversampling and output data rate configuration
        """
        osrConfig = self._i2c.read_byte(self.address, self.kRegOsrConfig)

        config = OsrOdrPressConfig()
        config.osrT = (osrConfig & self.kTempOsMask) >> self.kTempOsShift
        config.osrP = (osrConfig & self.kPressOsMask) >> self.kPressOsShift
        config.pressEn = (osrConfig & self.kPressEnMask) >> self.kPressEnShift
        config.odr = (osrConfig & self.kOdrMask) >> self.kOdrShift

        return config
    
    def set_osr_odr_press_config(self):
        """!
        This API sets the configuration for oversampling temperature, oversampling of pressure 
        and ODR configuration along with pressure enable.

        NOTE: If ODR is set to a value higher than 5Hz then powermode is set as standby mode, 
        as ODR value greater than 5HZ without disabling deep-standby mode makes powermode invalid.
        """
        if self.osrOdrConfig.odr < self.kOdr05Hz:
            self._set_standby_mode()
        
        regData = list(self._i2c.read_block(self.address, self.kRegOsrConfig, 2))
        
        regData[0] = (regData[0] & ~self.kTempOsMask) | (self.osrOdrConfig.osrT << self.kTempOsShift)
        regData[0] = (regData[0] & ~self.kPressOsMask) | (self.osrOdrConfig.osrP << self.kPressOsShift)
        regData[0] = (regData[0] & ~self.kPressEnMask) | (self.osrOdrConfig.pressEn << self.kPressEnShift)
        regData[1] = (regData[1] & ~self.kOdrMask) | (self.osrOdrConfig.odr << self.kOdrShift)

        self._i2c.write_block(self.address, self.kRegOsrConfig, regData)

    def get_iir_config(self):
        """!
        Gets the current IIR configuration

        @return **IirConfig** The current IIR configuration
        """
        dspConfig = self._i2c.read_block(self.address, self.kRegDspConfig, 2)

        config = IirConfig()
        config.shdwSetIirT = (dspConfig[0] & self.kShdwSetIirTempMask) >> self.kShdwSetIirTempShift
        config.shdwSetIirP = (dspConfig[0] & self.kShdwSetIirPressMask) >> self.kShdwSetIirPressShift
        config.iirFlushForcedEn = (dspConfig[0] & self.kIirFlushForcedEnMask) >> self.kIirFlushForcedEnShift

        config.setIirT = (dspConfig[1] & self.kSetIirTempMask) >> self.kSetIirTempShift
        config.setIirP = (dspConfig[1] & self.kSetIirPressMask) >> self.kSetIirPressShift

        return config
    
    def get_power_mode(self):
        """!
        Gets the current power mode of the device

        @return **int** The current power mode or -1 on error
        """
        odrConfig = self._i2c.read_byte(self.address, self.kRegOdrConfig)
        powerMode = (odrConfig & self.kPowermodeMask) >> self.kPowermodeShift
        
        if powerMode == self.kPowerModeStandby:
            deepDis = (odrConfig & self.kDeepDisableMask) >> self.kDeepDisableShift
            if deepDis == self.kDeepEnabled:
                if self._check_deepstandby_mode():
                    return self.kPowerModeDeepStandby
                else: 
                    return self.kError
            else:
                return self.kPowerModeStandby
            
        if powerMode == self.kPowerModeNormal:
            return self.kPowerModeNormal
        if powerMode == self.kPowerModeForced:
            return self.kPowerModeForced
        if powerMode == self.kPowerModeContinuous:
            return self.kPowerModeContinuous
        
        return self.kError
    
    def set_power_mode(self, powerMode):
        """!
        Sets the power mode of the device

        @param int powerMode: The power mode to set

        Allowable powerMode values:
            - `kPowerModeStandby`
            - `kPowerModeNormal`
            - `kPowerModeForced`
            - `kPowerModeContinuous`
            - `kPowerModeDeepStandby`
        """
        lastMode = self.get_power_mode()

        # Device should be set to standby before transiting to
        # forced mode or normal mode or continous mode.
        if lastMode != self.kPowerModeStandby:
            self._direct_set_power_mode(self.kPowerModeStandby)
            time.sleep(1e-6 * self.kDelayUsStandby)
        
        if powerMode == self.kPowerModeDeepStandby:
            self._set_deepstandby_mode()
        # elif powerMode == self.kPowerModeStandby:
            # Since switching between powermodes require sensor to be in standby mode
            # it is performed above. So it is not explicitly performed here.
            # pass
        elif powerMode in [self.kPowerModeNormal, self.kPowerModeForced, self.kPowerModeContinuous]:
            self._direct_set_power_mode(powerMode)
    
    def get_sensor_data(self):
        """!
        This API reads the temperature(deg C) or both pressure(Pa) and temperature(deg C) data from the
        sensor and store it in the bmp5_sensor_data structure instance passed by the user.

        @return **SensorData** The sensor data
        """
        data = SensorData()

        regData = self._i2c.read_block(self.address, self.kRegTempDataXlsb, 6)
        
        raw_data_t = (regData[2] << 16) | (regData[1] << 8) | regData[0]
        data.temperature = raw_data_t / 65536.0

        if self.osrOdrConfig.pressEn:
            raw_data_p = (regData[5] << 16) | (regData[4] << 8) | regData[3]
            data.pressure = raw_data_p / 64.0
        else:
            data.pressure = 0
        
        return data
    
    def get_osr_odr_eff(self):
        """!
        This API reads the effective oversampling and output data rate configuration from the sensor.

        @return **OsrOdrEff** The effective oversampling and output data rate configuration
        """
        regData = self._i2c.read_block(self.address, self.kRegOsrEff, 1)

        eff = OsrOdrEff()
        eff.osrTEff = (regData[0] & self.kOsrTempEffMask) >> self.kOsrTempEffShift
        eff.osrPEff = (regData[0] & self.kOsrPressEffMask) >> self.kOsrPressEffShift
        eff.odrIsValid = (regData[0] & self.kOdrIsValidMask) >> self.kOdrIsValidShift

        return eff

    def set_iir_config(self, config):
        """!
        This API sets the configuration for IIR of temperature and pressure.
        
        If IIR value for both temperature and pressure is set a value other than bypass then powermode is set
        as standby mode, as IIR with value other than bypass without disabling deep-standby mode makes powermode invalid.
        """
        
        if (config.setIirT != config.kIirFilterBypass) or (config.setIirP != config.kIirFilterBypass):
            self._set_standby_mode()
        
        currPwrMode = self.get_power_mode()

        if currPwrMode != self.kPowerModeStandby:
            self.set_power_mode(self.kPowerModeStandby)
        
        self._direct_set_iir_config(config)

        # If previous mode is not standbymode return sensor to that previous mode
        # after setting iir configuration
        if (currPwrMode != self.kPowerModeStandby) and (currPwrMode != self.kPowerModeDeepStandby): 
            self.set_power_mode(currPwrMode)

    def set_oor_configuration(self, config):
        """!
        This API sets the configuration for out-of-range pressure threshold, range
        count limit and IIR.

        @param OorPressConfiguration config: The configuration to set
        """

        self._set_oor_iir_count_limit(config.oorSeliirP, config.oorCntLim)

        # Get the OOR Configurations
        regData = list(self._i2c.read_block(self.address, self.kRegOorThrPLsb, 4))

        regData[0] = (regData[0] & ~self.kOorThrPLsbMask) | (config.oorThrP << self.kOorThrPLsbShift)
        regData[1] = (regData[1] & ~self.kOorThrPMsbMask) | ( (config.oorThrP >> 8) << self.kOorThrPMsbShift)
        regData[2] = config.oorRangeP
        thresXMsb = (config.oorThrP & self.kOorThrPXmsbMask) >> self.kOorThrPXmsbShift
        regData[3] = (regData[3] & ~self.kOorThrPXmsbRegMask) | thresXMsb

        self._i2c.write_block(self.address, self.kRegOorThrPLsb, regData)
        
    def configure_interrupt(self, intMode, intPol, intOd, intEn):
        """!
        This API is used to configure the interrupt settings.

        @param int intMode: The interrupt mode to set

        Allowable values:
            - `kIntModePulsed`
            - `kIntModeLatched`
        @param int intPol: The interrupt polarity to set

        Allowable values:
            - `kIntPolActiveLow`
            - `kIntPolActiveHigh`
        @param int intOd: The interrupt output type to set

        Allowable values:
            - `kIntOdPushPull`
            - `kIntOdOpenDrain`
        @param int intEn: The interrupt enable to set

        Allowable values:
            - `kEnable`
            - `kDisable`
        """
        
        regData = self._i2c.read_block(self.address, self.kRegIntConfig, 1)

        # Any change between latched/pulsed mode has to be applied while interrupt is disabled
        # Step 1 : Turn off all INT sources (INT_SOURCE -> 0x00)
        # Step 2 : Read the INT_STATUS register to clear the status
        # Step 3 : Set the desired mode in INT_CONFIG.int_mode
        # Finally transfer the interrupt configurations 
        self._i2c.write_byte(self.address, self.kRegIntSource, 0x00)

        intStatus = self._i2c.read_byte(self.address, self.kRegIntStatus)
        
        regData = (regData & ~self.kIntModeMask) | (intMode << self.kIntModeShift)
        regData = (regData & ~self.kIntPolMask) | (intPol << self.kIntPolShift)
        regData = (regData & ~self.kIntOdMask) | (intOd << self.kIntOdShift)
        regData = (regData & ~self.kIntEnMask) | (intEn << self.kIntEnShift)

        self._i2c.write_byte(self.address, self.kRegIntConfig, regData)
    
    def int_source_select(self, select):
        """!
        This API is used to enable the interrupts(drdy interrupt, fifo full interrupt,
        fifo threshold enable and pressure data out of range interrupt).

        @param intSourceSelect select: The interrupt source select to set
        """
        regData = self._i2c.read_byte(self.address, self.kRegIntSource)

        regData = (regData & ~self.kIntDrdyEnMask) | (select.intDrdy << self.kIntDrdyEnShift)
        regData = (regData & ~self.kIntFifoFullEnMask) | (select.intFifoFull << self.kIntFifoFullEnShift)
        regData = (regData & ~self.kIntFifoThresEnMask) | (select.intFifoThres << self.kIntFifoThresEnShift)
        regData = (regData & ~self.kIntOorPressEnMask) | (select.intOorPress << self.kIntOorPressEnShift)

        self._i2c.write_byte(self.address, self.kRegIntSource, regData)
    
    def get_interrupt_status(self):
        """!
        This API is used to get interrupt status.
        """
        return self._i2c.read_byte(self.address, self.kRegIntStatus)
    
    def set_fifo_configuration(self, fifo):
        """!
        This API used to set the configurations of fifo in the sensor.
        
        If Fifo frame selection is enabled then powermode is set as standby mode, as fifo frame selection
        enabled without disabling deep-standby mode makes powermode invalid.
        """
        if fifo.frameSel != fifo.kFifoNotEnabled:
            self._set_standby_mode()
        
        self._set_fifo_iir_config(fifo.setFifoIirT, fifo.setFifoIirP)

        # Get the FIFO Configurations
        regData = list(self._i2c.read_byte(self.address, self.kRegFifoConfig))

        regData &= ~self.kFifoModeMask
        regData |= fifo.mode << self.kFifoModeShift

        self._set_fifo_threshold(regData, fifo)

        # Set the fifo configurations
        self._i2c.write_byte(self.address, self.kRegFifoConfig, regData)

        regData = self._i2c.read_byte(self.address, self.kRegFifoSel)

        regData &= ~self.kFifoFrameSelMask
        regData |= fifo.frameSel << self.kFifoFrameSelShift
        regData &= ~self.kFifoDecSelMask
        regData |= fifo.decimation << self.kFifoDecSelShift

        self._i2c.write_byte(self.address, self.kRegFifoSel, regData)

    def get_fifo_len(self, fifo):
        """!
        This API is used to get the length of FIFO data available in the sensor.

        @param FifoConfiguration fifo: The fifo configuration
        """

        regData = self._i2c.read_byte(self.address, self.kRegFifoCount)

        fifo.fifoCount = (regData & self.kFifoCountMask) >> self.kFifoCountShift

        if (fifo.frameSel == fifo.kFifoTemperatureData) or (fifo.frameSel == fifo.kFifoPressureData):
            return fifo.fifoCount  * 3
        elif fifo.frameSel == fifo.kFifoPressTempData:
            return fifo.fifoCount  * 6
        
        return 0

    def get_fifo_data(self, fifo):
        """!
        This API is used to read the FIFO data from the sensor.

        @param FifoConfiguration fifo: The fifo configuration
        """
        fifoLen = self.get_fifo_len(fifo)

        if fifo.length > fifoLen:
            fifo.length = fifoLen
        
        regData = self._i2c.read_block(self.address, self.kRegFifoData, fifo.length)

        fifo.data[:] = list(regData)[:]

    def extract_fifo_data(self, fifo, sensorData):
        """!
        This API extract the temperature and/or pressure data from the fifo data which is
        already read from the fifo.
        """

        idx = 0

        for i in range(0, fifo.length):
            res = self._unpack_sensor_data(sensorData[idx], i, fifo)
            if not res:
                break
            idx += 1

    def nvm_read(self, nvmAddr):
        """!
        This API is used to perform NVM reads.

        @param int nvmAddr: The NVM address to read
        """
        currPwrMode = self._nvm_write_addr(nvmAddr, self.kDisable)

        self._i2c.write_byte(self.address, self.kRegCmd, self.kNvmFirstCmd)
        self._i2c.write_byte(self.address, self.kRegCmd, self.kNvmReadEnableCmd)
        time.sleep(1e-6 * self.kDelayUsNvmReadyRead)

        nvmData = self._get_nvm_data()

        if currPwrMode != self.kPowerModeStandby:
            self.set_power_mode(currPwrMode)
        
        return nvmData

    def nvm_write(self, nvmAddr, nvmWriteData):
        currPwrMode = self._nvm_write_addr(nvmAddr, self.kEnable)
        nvmData = list(self._i2c.read_block(self.address, self.kRegNvmDataLsb, 2))

        nvmData[0] = nvmWriteData & self.kNvmDataLsbMask
        nvmData[1] = (nvmWriteData & self.kNvmDataMsbMask) >> 8

        self._i2c.write_block(self.address, self.kRegNvmDataLsb, nvmData)

        self._i2c.write_byte(self.address, self.kRegCmd, self.kNvmFirstCmd)

        # Write enable NVM command for user write sequence
        regData = self.kNvmWriteEnableCmd
        self._i2c.write_byte(self.address, self.kRegCmd, regData)
        time.sleep(1e-6 * self.kDelayUsNvmReadyWrite)

        nvmStatus = self._get_nvm_status()

        if (nvmStatus & self.kIntNvmRdy) and not(nvmStatus & self.kIntNvmErr) and not(nvmStatus & self.kIntNvmCmdErr):
            # Reset NVM prog_en
            # TODO: The below line looks strange to me, seems like regData is currently kNvmWriteEnableCmd from above
            #       and then we are clearing a bit that doesn't even exist in that command and then sending it.
            #       This is what the original code does, so I'll keep it for now, but might want to add this line before it:
            # regData = self._i2c.read_byte(self.address, self.kRegNvmAddr)
            regData = (regData & ~self.kNvmProgEnMask)
            self._i2c.write_byte(self.address, self.kRegNvmAddr, regData)

        if currPwrMode != self.kPowerModeStandby:
            self.set_power_mode(currPwrMode)

    # Private Methods
    def _power_up_check(self):
        """!
        This internal API is used to validate the post power-up procedure. Not to be used outside of driver.
        """
        nvmStatus = self._get_nvm_status()
        if (nvmStatus & self.kIntNvmRdy) and not(nvmStatus & self.kIntNvmErr):
            status = self.get_interrupt_status()
            if status & self.kIntAssertedPorSoftresetComplete:
                return True
        
        return False
    
    def _validate_chip_id(self, chipId):
        """!
        This internal API is used to validate the chip id of the sensor. Not to be used outside of driver.
        """
        if chipId == self.kChipId:
            return True
        return False

    def _check_deepstandby_mode(self):
        """!
        Checks if the device is in deepstandby mode. Not to be used outside of driver.

        @return **bool** `True` if in deepstandby mode, otherwise `False`
        """

        fifoFrameSel = self._i2c.read_byte(self.address, self.kRegFifoSel)
        fifoFrameSel = (fifoFrameSel & self.kFifoFrameSelMask) >> self.kFifoFrameSelShift

        osrConf = self.get_osr_odr_press_config()
        iirConf = self.get_iir_config()

        # As per datasheet odr should be less than 5Hz. But register value for 5Hz is less than 4Hz and so,
        # thus in this below condition odr is checked whether greater than 5Hz macro.
        if (osrConf.odr > self.kOdr05Hz) and (fifoFrameSel == self.kDisable) \
            and (iirConf.setIirT == iirConf.kIirFilterBypass) and (iirConf.setIirP == iirConf.kIirFilterBypass):
            return True
        
        return False
    
    def _set_deepstandby_mode(self):
        """!
        This function is used to set the device to deepstandby mode. Not to be used outside of driver.
        """
        regData = self._i2c.read_byte(self.address, self.kRegOdrConfig)

        regData &= ~self.kDeepDisableMask # Setting deep_dis = 0(BMP5_DEEP_ENABLED) enables the deep standby mode
        
        # Set ODR less then 5Hz - ODR used is 1Hz
        regData &= ~self.kOdrMask
        regData |= self.kOdr01Hz << self.kOdrShift

        self._i2c.write_byte(self.address, self.kRegOdrConfig, regData)

        regData = self._i2c.read_byte(self.address, self.kRegDspIir)
        regData &= self.kIirBypass

        self._i2c.write_byte(self.address, self.kRegDspIir, regData)

        regData = self._i2c.read_byte(self.address, self.kRegFifoSel)
        regData &= ~self.kFifoFrameSelMask

        self._i2c.write_byte(self.address, self.kRegFifoSel, regData)
    
    def _set_standby_mode(self):
        """!
        This function is used to set the device to standby powermode when powermoide is deepstandby mode. Not to be used outside of driver.
        """
        powerMode = self.get_power_mode()
        if powerMode == self.kPowerModeDeepStandby:
            self.set_power_mode(self.kPowerModeStandby)
    
    def _direct_set_power_mode(self, powerMode):
        """!
        Sets the power mode of the device. Not to be used outside of driver

        @param int powerMode: The power mode to set

        Allowable powerMode values:
            - `kPowerModeStandby`
            - `kPowerModeNormal`
            - `kPowerModeForced`
            - `kPowerModeContinuous`
            - `kPowerModeDeepStandby`
        """
        odrConfig = self._i2c.read_byte(self.address, self.kRegOdrConfig)
        
        odrConfig &= ~self.kDeepDisableMask
        odrConfig |= self.kDeepDisabled << self.kDeepDisableShift

        odrConfig &= ~self.kPowermodeMask
        odrConfig |= powerMode << self.kPowermodeShift

        self._i2c.write_byte(self.address, self.kRegOdrConfig, odrConfig)

    def _direct_set_iir_config(self, config):
        """!
        Sets the IIR for temperature and pressure. Not to be used outside of driver.
        """
        regData = list(self._i2c.read_block(self.address, self.kRegDspConfig, 2))

        regData[0] &= ~self.kShdwSetIirTempMask
        regData[0] |= config.shdwSetIirT << self.kShdwSetIirTempShift

        regData[0] &= ~self.kShdwSetIirPressMask
        regData[0] |= config.shdwSetIirP << self.kShdwSetIirPressShift

        regData[0] &= ~self.kIirFlushForcedEnMask
        regData[0] |= config.iirFlushForcedEn << self.kIirFlushForcedEnShift

        regData[1] &= ~self.kSetIirTempMask
        regData[1] |= config.setIirT << self.kSetIirTempShift

        regData[1] &= ~self.kSetIirPressMask
        regData[1] |= config.setIirP << self.kSetIirPressShift

        self._i2c.write_block(self.address, self.kRegDspIir, regData)

    def _set_oor_iir_count_limit(self, setOorIirP, setCountLimit):
        """!
        This internal API sets the IIR configuration and count limit of OOR pressure.
        """
        currPwrMode = self.get_power_mode()

        # OOR IIR configuration and count limit is writable only during STANDBY mode(as per datasheet)
        if currPwrMode != self.kPowerModeStandby:
            self.set_power_mode(self.kPowerModeStandby)
        
        # Get OOR pressure IIR configuration
        regData = self._i2c.read_byte(self.address, self.kRegDspConfig)

        regData &= ~self.kOorSelIirPressMask
        regData |= setOorIirP << self.kOorSelIirPressShift
        self._i2c.write_byte(self.address, self.kRegDspConfig, regData)

        regData = self._i2c.read_byte(self.address, self.kRegOorConfig)

        regData &= ~self.kOorCountLimitMask
        regData |= setCountLimit << self.kOorCountLimitShift

        self._i2c.write_byte(self.address, self.kRegOorConfig, regData)

        # If previous mode is not standbymode return sensor to that previous mode
        # after setting oor iir configuration and count limit
        if (currPwrMode != self.kPowerModeStandby) and (currPwrMode != self.kPowerModeDeepStandby): 
            self.set_power_mode(currPwrMode)

    def _set_fifo_iir_config(self, setFifoIirT, setFifoIirP):
        """!
        Sets the configuration for IIR of fifo. Not to be used outside of driver.
        """
        currPwrMode = self.get_power_mode()

        # Fifo IIR configuration is writable only during STANDBY mode(as per datasheet)
        if currPwrMode != self.kPowerModeStandby:
            self.set_power_mode(self.kPowerModeStandby)
        
        regData = self._i2c.read_byte(self.address, self.kRegDspConfig)

        regData &= ~self.kSetFifoIirTempMask
        regData |= setFifoIirT << self.kSetFifoIirTempShift
        regData &= ~self.kSetFifoIirPressMask
        regData |= setFifoIirP << self.kSetFifoIirPressShift

        self._i2c.write_byte(self.address, self.kRegDspConfig, regData)

        # If previous mode is not standbymode return sensor to that previous mode
        # after setting fifo iir configuration
        if (currPwrMode != self.kPowerModeStandby) and (currPwrMode != self.kPowerModeDeepStandby): 
            self.set_power_mode(currPwrMode)
        
    def _set_fifo_threshold(self, regData, fifo):
        """!
        This internal API is used to set fifo threshold based on the frame type selected. Not to be used outside of driver.

        @param FifoConfiguration fifo: The fifo configuration

        return: kNoError on success, kError on failure
        """
        if (fifo.frameSel == fifo.kFifoTemperatureData) or (fifo.frameSel == fifo.kFifoPressureData):
            if fifo.threshold <= self.kFifoMaxThresholdPMode:
                regData[0] = (regData[0] & ~self.kFifoThresholdMask) | ( fifo.threshold << self.kFifoThresholdShift)
            else:
                return self.kError

        elif (fifo.frameSel == fifo.kFifoPressTempData):
            if fifo.threshold <= self.kFifoMaxThresholdPTMode:
                regData[0] = (regData[0] & ~self.kFifoThresholdMask) | ( fifo.threshold << self.kFifoThresholdShift)
            else:
                return self.kError
        
        return self.kNoError

    def _unpack_sensor_data(self, sensorData, dataIndex, fifo):
        """!
        This internal API is used to unpack the FIFO data and store it in the sensorData parameter

        @param SensorData sensorData: The sensor data
        @param int dataIndex: The data index
        @param FifoConfiguration fifo: The fifo configuration

        @return  True on success, False on failure/frame empty
        
        """
        res = True 
        if fifo.frameSel == fifo.kFifoTemperatureData:
            if not ((fifo.data[dataIndex] == self.kFifoEmpty) and (fifo.data[dataIndex + 1] == self.kFifoEmpty) and (fifo.data[dataIndex + 2] == self.kFifoEmpty)):
                rawDataT = (fifo.data[dataIndex + 2] << 16) | (fifo.data[dataIndex + 1] << 8) | fifo.data[dataIndex]
                
                sensorData.temperature = rawDataT / 65536.0
                sensorData.pressure = 0.0
                dataIndex += 3
            else:
                dataIndex = fifo.length
                res = False

        if fifo.frameSel == fifo.kFifoPressureData:
            if not ((fifo.data[dataIndex] == self.kFifoEmpty) and (fifo.data[dataIndex + 1] == self.kFifoEmpty) and (fifo.data[dataIndex + 2] == self.kFifoEmpty)):
                rawDataP = (fifo.data[dataIndex + 2] << 16) | (fifo.data[dataIndex + 1] << 8) | fifo.data[dataIndex]
                
                sensorData.pressure = rawDataP / 64.0
                sensorData.temperature = 0.0
                dataIndex += 3
            else:
                dataIndex = fifo.length
                res = False

        if fifo.frameSel == fifo.kFifoPressTempData:
            if not ((fifo.data[dataIndex] == self.kFifoEmpty) and (fifo.data[dataIndex + 1] == self.kFifoEmpty) and (fifo.data[dataIndex + 2] == self.kFifoEmpty) \
                and (fifo.data[dataIndex + 3] == self.kFifoEmpty) and (fifo.data[dataIndex + 4] == self.kFifoEmpty) and (fifo.data[dataIndex + 5] == self.kFifoEmpty)):
                rawDataT = (fifo.data[dataIndex + 2] << 16) | (fifo.data[dataIndex + 1] << 8) | fifo.data[dataIndex]
                rawDataP = (fifo.data[dataIndex + 5] << 16) | (fifo.data[dataIndex + 4] << 8) | fifo.data[dataIndex + 3]

                sensorData.temperature = rawDataT / 65536.0
                sensorData.pressure = rawDataP / 64.0
                dataIndex += 6
            else:
                dataIndex = fifo.length
                res = False
        
        else:
            sensorData.pressure = 0.0
            sensorData.temperature = 0.0
        
        return res

    def _get_nvm_status(self):
        """!
        This API is used to get the status of NVM data. Not to be used outside of driver.
        """
        return self._i2c.read_byte(self.address, self.kRegStatus)

    def _get_nvm_data(self):
        """!
        This internal API is used to read the nvm data
        """
        nvmStatus = self._get_nvm_status()

        if (nvmStatus & self.kIntNvmRdy) and (not(nvmStatus & self.kIntNvmErr)) and (not(nvmStatus & self.kIntNvmCmdErr)):
            nvmData = self._i2c.read_block(self.address, self.kRegNvmDataLsb, 2)
            return (nvmData[1] << 8) | nvmData[0]

        return self.kError

    def _set_nvm_addr(self, nvmAddr, progEn):
        """!
        This internal API is used to set the nvm address and prog_enable based on NVM read/write selected.

        @param int nvmAddr: The NVM address to set
        @param int progEn: The program enable

        Allowable values:
            - `kEnable`
            - `kDisable`
        """
        nvmStatus = self._get_nvm_status()
        
        if nvmStatus & self.kIntNvmRdy:
            regData = self._i2c.read_byte(self.address, self.kRegNvmAddr)
            regData = (regData & ~self.kNvmAddrMask) | (nvmAddr << self.kNvmAddrShift)
            regData &= ~self.kNvmProgEnMask
            if progEn == self.kEnable:
                regData |= progEn << self.kNvmProgEnShift
            
            self._i2c.write_byte(self.address, self.kRegNvmAddr, regData)

    def _nvm_write_addr(self, nvmAddr, progEn):
        """!
        This internal API is used to write the nvm data. Not to be used outside of driver.

        @param int nvmAddr: The NVM address to write
        @param int progEn: The program enable
        @param int currPwrMode: The current power mode

        @return  The new power mode
        
        """
        currPwrMode = self.kError

        if (nvmAddr >= self.kNvmStartAddr) and (nvmAddr <= self.kNvmEndAddr):
            currPwrMode = self.get_power_mode()
            if currPwrMode != self.kPowerModeStandby:
                self.set_power_mode(self.kPowerModeStandby)
            self._set_nvm_addr(nvmAddr, progEn)
        
        return currPwrMode