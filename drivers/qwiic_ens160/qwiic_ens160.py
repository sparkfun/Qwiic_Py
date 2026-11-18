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

__version__ = "3.0.0"

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
    REG_PART_ID = 0x00
    REG_OP_MODE = 0x10
    REG_CONFIG = 0x11
    REG_COMMAND = 0x12
    REG_TEMP_IN = 0x13
    REG_RH_IN = 0x15
    REG_DEVICE_STATUS = 0x20
    REG_DATA_AQI = 0x21
    REG_DATA_TVOC = 0x22
    REG_DATA_ETOH = 0x22 
    REG_DATA_ECO2 = 0x24
    REG_DATA_T = 0x30
    REG_DATA_RH = 0x32
    REG_DATA_MISR = 0x38
    REG_GPR_WRITE_0 = 0x40
    REG_GPR_WRITE_1 = 0x41
    REG_GPR_WRITE_2 = 0x42
    REG_GPR_WRITE_3 = 0x43
    REG_GPR_WRITE_4 = 0x44
    REG_GPR_WRITE_5 = 0x45
    REG_GPR_WRITE_6 = 0x46
    REG_GPR_WRITE_7 = 0x47
    REG_GPR_READ_0 = 0x48
    REG_GPR_READ_1 = 0x49
    REG_GPR_READ_2 = 0x4A
    REG_GPR_READ_3 = 0x4B
    REG_GPR_READ_4 = 0x4C 
    REG_GPR_READ_5 = 0x4D
    REG_GPR_READ_6 = 0x4E
    REG_GPR_READ_7 = 0x4F

    # ENS160 defines and masks
    PART_ID = 0x0160

    # Possible Operating Mode defines/masks
    # Default = 0x00
    OP_MODE_DEEP_SLEEP = 0x00
    OP_MODE_IDLE = 0x01
    OP_MODE_STANDARD = 0x02
    OP_MODE_RESET = 0xF0
    
    # Config defines/masks
    # Default = 0x00
    SHIFT_CONFIG_INT_POL = 6  # INTn pin polarity 0: active low, 1: active high
    SHIFT_CONFIG_INT_CFG = 5  # INTn Pin Drive (INT_CFG) 0: open drain, 1: push/pull
    SHIFT_CONFIG_INT_GPR = 3  # INTn assert on new data in GPR reg (INTGPR)
    SHIFT_CONFIG_INT_DAT = 1  # INTn pin assert on new data in DATA reg (INTDAT)
    SHIFT_CONFIG_INT_EN = 0   # INTn enable
    
    MASK_CONFIG_INT_POL = 0b1 << SHIFT_CONFIG_INT_POL
    MASK_CONFIG_INT_CFG = 0b1 << SHIFT_CONFIG_INT_CFG
    MASK_CONFIG_INT_GPR = 0b1 << SHIFT_CONFIG_INT_GPR
    MASK_CONFIG_INT_DAT = 0b1 << SHIFT_CONFIG_INT_DAT
    MASK_CONFIG_INT_EN = 0b1 << SHIFT_CONFIG_INT_EN

    # Command defines/masks
    # All commands must be issued when device is idle.
    COMMAND_NOP = 0x00
    # Get Firwmware App Version - version is placed in General Purpose Read Registers as follows:
    # GPR_READ04 - Version (Major)
    # GPR_READ05 - Version (Minor)
    # GPR_READ06 - Version (Release)
    COMMAND_GET_APP_VER = 0x0E
    COMMAND_CLEAR_GPR = 0xCC

    # DeviceStatus defines/masks
    SHIFT_DEVICE_STATUS_STAT_AS = 7 # indicates an OPMODE is running
    SHIFT_DEVICE_STATUS_STAT_ER = 6 # indicates an error
    SHIFT_DEVICE_STATUS_VALIDITY_FLAG = 2 # 0: normal, 1: warm-up, 2: initial start-up, 3: invalid
    SHIFT_DEVICE_STATUS_NEW_DAT = 1 # new data available on DATA_x regs
    SHIFT_DEVICE_STATUS_NEW_GPR = 0  # new data available on GPR_READx regs

    MASK_DEVICE_STATUS_STAT_AS = 0b1 << SHIFT_DEVICE_STATUS_STAT_AS
    MASK_DEVICE_STATUS_STAT_ER = 0b1 << SHIFT_DEVICE_STATUS_STAT_ER
    MASK_DEVICE_STATUS_VALIDITY_FLAG = 0b11 << SHIFT_DEVICE_STATUS_VALIDITY_FLAG
    MASK_DEVICE_STATUS_NEW_DAT = 0b1 << SHIFT_DEVICE_STATUS_NEW_DAT
    MASK_DEVICE_STATUS_NEW_GPR = 0b1 << SHIFT_DEVICE_STATUS_NEW_GPR

    VALIDITY_FLAG_NORMAL = 0
    VALIDITY_FLAG_WARM_UP = 1
    VALIDITY_FLAG_START_UP = 2
    VALIDITY_FLAG_INVALID = 3

    # DataAqi defines/masks
    SHIFT_DATA_AQI_UBA = 0 # Air quality index according to UBA

    MASK_DATA_AQI_UBA = 0b11 << SHIFT_DATA_AQI_UBA

    # DataMisr defines/masks
    # Gives calculated checksum of "DATA_" registers
    POLY = 0x1D #  0b00011101 = x^8+x^4+x^3+x^2+x^0 (x^8 is implicit)

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

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        if not self._i2c.is_device_connected(self.address):
            return False

        prodid = self.get_unique_id()

        return prodid == self.PART_ID

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

        @param val: **int** The desired operating mode to set
        """
        if (val > self.OP_MODE_RESET) or (val < self.OP_MODE_DEEP_SLEEP):
            return False
        
        self._i2c.write_byte(self.address, self.REG_OP_MODE, val)

        return True
    
    def get_operating_mode(self):
        """!
        Gets the current operating mode: Deep Sleep (0x00), Idle (0x01), Standard
        (0x02), Reset (0xF0)

        @return **int** The current operating mode
        """
        return self._i2c.read_byte(self.address, self.REG_OP_MODE)
    
    def get_app_ver(self):
        """!
        Retrieves the 24 bit application version of the device

        @return **int** Application version
        """

        old_mode = self.get_operating_mode()
        self.set_operating_mode(self.OP_MODE_IDLE)
        self._i2c.write_byte(self.address, self.REG_COMMAND, self.COMMAND_CLEAR_GPR)
        self._i2c.write_byte(self.address, self.REG_COMMAND, self.COMMAND_GET_APP_VER)

        while not self.check_gpr_status():
            pass

        version_bytes = self._i2c.read_block(self.address, self.REG_GPR_READ_4, 3)

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
        id_bytes = self._i2c.read_block(self.address, self.REG_PART_ID, 2) 

        id = id_bytes[0]
        id |= id_bytes[1] << 8

        return id
    
    def configure_interrupt(self, val):
        """!
        Changes all of the settings within the interrupt configuration register

        @param val: **int** The desired configuration settings.
        """

        self._i2c.write_byte(self.address, self.REG_CONFIG, val)

    def enable_interrupt(self, enable=True):
        """!
        Enables the interrupt.

        @param enable: **bool** Turns on or off the interrupt
        """

        new_config = self._i2c.read_byte(self.address, self.REG_CONFIG)

        new_config &= ~self.MASK_CONFIG_INT_EN

        if enable:
            new_config |= self.MASK_CONFIG_INT_EN

        self._i2c.write_byte(self.address, self.REG_CONFIG, new_config)

    def set_interrupt_polarity(self, active_high = True):
        """!
        Changes the polarity of the interrupt: active high or active low. By default
        this value is set to zero or active low.

        @param active_high: **bool** Changes active state of interrupt from high to low.
        """
        new_config = self._i2c.read_byte(self.address, self.REG_CONFIG)

        new_config &= ~self.MASK_CONFIG_INT_POL

        if active_high:
            new_config |= self.MASK_CONFIG_INT_POL
        
        self._i2c.write_byte(self.address, self.REG_CONFIG, new_config)
    
    def get_interrupt_polarity(self):
        """!
        Retrieves the Retrieves the polarity of the physical interrupt.

        @return **int** Interrupt polarity (0: active low, 1: active high)
        """
        current_config = self._i2c.read_byte(self.address, self.REG_CONFIG)

        int_pol = current_config & self.MASK_CONFIG_INT_POL

        return (int_pol >> self.SHIFT_CONFIG_INT_POL)
    
    def set_interrupt_drive(self, push_pull = True):
        """!
        Changes the pin drive of the interrupt: open drain (default) to push/pull

        @param push_pull: **bool** Changes the drive of the pin.
        """
        new_config = self._i2c.read_byte(self.address, self.REG_CONFIG)
        
        new_config &= ~self.MASK_CONFIG_INT_CFG

        if push_pull:
            new_config |= self.MASK_CONFIG_INT_CFG
        
        self._i2c.write_byte(self.address, self.REG_CONFIG, new_config)

    def set_data_interrupt(self, enable):
        """!
        Routes the data ready signal to the interrupt pin.

        @param enable: **bool** enables or disables data ready on
        """
        new_config = self._i2c.read_byte(self.address, self.REG_CONFIG)
        
        new_config &= ~self.MASK_CONFIG_INT_DAT

        if enable:
            new_config |= self.MASK_CONFIG_INT_DAT
        
        self._i2c.write_byte(self.address, self.REG_CONFIG, new_config)
    
    def set_gpr_interrupt(self, enable):
        """!
        Routes the general purporse read register signal to the interrupt pin.

        @param enable: **bool** whether to turn on or off general purpose read
        """
        new_config = self._i2c.read_byte(self.address, self.REG_CONFIG)

        new_config &= ~self.MASK_CONFIG_INT_GPR

        if enable:
            new_config |= self.MASK_CONFIG_INT_GPR

        self._i2c.write_byte(self.address, self.REG_CONFIG, new_config)
    
    # ////////////////////////////////////////////////////////////////////////////////
    # Temperature and Humidity Compensation
    #

    def set_temp_compensation(self, temp_kelvin):
        """!
        The ENS160 can use temperature data to help give more accurate sensor data.

        @param temp_kelvin: **float** The given temperature in Kelvin
        """
        
        temp_val = [None] * 2
        kelvin_conversion = int(temp_kelvin * 64) # convert value - fixed equation pg. 29 of datasheet
        temp_val[0] = (kelvin_conversion & 0x00FF)
        temp_val[1] = ( (kelvin_conversion & 0xFF00) >> 8)

        self._i2c.write_block(self.address, self.REG_TEMP_IN, temp_val)

    def set_temp_compensation_celsius(self, temp_celsius):
        """!
        The ENS160 can use temperature data to help give more accurate sensor data.

        @param temp_celsius: **float** The given temperature in Celsius
        """

        kelvin_conversion = temp_celsius + 273.15
        self.set_temp_compensation(kelvin_conversion)

    def set_rh_compensation(self, humidity):
        """!
        The ENS160 can use relative Humidiy data to help give more accurate sensor data.

        @param humidity: **float** The given relative humidity
        """
        
        humidity_conversion = int(humidity * 512) # convert value - fixed equation pg. 29 in datasheet.
        
        temp_val = [None] * 2
        temp_val[0] = (humidity_conversion & 0x00FF)
        temp_val[1] = ( (humidity_conversion & 0xFF00) >> 8)

        self._i2c.write_block(self.address, self.REG_RH_IN, temp_val)

    # ////////////////////////////////////////////////////////////////////////////////
    # Device Status
    # 

    def check_data_status(self):
        """!
        This checks the if the NEWDAT bit is high indicating that new data is ready
        to be read. The bit is cleared when data has been read from their registers.

        @return **bool** Whether NEWDAT bit is high
        """

        current_status = self._i2c.read_byte(self.address, self.REG_DEVICE_STATUS)
        
        current_status &= self.MASK_DEVICE_STATUS_NEW_DAT

        if current_status == self.MASK_DEVICE_STATUS_NEW_DAT:
            return True

        return False

    def check_gpr_status(self):
        """!
        This checks the if the NEWGPR bit is high indicating that there is data in
        the general purpose read registers. The bit is cleared the relevant registers
        have been read.

        @return **bool** Whether NEWGPR bit is high
        """
        current_status = self._i2c.read_byte(self.address, self.REG_DEVICE_STATUS)
        
        current_status &= self.MASK_DEVICE_STATUS_NEW_GPR

        if current_status == self.MASK_DEVICE_STATUS_NEW_GPR:
            return True

        return False

    def get_flags(self):
        """!
        This checks the status "flags" of the device (0-3).

        @return **int** The current status flag (0: normal, 1: warm-up, 2: initial start-up, 3: invalid)
        """
        
        current_status = self._i2c.read_byte(self.address, self.REG_DEVICE_STATUS)

        flags = (current_status & self.MASK_DEVICE_STATUS_VALIDITY_FLAG) >> self.SHIFT_DEVICE_STATUS_VALIDITY_FLAG
        
        return flags

    def check_operation_status(self):
        """!
        Checks the bit that indicates if an operation mode is running i.e. the device
        is not off.

        @return **bool** Whether NEWGPR bit is high
        """
        current_status = self._i2c.read_byte(self.address, self.REG_DEVICE_STATUS)
        
        current_status &= self.MASK_DEVICE_STATUS_STAT_AS

        if current_status == self.MASK_DEVICE_STATUS_STAT_AS:
            return True

        return False

    def get_operation_error(self):
        """!
        Checks the bit that indicates if an invalid operating mode has been selected.

        @return **bool** Whether an OpMode error is selected
        """
        current_status = self._i2c.read_byte(self.address, self.REG_DEVICE_STATUS)
        
        current_status &= self.MASK_DEVICE_STATUS_STAT_ER

        if current_status == self.MASK_DEVICE_STATUS_STAT_ER:
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
        current_data_aqi = self._i2c.read_byte(self.address, self.REG_DATA_AQI)
        
        aqi_uba = current_data_aqi & self.MASK_DATA_AQI_UBA

        return (aqi_uba >> self.SHIFT_DATA_AQI_UBA)


    def get_tvoc(self):
        """!
        This reports the Total Volatile Organic Compounds in ppb (parts per billion)

        @return **int** Total Volatile Organic Compounds in ppb
        """
        
        tvoc_bytes = self._i2c.read_block(self.address, self.REG_DATA_TVOC, 2)

        tvoc = tvoc_bytes[0]
        tvoc |= tvoc_bytes[1] << 8

        return tvoc

    def get_etoh(self):
        """!
        This reports the ehtanol concentration in ppb (parts per billion). According
        to the datasheet this is a "virtual mirror" of the ethanol-calibrated TVOC
        register, which is why they share the same register.

        @return **int** Ethanol concentration in ppb
        """
        
        ethanol_bytes = self._i2c.read_block(self.address, self.REG_DATA_ETOH, 2)

        ethanol = ethanol_bytes[0]
        ethanol |= ethanol_bytes[1] << 8

        return ethanol

    def get_eco2(self):
        """!
        This reports the CO2 concentration in ppm (parts per million) based on the
        detected VOCs and hydrogen.

        @return **int** CO2 concentration in ppm
        """
        
        eco_bytes = self._i2c.read_block(self.address, self.REG_DATA_ECO2, 2)

        eco = eco_bytes[0]
        eco |= eco_bytes[1] << 8

        return eco
        
    def get_temp_kelvin(self):
        """!
        This reports the temperature compensation value given to the sensor in
        Kelvin.

        @return **float** Temperature compensation in Kelvin
        """
        
        temp_bytes = self._i2c.read_block(self.address, self.REG_DATA_T, 2)

        temp_conversion = temp_bytes[0]
        temp_conversion |= temp_bytes[1] << 8

        temperature = float(temp_conversion) / 64.0 # Formula as described on pg. 32 of datasheet.

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

        rh_bytes = self._i2c.read_block(self.address, self.REG_DATA_RH, 2)

        rh = rh_bytes[0]
        rh |= rh_bytes[1] << 8

        return rh / 512.0 # Formula as described on pg. 33 of datasheet.
    
    def get_raw_resistance(self):
        """!
        For certain gases the raw resistance values of the hot plates can be 
        used for post processing. More information can be found within the datasheet.

        @return **float** Raw Resistance
        """

        res_bytes = self._i2c.read_block(self.address, self.REG_GPR_READ_6, 2)

        res = res_bytes[0]
        res |= res_bytes[1] << 8

        resistance = 2 ** (res / 2048) # Formula as described on page 13 of datasheet.

        return resistance

