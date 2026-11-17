#-------------------------------------------------------------------------------
# qwiic_lsm6dso.py
#
# Python library for the SparkFun Qwiic 6-DoF LSM6DSO, available here:
# https://www.sparkfun.com/products/18020
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2023
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
# This code was generated in part with ChatGPT, created by OpenAI. The code was
# reviewed and edited by the following human(s):
#
# Dryw Wade
#===============================================================================

"""!
qwiic_lsm6dso
============
Python module for the [SparkFun Qwiic 6-DoF LSM6DSO](https://www.sparkfun.com/products/18020)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_6DoF_LSM6DSO_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic LSM6DSO"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x6B, 0x6A]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicLSM6DSO(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Register addresses
    FUNC_CFG_ACCESS        = 0x01
    LSM6DO_PIN_CTRL        = 0x02
    FIFO_CTRL1             = 0x07
    FIFO_CTRL2             = 0x08
    FIFO_CTRL3             = 0x09
    FIFO_CTRL4             = 0x0A
    COUNTER_BDR_REG1       = 0x0B
    COUNTER_BDR_REG2       = 0x0C
    INT1_CTRL              = 0x0D
    INT2_CTRL              = 0x0E
    WHO_AM_I_REG           = 0x0F
    CTRL1_XL               = 0x10
    CTRL2_G                = 0x11
    CTRL3_C                = 0x12
    CTRL4_C                = 0x13
    CTRL5_C                = 0x14
    CTRL6_C                = 0x15
    CTRL7_G                = 0x16
    CTRL8_XL               = 0x17
    CTRL9_XL               = 0x18
    CTRL10_C               = 0x19
    ALL_INT_SRC            = 0x1A
    WAKE_UP_SRC            = 0x1B
    TAP_SRC                = 0x1C
    D6D_SRC                = 0x1D
    STATUS_REG             = 0x1E
    OUT_TEMP_L             = 0x20
    OUT_TEMP_H             = 0x21
    OUTX_L_G               = 0x22
    OUTX_H_G               = 0x23
    OUTY_L_G               = 0x24
    OUTY_H_G               = 0x25
    OUTZ_L_G               = 0x26
    OUTZ_H_G               = 0x27
    OUTX_L_A               = 0x28
    OUTX_H_A               = 0x29
    OUTY_L_A               = 0x2A
    OUTY_H_A               = 0x2B
    OUTZ_L_A               = 0x2C
    OUTZ_H_A               = 0x2D
    EMB_FUNC_STATUS_MP     = 0x35
    FSM_FUNC_STATUS_A_MP   = 0x36
    FSM_FUNC_STATUS_B_MP   = 0x37
    STATUS_MASTER_MAINPAGE = 0x39
    FIFO_STATUS1           = 0x3A
    FIFO_STATUS2           = 0x3B
    TIMESTAMP0_REG         = 0x40
    TIMESTAMP1_REG         = 0x41
    TIMESTAMP2_REG         = 0x42
    TIMESTAMP3_REG         = 0x43
    TAP_CFG0               = 0x56
    TAP_CFG1               = 0x57
    TAP_CFG2               = 0x58
    TAP_THS_6D             = 0x59
    INT_DUR2               = 0x5A
    WAKE_UP_THS            = 0x5B
    WAKE_UP_DUR            = 0x5C
    FREE_FALL              = 0x5D
    MD1_CFG                = 0x5E
    MD2_CFG                = 0x5F
    I3C_BUS_AVB            = 0x62
    INTERNAL_FREQ_FINE     = 0x63
    INT_OIS                = 0x6F
    CTRL1_OIS              = 0x70
    CTRL2_OIS              = 0x71
    CTRL3_OIS              = 0x72
    X_OFS_USR              = 0x73
    Y_OFS_USR              = 0x74
    Z_OFS_USR              = 0x75
    FIFO_DATA_OUT_TAG      = 0x78
    FIFO_DATA_OUT_X_L      = 0x79
    FIFO_DATA_OUT_X_H      = 0x7A
    FIFO_DATA_OUT_Y_L      = 0x7B
    FIFO_DATA_OUT_Y_H      = 0x7C
    FIFO_DATA_OUT_Z_L      = 0x7D
    FIFO_DATA_OUT_Z_H      = 0x7E

    # Expected Who Am I value
    WHO_AM_I_VALUE = 0x6C
    
    # Software reset value
    SW_RESET_DEVICE = 0x01

    # Accelerometer full scale range values
    FS_XL_2g = 0x00
    FS_XL_16g = 0x01
    FS_XL_4g = 0x02
    FS_XL_8g = 0x03
    FS_XL_MASK = 0xF3
    FS_XL_POS = 2

    # Gyroscope full scale range values
    FS_G_125dps   	= 0x01
    FS_G_250dps 	= 0x00
    FS_G_500dps 	= 0x02
    FS_G_1000dps 	= 0x04
    FS_G_2000dps 	= 0x06
    FS_G_MASK       = 0xF1
    FS_G_POS        = 1

    # Accelerometer and gyroscope output data rate values
    ODR_DISABLE   = 0x00 
    ODR_12_5Hz    = 0x01 # Low Power only
    ODR_26Hz      = 0x02 # Low Power only
    ODR_52Hz      = 0x03 # Low Power only 
    ODR_104Hz     = 0x04 # Normal Mode
    ODR_208Hz     = 0x05 # Normal Mode
    ODR_416Hz     = 0x06 # High performance
    ODR_833Hz     = 0x07 # High Performance 
    ODR_1660Hz    = 0x08 # High Performance
    ODR_3330Hz    = 0x09 # High Performance
    ODR_6660Hz    = 0x0A # High Performance
    ODR_1_6Hz     = 0x0B # Low Power only, and only accelerometer
    ODR_MASK      = 0x0F
    ODR_POS       = 4

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

        # Initialize member variables by resetting them to their default values
        self.reset_member_variables()

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        if not self._i2c.isDeviceConnected(self.address):
            return False
        
        # Check the Who Am I register to see if it's correct
        reg_val = self._i2c.readByte(self.address, self.WHO_AM_I_REG)
        return reg_val == self.WHO_AM_I_VALUE

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        # Reset to clear any previous settings
        self.software_reset()
        
        # Ensure data registers don't change until data has been read
        self.set_block_data_update(True)

        # Both the accelerometer and gyroscope are disabled by default, which is
        # controlled by the ODR value. Because the ranges both default to their
        # minimum values, we'll default the ODR to the minimum value as well.
        self.set_accel_data_rate(self.ODR_12_5Hz)
        self.set_gyro_data_rate(self.ODR_12_5Hz)

        # Done!
        return True

    def reset_member_variables(self):
        """!
        Resets member variables to their default values
        """
        # The accelerometer and gyroscope default to their minimum ranges, which
        # result in these conversion factors
        self.accel_raw_to_g = 0.000061
        self.gyro_raw_to_dps = .004375

    def software_reset(self):
        """!
        Resets the device to its default settings
        """
        self._i2c.writeByte(self.address, self.CTRL3_C, self.SW_RESET_DEVICE)

        # Also reset member variables to reflect change of device settings
        self.reset_member_variables()

    def set_block_data_update(self, enable):
        """!
        Sets whether data registers should only update after both the MSB and
        LSB registers have been read

        @param bool enable: `True` to enable, `False` to disable
        """
        reg_val = self._i2c.readByte(self.address, self.CTRL3_C)
        reg_val &= 0xBF
        reg_val |= enable << 6
        self._i2c.writeByte(self.address, self.CTRL3_C, reg_val)
        
    def get_status_reg(self):
        """!
        Returns the status register value. Bit 0 is accelerometer data ready,
        bit 1 is gyroscope data ready, and bit 2 is temperature data ready

        @return **int** The status register value
        """
        return self._i2c.readByte(self.address, self.STATUS_REG)
        
    def set_accel_range(self, range):
        """!
        Sets the accelerometer full scale range. Can be 2g, 4g, 8g, or 16g

        @param int range: The full scale range to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Ensure provided range is valid
        if range < self.FS_XL_2g or range > self.FS_XL_8g:
            return False

        # Get full scale value, can't have 16g with XL_FS_MODE == 1
        full_scale = self.get_accel_full_scale()
        if full_scale == 1 and range == self.FS_XL_16g:
            return False

        # Get current register value, set new range, write new register value
        reg_val = self._i2c.readByte(self.address, self.CTRL1_XL)
        reg_val &= self.FS_XL_MASK
        reg_val |= range << self.FS_XL_POS
        self._i2c.writeByte(self.address, self.CTRL1_XL, reg_val)

        # Compute raw to G conversion value
        if range == self.FS_XL_2g:
            self.accel_raw_to_g = 0.000061
        elif range == self.FS_XL_4g:
            self.accel_raw_to_g = 0.000122
        elif range == self.FS_XL_8g:
            self.accel_raw_to_g = 0.000244
        elif range == self.FS_XL_16g:
            self.accel_raw_to_g = 0.000488

        # Done!
        return True

    def get_accel_range_raw(self):
        """!
        Returns the accelerometer full scale range, raw register value

        @return **int** The range register's raw value
        """
        # Get current register value and extract range
        reg_val = self._i2c.readByte(self.address, self.CTRL1_XL)
        return (reg_val & (0xFF ^ self.FS_XL_MASK)) >> self.FS_XL_POS

    def get_accel_range_g(self):
        """!
        Returns the accelerometer full scale range in G

        @return **float** The range in G
        """
        # Get current raw range
        range = self.get_accel_range_raw()

        # If XL_FS_MODE == 1 and range is 0x01 (16g), the range is actually 2g
        full_scale = self.get_accel_full_scale()
        if full_scale == 1 and range == self.FS_XL_16g:
            range = self.FS_XL_2g

        # Determine G value based on raw range
        if range == self.FS_XL_2g:
            return 2
        elif range == self.FS_XL_4g:
            return 4
        elif range == self.FS_XL_8g:
            return 8
        return 16

    def set_accel_data_rate(self, rate):
        """!
        Sets the accelerometer output data rate. Can be 1.6Hz, 12.5Hz, 26Hz,
        52Hz, 104Hz, 208Hz, 416Hz, 833Hz, 1660Hz, 3330Hz, 6660Hz, or DISABLE

        @param int rate: The output data rate to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Ensure provided rate is valid
        if rate < self.ODR_DISABLE or rate > self.ODR_1_6Hz:
            return False

        # Get high performance value, can't have 1.6Hz with HP mode enabled
        high_perf = self.get_accel_high_perf()
        if high_perf == 1 and rate == self.ODR_1_6Hz:
            return False

        # Get current register value, set new rate, write new register value
        reg_val = self._i2c.readByte(self.address, self.CTRL1_XL)
        reg_val &= self.ODR_MASK
        reg_val |= rate << self.ODR_POS
        self._i2c.writeByte(self.address, self.CTRL1_XL, reg_val)

        # Done!
        return True

    def get_accel_data_rate_raw(self):
        """!
        Returns the accelerometer output data rate, raw register value

        @return **int** The accelerometer output data rate register's raw value
        """
        # Get current register value and extract range
        reg_val = self._i2c.readByte(self.address, self.CTRL1_XL)
        return (reg_val & (0xFF ^ self.ODR_MASK)) >> self.ODR_POS

    def get_accel_data_rate_odr(self):
        """!
        Returns the accelerometer output data rate in Hz

        @return **float** The output data rate in Hz
        """
        # Get current raw rate
        rate = self.get_accel_data_rate_raw()

        # If HP mode is enabled and rate is 0x0B (1.6Hz), the rate is 12.5Hz
        high_perf = self.get_accel_high_perf()
        if high_perf == 1 and rate == self.ODR_1_6Hz:
            rate = self.ODR_12_5Hz

        # Determine ODR value based on raw rate
        if rate == self.ODR_DISABLE:
            return 0
        elif rate == self.ODR_1_6Hz:
            return 1.6
        elif rate == self.ODR_12_5Hz:
            return 12.5
        elif rate == self.ODR_26Hz:
            return 26
        elif rate == self.ODR_52Hz:
            return 52
        elif rate == self.ODR_104Hz:
            return 104
        elif rate == self.ODR_208Hz:
            return 208
        elif rate == self.ODR_416Hz:
            return 416
        elif rate == self.ODR_833Hz:
            return 833
        elif rate == self.ODR_1660Hz:
            return 1660
        elif rate == self.ODR_3330Hz:
            return 3330
        return 6660

    def set_accel_full_scale(self, enable):
        """!
        Sets the accelerometer full scale mode

        @param bool enable: `True` to enable, `False` to disable
        """
        reg_val = self._i2c.readByte(self.address, self.CTRL8_XL)
        reg_val &= 0xFD
        reg_val |= enable << 1
        self._i2c.writeByte(self.address, self.CTRL8_XL, reg_val)

    def get_accel_full_scale(self):
        """!
        Returns the accelerometer full scale mode

        @return **int** The accelerometer full scale mode
        """
        reg_val = self._i2c.readByte(self.address, self.CTRL8_XL)
        return (reg_val & 0x02) >> 1

    def set_accel_high_perf(self, enable):
        """!
        Sets the accelerometer high performance mode

        @param bool enable: `True` to enable, `False` to disable
        """
        reg_val = self._i2c.readByte(self.address, self.CTRL6_C)
        reg_val &= 0xEF
        reg_val |= enable << 4
        self._i2c.writeByte(self.address, self.CTRL6_C, reg_val)

    def get_accel_high_perf(self):
        """!
        Returns the accelerometer high performance mode

        @return **int** The accelerometer high performance mode
        """
        reg_val = self._i2c.readByte(self.address, self.CTRL6_C)
        return (reg_val & 0x10) >> 4

    def set_gyro_range(self, range):
        """!
        Sets the gyroscope full scale range. Can be 125dps, 250dps, 500dps,
        1000dps, or 2000dps

        @param int range: The full scale range to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Ensure provided range is valid
        if range < self.FS_G_250dps or range > self.FS_G_2000dps:
            return False

        # Get current register value, set new range, write new register value
        reg_val = self._i2c.readByte(self.address, self.CTRL2_G)
        reg_val &= self.FS_G_MASK
        reg_val |= range << self.FS_G_POS
        self._i2c.writeByte(self.address, self.CTRL2_G, reg_val)

        # Compute raw to DPS conversion value
        if range == self.FS_G_125dps:
            self.gyro_raw_to_dps = .004375
        elif range == self.FS_G_250dps:
            self.gyro_raw_to_dps = .00875
        elif range == self.FS_G_500dps:
            self.gyro_raw_to_dps = .0175
        elif range == self.FS_G_1000dps:
            self.gyro_raw_to_dps = .035
        elif range == self.FS_G_2000dps:
            self.gyro_raw_to_dps = .070

        # Done!
        return True

    def get_gyro_range_raw(self):
        """!
        Returns the gyroscope full scale range, raw register value

        @return **int** The range register's raw value
        """
        # Get current register value and extract range
        reg_val = self._i2c.readByte(self.address, self.CTRL2_G)
        return (reg_val & (0xFF ^ self.FS_G_MASK)) >> self.FS_G_POS

    def get_gyro_range_dps(self):
        """!
        Returns the gyroscope full scale range in DPS

        @return **int** The range in DPS
        """
        # Get current raw range
        range = self.get_gyro_range_raw()

        # Determine dps value based on raw range
        if range == self.FS_G_125dps:
            return 125
        elif range == self.FS_G_250dps:
            return 250
        elif range == self.FS_G_500dps:
            return 500
        elif range == self.FS_G_1000dps:
            return 1000
        return 2000

    def set_gyro_data_rate(self, rate):
        """!
        Sets the gyroscope output data rate. Can be 12.5Hz, 26Hz, 52Hz, 104Hz,
        208Hz, 416Hz, 833Hz, 1660Hz, 3330Hz, or 6660Hz

        @param float rate: The output data rate to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Ensure provided rate is valid
        if rate < self.ODR_DISABLE or rate > self.ODR_6660Hz:
            return False

        # Get current register value, set new rate, write new register value
        reg_val = self._i2c.readByte(self.address, self.CTRL2_G)
        reg_val &= self.ODR_MASK
        reg_val |= rate << self.ODR_POS
        self._i2c.writeByte(self.address, self.CTRL2_G, reg_val)

        # Done!
        return True

    def get_gyro_data_rate_raw(self):
        """!
        Returns the gyroscope output data rate, raw register value

        @return **int** The gyroscope output data rate register's raw value
        """
        # Get current register value and extract range
        reg_val = self._i2c.readByte(self.address, self.CTRL2_G)
        return (reg_val & (0xFF ^ self.ODR_MASK)) >> self.ODR_POS

    def get_gyro_data_rate_odr(self):
        """!
        Returns the gyroscope output data rate in Hz

        @return **float** The output data rate in Hz
        """
        # Get current raw rate
        rate = self.get_gyro_data_rate_raw()

        # Determine ODR value based on raw rate
        if rate == self.ODR_DISABLE:
            return 0
        elif rate == self.ODR_12_5Hz:
            return 12.5
        elif rate == self.ODR_26Hz:
            return 26
        elif rate == self.ODR_52Hz:
            return 52
        elif rate == self.ODR_104Hz:
            return 104
        elif rate == self.ODR_208Hz:
            return 208
        elif rate == self.ODR_416Hz:
            return 416
        elif rate == self.ODR_833Hz:
            return 833
        elif rate == self.ODR_1660Hz:
            return 1660
        elif rate == self.ODR_3330Hz:
            return 3330
        return 6660

    def read_raw_accel_x(self):
        """!
        Reads the raw accelerometer X axis value

        @return **int** The raw accelerometer X axis value
        """
        return self._i2c.readWord(self.address, self.OUTX_L_A)

    def read_float_accel_x(self):
        """!
        Reads the accelerometer X axis value in G

        @return **float** The accelerometer X axis value in G
        """
        return self.calc_accel(self.read_raw_accel_x())

    def read_raw_accel_y(self):
        """!
        Reads the raw accelerometer Y axis value

        @return **int** The raw accelerometer Y axis value
        """
        return self._i2c.readWord(self.address, self.OUTY_L_A)

    def read_float_accel_y(self):
        """!
        Reads the accelerometer Y axis value in G

        @return **float** The accelerometer Y axis value in G
        """
        return self.calc_accel(self.read_raw_accel_y())

    def read_raw_accel_z(self):
        """!
        Reads the raw accelerometer Z axis value

        @return **int** The raw accelerometer Z axis value
        """
        return self._i2c.readWord(self.address, self.OUTZ_L_A)

    def read_float_accel_z(self):
        """!
        Reads the accelerometer Z axis value in G

        @return **float** The accelerometer Z axis value in G
        """
        return self.calc_accel(self.read_raw_accel_z())

    def read_raw_accel_all(self):
        """!
        Reads the raw accelerometer X, Y, and Z axis values

        @return **list** The raw accelerometer X, Y, and Z axis values
        """
        return self._i2c.readBlock(self.address, self.OUTX_L_A, 6)

    def read_float_accel_all(self):
        """!
        Reads the accelerometer X, Y, and Z axis values in G

        @return **tuple** The accelerometer X, Y, and Z axis values in G
        """
        raw = self.read_raw_accel_all()
        outputX = self.calc_accel(raw[0] | (raw[1] << 8))
        outputY = self.calc_accel(raw[2] | (raw[3] << 8))
        outputZ = self.calc_accel(raw[4] | (raw[5] << 8))
        return outputX, outputY, outputZ

    def calc_accel(self, input):
        """!
        Calculates the acceleration in G based on the raw input value

        @param int input: The raw input value

        @return **float** The acceleration in G
        """
        # Convert input to signed 16-bit
        if input >= 32768:
            input -= 65536
        return input * self.accel_raw_to_g

    def read_raw_gyro_x(self):
        """!
        Reads the raw gyroscope X axis value

        @return **int** The raw gyroscope X axis value
        """
        return self._i2c.readWord(self.address, self.OUTX_L_G)

    def read_float_gyro_x(self):
        """!
        Reads the gyroscope X axis value in degrees per second

        @return **float** The gyroscope X axis value in degrees per second
        """
        return self.calc_gyro(self.read_raw_gyro_x())

    def read_raw_gyro_y(self):
        """!
        Reads the raw gyroscope Y axis value

        @return **int** The raw gyroscope Y axis value
        """
        return self._i2c.readWord(self.address, self.OUTY_L_G)

    def read_float_gyro_y(self):
        """!
        Reads the gyroscope Y axis value in degrees per second

        @return **float** The gyroscope Y axis value in degrees per second
        """
        return self.calc_gyro(self.read_raw_gyro_y())

    def read_raw_gyro_z(self):
        """!
        Reads the raw gyroscope Z axis value

        @return **int** The raw gyroscope Z axis value
        """
        return self._i2c.readWord(self.address, self.OUTZ_L_G)

    def read_float_gyro_z(self):
        """!
        Reads the gyroscope Z axis value in degrees per second

        @return **float** The gyroscope Z axis value in degrees per second
        """
        return self.calc_gyro(self.read_raw_gyro_z())

    def read_raw_gyro_all(self):
        """!
        Reads the raw gyroscope X, Y, and Z axis values

        @return **list** The raw gyroscope X, Y, and Z axis values
        """
        return self._i2c.readBlock(self.address, self.OUTX_L_G, 6)

    def read_float_gyro_all(self):
        """!
        Reads the gyroscope X, Y, and Z axis values in degrees per second

        @return **tuple** The gyroscope X, Y, and Z axis values in degrees per second
        """
        raw = self.read_raw_gyro_all()
        outputX = self.calc_gyro(raw[0] | (raw[1] << 8))
        outputY = self.calc_gyro(raw[2] | (raw[3] << 8))
        outputZ = self.calc_gyro(raw[4] | (raw[5] << 8))
        return outputX, outputY, outputZ

    def calc_gyro(self, input):
        """!
        Calculates the angular velocity in degrees per second based on the raw
        input value

        @param int input: The raw input value

        @return **float** The angular velocity in degrees per second
        """
        # Convert input to signed 16-bit
        if input >= 32768:
            input -= 65536
        return input * self.gyro_raw_to_dps

    def read_raw_accel_gyro_all(self):
        """!
        Reads the raw accelerometer and gyroscope X, Y, and Z axis values

        @return **list** The raw accelerometer and gyroscope X, Y, and Z axis values
        """
        return self._i2c.readBlock(self.address, self.OUTX_L_G, 12)

    def read_float_accel_gyro_all(self):
        """!
        Reads the accelerometer and gyroscope X, Y, and Z axis values in G and
        degrees per second

        @return **tuple** The accelerometer and gyroscope X, Y, and Z axis values in G
            and degrees per second
        """
        raw = self.read_raw_accel_gyro_all()
        gyrX = self.calc_gyro(raw[0] | (raw[1] << 8))
        gyrY = self.calc_gyro(raw[2] | (raw[3] << 8))
        gyrZ = self.calc_gyro(raw[4] | (raw[5] << 8))
        accX = self.calc_accel(raw[6] | (raw[7] << 8))
        accY = self.calc_accel(raw[8] | (raw[9] << 8))
        accZ = self.calc_accel(raw[10] | (raw[11] << 8))
        return accX, accY, accZ, gyrX, gyrY, gyrZ

    def read_raw_temp(self):
        """!
        Reads the raw temperature value

        @return **int** The raw temperature value
        """
        return self._i2c.readWord(self.address, self.OUT_TEMP_L)

    def read_temp_c(self):
        """!
        Reads the temperature value in degrees Celsius

        @return **float** The temperature value in degrees Celsius
        """
        temp = self.read_raw_temp()
        msb_temp = (temp & 0xFF00) >> 8
        temp_float = float(msb_temp)
        lsb_temp = temp & 0x00FF
        lsb_temp /= 256
        temp_float += lsb_temp
        temp_float += 25  # Add 25 degrees to remove offset
        return temp_float

    def read_temp_f(self):
        """!
        Reads the temperature value in degrees Fahrenheit

        @return **float** The temperature value in degrees Fahrenheit
        """
        return (self.read_temp_c() * 9) / 5 + 32
