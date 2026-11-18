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

__version__ = "3.0.0"

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
    OVERSAMPLING_1X = 0x00
    OVERSAMPLING_2X = 0x01
    OVERSAMPLING_4X = 0x02
    OVERSAMPLING_8X = 0x03
    OVERSAMPLING_16X = 0x04
    OVERSAMPLING_32X = 0x05
    OVERSAMPLING_64X = 0x06
    OVERSAMPLING_128X = 0x07

    def __init__(self):
        # Oversampling 
        # Temperature and Pressure oversampling respectively
        self.osrT = self.OVERSAMPLING_1X
        self.osrP = self.OVERSAMPLING_1X

        # Enable Pressure (1 - enabled, 0 - disabled)
        self.pressEn = 0

        # Output data rate
        self.odr = 0

# OSR, ODR and pressure configuration structure
class IirConfig(object):
    # IIR filter for temperature and pressure
    IIR_FILTER_BYPASS = 0x00
    IIR_FILTER_COEFF_1 = 0x01
    IIR_FILTER_COEFF_3 = 0x02
    IIR_FILTER_COEFF_7 = 0x03
    IIR_FILTER_COEFF_15 = 0x04
    IIR_FILTER_COEFF_31 = 0x05
    IIR_FILTER_COEFF_63 = 0x06
    IIR_FILTER_COEFF_127 = 0x07

    def __init__(self):
        # Temperature IIR
        self.setIirT = self.IIR_FILTER_BYPASS
        
        # Pressure IIR
        self.setIirP = self.IIR_FILTER_BYPASS
        
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
class IntSourceSelect(object):
    def __init__(self):
        # All of these are enables for the corresponding interrupt, (1 - enabled, 0 - disabled)
        self.intDrdy = 0
        self.intFifoFull = 0
        self.intFifoThres = 0
        self.intOorPress = 0

# BMP5 Out-of-range pressure configuration.
class OorPressConfiguration(object):
    # Pressure Out-of-range count limit
    OOR_COUNT_LIMIT_1 = 0x00
    OOR_COUNT_LIMIT_3 = 0x01
    OOR_COUNT_LIMIT_7 = 0x02
    OOR_COUNT_LIMIT_15 = 0x03

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
    FIFO_NOT_ENABLED = 1
    FIFO_TEMPERATURE_DATA = 2
    FIFO_PRESSURE_DATA = 3
    FIFO_PRESS_TEMP_DATA = 4
    
    # Possible fifo decimation(downsampling) selection
    FIFO_NO_DOWNSAMPLING = 0
    FIFO_DOWNSAMPLING_2X = 1
    FIFO_DOWNSAMPLING_4X = 2
    FIFO_DOWNSAMPLING_8X = 3
    FIFO_DOWNSAMPLING_16X = 4
    FIFO_DOWNSAMPLING_32X = 5
    FIFO_DOWNSAMPLING_64X = 6
    FIFO_DOWNSAMPLING_128X = 7

    # Possible fifo mode selection
    FIFO_MODE_STREAMING = 0
    FIFO_MODE_STOP_ON_FULL = 1

    def __init__(self):
        self.data = []
        self.length = 0
        self.frameSel = self.FIFO_NOT_ENABLED
        self.decSel = self.FIFO_NO_DOWNSAMPLING
        self.fifoCount = 0 # frame count
        self.mode = self.FIFO_MODE_STREAMING
        self.threshold = 0
        self.setFifoIirT = 0 # Fifo IIR for temperature (1 - enabled, 0 - disabled)
        self.setFifoIirP = 0 # Fifo IIR for pressure (1 - enabled, 0 - disabled)

class QwiicBMP581(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Register definitions
    REG_CHIP_ID = 0x01
    REG_REV_ID = 0x02
    REG_CHIP_STATUS = 0x11
    REG_DRIVE_CONFIG = 0x13
    REG_INT_CONFIG = 0x14
    REG_INT_SOURCE = 0x15
    REG_FIFO_CONFIG = 0x16
    REG_FIFO_COUNT = 0x17
    REG_FIFO_SEL = 0x18
    REG_TEMP_DATA_XLSB = 0x1D
    REG_TEMP_DATA_LSB = 0x1E
    REG_TEMP_DATA_MSB = 0x1F
    REG_PRESS_DATA_XLSB = 0x20
    REG_PRESS_DATA_LSB = 0x21
    REG_PRESS_DATA_MSB = 0x22
    REG_INT_STATUS = 0x27
    REG_STATUS = 0x28
    REG_FIFO_DATA = 0x29
    REG_NVM_ADDR = 0x2B
    REG_NVM_DATA_LSB = 0x2C
    REG_NVM_DATA_MSB = 0x2D
    REG_DSP_CONFIG = 0x30
    REG_DSP_IIR = 0x31
    REG_OOR_THR_P_LSB = 0x32
    REG_OOR_THR_P_MSB = 0x33
    REG_OOR_RANGE = 0x34
    REG_OOR_CONFIG = 0x35
    REG_OSR_CONFIG = 0x36
    REG_ODR_CONFIG = 0x37
    REG_OSR_EFF = 0x38
    REG_CMD = 0x7E

    # Power mode definitions
    POWER_MODE_STANDBY = 0
    POWER_MODE_NORMAL = 1
    POWER_MODE_FORCED = 2
    POWER_MODE_CONTINUOUS = 3
    POWER_MODE_DEEP_STANDBY = 4

    # Masks and Shifts
    # Interrupt configurations
    INT_MODE_MASK = 0x01
    INT_MODE_SHIFT = 0
    
    INT_POL_MASK = 0x02
    INT_POL_SHIFT = 1

    INT_OD_MASK = 0x04
    INT_OD_SHIFT = 2

    INT_EN_MASK = 0x08
    INT_EN_SHIFT = 3

    INT_DRDY_EN_MASK = 0x01
    INT_DRDY_EN_SHIFT = 0

    INT_FIFO_FULL_EN_MASK = 0x02
    INT_FIFO_FULL_EN_SHIFT = 1

    INT_FIFO_THRES_EN_MASK = 0x04
    INT_FIFO_THRES_EN_SHIFT = 2

    INT_OOR_PRESS_EN_MASK = 0x08
    INT_OOR_PRESS_EN_SHIFT = 3

    # ODR configuration
    ODR_MASK = 0x7C
    ODR_SHIFT = 2

    # OSR configurations
    TEMP_OS_MASK = 0x07
    TEMP_OS_SHIFT = 0

    PRESS_OS_MASK = 0x38
    PRESS_OS_SHIFT = 3

    # Pressure enable
    PRESS_EN_MASK = 0x40
    PRESS_EN_SHIFT = 6

    # IIR configurations
    SET_IIR_TEMP_MASK = 0x07
    SET_IIR_TEMP_SHIFT = 0

    SET_IIR_PRESS_MASK = 0x38
    SET_IIR_PRESS_SHIFT = 3

    OOR_SEL_IIR_PRESS_MASK = 0x80
    OOR_SEL_IIR_PRESS_SHIFT = 7

    SHDW_SET_IIR_TEMP_MASK = 0x08
    SHDW_SET_IIR_TEMP_SHIFT = 3

    SHDW_SET_IIR_PRESS_MASK = 0x20
    SHDW_SET_IIR_PRESS_SHIFT = 5

    SET_FIFO_IIR_TEMP_MASK = 0x10
    SET_FIFO_IIR_TEMP_SHIFT = 4

    SET_FIFO_IIR_PRESS_MASK = 0x40
    SET_FIFO_IIR_PRESS_SHIFT = 6

    IIR_FLUSH_FORCED_EN_MASK = 0x04
    IIR_FLUSH_FORCED_EN_SHIFT = 2

    # Effective OSR configurations and ODR valid status
    OSR_TEMP_EFF_MASK = 0x07
    OSR_TEMP_EFF_SHIFT = 0

    OSR_PRESS_EFF_MASK = 0x38
    OSR_PRESS_EFF_SHIFT = 3

    ODR_IS_VALID_MASK = 0x80
    ODR_IS_VALID_SHIFT = 7

    # Powermode
    POWERMODE_MASK = 0x03
    POWERMODE_SHIFT = 0

    DEEP_DISABLE_MASK = 0x80
    DEEP_DISABLE_SHIFT = 7

    # Fifo configurations
    FIFO_THRESHOLD_MASK = 0x1F
    FIFO_THRESHOLD_SHIFT = 0

    FIFO_MODE_MASK = 0x20
    FIFO_MODE_SHIFT = 5

    FIFO_DEC_SEL_MASK = 0x1C
    FIFO_DEC_SEL_SHIFT = 2

    FIFO_COUNT_MASK = 0x3F
    FIFO_COUNT_SHIFT = 0

    FIFO_FRAME_SEL_MASK = 0x03
    FIFO_FRAME_SEL_SHIFT = 0

    # Out-of-range configuration
    OOR_THR_P_LSB_MASK = 0x0000FF
    OOR_THR_P_LSB_SHIFT = 0

    OOR_THR_P_MSB_MASK = 0x00FF00
    OOR_THR_P_MSB_SHIFT = 0

    OOR_THR_P_XMSB_MASK = 0x010000
    OOR_THR_P_XMSB_SHIFT = 16

    # Macro to mask xmsb value of oor threshold from register(0x35) value
    OOR_THR_P_XMSB_REG_MASK = 0x01
    OOR_THR_P_XMSB_REG_SHIFT = 0

    OOR_COUNT_LIMIT_MASK = 0xC0
    OOR_COUNT_LIMIT_SHIFT = 6

    # NVM configuration
    NVM_ADDR_MASK = 0x3F
    NVM_ADDR_SHIFT = 0

    NVM_PROG_EN_MASK = 0x40
    NVM_PROG_EN_SHIFT = 6

    NVM_DATA_LSB_MASK = 0x00FF
    NVM_DATA_LSB_SHIFT = 0

    NVM_DATA_MSB_MASK = 0xFF00
    NVM_DATA_MSB_SHIFT = 0

    # Constant Value definitions
    # Delay definitions
    DELAY_US_SOFT_RESET = 2000
    DELAY_US_STANDBY = 2500
    DELAY_US_NVM_READY_READ = 800
    DELAY_US_NVM_READY_WRITE = 10000

    # Soft reset command
    SOFT_RESET_CMD = 0xB6

    # NVM command
    NVM_FIRST_CMD = 0x5D
    NVM_READ_ENABLE_CMD = 0xA5
    NVM_WRITE_ENABLE_CMD = 0xA0

    # Deepstandby enable/disable
    DEEP_ENABLED = 0
    DEEP_DISABLED = 1

    # General enable/disable
    ENABLE = 1
    DISABLE = 0
    ERROR = -1
    NO_ERROR = 0

    # ODR settings
    ODR_240HZ = 0x00
    ODR_218_5HZ = 0x01
    ODR_199_1HZ = 0x02
    ODR_179_2HZ = 0x03
    ODR_160HZ = 0x04
    ODR_149_3HZ = 0x05
    ODR_140HZ = 0x06
    ODR_129_8HZ = 0x07
    ODR_120HZ = 0x08
    ODR_110_1HZ = 0x09
    ODR_100_2HZ = 0x0A
    ODR_89_6HZ = 0x0B
    ODR_80HZ = 0x0C
    ODR_70HZ = 0x0D
    ODR_60HZ = 0x0E
    ODR_50HZ = 0x0F
    ODR_45HZ = 0x10
    ODR_40HZ = 0x11
    ODR_35HZ = 0x12
    ODR_30HZ = 0x13
    ODR_25HZ = 0x14
    ODR_20HZ = 0x15
    ODR_15HZ = 0x16
    ODR_10HZ = 0x17
    ODR_05HZ = 0x18
    ODR_04HZ = 0x19
    ODR_03HZ = 0x1A
    ODR_02HZ = 0x1B
    ODR_01HZ = 0x1C
    ODR_0_5HZ = 0x1D
    ODR_0_250HZ = 0x1E
    ODR_0_125HZ = 0x1F

    # Fifo frame configuration
    FIFO_EMPTY = 0x7F
    FIFO_MAX_THRESHOLD_PT_MODE = 0x0F
    FIFO_MAX_THRESHOLD_P_MODE = 0x1F

    # Macro to bypass both iir_t and iir_p together
    IIR_BYPASS = 0xC0

    # Interrupt configurations
    INT_MODE_PULSED = 0
    INT_MODE_LATCHED = 1

    INT_POL_ACTIVE_LOW = 0
    INT_POL_ACTIVE_HIGH = 1

    INT_OD_PUSH_PULL = 0
    INT_OD_OPEN_DRAIN = 1

    # NVM and Interrupt status asserted macros
    INT_ASSERTED_DRDY = 0x01
    INT_ASSERTED_FIFO_FULL = 0x02
    INT_ASSERTED_FIFO_THRES = 0x04
    INT_ASSERTED_PRESSURE_OOR = 0x08
    INT_ASSERTED_POR_SOFTRESET_COMPLETE = 0x10
    INT_NVM_RDY = 0x02
    INT_NVM_ERR = 0x04
    INT_NVM_CMD_ERR = 0x08

    # NVM addresses
    NVM_START_ADDR = 0x20
    NVM_END_ADDR = 0x22

    # Chip ID
    CHIP_ID = 0x50

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
        
        self.osrOdrConfig = OsrOdrPressConfig()
        self.fifo = FifoConfig()

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        return self._i2c.is_device_connected(self.address)

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
        
        chip_id = self._i2c.read_byte(self.address, self.REG_CHIP_ID)

        if self._power_up_check() == False:
            return False
        if self._validate_chip_id(chip_id) == False:
            return False
        
        # Enable both pressure and temperature sensors
        self.enable_press(self.ENABLE)

        # Set to normal mode
        self.set_power_mode(self.POWER_MODE_NORMAL)
        return True
    
    def enable_press(self, enable):
        """!
        Enables or disables the pressure sensor.

        @param enable: **int** The value to set

        Allowable values:
            - `ENABLE`
            - `DISABLE`
        """
        self.osrOdrConfig.pressEn = enable
        self.set_osr_odr_press_config()
    
    def set_odr_frequency(self, odr):
        """!
        Sets the output data rate of the sensor.

        @param odr: **int** The output data rate to set
        """
        # check whether ODR is valid
        if odr > self.ODR_0_125HZ:
            return self.ERROR

        self.osrOdrConfig.odr = odr
        self.set_osr_odr_press_config()

    def set_osr_multipliers(self, config):
        """!
        Set the temperature and pressure oversampling multipliers.

        @param config: **OsrOdrPressConfig** The configuration to set
        """
        # check whether OSR multipliers are valid
        if config.osrT > config.OVERSAMPLING_128X or config.osrP > config.OVERSAMPLING_128X:
            return self.ERROR
        
        self.osrOdrConfig.osrT = config.osrT
        self.osrOdrConfig.osrP = config.osrP
        self.set_osr_odr_press_config()

    def soft_reset(self):
        """!
        This API performs the soft reset of the sensor.
        """
        self._i2c.write_byte(self.address, self.REG_CMD, self.SOFT_RESET_CMD)
        self._i2c.delay_us(self.DELAY_US_SOFT_RESET)

    def get_osr_odr_press_config(self):
        """!
        Gets the current oversampling and output data rate configuration

        @return **OsrOdrPressConfig** The current oversampling and output data rate configuration
        """
        osr_config = self._i2c.read_byte(self.address, self.REG_OSR_CONFIG)

        config = OsrOdrPressConfig()
        config.osrT = (osr_config & self.TEMP_OS_MASK) >> self.TEMP_OS_SHIFT
        config.osrP = (osr_config & self.PRESS_OS_MASK) >> self.PRESS_OS_SHIFT
        config.pressEn = (osr_config & self.PRESS_EN_MASK) >> self.PRESS_EN_SHIFT
        config.odr = (osr_config & self.ODR_MASK) >> self.ODR_SHIFT

        return config
    
    def set_osr_odr_press_config(self):
        """!
        This API sets the configuration for oversampling temperature, oversampling of pressure 
        and ODR configuration along with pressure enable.

        NOTE: If ODR is set to a value higher than 5Hz then powermode is set as standby mode, 
        as ODR value greater than 5HZ without disabling deep-standby mode makes powermode invalid.
        """
        if self.osrOdrConfig.odr < self.ODR_05HZ:
            self._set_standby_mode()
        
        reg_data = list(self._i2c.read_block(self.address, self.REG_OSR_CONFIG, 2))
        
        reg_data[0] = (reg_data[0] & ~self.TEMP_OS_MASK) | (self.osrOdrConfig.osrT << self.TEMP_OS_SHIFT)
        reg_data[0] = (reg_data[0] & ~self.PRESS_OS_MASK) | (self.osrOdrConfig.osrP << self.PRESS_OS_SHIFT)
        reg_data[0] = (reg_data[0] & ~self.PRESS_EN_MASK) | (self.osrOdrConfig.pressEn << self.PRESS_EN_SHIFT)
        reg_data[1] = (reg_data[1] & ~self.ODR_MASK) | (self.osrOdrConfig.odr << self.ODR_SHIFT)

        self._i2c.write_block(self.address, self.REG_OSR_CONFIG, reg_data)

    def get_iir_config(self):
        """!
        Gets the current IIR configuration

        @return **IirConfig** The current IIR configuration
        """
        dsp_config = self._i2c.read_block(self.address, self.REG_DSP_CONFIG, 2)

        config = IirConfig()
        config.shdwSetIirT = (dsp_config[0] & self.SHDW_SET_IIR_TEMP_MASK) >> self.SHDW_SET_IIR_TEMP_SHIFT
        config.shdwSetIirP = (dsp_config[0] & self.SHDW_SET_IIR_PRESS_MASK) >> self.SHDW_SET_IIR_PRESS_SHIFT
        config.iirFlushForcedEn = (dsp_config[0] & self.IIR_FLUSH_FORCED_EN_MASK) >> self.IIR_FLUSH_FORCED_EN_SHIFT

        config.setIirT = (dsp_config[1] & self.SET_IIR_TEMP_MASK) >> self.SET_IIR_TEMP_SHIFT
        config.setIirP = (dsp_config[1] & self.SET_IIR_PRESS_MASK) >> self.SET_IIR_PRESS_SHIFT

        return config
    
    def get_power_mode(self):
        """!
        Gets the current power mode of the device

        @return **int** The current power mode or -1 on error
        """
        odr_config = self._i2c.read_byte(self.address, self.REG_ODR_CONFIG)
        power_mode = (odr_config & self.POWERMODE_MASK) >> self.POWERMODE_SHIFT
        
        if power_mode == self.POWER_MODE_STANDBY:
            deep_dis = (odr_config & self.DEEP_DISABLE_MASK) >> self.DEEP_DISABLE_SHIFT
            if deep_dis == self.DEEP_ENABLED:
                if self._check_deepstandby_mode():
                    return self.POWER_MODE_DEEP_STANDBY
                else: 
                    return self.ERROR
            else:
                return self.POWER_MODE_STANDBY
            
        if power_mode == self.POWER_MODE_NORMAL:
            return self.POWER_MODE_NORMAL
        if power_mode == self.POWER_MODE_FORCED:
            return self.POWER_MODE_FORCED
        if power_mode == self.POWER_MODE_CONTINUOUS:
            return self.POWER_MODE_CONTINUOUS
        
        return self.ERROR
    
    def set_power_mode(self, power_mode):
        """!
        Sets the power mode of the device

        @param power_mode: **int** The power mode to set

        Allowable power_mode values:
            - `POWER_MODE_STANDBY`
            - `POWER_MODE_NORMAL`
            - `POWER_MODE_FORCED`
            - `POWER_MODE_CONTINUOUS`
            - `POWER_MODE_DEEP_STANDBY`
        """
        last_mode = self.get_power_mode()

        # Device should be set to standby before transiting to
        # forced mode or normal mode or continous mode.
        if last_mode != self.POWER_MODE_STANDBY:
            self._direct_set_power_mode(self.POWER_MODE_STANDBY)
            self._i2c.delay_us(self.DELAY_US_STANDBY)
        
        if power_mode == self.POWER_MODE_DEEP_STANDBY:
            self._set_deepstandby_mode()
        # elif power_mode == self.POWER_MODE_STANDBY:
            # Since switching between powermodes require sensor to be in standby mode
            # it is performed above. So it is not explicitly performed here.
            # pass
        elif power_mode in [self.POWER_MODE_NORMAL, self.POWER_MODE_FORCED, self.POWER_MODE_CONTINUOUS]:
            self._direct_set_power_mode(power_mode)
    
    def get_sensor_data(self):
        """!
        This API reads the temperature(deg C) or both pressure(Pa) and temperature(deg C) data from the
        sensor and store it in the bmp5_sensor_data structure instance passed by the user.

        @return **SensorData** The sensor data
        """
        data = SensorData()

        reg_data = self._i2c.read_block(self.address, self.REG_TEMP_DATA_XLSB, 6)
        
        raw_data_t = (reg_data[2] << 16) | (reg_data[1] << 8) | reg_data[0]
        data.temperature = raw_data_t / 65536.0

        if self.osrOdrConfig.pressEn:
            raw_data_p = (reg_data[5] << 16) | (reg_data[4] << 8) | reg_data[3]
            data.pressure = raw_data_p / 64.0
        else:
            data.pressure = 0
        
        return data
    
    def get_osr_odr_eff(self):
        """!
        This API reads the effective oversampling and output data rate configuration from the sensor.

        @return **OsrOdrEff** The effective oversampling and output data rate configuration
        """
        reg_data = self._i2c.read_block(self.address, self.REG_OSR_EFF, 1)

        eff = OsrOdrEff()
        eff.osrTEff = (reg_data[0] & self.OSR_TEMP_EFF_MASK) >> self.OSR_TEMP_EFF_SHIFT
        eff.osrPEff = (reg_data[0] & self.OSR_PRESS_EFF_MASK) >> self.OSR_PRESS_EFF_SHIFT
        eff.odrIsValid = (reg_data[0] & self.ODR_IS_VALID_MASK) >> self.ODR_IS_VALID_SHIFT

        return eff

    def set_iir_config(self, config):
        """!
        This API sets the configuration for IIR of temperature and pressure.
        
        If IIR value for both temperature and pressure is set a value other than bypass then powermode is set
        as standby mode, as IIR with value other than bypass without disabling deep-standby mode makes powermode invalid.
        """
        
        if (config.setIirT != config.IIR_FILTER_BYPASS) or (config.setIirP != config.IIR_FILTER_BYPASS):
            self._set_standby_mode()
        
        curr_pwr_mode = self.get_power_mode()

        if curr_pwr_mode != self.POWER_MODE_STANDBY:
            self.set_power_mode(self.POWER_MODE_STANDBY)
        
        self._direct_set_iir_config(config)

        # If previous mode is not standbymode return sensor to that previous mode
        # after setting iir configuration
        if (curr_pwr_mode != self.POWER_MODE_STANDBY) and (curr_pwr_mode != self.POWER_MODE_DEEP_STANDBY): 
            self.set_power_mode(curr_pwr_mode)

    def set_oor_configuration(self, config):
        """!
        This API sets the configuration for out-of-range pressure threshold, range
        count limit and IIR.

        @param config: **OorPressConfiguration** The configuration to set
        """

        self._set_oor_iir_count_limit(config.oorSeliirP, config.oorCntLim)

        # Get the OOR Configurations
        reg_data = list(self._i2c.read_block(self.address, self.REG_OOR_THR_P_LSB, 4))

        reg_data[0] = (reg_data[0] & ~self.OOR_THR_P_LSB_MASK) | (config.oorThrP << self.OOR_THR_P_LSB_SHIFT)
        reg_data[1] = (reg_data[1] & ~self.OOR_THR_P_MSB_MASK) | ( (config.oorThrP >> 8) << self.OOR_THR_P_MSB_SHIFT)
        reg_data[2] = config.oorRangeP
        thres_x_msb = (config.oorThrP & self.OOR_THR_P_XMSB_MASK) >> self.OOR_THR_P_XMSB_SHIFT
        reg_data[3] = (reg_data[3] & ~self.OOR_THR_P_XMSB_REG_MASK) | thres_x_msb

        self._i2c.write_block(self.address, self.REG_OOR_THR_P_LSB, reg_data)
        
    def configure_interrupt(self, int_mode, int_pol, int_od, int_en):
        """!
        This API is used to configure the interrupt settings.

        @param int_mode: **int** The interrupt mode to set

        Allowable values:
            - `INT_MODE_PULSED`
            - `INT_MODE_LATCHED`
        @param int_pol: **int** The interrupt polarity to set

        Allowable values:
            - `INT_POL_ACTIVE_LOW`
            - `INT_POL_ACTIVE_HIGH`
        @param int_od: **int** The interrupt output type to set

        Allowable values:
            - `INT_OD_PUSH_PULL`
            - `INT_OD_OPEN_DRAIN`
        @param int_en: **int** The interrupt enable to set

        Allowable values:
            - `ENABLE`
            - `DISABLE`
        """
        
        reg_data = self._i2c.read_block(self.address, self.REG_INT_CONFIG, 1)

        # Any change between latched/pulsed mode has to be applied while interrupt is disabled
        # Step 1 : Turn off all INT sources (INT_SOURCE -> 0x00)
        # Step 2 : Read the INT_STATUS register to clear the status
        # Step 3 : Set the desired mode in INT_CONFIG.int_mode
        # Finally transfer the interrupt configurations 
        self._i2c.write_byte(self.address, self.REG_INT_SOURCE, 0x00)

        int_status = self._i2c.read_byte(self.address, self.REG_INT_STATUS)
        
        reg_data = (reg_data & ~self.INT_MODE_MASK) | (int_mode << self.INT_MODE_SHIFT)
        reg_data = (reg_data & ~self.INT_POL_MASK) | (int_pol << self.INT_POL_SHIFT)
        reg_data = (reg_data & ~self.INT_OD_MASK) | (int_od << self.INT_OD_SHIFT)
        reg_data = (reg_data & ~self.INT_EN_MASK) | (int_en << self.INT_EN_SHIFT)

        self._i2c.write_byte(self.address, self.REG_INT_CONFIG, reg_data)
    
    def int_source_select(self, select):
        """!
        This API is used to enable the interrupts(drdy interrupt, fifo full interrupt,
        fifo threshold enable and pressure data out of range interrupt).

        @param select: **IntSourceSelect** The interrupt source select to set
        """
        reg_data = self._i2c.read_byte(self.address, self.REG_INT_SOURCE)

        reg_data = (reg_data & ~self.INT_DRDY_EN_MASK) | (select.intDrdy << self.INT_DRDY_EN_SHIFT)
        reg_data = (reg_data & ~self.INT_FIFO_FULL_EN_MASK) | (select.intFifoFull << self.INT_FIFO_FULL_EN_SHIFT)
        reg_data = (reg_data & ~self.INT_FIFO_THRES_EN_MASK) | (select.intFifoThres << self.INT_FIFO_THRES_EN_SHIFT)
        reg_data = (reg_data & ~self.INT_OOR_PRESS_EN_MASK) | (select.intOorPress << self.INT_OOR_PRESS_EN_SHIFT)

        self._i2c.write_byte(self.address, self.REG_INT_SOURCE, reg_data)
    
    def get_interrupt_status(self):
        """!
        This API is used to get interrupt status.
        """
        return self._i2c.read_byte(self.address, self.REG_INT_STATUS)
    
    def set_fifo_configuration(self, fifo):
        """!
        This API used to set the configurations of fifo in the sensor.
        
        If Fifo frame selection is enabled then powermode is set as standby mode, as fifo frame selection
        enabled without disabling deep-standby mode makes powermode invalid.
        """
        if fifo.frameSel != fifo.FIFO_NOT_ENABLED:
            self._set_standby_mode()
        
        self._set_fifo_iir_config(fifo.setFifoIirT, fifo.setFifoIirP)

        # Get the FIFO Configurations
        reg_data = list(self._i2c.read_byte(self.address, self.REG_FIFO_CONFIG))

        reg_data &= ~self.FIFO_MODE_MASK
        reg_data |= fifo.mode << self.FIFO_MODE_SHIFT

        self._set_fifo_threshold(reg_data, fifo)

        # Set the fifo configurations
        self._i2c.write_byte(self.address, self.REG_FIFO_CONFIG, reg_data)

        reg_data = self._i2c.read_byte(self.address, self.REG_FIFO_SEL)

        reg_data &= ~self.FIFO_FRAME_SEL_MASK
        reg_data |= fifo.frameSel << self.FIFO_FRAME_SEL_SHIFT
        reg_data &= ~self.FIFO_DEC_SEL_MASK
        reg_data |= fifo.decimation << self.FIFO_DEC_SEL_SHIFT

        self._i2c.write_byte(self.address, self.REG_FIFO_SEL, reg_data)

    def get_fifo_len(self, fifo):
        """!
        This API is used to get the length of FIFO data available in the sensor.

        @param fifo: **FifoConfiguration** The fifo configuration
        """

        reg_data = self._i2c.read_byte(self.address, self.REG_FIFO_COUNT)

        fifo.fifoCount = (reg_data & self.FIFO_COUNT_MASK) >> self.FIFO_COUNT_SHIFT

        if (fifo.frameSel == fifo.FIFO_TEMPERATURE_DATA) or (fifo.frameSel == fifo.FIFO_PRESSURE_DATA):
            return fifo.fifoCount  * 3
        elif fifo.frameSel == fifo.FIFO_PRESS_TEMP_DATA:
            return fifo.fifoCount  * 6
        
        return 0

    def get_fifo_data(self, fifo):
        """!
        This API is used to read the FIFO data from the sensor.

        @param fifo: **FifoConfiguration** The fifo configuration
        """
        fifo_len = self.get_fifo_len(fifo)

        if fifo.length > fifo_len:
            fifo.length = fifo_len
        
        reg_data = self._i2c.read_block(self.address, self.REG_FIFO_DATA, fifo.length)

        fifo.data[:] = list(reg_data)[:]

    def extract_fifo_data(self, fifo, sensor_data):
        """!
        This API extract the temperature and/or pressure data from the fifo data which is
        already read from the fifo.
        """

        idx = 0

        for i in range(0, fifo.length):
            res = self._unpack_sensor_data(sensor_data[idx], i, fifo)
            if not res:
                break
            idx += 1

    def nvm_read(self, nvm_addr):
        """!
        This API is used to perform NVM reads.

        @param nvm_addr: **int** The NVM address to read
        """
        curr_pwr_mode = self._nvm_write_addr(nvm_addr, self.DISABLE)

        self._i2c.write_byte(self.address, self.REG_CMD, self.NVM_FIRST_CMD)
        self._i2c.write_byte(self.address, self.REG_CMD, self.NVM_READ_ENABLE_CMD)
        self._i2c.delay_us(self.DELAY_US_NVM_READY_READ)

        nvm_data = self._get_nvm_data()

        if curr_pwr_mode != self.POWER_MODE_STANDBY:
            self.set_power_mode(curr_pwr_mode)
        
        return nvm_data

    def nvm_write(self, nvm_addr, nvm_write_data):
        curr_pwr_mode = self._nvm_write_addr(nvm_addr, self.ENABLE)
        nvm_data = list(self._i2c.read_block(self.address, self.REG_NVM_DATA_LSB, 2))

        nvm_data[0] = nvm_write_data & self.NVM_DATA_LSB_MASK
        nvm_data[1] = (nvm_write_data & self.NVM_DATA_MSB_MASK) >> 8

        self._i2c.write_block(self.address, self.REG_NVM_DATA_LSB, nvm_data)

        self._i2c.write_byte(self.address, self.REG_CMD, self.NVM_FIRST_CMD)

        # Write enable NVM command for user write sequence
        reg_data = self.NVM_WRITE_ENABLE_CMD
        self._i2c.write_byte(self.address, self.REG_CMD, reg_data)
        self._i2c.delay_us(self.DELAY_US_NVM_READY_WRITE)

        nvm_status = self._get_nvm_status()

        if (nvm_status & self.INT_NVM_RDY) and not(nvm_status & self.INT_NVM_ERR) and not(nvm_status & self.INT_NVM_CMD_ERR):
            # Reset NVM prog_en
            # TODO: The below line looks strange to me, seems like reg_data is currently NVM_WRITE_ENABLE_CMD from above
            #       and then we are clearing a bit that doesn't even exist in that command and then sending it.
            #       This is what the original code does, so I'll keep it for now, but might want to add this line before it:
            # reg_data = self._i2c.read_byte(self.address, self.REG_NVM_ADDR)
            reg_data = (reg_data & ~self.NVM_PROG_EN_MASK)
            self._i2c.write_byte(self.address, self.REG_NVM_ADDR, reg_data)

        if curr_pwr_mode != self.POWER_MODE_STANDBY:
            self.set_power_mode(curr_pwr_mode)

    # Private Methods
    def _power_up_check(self):
        """!
        This internal API is used to validate the post power-up procedure. Not to be used outside of driver.
        """
        nvm_status = self._get_nvm_status()
        if (nvm_status & self.INT_NVM_RDY) and not(nvm_status & self.INT_NVM_ERR):
            status = self.get_interrupt_status()
            if status & self.INT_ASSERTED_POR_SOFTRESET_COMPLETE:
                return True
        
        return False
    
    def _validate_chip_id(self, chip_id):
        """!
        This internal API is used to validate the chip id of the sensor. Not to be used outside of driver.
        """
        if chip_id == self.CHIP_ID:
            return True
        return False

    def _check_deepstandby_mode(self):
        """!
        Checks if the device is in deepstandby mode. Not to be used outside of driver.

        @return **bool** `True` if in deepstandby mode, otherwise `False`
        """

        fifo_frame_sel = self._i2c.read_byte(self.address, self.REG_FIFO_SEL)
        fifo_frame_sel = (fifo_frame_sel & self.FIFO_FRAME_SEL_MASK) >> self.FIFO_FRAME_SEL_SHIFT

        osr_conf = self.get_osr_odr_press_config()
        iir_conf = self.get_iir_config()

        # As per datasheet odr should be less than 5Hz. But register value for 5Hz is less than 4Hz and so,
        # thus in this below condition odr is checked whether greater than 5Hz macro.
        if (osr_conf.odr > self.ODR_05HZ) and (fifo_frame_sel == self.DISABLE) \
            and (iir_conf.setIirT == iir_conf.IIR_FILTER_BYPASS) and (iir_conf.setIirP == iir_conf.IIR_FILTER_BYPASS):
            return True
        
        return False
    
    def _set_deepstandby_mode(self):
        """!
        This function is used to set the device to deepstandby mode. Not to be used outside of driver.
        """
        reg_data = self._i2c.read_byte(self.address, self.REG_ODR_CONFIG)

        reg_data &= ~self.DEEP_DISABLE_MASK # Setting deep_dis = 0(BMP5_DEEP_ENABLED) enables the deep standby mode
        
        # Set ODR less then 5Hz - ODR used is 1Hz
        reg_data &= ~self.ODR_MASK
        reg_data |= self.ODR_01HZ << self.ODR_SHIFT

        self._i2c.write_byte(self.address, self.REG_ODR_CONFIG, reg_data)

        reg_data = self._i2c.read_byte(self.address, self.REG_DSP_IIR)
        reg_data &= self.IIR_BYPASS

        self._i2c.write_byte(self.address, self.REG_DSP_IIR, reg_data)

        reg_data = self._i2c.read_byte(self.address, self.REG_FIFO_SEL)
        reg_data &= ~self.FIFO_FRAME_SEL_MASK

        self._i2c.write_byte(self.address, self.REG_FIFO_SEL, reg_data)
    
    def _set_standby_mode(self):
        """!
        This function is used to set the device to standby powermode when powermoide is deepstandby mode. Not to be used outside of driver.
        """
        power_mode = self.get_power_mode()
        if power_mode == self.POWER_MODE_DEEP_STANDBY:
            self.set_power_mode(self.POWER_MODE_STANDBY)
    
    def _direct_set_power_mode(self, power_mode):
        """!
        Sets the power mode of the device. Not to be used outside of driver

        @param power_mode: **int** The power mode to set

        Allowable power_mode values:
            - `POWER_MODE_STANDBY`
            - `POWER_MODE_NORMAL`
            - `POWER_MODE_FORCED`
            - `POWER_MODE_CONTINUOUS`
            - `POWER_MODE_DEEP_STANDBY`
        """
        odr_config = self._i2c.read_byte(self.address, self.REG_ODR_CONFIG)
        
        odr_config &= ~self.DEEP_DISABLE_MASK
        odr_config |= self.DEEP_DISABLED << self.DEEP_DISABLE_SHIFT

        odr_config &= ~self.POWERMODE_MASK
        odr_config |= power_mode << self.POWERMODE_SHIFT

        self._i2c.write_byte(self.address, self.REG_ODR_CONFIG, odr_config)

    def _direct_set_iir_config(self, config):
        """!
        Sets the IIR for temperature and pressure. Not to be used outside of driver.
        """
        reg_data = list(self._i2c.read_block(self.address, self.REG_DSP_CONFIG, 2))

        reg_data[0] &= ~self.SHDW_SET_IIR_TEMP_MASK
        reg_data[0] |= config.shdwSetIirT << self.SHDW_SET_IIR_TEMP_SHIFT

        reg_data[0] &= ~self.SHDW_SET_IIR_PRESS_MASK
        reg_data[0] |= config.shdwSetIirP << self.SHDW_SET_IIR_PRESS_SHIFT

        reg_data[0] &= ~self.IIR_FLUSH_FORCED_EN_MASK
        reg_data[0] |= config.iirFlushForcedEn << self.IIR_FLUSH_FORCED_EN_SHIFT

        reg_data[1] &= ~self.SET_IIR_TEMP_MASK
        reg_data[1] |= config.setIirT << self.SET_IIR_TEMP_SHIFT

        reg_data[1] &= ~self.SET_IIR_PRESS_MASK
        reg_data[1] |= config.setIirP << self.SET_IIR_PRESS_SHIFT

        self._i2c.write_block(self.address, self.REG_DSP_IIR, reg_data)

    def _set_oor_iir_count_limit(self, set_oor_iir_p, set_count_limit):
        """!
        This internal API sets the IIR configuration and count limit of OOR pressure.
        """
        curr_pwr_mode = self.get_power_mode()

        # OOR IIR configuration and count limit is writable only during STANDBY mode(as per datasheet)
        if curr_pwr_mode != self.POWER_MODE_STANDBY:
            self.set_power_mode(self.POWER_MODE_STANDBY)
        
        # Get OOR pressure IIR configuration
        reg_data = self._i2c.read_byte(self.address, self.REG_DSP_CONFIG)

        reg_data &= ~self.OOR_SEL_IIR_PRESS_MASK
        reg_data |= set_oor_iir_p << self.OOR_SEL_IIR_PRESS_SHIFT
        self._i2c.write_byte(self.address, self.REG_DSP_CONFIG, reg_data)

        reg_data = self._i2c.read_byte(self.address, self.REG_OOR_CONFIG)

        reg_data &= ~self.OOR_COUNT_LIMIT_MASK
        reg_data |= set_count_limit << self.OOR_COUNT_LIMIT_SHIFT

        self._i2c.write_byte(self.address, self.REG_OOR_CONFIG, reg_data)

        # If previous mode is not standbymode return sensor to that previous mode
        # after setting oor iir configuration and count limit
        if (curr_pwr_mode != self.POWER_MODE_STANDBY) and (curr_pwr_mode != self.POWER_MODE_DEEP_STANDBY): 
            self.set_power_mode(curr_pwr_mode)

    def _set_fifo_iir_config(self, set_fifo_iir_t, set_fifo_iir_p):
        """!
        Sets the configuration for IIR of fifo. Not to be used outside of driver.
        """
        curr_pwr_mode = self.get_power_mode()

        # Fifo IIR configuration is writable only during STANDBY mode(as per datasheet)
        if curr_pwr_mode != self.POWER_MODE_STANDBY:
            self.set_power_mode(self.POWER_MODE_STANDBY)
        
        reg_data = self._i2c.read_byte(self.address, self.REG_DSP_CONFIG)

        reg_data &= ~self.SET_FIFO_IIR_TEMP_MASK
        reg_data |= set_fifo_iir_t << self.SET_FIFO_IIR_TEMP_SHIFT
        reg_data &= ~self.SET_FIFO_IIR_PRESS_MASK
        reg_data |= set_fifo_iir_p << self.SET_FIFO_IIR_PRESS_SHIFT

        self._i2c.write_byte(self.address, self.REG_DSP_CONFIG, reg_data)

        # If previous mode is not standbymode return sensor to that previous mode
        # after setting fifo iir configuration
        if (curr_pwr_mode != self.POWER_MODE_STANDBY) and (curr_pwr_mode != self.POWER_MODE_DEEP_STANDBY): 
            self.set_power_mode(curr_pwr_mode)
        
    def _set_fifo_threshold(self, reg_data, fifo):
        """!
        This internal API is used to set fifo threshold based on the frame type selected. Not to be used outside of driver.

        @param reg_data: **list of int** The FIFO configuration register bytes, updated in place
        @param fifo: **FifoConfiguration** The fifo configuration

        @return **int** NO_ERROR on success, ERROR on failure
        """
        if (fifo.frameSel == fifo.FIFO_TEMPERATURE_DATA) or (fifo.frameSel == fifo.FIFO_PRESSURE_DATA):
            if fifo.threshold <= self.FIFO_MAX_THRESHOLD_P_MODE:
                reg_data[0] = (reg_data[0] & ~self.FIFO_THRESHOLD_MASK) | ( fifo.threshold << self.FIFO_THRESHOLD_SHIFT)
            else:
                return self.ERROR

        elif (fifo.frameSel == fifo.FIFO_PRESS_TEMP_DATA):
            if fifo.threshold <= self.FIFO_MAX_THRESHOLD_PT_MODE:
                reg_data[0] = (reg_data[0] & ~self.FIFO_THRESHOLD_MASK) | ( fifo.threshold << self.FIFO_THRESHOLD_SHIFT)
            else:
                return self.ERROR
        
        return self.NO_ERROR

    def _unpack_sensor_data(self, sensor_data, data_index, fifo):
        """!
        This internal API is used to unpack the FIFO data and store it in the sensor_data parameter

        @param sensor_data: **SensorData** The sensor data
        @param data_index: **int** The data index
        @param fifo: **FifoConfiguration** The fifo configuration

        @return  True on success, False on failure/frame empty
        
        """
        res = True 
        if fifo.frameSel == fifo.FIFO_TEMPERATURE_DATA:
            if not ((fifo.data[data_index] == self.FIFO_EMPTY) and (fifo.data[data_index + 1] == self.FIFO_EMPTY) and (fifo.data[data_index + 2] == self.FIFO_EMPTY)):
                raw_data_t = (fifo.data[data_index + 2] << 16) | (fifo.data[data_index + 1] << 8) | fifo.data[data_index]
                
                sensor_data.temperature = raw_data_t / 65536.0
                sensor_data.pressure = 0.0
                data_index += 3
            else:
                data_index = fifo.length
                res = False

        if fifo.frameSel == fifo.FIFO_PRESSURE_DATA:
            if not ((fifo.data[data_index] == self.FIFO_EMPTY) and (fifo.data[data_index + 1] == self.FIFO_EMPTY) and (fifo.data[data_index + 2] == self.FIFO_EMPTY)):
                raw_data_p = (fifo.data[data_index + 2] << 16) | (fifo.data[data_index + 1] << 8) | fifo.data[data_index]
                
                sensor_data.pressure = raw_data_p / 64.0
                sensor_data.temperature = 0.0
                data_index += 3
            else:
                data_index = fifo.length
                res = False

        if fifo.frameSel == fifo.FIFO_PRESS_TEMP_DATA:
            if not ((fifo.data[data_index] == self.FIFO_EMPTY) and (fifo.data[data_index + 1] == self.FIFO_EMPTY) and (fifo.data[data_index + 2] == self.FIFO_EMPTY) \
                and (fifo.data[data_index + 3] == self.FIFO_EMPTY) and (fifo.data[data_index + 4] == self.FIFO_EMPTY) and (fifo.data[data_index + 5] == self.FIFO_EMPTY)):
                raw_data_t = (fifo.data[data_index + 2] << 16) | (fifo.data[data_index + 1] << 8) | fifo.data[data_index]
                raw_data_p = (fifo.data[data_index + 5] << 16) | (fifo.data[data_index + 4] << 8) | fifo.data[data_index + 3]

                sensor_data.temperature = raw_data_t / 65536.0
                sensor_data.pressure = raw_data_p / 64.0
                data_index += 6
            else:
                data_index = fifo.length
                res = False
        
        else:
            sensor_data.pressure = 0.0
            sensor_data.temperature = 0.0
        
        return res

    def _get_nvm_status(self):
        """!
        This API is used to get the status of NVM data. Not to be used outside of driver.
        """
        return self._i2c.read_byte(self.address, self.REG_STATUS)

    def _get_nvm_data(self):
        """!
        This internal API is used to read the nvm data
        """
        nvm_status = self._get_nvm_status()

        if (nvm_status & self.INT_NVM_RDY) and (not(nvm_status & self.INT_NVM_ERR)) and (not(nvm_status & self.INT_NVM_CMD_ERR)):
            nvm_data = self._i2c.read_block(self.address, self.REG_NVM_DATA_LSB, 2)
            return (nvm_data[1] << 8) | nvm_data[0]

        return self.ERROR

    def _set_nvm_addr(self, nvm_addr, prog_en):
        """!
        This internal API is used to set the nvm address and prog_enable based on NVM read/write selected.

        @param nvm_addr: **int** The NVM address to set
        @param prog_en: **int** The program enable

        Allowable values:
            - `ENABLE`
            - `DISABLE`
        """
        nvm_status = self._get_nvm_status()
        
        if nvm_status & self.INT_NVM_RDY:
            reg_data = self._i2c.read_byte(self.address, self.REG_NVM_ADDR)
            reg_data = (reg_data & ~self.NVM_ADDR_MASK) | (nvm_addr << self.NVM_ADDR_SHIFT)
            reg_data &= ~self.NVM_PROG_EN_MASK
            if prog_en == self.ENABLE:
                reg_data |= prog_en << self.NVM_PROG_EN_SHIFT
            
            self._i2c.write_byte(self.address, self.REG_NVM_ADDR, reg_data)

    def _nvm_write_addr(self, nvm_addr, prog_en):
        """!
        This internal API is used to write the nvm data. Not to be used outside of driver.

        @param nvm_addr: **int** The NVM address to write
        @param prog_en: **int** The program enable

        @return  The new power mode
        
        """
        curr_pwr_mode = self.ERROR

        if (nvm_addr >= self.NVM_START_ADDR) and (nvm_addr <= self.NVM_END_ADDR):
            curr_pwr_mode = self.get_power_mode()
            if curr_pwr_mode != self.POWER_MODE_STANDBY:
                self.set_power_mode(self.POWER_MODE_STANDBY)
            self._set_nvm_addr(nvm_addr, prog_en)
        
        return curr_pwr_mode