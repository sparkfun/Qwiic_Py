#-------------------------------------------------------------------------------
# qwiic_ism330dhcx.py
#
# Python library for the SparkFun Qwiic ISM330DHCX, available here:
# https://www.sparkfun.com/products/19764
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
qwiic_ism330dhcx
============
Python module for the [SparkFun Qwiic ISM330DHCX](https://www.sparkfun.com/products/19764)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_6DoF_ISM330DHCX_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic ISM330DHCX"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x6B, 0x6A]

class ISMData:
    # Contains 3 axis data for storing either raw or calculated data from the ISM330DHCX
    def __init__(self):
        self.x_data = 0
        self.y_data = 0
        self.z_data = 0

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicISM330DHCX(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Device identification
    DEV_ID = 0x6B
    REG_WHO_AM_I = 0x0F

    # Ctrl1 XL register
    REG_CTRL1_XL = 0x10

    CTRL1_XL_SHIFT_ODR = 4
    CTRL1_XL_MASK_ODR = 0b1111 << CTRL1_XL_SHIFT_ODR
    CTRL1_XL_SHIFT_FS = 2
    CTRL1_XL_MASK_FS = 0b11 << CTRL1_XL_SHIFT_FS
    CTRL1_XL_SHIFT_LPF2_XL_EN = 1
    CTRL1_XL_MASK_LPF2_XL_EN = 0b1 << CTRL1_XL_SHIFT_LPF2_XL_EN

    XL_FS_2G = 0
    XL_FS_16G = 1
    XL_FS_4G = 2
    XL_FS_8G = 3
    
    # Ctrl2 G register
    REG_CTRL2_G = 0x11
    CTRL2_G_SHIFT_ODR = 4
    CTRL2_G_MASK_ODR = 0b1111 << CTRL2_G_SHIFT_ODR
    CTRL2_G_SHIFT_FS = 0
    CTRL2_G_MASK_FS = 0b1111 << CTRL2_G_SHIFT_FS

    GYRO_FS_125DPS = 2
    GYRO_FS_250DPS = 0
    GYRO_FS_500DPS = 4
    GYRO_FS_1000DPS = 8
    GYRO_FS_2000DPS = 12
    GYRO_FS_4000DPS = 1

    # Temperature register
    REG_OUT_TEMP_L = 0x20
    
    # Accelerometer and Gyro output registers
    REG_OUT_XLA = 0x28
    REG_OUT_XLG = 0x22

    # Configuration regs
    REG_FUNC_CFG_ACCESS = 0x01
    FUNC_CFG_ACCESS_SHIFT_REG_ACCESS = 6
    FUNC_CFG_ACCESS_MASK_REG_ACCESS = 0b11 << FUNC_CFG_ACCESS_SHIFT_REG_ACCESS

    REG_CTRL9_XL = 0x18
    CTRL9_XL_SHIFT_DEN_X = 7
    CTRL9_XL_MASK_DEN_X = 0b1 << CTRL9_XL_SHIFT_DEN_X
    CTRL9_XL_SHIFT_DEN_Y = 6
    CTRL9_XL_MASK_DEN_Y = 0b1 << CTRL9_XL_SHIFT_DEN_Y
    CTRL9_XL_SHIFT_DEN_Z = 5
    CTRL9_XL_MASK_DEN_Z = 0b1 << CTRL9_XL_SHIFT_DEN_Z
    CTRL9_XL_SHIFT_DEN_XL_G = 3
    CTRL9_XL_MASK_DEN_XL_G = 0b11 << CTRL9_XL_SHIFT_DEN_XL_G
    CTRL9_XL_SHIFT_DEN_LH = 2
    CTRL9_XL_MASK_DEN_LH = 0b1 << CTRL9_XL_SHIFT_DEN_LH
    CTRL9_XL_SHIFT_DEVICE_CONF = 1
    CTRL9_XL_MASK_DEVICE_CONF = 0b1 << CTRL9_XL_SHIFT_DEVICE_CONF

    REG_CTRL3_C = 0x12
    CTRL3_C_SHIFT_BOOT = 7
    CTRL3_C_MASK_BOOT = 0b1 << CTRL3_C_SHIFT_BOOT
    CTRL3_C_SHIFT_BDU = 6
    CTRL3_C_MASK_BDU = 0b1 << CTRL3_C_SHIFT_BDU
    CTRL3_C_SHIFT_HL_ACTIVE = 5
    CTRL3_C_MASK_HL_ACTIVE = 0b1 << CTRL3_C_SHIFT_HL_ACTIVE
    CTRL3_C_SHIFT_PP_OD = 4
    CTRL3_C_MASK_PP_OD = 0b1 << CTRL3_C_SHIFT_PP_OD
    CTRL3_C_SHIFT_SIM = 3
    CTRL3_C_MASK_SIM = 0b1 << CTRL3_C_SHIFT_SIM
    CTRL3_C_SHIFT_IF_INC = 2
    CTRL3_C_MASK_IF_INC = 0b1 << CTRL3_C_SHIFT_IF_INC
    CTRL3_C_SHIFT_SW_RESET = 0
    CTRL3_C_MASK_SW_RESET = 0b1 << CTRL3_C_SHIFT_SW_RESET

    REG_CTRL4_C = 0x13
    CTRL4_C_SHIFT_SLEEP_G = 6
    CTRL4_C_MASK_SLEEP_G = 0b1 << CTRL4_C_SHIFT_SLEEP_G
    CTRL4_C_SHIFT_INT2_ON_INT1 = 5
    CTRL4_C_MASK_INT2_ON_INT1 = 0b1 << CTRL4_C_SHIFT_INT2_ON_INT1
    CTRL4_C_SHIFT_DRDY_MASK = 3
    CTRL4_C_MASK_DRDY_MASK = 0b1 << CTRL4_C_SHIFT_DRDY_MASK
    CTRL4_C_SHIFT_I2C_DISABLE = 2
    CTRL4_C_MASK_I2C_DISABLE = 0b1 << CTRL4_C_SHIFT_I2C_DISABLE
    CTRL4_C_SHIFT_LPF1_SEL_G = 1
    CTRL4_C_MASK_LPF1_SEL_G = 0b1 << CTRL4_C_SHIFT_LPF1_SEL_G

    REG_CTRL6_C = 0x15
    CTRL6_C_SHIFT_DEN_MODE = 5
    CTRL6_C_MASK_DEN_MODE = 0b111 << CTRL6_C_SHIFT_DEN_MODE
    CTRL6_C_SHIFT_XL_HM_MODE = 4
    CTRL6_C_MASK_XL_HM_MODE = 0b1 << CTRL6_C_SHIFT_XL_HM_MODE
    CTRL6_C_SHIFT_USR_OFF_W = 3
    CTRL6_C_MASK_USR_OFF_W = 0b1 << CTRL6_C_SHIFT_USR_OFF_W
    CTRL6_C_SHIFT_FTYPE = 0
    CTRL6_C_MASK_FTYPE = 0b111 << CTRL6_C_SHIFT_FTYPE

    REG_CTRL10_C = 0x19
    CTRL10_C_SHIFT_TIMESTAMP_EN = 2
    CTRL10_C_MASK_TIMESTAMP_EN = 0b1 << CTRL10_C_SHIFT_TIMESTAMP_EN

    REG_TIMESTAMP0 = 0x40
    REG_TIMESTAMP1 = 0x41
    REG_TIMESTAMP2 = 0x42
    REG_TIMESTAMP3 = 0x43

    # Slope Filtering
    REG_CTRL8_XL = 0x17
    CTRL8_XL_SHIFT_HPCF_XL = 5
    CTRL8_XL_MASK_HPCF_XL = 0b111 << CTRL8_XL_SHIFT_HPCF_XL
    CTRL8_XL_SHIFT_HP_REF_MODE_XL = 4
    CTRL8_XL_MASK_HP_REF_MODE_XL = 0b1 << CTRL8_XL_SHIFT_HP_REF_MODE_XL
    CTRL8_XL_SHIFT_FAST_SETTL_MODE_XL = 3
    CTRL8_XL_MASK_FAST_SETTL_MODE_XL = 0b1 << CTRL8_XL_SHIFT_FAST_SETTL_MODE_XL
    CTRL8_XL_SHIFT_HP_SLOPE_XL_EN = 2
    CTRL8_XL_MASK_HP_SLOPE_XL_EN = 0b1 << CTRL8_XL_SHIFT_HP_SLOPE_XL_EN
    CTRL8_XL_SHIFT_LOW_PASS_ON_6D = 0
    CTRL8_XL_MASK_LOW_PASS_ON_6D = 0b1 << CTRL8_XL_SHIFT_LOW_PASS_ON_6D

    # Possilbe Slope Filters
    HP_PATH_DISABLE_ON_OUT = 0x00
    SLOPE_ODR_DIV4 = 0x10
    HP_ODR_DIV10 = 0x11
    HP_ODR_DIV20 = 0x12
    HP_ODR_DIV45 = 0x13
    HP_ODR_DIV100 = 0x14
    HP_ODR_DIV200 = 0x15
    HP_ODR_DIV400 = 0x16
    HP_ODR_DIV800 = 0x17
    HP_REF_MD_ODR_DIV10 = 0x31
    HP_REF_MD_ODR_DIV20 = 0x32
    HP_REF_MD_ODR_DIV45 = 0x33
    HP_REF_MD_ODR_DIV100 = 0x34
    HP_REF_MD_ODR_DIV200 = 0x35
    HP_REF_MD_ODR_DIV400 = 0x36
    HP_REF_MD_ODR_DIV800 = 0x37
    LP_ODR_DIV10 = 0x01
    LP_ODR_DIV20 = 0x02
    LP_ODR_DIV45 = 0x03
    LP_ODR_DIV100 = 0x04
    LP_ODR_DIV200 = 0x05
    LP_ODR_DIV400 = 0x06
    LP_ODR_DIV800 = 0x07

    # Possible bandwidths
    BW_ULTRA_LIGHT = 0
    BW_VERY_LIGHT = 1
    BW_LIGHT = 2
    BW_MEDIUM = 3
    BW_STRONG = 4
    BW_VERY_STRONG = 5
    BW_AGGRESSIVE = 6
    BW_XTREME = 7

    # Possible data rates (ODRs)
    # Accelerometer
    XL_ODR_OFF    = 0
    XL_ODR_12_5HZ  = 1
    XL_ODR_26HZ   = 2
    XL_ODR_52HZ   = 3
    XL_ODR_104HZ  = 4
    XL_ODR_208HZ  = 5
    XL_ODR_416HZ  = 6
    XL_ODR_833HZ  = 7
    XL_ODR_1666HZ = 8
    XL_ODR_3332HZ = 9
    XL_ODR_6667HZ = 10
    XL_ODR_1_6HZ   = 11
    
    # Gyroscope
    GYRO_ODR_OFF    = 0
    GYRO_ODR_12_5HZ  = 1
    GYRO_ODR_26HZ   = 2
    GYRO_ODR_52HZ   = 3
    GYRO_ODR_104HZ  = 4
    GYRO_ODR_208HZ  = 5
    GYRO_ODR_416HZ  = 6
    GYRO_ODR_833HZ  = 7
    GYRO_ODR_1666HZ = 8
    GYRO_ODR_3332HZ = 9
    GYRO_ODR_6667HZ = 10

    # MLC
    MLC_ODR_12_5HZ = 0
    MLC_ODR_26HZ  = 1
    MLC_ODR_52HZ  = 2
    MLC_ODR_104HZ = 3

    # Sensor Hub
    SH_ODR_104HZ = 0
    SH_ODR_52HZ  = 1
    SH_ODR_26HZ  = 2
    SH_ODR_13HZ  = 3

    # Possible mem bank values
    USER_BANK = 0
    SENSOR_HUB_BANK = 1
    EMBEDDED_FUNC_BANK = 2

    REG_EMB_FUNC_ODR_CFG_B = 0x5F
    EMB_FUNC_ODR_SHIFT_FSM_ODR = 3
    EMB_FUNC_ODR_MASK_FSM_ODR = 0b11 << EMB_FUNC_ODR_SHIFT_FSM_ODR

    ODR_FSM_12_5HZ = 0
    ODR_FSM_26HZ  = 1
    ODR_FSM_52HZ  = 2
    ODR_FSM_104HZ = 3

    REG_EMB_FUNC_EN_B = 0x05
    EMB_FUNC_EN_B_SHIFT_MLC_EN = 4
    EMB_FUNC_EN_B_MASK_MLC_EN = 0b1 << EMB_FUNC_EN_B_SHIFT_MLC_EN
    EMB_FUNC_EN_B_SHIFT_FIFO_COMPR_EN = 3
    EMB_FUNC_EN_B_MASK_FIFO_COMPR_EN = 0b1 << EMB_FUNC_EN_B_SHIFT_FIFO_COMPR_EN
    EMB_FUNC_EN_B_SHIFT_FSM_EN = 0
    EMB_FUNC_EN_B_MASK_FSM_EN = 0b1 << EMB_FUNC_EN_B_SHIFT_FSM_EN

    REG_EMB_FUNC_ODR_CFG_C = 0x60
    EMB_FUNC_ODR_SHIFT_MLC_ODR = 2
    EMB_FUNC_ODR_MASK_MLC_ODR = 0b11 << EMB_FUNC_ODR_SHIFT_MLC_ODR

    # Fifo Registers
    REG_FIFO_CTRL1 = 0x07

    REG_FIFO_CTRL2 = 0x08
    FIFO_CTRL2_SHIFT_STOP_ON_WTM = 7
    FIFO_CTRL2_MASK_STOP_ON_WTM = 0b1 << FIFO_CTRL2_SHIFT_STOP_ON_WTM
    FIFO_CTRL2_SHIFT_FIFO_COMPR_RT_EN = 6
    FIFO_CTRL2_MASK_FIFO_COMPR_RT_EN = 0b1 << FIFO_CTRL2_SHIFT_FIFO_COMPR_RT_EN
    FIFO_CTRL2_SHIFT_ODR_CHG_EN = 4
    FIFO_CTRL2_MASK_ODR_CHG_EN = 0b1 << FIFO_CTRL2_SHIFT_ODR_CHG_EN
    FIFO_CTRL2_SHIFT_UNCOPTR_RATE = 1
    FIFO_CTRL2_MASK_UNCOPTR_RATE = 0b11 << FIFO_CTRL2_SHIFT_UNCOPTR_RATE
    FIFO_CTRL2_SHIFT_WTM = 0
    FIFO_CTRL2_MASK_WTM = 0b1 << FIFO_CTRL2_SHIFT_WTM

    REG_FIFO_CTRL3 = 0x09
    FIFO_CTRL3_SHIFT_BDR_GY = 4
    FIFO_CTRL3_MASK_BDR_GY = 0b1111 << FIFO_CTRL3_SHIFT_BDR_GY
    FIFO_CTRL3_SHIFT_BDR_XL = 0
    FIFO_CTRL3_MASK_BDR_XL = 0b1111 << FIFO_CTRL3_SHIFT_BDR_XL

    REG_FIFO_CTRL4 = 0x0A
    FIFO_CTRL4_SHIFT_ODR_TS_BATCH = 6
    FIFO_CTRL4_MASK_ODR_TS_BATCH = 0b11 << FIFO_CTRL4_SHIFT_ODR_TS_BATCH
    FIFO_CTRL4_SHIFT_ODR_T_BATCH = 4
    FIFO_CTRL4_MASK_ODR_T_BATCH = 0b11 << FIFO_CTRL4_SHIFT_ODR_T_BATCH
    FIFO_CTRL4_SHIFT_FIFO_MODE = 0
    FIFO_CTRL4_MASK_FIFO_MODE = 0b111 << FIFO_CTRL4_SHIFT_FIFO_MODE


    # Possible Fifo Modes
    BYPASS_MODE = 0
    FIFO_MODE = 1
    STREAM_TO_FIFO_MODE = 3
    BYPASS_TO_STREAM_MODE = 4
    STREAM_MODE = 6
    BYPASS_TO_FIFO_MODE = 7

    # Possible Accelerometer Batch Data Rates
    XL_NOT_BATCHED = 0
    XL_BATCHED_AT_12_5HZ = 1
    XL_BATCHED_AT_26HZ = 2
    XL_BATCHED_AT_52HZ = 3
    XL_BATCHED_AT_104HZ = 4
    XL_BATCHED_AT_208HZ = 5
    XL_BATCHED_AT_417HZ = 6
    XL_BATCHED_AT_833HZ = 7
    XL_BATCHED_AT_1667HZ = 8
    XL_BATCHED_AT_3333HZ = 9
    XL_BATCHED_AT_6667HZ = 10
    XL_BATCHED_AT_6_5HZ = 11

    # Possible Gyroscope Batch Data Rates
    GYRO_NOT_BATCHED = 0
    GYRO_BATCHED_AT_12_5HZ = 1
    GYRO_BATCHED_AT_26HZ = 2
    GYRO_BATCHED_AT_52HZ = 3
    GYRO_BATCHED_AT_104HZ = 4
    GYRO_BATCHED_AT_208HZ = 5
    GYRO_BATCHED_AT_417HZ = 6
    GYRO_BATCHED_AT_833HZ = 7
    GYRO_BATCHED_AT_1667HZ = 8
    GYRO_BATCHED_AT_3333HZ = 9
    GYRO_BATCHED_AT_6667HZ = 10
    GYRO_BATCHED_AT_6_5HZ = 11

    # Possible Decimation Rates
    NO_DECIMATION = 0
    DEC1 = 1
    DEC8 = 2
    DEC32 = 3

    # Possible Interrupt Events
    ALL_INT_PULSED = 0
    BASE_LATCHED_EMB_PULSED = 1
    BASE_PULSED_EMB_LATCHED = 2
    ALL_INT_LATCHED = 3

    # Interrupt configuration
    REG_TAP_CFG0 = 0x56
    TAP_CFG0_SHIFT_INT_CLR_ON_READ = 6
    TAP_CFG0_MASK_INT_CLR_ON_READ = 0b1 << TAP_CFG0_SHIFT_INT_CLR_ON_READ
    TAP_CFG0_SHIFT_SLEEP_STATUS_ON_INT = 5
    TAP_CFG0_MASK_SLEEP_STATUS_ON_INT = 0b1 << TAP_CFG0_SHIFT_SLEEP_STATUS_ON_INT
    TAP_CFG0_SHIFT_SLOPE_FDS = 4
    TAP_CFG0_MASK_SLOPE_FDS = 0b1 << TAP_CFG0_SHIFT_SLOPE_FDS
    TAP_CFG0_SHIFT_TAP_X_EN = 3
    TAP_CFG0_MASK_TAP_X_EN = 0b1 << TAP_CFG0_SHIFT_TAP_X_EN
    TAP_CFG0_SHIFT_TAP_Y_EN = 2
    TAP_CFG0_MASK_TAP_Y_EN = 0b1 << TAP_CFG0_SHIFT_TAP_Y_EN
    TAP_CFG0_SHIFT_TAP_Z_EN = 1
    TAP_CFG0_MASK_TAP_Z_EN = 0b1 << TAP_CFG0_SHIFT_TAP_Z_EN
    TAP_CFG0_SHIFT_LIR = 0
    TAP_CFG0_MASK_LIR = 0b1 << TAP_CFG0_SHIFT_LIR

    REG_TAP_CFG2 = 0x58
    TAP_CFG2_SHIFT_INTERRUPTS_ENABLE = 7
    TAP_CFG2_MASK_INTERRUPTS_ENABLE = 0b1 << TAP_CFG2_SHIFT_INTERRUPTS_ENABLE
    TAP_CFG2_SHIFT_INACT_EN = 5
    TAP_CFG2_MASK_INACT_EN = 0b11 << TAP_CFG2_SHIFT_INACT_EN
    TAP_CFG2_SHIFT_TAP_THS_Y = 0
    TAP_CFG2_MASK_TAP_THS_Y = 0b11111 << TAP_CFG2_SHIFT_TAP_THS_Y

    REG_PAGE_RW = 0x17
    PAGE_RW_SHIFT_EMB_FUNC_LIR = 7
    PAGE_RW_MASK_EMB_FUNC_LIR = 0b1 << PAGE_RW_SHIFT_EMB_FUNC_LIR
    PAGE_RW_SHIFT_PAGE_RW = 5
    PAGE_RW_MASK_PAGE_RW = 0b11 << PAGE_RW_SHIFT_PAGE_RW

    REG_MLC_INT1 = 0x0D

    REG_EMB_FUNC_INT1 = 0x0A
    EMB_FUNC_INT1_SHIFT_FSM_LC = 7
    EMB_FUNC_INT1_MASK_FSM_LC = 0b1 << EMB_FUNC_INT1_SHIFT_FSM_LC
    EMB_FUNC_INT1_SHIFT_SIG_MOT = 5
    EMB_FUNC_INT1_MASK_SIG_MOT = 0b1 << EMB_FUNC_INT1_SHIFT_SIG_MOT
    EMB_FUNC_INT1_SHIFT_TILT = 4
    EMB_FUNC_INT1_MASK_TILT = 0b1 << EMB_FUNC_INT1_SHIFT_TILT
    EMB_FUNC_INT1_SHIFT_STEP_DETECTOR = 3
    EMB_FUNC_INT1_MASK_STEP_DETECTOR = 0b1 << EMB_FUNC_INT1_SHIFT_STEP_DETECTOR
    
    REG_FSM_ENABLE_A = 0x46
    REG_FSM_ENABLE_B = 0x47

    REG_FSM_INT1_A = 0x0B
    REG_FSM_INT1_B = 0x0C

    REG_INT1_CTRL = 0x0D
    INT1_CTRL_SHIFT_DEN_DRDY_FLAG = 7
    INT1_CTRL_MASK_DEN_DRDY_FLAG = 0b1 << INT1_CTRL_SHIFT_DEN_DRDY_FLAG
    INT1_CTRL_SHIFT_INT1_CNT_BDR = 6
    INT1_CTRL_MASK_INT1_CNT_BDR = 0b1 << INT1_CTRL_SHIFT_INT1_CNT_BDR
    INT1_CTRL_SHIFT_INT1_FIFO_FULL = 5
    INT1_CTRL_MASK_INT1_FIFO_FULL = 0b1 << INT1_CTRL_SHIFT_INT1_FIFO_FULL
    INT1_CTRL_SHIFT_INT1_FIFO_OVR = 4
    INT1_CTRL_MASK_INT1_FIFO_OVR = 0b1 << INT1_CTRL_SHIFT_INT1_FIFO_OVR
    INT1_CTRL_SHIFT_INT1_FIFO_TH = 3
    INT1_CTRL_MASK_INT1_FIFO_TH = 0b1 << INT1_CTRL_SHIFT_INT1_FIFO_TH
    INT1_CTRL_SHIFT_INT1_BOOT = 2
    INT1_CTRL_MASK_INT1_BOOT = 0b1 << INT1_CTRL_SHIFT_INT1_BOOT
    INT1_CTRL_SHIFT_INT1_DRDY_G = 1
    INT1_CTRL_MASK_INT1_DRDY_G = 0b1 << INT1_CTRL_SHIFT_INT1_DRDY_G
    INT1_CTRL_SHIFT_INT1_DRDY_XL = 0
    INT1_CTRL_MASK_INT1_DRDY_XL = 0b1 << INT1_CTRL_SHIFT_INT1_DRDY_XL

    REG_MD1_CFG = 0x5E
    MD1_CFG_SHIFT_INT1_SLEEP_CHANGE = 7
    MD1_CFG_MASK_INT1_SLEEP_CHANGE = 0b1 << MD1_CFG_SHIFT_INT1_SLEEP_CHANGE
    MD1_CFG_SHIFT_INT1_SINGLE_TAP = 6
    MD1_CFG_MASK_INT1_SINGLE_TAP = 0b1 << MD1_CFG_SHIFT_INT1_SINGLE_TAP
    MD1_CFG_SHIFT_INT1_WU = 5
    MD1_CFG_MASK_INT1_WU = 0b1 << MD1_CFG_SHIFT_INT1_WU
    MD1_CFG_SHIFT_INT1_FF = 4
    MD1_CFG_MASK_INT1_FF = 0b1 << MD1_CFG_SHIFT_INT1_FF
    MD1_CFG_SHIFT_INT1_DOUBLE_TAP = 3
    MD1_CFG_MASK_INT1_DOUBLE_TAP = 0b1 << MD1_CFG_SHIFT_INT1_DOUBLE_TAP
    MD1_CFG_SHIFT_INT1_6D = 2
    MD1_CFG_MASK_INT1_6D = 0b1 << MD1_CFG_SHIFT_INT1_6D
    MD1_CFG_SHIFT_INT1_EMB_FUNC = 1
    MD1_CFG_MASK_INT1_EMB_FUNC = 0b1 << MD1_CFG_SHIFT_INT1_EMB_FUNC
    MD1_CFG_SHIFT_INT1_SHUB = 0
    MD1_CFG_MASK_INT1_SHUB = 0b1 << MD1_CFG_SHIFT_INT1_SHUB

    REG_EMB_FUN_INT2 = 0x0E
    EMB_FUNC_INT2_SHIFT_FSM_LC = 7
    EMB_FUNC_INT2_MASK_FSM_LC = 0b1 << EMB_FUNC_INT2_SHIFT_FSM_LC
    EMB_FUNC_INT2_SHIFT_SIG_MOT = 5
    EMB_FUNC_INT2_MASK_SIG_MOT = 0b1 << EMB_FUNC_INT2_SHIFT_SIG_MOT
    EMB_FUNC_INT2_SHIFT_TILT = 4
    EMB_FUNC_INT2_MASK_TILT = 0b1 << EMB_FUNC_INT2_SHIFT_TILT
    EMB_FUNC_INT2_SHIFT_STEP_DETECTOR = 3
    EMB_FUNC_INT2_MASK_STEP_DETECTOR = 0b1 << EMB_FUNC_INT2_SHIFT_STEP_DETECTOR

    REG_FSM_INT2_A = 0x0F
    REG_FSM_INT2_B = 0x10
    REG_MLC_INT2 = 0x11

    REG_INT2_CTRL = 0x0E
    INT2_CTRL_SHIFT_INT2_CNT_BDR = 6
    INT2_CTRL_MASK_INT2_CNT_BDR = 0b1 << INT2_CTRL_SHIFT_INT2_CNT_BDR
    INT2_CTRL_SHIFT_INT2_FIFO_FULL = 5
    INT2_CTRL_MASK_INT2_FIFO_FULL = 0b1 << INT2_CTRL_SHIFT_INT2_FIFO_FULL
    INT2_CTRL_SHIFT_INT2_FIFO_OVR = 4
    INT2_CTRL_MASK_INT2_FIFO_OVR = 0b1 << INT2_CTRL_SHIFT_INT2_FIFO_OVR
    INT2_CTRL_SHIFT_INT2_FIFO_TH = 3
    INT2_CTRL_MASK_INT2_FIFO_TH = 0b1 << INT2_CTRL_SHIFT_INT2_FIFO_TH
    INT2_CTRL_SHIFT_INT2_DRDY_TEMP = 2
    INT2_CTRL_MASK_INT2_DRDY_TEMP = 0b1 << INT2_CTRL_SHIFT_INT2_DRDY_TEMP
    INT2_CTRL_SHIFT_INT2_DRDY_G = 1
    INT2_CTRL_MASK_INT2_DRDY_G = 0b1 << INT2_CTRL_SHIFT_INT2_DRDY_G
    INT2_CTRL_SHIFT_INT2_DRDY_XL = 0
    INT2_CTRL_MASK_INT2_DRDY_XL = 0b1 << INT2_CTRL_SHIFT_INT2_DRDY_XL

    REG_MD2_CFG = 0x5F
    MD2_CFG_SHIFT_INT2_SLEEP_CHANGE = 7
    MD2_CFG_MASK_INT2_SLEEP_CHANGE = 0b1 << MD2_CFG_SHIFT_INT2_SLEEP_CHANGE
    MD2_CFG_SHIFT_INT2_SINGLE_TAP = 6
    MD2_CFG_MASK_INT2_SINGLE_TAP = 0b1 << MD2_CFG_SHIFT_INT2_SINGLE_TAP
    MD2_CFG_SHIFT_INT2_WU = 5
    MD2_CFG_MASK_INT2_WU = 0b1 << MD2_CFG_SHIFT_INT2_WU
    MD2_CFG_SHIFT_INT2_FF = 4
    MD2_CFG_MASK_INT2_FF = 0b1 << MD2_CFG_SHIFT_INT2_FF
    MD2_CFG_SHIFT_INT2_DOUBLE_TAP = 3
    MD2_CFG_MASK_INT2_DOUBLE_TAP = 0b1 << MD2_CFG_SHIFT_INT2_DOUBLE_TAP
    MD2_CFG_SHIFT_INT2_6D = 2
    MD2_CFG_MASK_INT2_6D = 0b1 << MD2_CFG_SHIFT_INT2_6D
    MD2_CFG_SHIFT_INT2_EMB_FUNC = 1
    MD2_CFG_MASK_INT2_EMB_FUNC = 0b1 << MD2_CFG_SHIFT_INT2_EMB_FUNC
    MD2_CFG_SHIFT_INT2_TIMESTAMP = 0
    MD2_CFG_MASK_INT2_TIMESTAMP = 0b1 << MD2_CFG_SHIFT_INT2_TIMESTAMP

    REG_SLV0_CONFIG = 0x17
    SLV0_CONFIG_SHIFT_SHUB_ODR = 6
    SLV0_CONFIG_MASK_SHUB_ODR = 0b11 << SLV0_CONFIG_SHIFT_SHUB_ODR
    SLV0_CONFIG_SHIFT_BATCH_EXT_SENS0_EN = 3
    SLV0_CONFIG_MASK_BATCH_EXT_SENS0_EN = 0b1 << SLV0_CONFIG_SHIFT_BATCH_EXT_SENS0_EN
    SLV0_CONFIG_SHIFT_SLAVE0_NUMOP = 0
    SLV0_CONFIG_MASK_SLAVE0_NUMOP = 0b111 << SLV0_CONFIG_SHIFT_SLAVE0_NUMOP

    # Data Ready Pulse modes
    DRDY_LATCHED = 0
    DRDY_PULSED = 1

    REG_CNTR_BDR1 = 0x0B
    CNTR_BDR1_SHIFT_DATAREADY_PULSED = 7
    CNTR_BDR1_MASK_DATAREADY_PULSED = 0b1 << CNTR_BDR1_SHIFT_DATAREADY_PULSED
    CNTR_BDR1_SHIFT_RST_COUNTER_BDR = 6
    CNTR_BDR1_MASK_RST_COUNTER_BDR = 0b1 << CNTR_BDR1_SHIFT_RST_COUNTER_BDR
    CNTR_BDR1_SHIFT_TRIG_COUNTER_BDR = 5
    CNTR_BDR1_MASK_TRIG_COUNTER_BDR = 0b1 << CNTR_BDR1_SHIFT_TRIG_COUNTER_BDR
    CNTR_BDR1_SHIFT_CNT_BDR_TH = 0
    CNTR_BDR1_MASK_CNT_BDR_TH = 0b111 << CNTR_BDR1_SHIFT_CNT_BDR_TH

    # Sensor Hub registers
    REG_DATAWRITE_SLV0 = 0x21
    REG_SLV0_SUBADD = 0x16
    REG_SLV0_ADD = 0x15
    SLV0_ADD_SHIFT_SLAVE0 = 1
    SLV0_ADD_MASK_SLAVE0 = 0x7F << SLV0_ADD_SHIFT_SLAVE0
    SLV0_ADD_SHIFT_RW0 = 0
    SLV0_ADD_MASK_RW0 = 0b1 << SLV0_ADD_SHIFT_RW0
    
    REG_SLV1_SUBADD = 0x19
    REG_SLV1_ADD = 0x18
    SLV1_ADD_SHIFT_SLAVE1 = 1
    SLV1_ADD_MASK_SLAVE1 = 0x7F << SLV1_ADD_SHIFT_SLAVE1
    SLV1_ADD_SHIFT_R1 = 0

    REG_SLV1_CONFIG = 0x1A
    SLV1_CONFIG_SHIFT_BATCH_EXT_SENS1_EN = 3
    SLV1_CONFIG_MASK_BATCH_EXT_SENS1_EN = 0b1 << SLV1_CONFIG_SHIFT_BATCH_EXT_SENS1_EN
    SLV1_CONFIG_SHIFT_SLAVE1_NUMOP = 0
    SLV1_CONFIG_MASK_SLAVE1_NUMOP = 0b111 << SLV1_CONFIG_SHIFT_SLAVE1_NUMOP

    REG_SLV2_SUBADD = 0x1C
    REG_SLV2_ADD = 0x1B

    REG_SLV2_CONFIG = 0x1D
    SLV2_CONFIG_SHIFT_BATCH_EXT_SENS2_EN = 3
    SLV2_CONFIG_MASK_BATCH_EXT_SENS2_EN = 0b1 << SLV2_CONFIG_SHIFT_BATCH_EXT_SENS2_EN
    SLV2_CONFIG_SHIFT_SLAVE2_NUMOP = 0
    SLV2_CONFIG_MASK_SLAVE2_NUMOP = 0b111 << SLV2_CONFIG_SHIFT_SLAVE2_NUMOP

    REG_SLV3_SUBADD = 0x1F
    REG_SLV3_ADD = 0x1E

    REG_SLV3_CONFIG = 0x20
    SLV3_CONFIG_SHIFT_BATCH_EXT_SENS3_EN = 3
    SLV3_CONFIG_MASK_BATCH_EXT_SENS3_EN = 0b1 << SLV3_CONFIG_SHIFT_BATCH_EXT_SENS3_EN
    SLV3_CONFIG_SHIFT_SLAVE3_NUMOP = 0
    SLV3_CONFIG_MASK_SLAVE3_NUMOP = 0b111 << SLV3_CONFIG_SHIFT_SLAVE3_NUMOP
    
    REG_MASTER_CONFIG = 0x14
    MASTER_CONFIG_SHIFT_RST_MASTER_REGS = 7
    MASTER_CONFIG_MASK_RST_MASTER_REGS = 0b1 << MASTER_CONFIG_SHIFT_RST_MASTER_REGS
    MASTER_CONFIG_SHIFT_WRITE_ONCE = 6
    MASTER_CONFIG_MASK_WRITE_ONCE = 0b1 << MASTER_CONFIG_SHIFT_WRITE_ONCE
    MASTER_CONFIG_SHIFT_START_CONFIG = 5
    MASTER_CONFIG_MASK_START_CONFIG = 0b1 << MASTER_CONFIG_SHIFT_START_CONFIG
    MASTER_CONFIG_SHIFT_PASS_THROUGH_MODE = 4
    MASTER_CONFIG_MASK_PASS_THROUGH_MODE = 0b1 << MASTER_CONFIG_SHIFT_PASS_THROUGH_MODE
    MASTER_CONFIG_SHIFT_SHUB_PU_EN = 3
    MASTER_CONFIG_MASK_SHUB_PU_EN = 0b1 << MASTER_CONFIG_SHIFT_SHUB_PU_EN
    MASTER_CONFIG_SHIFT_MASTER_ON = 2
    MASTER_CONFIG_MASK_MASTER_ON = 0b1 << MASTER_CONFIG_SHIFT_MASTER_ON
    MASTER_CONFIG_SHIFT_AUX_SENS_ON = 0
    MASTER_CONFIG_MASK_AUX_SENS_ON = 0b11 << MASTER_CONFIG_SHIFT_AUX_SENS_ON

    REG_SENSOR_HUB1 = 0x02
    REG_STATUS_MASTER = 0x22

    STATUS_MASTER_SHIFT_WR_ONCE_DONE = 7
    STATUS_MASTER_MASK_WR_ONCE_DONE = 0b1 << STATUS_MASTER_SHIFT_WR_ONCE_DONE
    STATUS_MASTER_SHIFT_SLAVE3_NACK = 6
    STATUS_MASTER_MASK_SLAVE3_NACK = 0b1 << STATUS_MASTER_SHIFT_SLAVE3_NACK
    STATUS_MASTER_SHIFT_SLAVE2_NACK = 5
    STATUS_MASTER_MASK_SLAVE2_NACK = 0b1 << STATUS_MASTER_SHIFT_SLAVE2_NACK
    STATUS_MASTER_SHIFT_SLAVE1_NACK = 4
    STATUS_MASTER_MASK_SLAVE1_NACK = 0b1 << STATUS_MASTER_SHIFT_SLAVE1_NACK
    STATUS_MASTER_SHIFT_SLAVE0_NACK = 3
    STATUS_MASTER_MASK_SLAVE0_NACK = 0b1 << STATUS_MASTER_SHIFT_SLAVE0_NACK
    STATUS_MASTER_SHIFT_SENS_HUB_ENDOP = 0
    STATUS_MASTER_MASK_SENS_HUB_ENDOP = 0b1 << STATUS_MASTER_SHIFT_SENS_HUB_ENDOP

    HUB_WRITE_MODE_CYCLE = 0 # Write each cycle
    HUB_WRITE_MODE_SINGLE = 1 # Write once

    SELF_TEST_DISABLE = 0
    SELF_TEST_POSITIVE = 1
    SELF_TEST_NEGATIVE = 2

    REG_CTRL5_C = 0x14
    CTRL5_C_SHIFT_ROUNDING = 5
    CTRL5_C_MASK_ROUNDING = 0b11 << CTRL5_C_SHIFT_ROUNDING
    CTRL5_C_SHIFT_ST_G = 2
    CTRL5_C_MASK_ST_G = 0b11 << CTRL5_C_SHIFT_ST_G
    CTRL5_C_SHIFT_ST_XL = 0
    CTRL5_C_MASK_ST_XL = 0b11 << CTRL5_C_SHIFT_ST_XL

    # Status Register
    REG_STATUS = 0x1E
    STATUS_SHIFT_TDA = 2
    STATUS_MASK_TDA = 0b1 << STATUS_SHIFT_TDA
    STATUS_SHIFT_GDA = 1
    STATUS_MASK_GDA = 0b1 << STATUS_SHIFT_GDA
    STATUS_SHIFT_XLDA = 0
    STATUS_MASK_XLDA = 0b1 << STATUS_SHIFT_XLDA

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

        self._full_scale_accel = 0 # powered down by default
        self._full_scale_gyro = 0  # powered down by default

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        
        if not self._i2c.is_device_connected(self.address):
            return False
        
        # Confirm device ID is correct
        if self.get_id() != self.DEV_ID:
            return False

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        return self.is_connected()

    def get_id(self):
        """!
        Get the device ID

        @return **int** The device ID
        """
        return self._i2c.read_byte(self.address, self.REG_WHO_AM_I)

    def set_accel_full_scale(self, val):
        """!
        Set the scale of the accelerometer's readings 2g - 16g

        @param val: **int** The scale to be applied to the accelerometer (0 - 3)

        Possible values:
            - XL_FS_2G
            - XL_FS_16G
            - XL_FS_4G
            - XL_FS_8G
        """
        if val < self.XL_FS_2G or val > self.XL_FS_8G:
            return

        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL1_XL)

        reg_val &= ~self.CTRL1_XL_MASK_FS
        reg_val |= (val << self.CTRL1_XL_SHIFT_FS)

        self._i2c.write_byte(self.address, self.REG_CTRL1_XL, reg_val)

        self._full_scale_accel = val
    
    def set_gyro_full_scale(self, val):
        """!
        Set the scale of the gyroscope's readings 125, 250, 500, 1000, 2000, 4000 degrees per second

        @param val: **int** The scale to be applied to the gyroscope (0, 1, 2, 4, 6, 12)
        """
        if val < self.GYRO_FS_250DPS or val > self.GYRO_FS_2000DPS:
            return

        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL2_G)

        reg_val &= ~self.CTRL2_G_MASK_FS
        reg_val |= (val << self.CTRL2_G_SHIFT_FS)

        self._i2c.write_byte(self.address, self.REG_CTRL2_G, reg_val)

        self._full_scale_gyro = val

    def get_accel_full_scale(self):
        """!
        Get the scale of the accelerometer's readings

        @return **int** The scale of the accelerometer's readings

        Possible return values:
            - XL_FS_2G
            - XL_FS_16G
            - XL_FS_4G
            - XL_FS_8G
        """
        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL1_XL)

        return (reg_val & self.CTRL1_XL_MASK_FS) >> self.CTRL1_XL_SHIFT_FS


    def get_gyro_full_scale(self):
        """!
        Get the scale of the gyroscope's readings

        @return **int** The scale of the gyroscope's readings

        Possible return values:
            - GYRO_FS_125DPS
            - GYRO_FS_250DPS
            - GYRO_FS_500DPS
            - GYRO_FS_1000DPS
            - GYRO_FS_2000DPS
            - GYRO_FS_4000DPS
        """
        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL2_G)

        return (reg_val & self.CTRL2_G_MASK_FS) >> self.CTRL2_G_SHIFT_FS

    def get_temp(self):
        """!
        Get the raw temperature reading. Convert it to degrees Celsius with
        convert_lsb_to_celsius()

        @return **int** The raw temperature reading (signed 16-bit)
        """
        temp = self._i2c.read_block(self.address, self.REG_OUT_TEMP_L,2)
        val = (temp[1] << 8) | temp[0]
        # Convert to from unsigned to signed 16-bit
        if val > 32767:
            val -= 65536
        
        return val

    def _get_raw_data(self, reg):
        """!
        Get the raw data from the specified register

        @param reg: **int** The register to read from
        """
        bytes = self._i2c.read_block(self.address, reg, 6)

        data_out = ISMData()
        data_out.x_data = (bytes[1] << 8) | bytes[0]
        data_out.y_data = (bytes[3] << 8) | bytes[2]
        data_out.z_data = (bytes[5] << 8) | bytes[4]

        # Convert to signed 16-bit
        data_out.x_data, data_out.y_data, data_out.z_data = [
            val if val < 32768 else val - 65536 for val in [data_out.x_data, data_out.y_data, data_out.z_data]
        ]

        return data_out

    def get_raw_accel(self):
        """!
        Get the raw accelerometer readings

        @return **list** The raw accelerometer readings
        """
        return self._get_raw_data(self.REG_OUT_XLA)
    
    def get_raw_gyro(self):
        """!
        Get the raw gyroscope readings

        @return **list** The raw gyroscope readings
        """
        return self._get_raw_data(self.REG_OUT_XLG)

    def _convert_data(self, data, key, conv_dict):
        """!
        Use the key parameter to extract the conversion function from conv_dict and apply it to the data

        @param data: **ISMData** The data to be converted
        @param key: **int** The key to be used to extract the conversion function from conv_dict
        @param conv_dict: **dict** The dictionary containing the conversion functions

        @return **ISMData** The converted data
        """
        if key in conv_dict:
            conv = conv_dict[key]
            data.x_data = conv(data.x_data)
            data.y_data = conv(data.y_data)
            data.z_data = conv(data.z_data)
        else:
            return None

        return data

    def get_accel(self):
        """!
        Retrieves raw register values and converts them according to the full scale settings

        @return **ISMData** The accelerometer data in mg
        """
        data = self.get_raw_accel()

        full_scale_conversions = {
            self.XL_FS_2G: self.convert_2g_to_mg,
            self.XL_FS_4G: self.convert_4g_to_mg,
            self.XL_FS_8G: self.convert_8g_to_mg,
            self.XL_FS_16G: self.convert_16g_to_mg
        }

        return self._convert_data(data, self._full_scale_accel, full_scale_conversions)

    def get_gyro(self):
        """!
        Retrieves raw register values and converts them according to the full scale settings

        @return **ISMData** The gyroscope data in mdps
        """
        data = self.get_raw_gyro()

        full_scale_conversions = {
            self.GYRO_FS_125DPS: self.convert_125dps_to_mdps,
            self.GYRO_FS_250DPS: self.convert_250dps_to_mdps,
            self.GYRO_FS_500DPS: self.convert_500dps_to_mdps,
            self.GYRO_FS_1000DPS: self.convert_1000dps_to_mdps,
            self.GYRO_FS_2000DPS: self.convert_2000dps_to_mdps,
            self.GYRO_FS_4000DPS: self.convert_4000dps_to_mdps
        }

        return self._convert_data(data, self._full_scale_gyro, full_scale_conversions)

    # Conversion functions
    def convert_2g_to_mg(self, lsb):
        return lsb * 0.061

    def convert_4g_to_mg(self, lsb):
        return lsb * 0.122

    def convert_8g_to_mg(self, lsb):
        return lsb * 0.244

    def convert_16g_to_mg(self, lsb):
        return lsb * 0.488

    def convert_125dps_to_mdps(self, lsb):
        return lsb * 4.375

    def convert_250dps_to_mdps(self, lsb):
        return lsb * 8.75

    def convert_500dps_to_mdps(self, lsb):
        return lsb * 17.50

    def convert_1000dps_to_mdps(self, lsb):
        return lsb * 35.0

    def convert_2000dps_to_mdps(self, lsb):
        return lsb * 70.0

    def convert_4000dps_to_mdps(self, lsb):
        return lsb * 140.0

    def convert_lsb_to_celsius(self, lsb):
        return (lsb / 256.0) + 25.0

    def convert_lsb_to_nsec(self, lsb):
        return lsb * 25000.0

    def set_device_config(self, enable=True):
        """!
        Enable the general device configuration

        @param enable: **bool** Enable or disable the device configuration
        """
        if enable != 0 and enable != 1:
            return
        
        val = self._i2c.read_byte(self.address, self.REG_CTRL9_XL)
        
        val &= ~self.CTRL9_XL_MASK_DEVICE_CONF
        val |= (enable << self.CTRL9_XL_SHIFT_DEVICE_CONF)

        self._i2c.write_byte(self.address, self.REG_CTRL9_XL, val)

    def device_reset(self):
        """!
        Reset the device to default settings
        """
        val = self._i2c.read_byte(self.address, self.REG_CTRL3_C)
        
        val |= self.CTRL3_C_MASK_SW_RESET

        self._i2c.write_byte(self.address, self.REG_CTRL3_C, val)

    def get_device_reset(self):
        """!
        Get the device reset state

        @return **bool** The device reset state
        """
        val = self._i2c.read_byte(self.address, self.REG_CTRL3_C)

        return (val & self.CTRL3_C_MASK_SW_RESET) == 0

    def set_accel_slope_filter(self, val):
        """!
        Set's the accelerometer's slope filter

        @param val: **int** The intensity of the filter (0x00 - 0x37)

        See the constants in the class definition under "Possilbe Slope Filters" for a list of valid arguments
        """
        if val < self.HP_PATH_DISABLE_ON_OUT or val > self.HP_REF_MD_ODR_DIV800:
            return
        

        new_slope_en = (val & 0x10) >> 4
        new_ref_mode = (val & 0x20) >> 5
        new_cf = (val & 0x07)

        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL8_XL)

        reg_val &= ~self.CTRL8_XL_MASK_HP_SLOPE_XL_EN
        reg_val |= (new_slope_en << self.CTRL8_XL_SHIFT_HP_SLOPE_XL_EN)

        reg_val &= ~self.CTRL8_XL_MASK_HP_REF_MODE_XL
        reg_val |= (new_ref_mode << self.CTRL8_XL_SHIFT_HP_REF_MODE_XL)

        reg_val &= ~self.CTRL8_XL_MASK_HPCF_XL
        reg_val |= (new_cf << self.CTRL8_XL_SHIFT_HPCF_XL)
        
        self._i2c.write_byte(self.address, self.REG_CTRL8_XL, reg_val)
    
    def set_accel_filter_lp2(self, enable = True):
        """!
        Enable the accelerometer's high resolution slope filter

        @param enable: **bool** Enable or disable the filter
        """
        if enable != True and enable != False:
            return
        
        val = self._i2c.read_byte(self.address, self.REG_CTRL1_XL)
        
        val &= ~self.CTRL1_XL_MASK_LPF2_XL_EN
        val |= (enable << self.CTRL1_XL_SHIFT_LPF2_XL_EN)

        self._i2c.write_byte(self.address, self.REG_CTRL1_XL, val)

    def set_gyro_filter_lp1(self, enable = True):
        """!
        Enables the gyroscope's slope filter

        @param enable: **bool** Enable or disable the filter
        """
        if enable != True and enable != False:
            return
        
        val = self._i2c.read_byte(self.address, self.REG_CTRL4_C)

        val &= ~self.CTRL4_C_MASK_LPF1_SEL_G
        val |= (enable << self.CTRL4_C_SHIFT_LPF1_SEL_G)

        self._i2c.write_byte(self.address, self.REG_CTRL4_C, val)
        
    def set_gyro_lp1_bandwidth(self, val):
        """!
        Sets the low pass filter's bandwidth for the gyroscope

        @param val: **int** The bandwidth of the filter

        Possible values:
            - BW_ULTRA_LIGHT
            - BW_VERY_LIGHT
            - BW_LIGHT
            - BW_MEDIUM
            - BW_STRONG
            - BW_VERY_STRONG
            - BW_AGGRESSIVE
            - BW_XTREME
        """
        if val < self.BW_ULTRA_LIGHT or val > self.BW_XTREME:
            return
        
        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL6_C)

        reg_val &= ~self.CTRL6_C_MASK_FTYPE
        reg_val |= (val << self.CTRL6_C_SHIFT_FTYPE)

        self._i2c.write_byte(self.address, self.REG_CTRL6_C, reg_val)

    def set_block_data_update(self, enable = True):
        """!
        Data is not updated until both MSB and LSB have been read from output registers

        @param enable: **bool** Enable or disable the block data update
        """
        if enable != True and enable != False:
            return
        
        val = self._i2c.read_byte(self.address, self.REG_CTRL3_C)

        val &= ~self.CTRL3_C_MASK_BDU
        val |= (enable << self.CTRL3_C_SHIFT_BDU)

        self._i2c.write_byte(self.address, self.REG_CTRL3_C, val)

    def get_block_data_update(self):
        """!
        Retrieves the bit indicating if block data update is enabled

        @return **int** The block data update state
        """
        val = self._i2c.read_byte(self.address, self.REG_CTRL3_C)

        return (val & self.CTRL3_C_MASK_BDU) >> self.CTRL3_C_SHIFT_BDU
    
    def _mem_bank_set(self, val):
        """!
        Enable access to the embedded functions/sensor hub configuration registers. Not to be used outside this module

        @param val: **int** The value to set the memory bank to

        Possible values:
            - USER_BANK
            - SENSOR_HUB_BANK
            - EMBEDDED_FUNC_BANK
        """
        if val < self.USER_BANK or val > self.EMBEDDED_FUNC_BANK:
            return

        reg_val = self._i2c.read_byte(self.address, self.REG_FUNC_CFG_ACCESS)

        reg_val &= ~self.FUNC_CFG_ACCESS_MASK_REG_ACCESS
        reg_val |= (val << self.FUNC_CFG_ACCESS_SHIFT_REG_ACCESS)

        self._i2c.write_byte(self.address, self.REG_FUNC_CFG_ACCESS, reg_val)

    def _fsm_enable_get(self):
        """!
        Embedded finite state machine functions mode. Not to be used outside this module

        @return **tuple of int** Tuple containing fsm_enable_a followed by fsm_enable_b
        """
        self._mem_bank_set(self.EMBEDDED_FUNC_BANK)

        fsm_enable_a = self._i2c.read_byte(self.address, self.REG_FSM_ENABLE_A)
        fsm_enable_b = self._i2c.read_byte(self.address, self.REG_FSM_ENABLE_B)

        self._mem_bank_set(self.USER_BANK)

        return (fsm_enable_a, fsm_enable_b)
    
    def _fsm_data_rate_get(self):
        """!
        Get the data rate (ODR) of the finite state machine

        @return **int** The data rate of the finite state machine

        Possible return values:
            - ODR_FSM_12_5HZ
            - ODR_FSM_26HZ
            - ODR_FSM_52HZ
            - ODR_FSM_104HZ
        """
        self._mem_bank_set(self.EMBEDDED_FUNC_BANK)

        fsm_odr_cfg_b = self._i2c.read_byte(self.address, self.REG_EMB_FUNC_ODR_CFG_B)

        self._mem_bank_set(self.USER_BANK)

        return (fsm_odr_cfg_b & self.EMB_FUNC_ODR_MASK_FSM_ODR) >> self.EMB_FUNC_ODR_SHIFT_FSM_ODR
    
    def _mlc_get(self):
        """!
        Get the Machine Learning Core enable state

        @return **int** The Machine Learning Core enable state
        """
        self._mem_bank_set(self.EMBEDDED_FUNC_BANK)

        reg_val = self._i2c.read_byte(self.address, self.REG_EMB_FUNC_EN_B)

        self._mem_bank_set(self.USER_BANK)

        return (reg_val & self.EMB_FUNC_EN_B_MASK_MLC_EN) >> self.EMB_FUNC_EN_B_SHIFT_MLC_EN
    
    def _mlc_data_rate_get(self):
        """!
        Get Machine Learning Core data rate selection

        @return **int** The Machine Learning Core data rate selection

        For possible return values see the "MLC" section in "Possible data rates" in the class definition
        """
        self._mem_bank_set(self.EMBEDDED_FUNC_BANK)

        reg_val = self._i2c.read_byte(self.address, self.REG_EMB_FUNC_ODR_CFG_C)

        self._mem_bank_set(self.USER_BANK)

        return (reg_val & self.EMB_FUNC_ODR_MASK_MLC_ODR) >> self.EMB_FUNC_ODR_SHIFT_MLC_ODR


    def set_accel_data_rate(self, val): 
        """!
        Sets the data output rate of the accelerometer

        @param val: **int** Data rate

        See the "Accelerometer section in Possible data rates" in the class definition for a list of valid arguments
        """
        if val < self.XL_ODR_OFF or val > self.XL_ODR_1_6HZ:
            return
        
        enable_a, enable_b = self._fsm_enable_get()

        odr_xl = val

        if (enable_a & 0xFF) or (enable_b & 0xFF):
            # Coresponds to any of the FSMs being enabled
            fsm_odr = self._fsm_data_rate_get()
            if fsm_odr == self.ODR_FSM_12_5HZ:
                if val == self.XL_ODR_OFF:
                    odr_xl = self.XL_ODR_12_5HZ

            elif fsm_odr == self.ODR_FSM_26HZ:
                if val == self.XL_ODR_OFF:
                    odr_xl = self.XL_ODR_26HZ
                elif val == self.XL_ODR_12_5HZ:
                    odr_xl = self.XL_ODR_26HZ

            elif fsm_odr == self.ODR_FSM_52HZ:
                if val == self.XL_ODR_OFF:
                    odr_xl = self.XL_ODR_52HZ
                elif val == self.XL_ODR_12_5HZ:
                    odr_xl = self.XL_ODR_52HZ
                elif val == self.XL_ODR_26HZ:
                    odr_xl = self.XL_ODR_52HZ

            elif fsm_odr == self.ODR_FSM_104HZ:
                if val == self.XL_ODR_OFF:
                    odr_xl = self.XL_ODR_104HZ
                elif val == self.XL_ODR_12_5HZ:
                    odr_xl = self.XL_ODR_104HZ
                elif val == self.XL_ODR_26HZ:
                    odr_xl = self.XL_ODR_104HZ
                elif val == self.XL_ODR_52HZ:
                    odr_xl = self.XL_ODR_104HZ

        # Machine Learning Core data rate constraints:
        mlc_enable = self._mlc_get()

        if mlc_enable:
            mlc_odr = self._mlc_data_rate_get()

            if mlc_odr == self.MLC_ODR_12_5HZ:
                if val == self.XL_ODR_OFF:
                    odr_xl = self.XL_ODR_12_5HZ
                else:
                    odr_xl = val

            elif mlc_odr == self.MLC_ODR_26HZ:
                if val == self.XL_ODR_OFF:
                    odr_xl = self.XL_ODR_26HZ
                elif val == self.XL_ODR_12_5HZ:
                    odr_xl = self.XL_ODR_26HZ
                else:
                    odr_xl = val

            elif mlc_odr == self.MLC_ODR_52HZ:
                if val == self.XL_ODR_OFF:
                    odr_xl = self.XL_ODR_52HZ
                elif val == self.XL_ODR_12_5HZ:
                    odr_xl = self.XL_ODR_52HZ
                elif val == self.XL_ODR_26HZ:
                    odr_xl = self.XL_ODR_52HZ
                else:
                    odr_xl = val

            elif mlc_odr == self.MLC_ODR_104HZ:
                if val == self.XL_ODR_OFF:
                    odr_xl = self.XL_ODR_104HZ
                elif val == self.XL_ODR_12_5HZ:
                    odr_xl = self.XL_ODR_104HZ
                elif val == self.XL_ODR_26HZ:
                    odr_xl = self.XL_ODR_104HZ
                elif val == self.XL_ODR_52HZ:
                    odr_xl = self.XL_ODR_104HZ
                else:
                    odr_xl = val

            else:
                odr_xl = val

        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL1_XL)

        reg_val &= ~self.CTRL1_XL_MASK_ODR
        reg_val |= (odr_xl << self.CTRL1_XL_SHIFT_ODR)

        self._i2c.write_byte(self.address, self.REG_CTRL1_XL, reg_val)

    def set_gyro_data_rate(self, val):
        """!
        Sets the data output rate of the gyroscope

        @param val: **int** Data rate

        See the "Gyroscope" section in Possible data rates" in the class definition for a list of valid arguments
        """
        if val < self.GYRO_ODR_OFF or val > self.GYRO_ODR_6667HZ:
            return
        
        enable_a, enable_b = self._fsm_enable_get()

        odr_gy = val

        if (enable_a & 0xFF) or (enable_b & 0xFF):
            # Coresponds to any of the FSMs being enabled
            fsm_odr = self._fsm_data_rate_get()
            if fsm_odr == self.ODR_FSM_12_5HZ:
                if val == self.GYRO_ODR_OFF:
                    odr_gy = self.GYRO_ODR_12_5HZ

            elif fsm_odr == self.ODR_FSM_26HZ:
                if val == self.GYRO_ODR_OFF:
                    odr_gy = self.GYRO_ODR_26HZ
                elif val == self.GYRO_ODR_12_5HZ:
                    odr_gy = self.GYRO_ODR_26HZ

            elif fsm_odr == self.ODR_FSM_52HZ:
                if val == self.GYRO_ODR_OFF:
                    odr_gy = self.GYRO_ODR_52HZ
                elif val == self.GYRO_ODR_12_5HZ:
                    odr_gy = self.GYRO_ODR_52HZ
                elif val == self.GYRO_ODR_26HZ:
                    odr_gy = self.GYRO_ODR_52HZ

            elif fsm_odr == self.ODR_FSM_104HZ:
                if val == self.GYRO_ODR_OFF:
                    odr_gy = self.GYRO_ODR_104HZ
                elif val == self.GYRO_ODR_12_5HZ:
                    odr_gy = self.GYRO_ODR_104HZ
                elif val == self.GYRO_ODR_26HZ:
                    odr_gy = self.GYRO_ODR_104HZ
                elif val == self.GYRO_ODR_52HZ:
                    odr_gy = self.GYRO_ODR_104HZ
        
        mlc_enable = self._mlc_get()
        if mlc_enable:
            mlc_odr = self._mlc_data_rate_get()
            if mlc_odr == self.MLC_ODR_12_5HZ:
                if val == self.GYRO_ODR_OFF:
                    odr_gy = self.GYRO_ODR_12_5HZ
                else:
                    odr_gy = val

            elif mlc_odr == self.MLC_ODR_26HZ:
                if val == self.GYRO_ODR_OFF:
                    odr_gy = self.GYRO_ODR_26HZ
                elif val == self.GYRO_ODR_12_5HZ:
                    odr_gy = self.GYRO_ODR_26HZ
                else:
                    odr_gy = val

            elif mlc_odr == self.MLC_ODR_52HZ:
                if val == self.GYRO_ODR_OFF:
                    odr_gy = self.GYRO_ODR_52HZ
                elif val == self.GYRO_ODR_12_5HZ:
                    odr_gy = self.GYRO_ODR_52HZ
                elif val == self.GYRO_ODR_26HZ:
                    odr_gy = self.GYRO_ODR_52HZ
                else:
                    odr_gy = val

            elif mlc_odr == self.MLC_ODR_104HZ:
                if val == self.GYRO_ODR_OFF:
                    odr_gy = self.GYRO_ODR_104HZ
                elif val == self.GYRO_ODR_12_5HZ:
                    odr_gy = self.GYRO_ODR_104HZ
                elif val == self.GYRO_ODR_26HZ:
                    odr_gy = self.GYRO_ODR_104HZ
                elif val == self.GYRO_ODR_52HZ:
                    odr_gy = self.GYRO_ODR_104HZ
                else:
                    odr_gy = val

            else:
                odr_gy = val
        
        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL2_G)

        reg_val &= ~self.CTRL2_G_MASK_ODR
        reg_val |= (odr_gy << self.CTRL2_G_SHIFT_ODR)

        self._i2c.write_byte(self.address, self.REG_CTRL2_G, reg_val)


    def enable_timestamp(self, enable = True):
        """!
        Enables the timestamp counter.

        @param enable: **bool** Enable or disable the timestamp counter
        """
        if enable != True and enable != False:
            return
        
        val = self._i2c.read_byte(self.address, self.REG_CTRL10_C)

        val &= ~self.CTRL10_C_MASK_TIMESTAMP_EN
        val |= (enable << self.CTRL10_C_SHIFT_TIMESTAMP_EN)

        self._i2c.write_byte(self.address, self.REG_CTRL10_C, val)
    
    def reset_timestamp(self):
        """!
        Resets the timestamp counter
        """
        reset_val = 0xAA
        self._i2c.write_byte(self.address, self.REG_TIMESTAMP2, reset_val)

    # Fifo Methods
    def set_fifo_watermark(self, val):
        """!
        Set the FIFO watermark level

        @param val: **int** The watermark level. Must be between 0 and 511 (a 9-bit value)
        """
        if val < 0 or val > 511:
            return
        
        ctrl2_val = (val >> 8) & 0x01 # WTM8
        ctrl1_val = val & 0xFF # WTM[7:0]

        reg_val = self._i2c.read_byte(self.address, self.REG_FIFO_CTRL2)

        reg_val &= ~self.FIFO_CTRL2_MASK_WTM
        reg_val |= (ctrl2_val << self.FIFO_CTRL2_SHIFT_WTM)

        self._i2c.write_byte(self.address, self.REG_FIFO_CTRL2, reg_val)

        self._i2c.write_byte(self.address, self.REG_FIFO_CTRL1, ctrl1_val)

    def set_fifo_mode(self, val):
        """!
        Sets the FIFO mode

        @param val: **int** The FIFO mode

        Possible values:
            - BYPASS_MODE
            - FIFO_MODE
            - STREAM_TO_FIFO_MODE
            - BYPASS_TO_STREAM_MODE
            - STREAM_MODE
            - BYPASS_TO_FIFO_MODE
        """
        if val < self.BYPASS_MODE or val > self.BYPASS_TO_FIFO_MODE:
            return
        
        reg_val = self._i2c.read_byte(self.address, self.REG_FIFO_CTRL4)

        reg_val &= ~self.FIFO_CTRL4_MASK_FIFO_MODE
        reg_val |= (val << self.FIFO_CTRL4_SHIFT_FIFO_MODE)

        self._i2c.write_byte(self.address, self.REG_FIFO_CTRL4, reg_val)

    def set_accel_fifo_batch_set(self, val):
        """!
        Sets the batch data rate for the accelerometer

        @param val: **int** The batch data rate

        See the "Possible Accelerometer Batch Data Rates" in the class definition for a list of valid arguments
        """
        if val < self.XL_NOT_BATCHED or val > self.XL_BATCHED_AT_6_5HZ:
            return

        reg_val = self._i2c.read_byte(self.address, self.REG_FIFO_CTRL3)

        reg_val &= ~self.FIFO_CTRL3_MASK_BDR_XL
        reg_val |= (val << self.FIFO_CTRL3_SHIFT_BDR_XL)
        
        self._i2c.write_byte(self.address, self.REG_FIFO_CTRL3, reg_val)


    def set_gyro_fifo_batch_set(self, val):
        """!
        Sets the batch data rate for the gyroscope

        @param val: **int** The batch data rate

        See the "Possible Gyroscope Batch Data Rates" in the class definition for a list of valid arguments
        """
        if val < self.GYRO_NOT_BATCHED or val > self.GYRO_BATCHED_AT_6_5HZ:
            return

        reg_val = self._i2c.read_byte(self.address, self.REG_FIFO_CTRL3)

        reg_val &= ~self.FIFO_CTRL3_MASK_BDR_G
        reg_val |= (val << self.FIFO_CTRL3_SHIFT_BDR_G)
        
        self._i2c.write_byte(self.address, self.REG_FIFO_CTRL3, reg_val)
    
    def set_fifo_timestamp_dec(self, val):
        """!
        Sets the FIFO time stamp decimation rate.

        @param val: **int** The decimation rate

        Possible values:
            - NO_DECIMATION
            - DEC1
            - DEC8
            - DEC32
        """
        if val < self.NO_DECIMATION or val > self.DEC32:
            return
        
        reg_val = self._i2c.read_byte(self.address, self.REG_FIFO_CTRL4)

        reg_val &= ~self.FIFO_CTRL4_MASK_ODR_TS_BATCH
        reg_val |= (val << self.FIFO_CTRL4_SHIFT_ODR_TS_BATCH)

        self._i2c.write_byte(self.address, self.REG_FIFO_CTRL4, reg_val)

    # Interrupt and pin mode settings
    def set_pin_mode(self, active_low):
        """!
        Sets the active state of the interrupt pin - high or low.

        @param active_low: **bool** Set to `True` for active low, `False` for active high
        """
        if active_low != True and active_low != False:
            return

        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL3_C)

        reg_val &= ~self.CTRL3_C_MASK_HL_ACTIVE
        reg_val |= (active_low << self.CTRL3_C_SHIFT_HL_ACTIVE)

        if active_low:
            # pinmode must be set to push-pull when active low is set.
            # See section 9.14 on pg 51 of datasheet for more information
            reg_val &= ~self.CTRL3_C_MASK_PP_OD

        self._i2c.write_byte(self.address, self.REG_CTRL3_C, reg_val)

    def set_int_notification(self, val):
        """!
        Sets what triggers an interrupt

        @param val: **int** The interrupt event type

        Possible Values:
            - ALL_INT_PULSED
            - BASE_LATCHED_EMB_PULSED
            - BASE_PULSED_EMB_LATCHED
            - ALL_INT_LATCHED
        """
        if val < self.ALL_INT_PULSED or val > self.ALL_INT_LATCHED:
            return


        lir = val & 0x01
        int_clr_on_read = val & 0x01

        # Set necessary values in the tap config register
        reg_val = self._i2c.read_byte(self.address, self.REG_TAP_CFG0)

        reg_val &= ~(self.TAP_CFG0_MASK_LIR | self.TAP_CFG0_MASK_INT_CLR_ON_READ)
        reg_val |= (lir << self.TAP_CFG0_SHIFT_LIR)
        reg_val |= (int_clr_on_read << self.TAP_CFG0_SHIFT_INT_CLR_ON_READ)
        
        self._i2c.write_byte(self.address, self.REG_TAP_CFG0, reg_val)

        # Set necessary values in the Page RW register
        self._mem_bank_set(self.EMBEDDED_FUNC_BANK)

        reg_val = self._i2c.read_byte(self.address, self.REG_PAGE_RW)

        emb_func_lir = (val & 0x02) >> 1
        reg_val &= ~self.PAGE_RW_MASK_EMB_FUNC_LIR
        reg_val |= (emb_func_lir << self.PAGE_RW_SHIFT_EMB_FUNC_LIR)

        self._i2c.write_byte(self.address, self.REG_PAGE_RW, reg_val)

        self._mem_bank_set(self.USER_BANK)

    class _PinIntRoute:
        """!
        The routing information for an interrupt pin
        """
        def __init__(self):
            self.int_ctrl = 0
            self.md_cfg = 0
            self.emb_func_int = 0
            self.fsm_int_a = 0
            self.fsm_int_b = 0
            self.mlc_int = 0

    def _pin_int1_route_get(self):
        """!
        Get the routing information from registers INT1_CTRL, MD1_CFG,
        EMB_FUNC_INT1, FSM_INT1_A, FSM_INT1_B

        @return **PinIntRoute** The routing information
        """
        route = self._PinIntRoute()

        self._mem_bank_set(self.EMBEDDED_FUNC_BANK)

        route.mlc_int = self._i2c.read_byte(self.address, self.REG_MLC_INT1)
        route.emb_func_int = self._i2c.read_byte(self.address, self.REG_EMB_FUNC_INT1)
        route.fsm_int_a = self._i2c.read_byte(self.address, self.REG_FSM_INT1_A)
        route.fsm_int_b = self._i2c.read_byte(self.address, self.REG_FSM_INT1_B)

        self._mem_bank_set(self.USER_BANK)
        
        route.int_ctrl = self._i2c.read_byte(self.address, self.REG_INT1_CTRL)
        route.md_cfg = self._i2c.read_byte(self.address, self.REG_MD1_CFG)

        return route

    def _pin_int2_route_get(self):
        """!
        Get the routing information from registers INT2_CTRL,  MD2_CFG,
        EMB_FUNC_INT2, FSM_INT2_A, FSM_INT2_B

        @return **PinIntRoute** The routing information
        """
        route = self._PinIntRoute()

        self._mem_bank_set(self.EMBEDDED_FUNC_BANK)

        route.mlc_int = self._i2c.read_byte(self.address, self.REG_MLC_INT2)
        route.emb_func_int = self._i2c.read_byte(self.address, self.REG_EMB_FUNC_INT2)
        route.fsm_int_a = self._i2c.read_byte(self.address, self.REG_FSM_INT2_A)
        route.fsm_int_b = self._i2c.read_byte(self.address, self.REG_FSM_INT2_B)

        self._mem_bank_set(self.USER_BANK)
        
        route.int_ctrl = self._i2c.read_byte(self.address, self.REG_INT2_CTRL)
        route.md_cfg = self._i2c.read_byte(self.address, self.REG_MD2_CFG)

        return route
    
    def _pin_int1_route_set(self, val):
        """!
        Set the routing information to registers INT1_CTRL, MD1_CFG,
        EMB_FUNC_INT1, FSM_INT1_A, FSM_INT1_B

        @param val: **PinIntRoute** The routing information
        """
        self._mem_bank_set(self.EMBEDDED_FUNC_BANK)

        self._i2c.write_byte(self.address, self.REG_MLC_INT1, val.mlc_int)
        self._i2c.write_byte(self.address, self.REG_EMB_FUNC_INT1, val.emb_func_int)
        self._i2c.write_byte(self.address, self.REG_FSM_INT1_A, val.fsm_int_a)
        self._i2c.write_byte(self.address, self.REG_FSM_INT1_B, val.fsm_int_b)

        self._mem_bank_set(self.USER_BANK)

        emb_fun_en = (
            (val.emb_func_int & self.EMB_FUNC_INT1_MASK_FSM_LC) or
            (val.emb_func_int & self.EMB_FUNC_INT1_MASK_SIG_MOT) or
            (val.emb_func_int & self.EMB_FUNC_INT1_MASK_TILT) or
            (val.emb_func_int & self.EMB_FUNC_INT1_MASK_STEP_DETECTOR)
        )

        if emb_fun_en or (val.fsm_int_a) or (val.fsm_int_b) or (val.mlc_int):
            val.md_cfg |= self.MD1_CFG_MASK_INT1_EMB_FUNC
        else:
            val.md_cfg &= ~self.MD1_CFG_MASK_INT1_EMB_FUNC
        
        self._i2c.write_byte(self.address, self.REG_INT1_CTRL, val.int_ctrl)
        self._i2c.write_byte(self.address, self.REG_MD1_CFG, val.md_cfg)

        tap_cfg2 = self._i2c.read_byte(self.address, self.REG_TAP_CFG2)

        ints_enable = (
            (val.md_cfg & self.MD1_CFG_MASK_INT1_SHUB) or
            (val.md_cfg & self.MD1_CFG_MASK_INT1_6D) or
            (val.md_cfg & self.MD1_CFG_MASK_INT1_DOUBLE_TAP) or
            (val.md_cfg & self.MD1_CFG_MASK_INT1_FF) or
            (val.md_cfg & self.MD1_CFG_MASK_INT1_WU) or
            (val.md_cfg & self.MD1_CFG_MASK_INT1_SINGLE_TAP) or
            (val.md_cfg & self.MD1_CFG_MASK_INT1_SLEEP_CHANGE)
        )

        if ints_enable or val.int_ctrl:
            tap_cfg2 |= self.TAP_CFG2_MASK_INTERRUPTS_ENABLE
        else:
            tap_cfg2 &= ~self.TAP_CFG2_MASK_INTERRUPTS_ENABLE

        self._i2c.write_byte(self.address, self.REG_TAP_CFG2, tap_cfg2)

    def _pin_int2_route_set(self, val):
        """!
        Select the signal that needs to route on the int2 pad

        @param val: **PinIntRoute** The routing information
        """
        self._mem_bank_set(self.EMBEDDED_FUNC_BANK)

        self._i2c.write_byte(self.address, self.REG_MLC_INT2, val.mlc_int)
        self._i2c.write_byte(self.address, self.REG_EMB_FUNC_INT2, val.emb_func_int)
        self._i2c.write_byte(self.address, self.REG_FSM_INT2_A, val.fsm_int_a)
        self._i2c.write_byte(self.address, self.REG_FSM_INT2_B, val.fsm_int_b)

        self._mem_bank_set(self.USER_BANK)

        emb_fun_en = (
            (val.emb_func_int & self.EMB_FUNC_INT2_MASK_FSM_LC) or
            (val.emb_func_int & self.EMB_FUNC_INT2_MASK_SIG_MOT) or
            (val.emb_func_int & self.EMB_FUNC_INT2_MASK_TILT) or
            (val.emb_func_int & self.EMB_FUNC_INT2_MASK_STEP_DETECTOR)
        )

        if emb_fun_en or (val.fsm_int_a) or (val.fsm_int_b) or (val.mlc_int):
            val.md_cfg |= self.MD2_CFG_MASK_INT2_EMB_FUNC
        else:
            val.md_cfg &= ~self.MD2_CFG_MASK_INT2_EMB_FUNC
        
        self._i2c.write_byte(self.address, self.REG_INT2_CTRL, val.int_ctrl)
        self._i2c.write_byte(self.address, self.REG_MD2_CFG, val.md_cfg)

        tap_cfg2 = self._i2c.read_byte(self.address, self.REG_TAP_CFG2)

        int_ctrl_en = (
            (val.int_ctrl & self.INT2_CTRL_MASK_INT2_DRDY_XL) or
            (val.int_ctrl & self.INT2_CTRL_MASK_INT2_DRDY_G) or
            (val.int_ctrl & self.INT2_CTRL_MASK_INT2_DRDY_TEMP) or
            (val.int_ctrl & self.INT2_CTRL_MASK_INT2_FIFO_TH) or
            (val.int_ctrl & self.INT2_CTRL_MASK_INT2_FIFO_OVR) or
            (val.int_ctrl & self.INT2_CTRL_MASK_INT2_FIFO_FULL) or
            (val.int_ctrl & self.INT2_CTRL_MASK_INT2_CNT_BDR)
        )

        md2_cfg_en = (
            (val.md_cfg & self.MD2_CFG_MASK_INT2_6D) or
            (val.md_cfg & self.MD2_CFG_MASK_INT2_DOUBLE_TAP) or
            (val.md_cfg & self.MD2_CFG_MASK_INT2_FF) or
            (val.md_cfg & self.MD2_CFG_MASK_INT2_WU) or
            (val.md_cfg & self.MD2_CFG_MASK_INT2_SINGLE_TAP) or
            (val.md_cfg & self.MD2_CFG_MASK_INT2_SLEEP_CHANGE)
        )

        if int_ctrl_en or md2_cfg_en:
            tap_cfg2 |= self.TAP_CFG2_MASK_INTERRUPTS_ENABLE
        else:
            tap_cfg2 &= ~self.TAP_CFG2_MASK_INTERRUPTS_ENABLE
        
        self._i2c.write_byte(self.address, self.REG_TAP_CFG2, tap_cfg2)

        
    def set_accel_status_to_int1(self, enable = True):
        """!
        Sends the accelerometer's data ready signal to interrupt one.

        @param enable: **bool** Enable or disable the accelerometer status to the interrupt pin
        """
        if enable != True and enable != False:
            return

        route = self._pin_int1_route_get()

        route.int_ctrl &= ~self.INT1_CTRL_MASK_INT1_DRDY_XL
        route.int_ctrl |= (enable << self.INT1_CTRL_SHIFT_INT1_DRDY_XL)

        self._pin_int1_route_set(route)
    

    def set_fifo_threshold_int1(self, enable = True):
        """!
        Sends the accelerometer's data ready signal to interrupt one.

        @param enable: **bool** Enable or disable the accelerometer status to the interrupt pin
        """
        if enable != True and enable != False:
            return

        route = self._pin_int1_route_get()

        route.int_ctrl &= ~self.INT1_CTRL_MASK_INT1_FIFO_TH
        route.int_ctrl |= (enable << self.INT1_CTRL_SHIFT_INT1_FIFO_TH)

        self._pin_int1_route_set(route)

    def set_batch_counter_int1(self, enable = True):
        """!
        Sends the accelerometer's data ready signal to interrupt one.

        @param enable: **bool** Enable or disable the accelerometer status to the interrupt pin
        """
        if enable != True and enable != False:
            return

        route = self._pin_int1_route_get()

        route.int_ctrl &= ~self.INT1_CTRL_MASK_INT1_CNT_BDR
        route.int_ctrl |= (enable << self.INT1_CTRL_SHIFT_INT1_CNT_BDR)

        self._pin_int1_route_set(route)

    def set_accel_status_to_int2(self, enable = True):
        """!
        Sends the accelerometer's data ready signal to interrupt two.

        @param enable: **bool** Enable or disable the accelerometer status to the interrupt pin
        """
        if enable != True and enable != False:
            return
        
        route = self._pin_int2_route_get()

        route.int_ctrl &= ~self.INT2_CTRL_MASK_INT2_DRDY_XL
        route.int_ctrl |= (enable << self.INT2_CTRL_SHIFT_INT2_DRDY_XL)

        self._pin_int2_route_set(route)
    
    def set_gyro_status_to_int1(self, enable = True):
        """!
        Sends the gyroscope's data ready signal to interrupt one.

        @param enable: **bool** Enable or disable the gyroscope status to the interrupt pin
        """
        if enable != True and enable != False:
            return
        
        route = self._pin_int1_route_get()

        route.int_ctrl &= ~self.INT1_CTRL_MASK_INT1_DRDY_G
        route.int_ctrl |= (enable << self.INT1_CTRL_SHIFT_INT1_DRDY_G)

        self._pin_int1_route_set(route)

    def set_gyro_status_to_int2(self, enable = True):
        """!
        Sends the gyroscope's data ready signal to interrupt two.

        @param enable: **bool** Enable or disable the gyroscope status to the interrupt pin
        """
        if enable != True and enable != False:
            return
        
        route = self._pin_int2_route_get()

        route.int_ctrl &= ~self.INT2_CTRL_MASK_INT2_DRDY_G
        route.int_ctrl |= (enable << self.INT2_CTRL_SHIFT_INT2_DRDY_G)

        self._pin_int2_route_set(route)

    def set_data_ready_mode(self, val):
        """!
        Sets how the data ready signal is latched i.e. only return zero after interface reading
        OR is pulsed.

        @param val: **int** The data ready mode.

        Possible values:
            - DATA_READY_PULSED
            - DATA_READY_LATCHED
        """
        if val < self.DATA_READY_PULSED or val > self.DATA_READY_LATCHED:
            return

        reg_val = self._i2c.read_byte(self.address, self.REG_CNTR_BDR1)

        reg_val &= ~self.CNTR_BDR1_SHIFT_DATAREADY_PULSED
        reg_val |= (val << self.CNTR_BDR1_SHIFT_DATAREADY_PULSED)

        self._i2c.write_byte(self.address, self.REG_CNTR_BDR1, reg_val)
    
    def set_hub_odr(self, rate):
        """!
        Sets the output data rate for the sensor hub.

        @param rate: **int** The output data rate

        Possible values:
            - SH_ODR_104HZ
            - SH_ODR_52HZ
            - SH_ODR_26HZ
            - SH_ODR_13HZ
        """
        if rate < self.SH_ODR_104HZ or rate > self.SH_ODR_13HZ:
            return
        
        self._mem_bank_set(self.SENSOR_HUB_BANK)

        reg_val = self._i2c.read_byte(self.address, self.REG_SLV0_CONFIG)

        reg_val &= ~self.SLV0_CONFIG_MASK_SHUB_ODR
        reg_val |= (rate << self.SLV0_CONFIG_SHIFT_SHUB_ODR)

        self._i2c.write_byte(self.address, self.REG_SLV0_CONFIG, reg_val)

        self._mem_bank_set(self.USER_BANK)


    def set_hub_sensor_read(self, sensor, address, sub_address, len_data):
        """!
        Sets the general sensor hub settings, which sensor and their I2C address and register
        to read.

        @param sensor: **int** The sensor to read from
        @param address: **int** The I2C address of the sensor
        @param sub_address: **int** The register address of the sensor
        @param len_data: **int** The length of data to read from the sensor
        """
        if sensor < 0 or sensor > 3:
            return
        
        if sensor == 0:
            slv_add_reg = self.REG_SLV0_ADD
            slv_subadd_reg = self.REG_SLV0_SUBADD
            slv_config_reg = self.REG_SLV0_CONFIG
        elif sensor == 1:
            slv_add_reg = self.REG_SLV1_ADDR
            slv_subadd_reg = self.REG_SLV1_SUBADD
            slv_config_reg = self.REG_SLV1_CONFIG
        elif sensor == 2:
            slv_add_reg = self.REG_SLV2_ADDR
            slv_subadd_reg = self.REG_SLV2_SUBADD
            slv_config_reg = self.REG_SLV2_CONFIG
        elif sensor == 3:
            slv_add_reg = self.REG_SLV3_ADDR
            slv_subadd_reg = self.REG_SLV3_SUBADD
            slv_config_reg = self.REG_SLV3_CONFIG
        
        
        self._mem_bank_set(self.SENSOR_HUB_BANK)
        
        # TODO: okay to use slave0 vals for all of this masking since bit pos are the same for all 3 slaves. 
        #       the vendor API explicitly has a different function for each slave, so we might want to switch to that way,
        #       but it creates a lot of duplicated code
        slv_add_val = (address >> 1) << self.SLV0_ADD_SHIFT_SLAVE0
        slv_add_val |= self.SLV0_ADD_MASK_RW0 

        self._i2c.write_byte(self.address, slv_add_reg, slv_add_val)

        self._i2c.write_byte(self.address, slv_subadd_reg, sub_address)

        slv_config_read = self._i2c.read_byte(self.address, slv_config_reg)

        slv_config_read &= ~self.SLV0_CONFIG_MASK_SLAVE0_NUMOP
        slv_config_read |= (len_data << self.SLV0_CONFIG_SHIFT_SLAVE0_NUMOP)

        self._i2c.write_byte(self.address, slv_config_reg, slv_config_read)

        self._mem_bank_set(self.USER_BANK)

    def set_hub_sensor_write(self, address, sub_address, data):
        """!
        Gives settings to the 6DoF to write to an external sensor.

        @param address: **int** The I2C address of the sensor
        @param sub_address: **int** The register address of the sensor
        @param data: **int** The single byte data to write to the sensor
        """
        
        if data < 0 or data > 255:
            return
        
        self._mem_bank_set(self.SENSOR_HUB_BANK)

        slv0_add_val = (address >> 1) << self.SLV0_ADD_SHIFT_SLAVE0
        slv0_add_val &= ~self.SLV0_ADD_MASK_RW0

        self._i2c.write_byte(self.address, self.REG_SLV0_ADD, slv0_add_val)

        self._i2c.write_byte(self.address, self.REG_SLV0_SUBADD, sub_address)

        self._i2c.write_byte(self.address, self.REG_DATAWRITE_SLV0, data)

        self._mem_bank_set(self.USER_BANK)

    def set_number_hub_sensors(self, highest_slave):
        """!
        Sets the number of sensors that the sensor hub will read from.

        @param highest_slave: **int** The highest sensor number to read from (0-3)

        For example, if highest slave is set to 2, the sensor hub will read from sensors 0, 1, and 2.
        """
        if highest_slave < 0 or highest_slave > 3:
            return
        
        self._mem_bank_set(self.SENSOR_HUB_BANK)

        master_config = self._i2c.read_byte(self.address, self.REG_MASTER_CONFIG)

        master_config &= ~self.MASTER_CONFIG_MASK_AUX_SENS_ON
        master_config |= (highest_slave << self.MASTER_CONFIG_SHIFT_AUX_SENS_ON)

        self._i2c.write_byte(self.address, self.REG_MASTER_CONFIG, master_config)

        self._mem_bank_set(self.USER_BANK)

    def enable_sensor_i2c(self, enable = True):
        """!
        Enables the 6DoF as an I2C sensor controller

        @param enable: **bool** Enable or disable the sensor I2C controller
        """

        if enable != 1 and enable != 0:
            return

        self._mem_bank_set(self.SENSOR_HUB_BANK)

        master_config = self._i2c.read_byte(self.address, self.REG_MASTER_CONFIG)

        master_config &= ~self.MASTER_CONFIG_MASK_MASTER_ON
        master_config |= (enable << self.MASTER_CONFIG_SHIFT_MASTER_ON)

        self._i2c.write_byte(self.address, self.REG_MASTER_CONFIG, master_config)

        self._mem_bank_set(self.USER_BANK)

    def read_peripheral_sensor(self, len):
        """!
        Read external sensor data from the sensor hub

        @param len: **int** The number of bytes to read from the sensor

        @return **list** The data read from the sensor
        """

        self._mem_bank_set(self.SENSOR_HUB_BANK)

        data = list(self._i2c.read_bytes(self.address, self.REG_SENSOR_HUB1, len))

        self._mem_bank_set(self.USER_BANK)

        return data

    def _sh_status_get(self): 
        """!
        Read the sensor hub source register

        @return **int** The status of the sensor hub
        """

        self._mem_bank_set(self.SENSOR_HUB_BANK)

        status = self._i2c.read_byte(self.address, self.REG_STATUS_MASTER)

        self._mem_bank_set(self.USER_BANK)

        return status


    def get_hub_status(self):
        """!
        Checks whether communication with the external sensor has concluded.

        @return **bool** Whether communication has ended or not
        """
        status = self._sh_status_get()

        if status & self.STATUS_MASTER_MASK_SENS_HUB_ENDOP:
            return True
        
        return False
    
    def get_external_sensor_nack(self, sensor):
        """!
        Get the NACK status of the external sensor

        @param sensor: **int** The sensor to check
        """
        status = self._sh_status_get()
        
        if sensor == 0:
            return status & self.STATUS_MASTER_MASK_SLAVE0_NACK
        elif sensor == 1:
            return status & self.STATUS_MASTER_MASK_SLAVE1_NACK
        elif sensor == 2:
            return status & self.STATUS_MASTER_MASK_SLAVE2_NACK
        elif sensor == 3:
            return status & self.STATUS_MASTER_MASK_SLAVE3_NACK
        
        return False

    def read_mmc_magnetometer(self, len):
        """!
        Read data from the MMC magnetometer

        @param len: **int** The number of bytes to read from the magnetometer

        @return **list** The data read from the magnetometer
        """
        return self.read_peripheral_sensor(len)
    
    def set_hub_write_mode(self, config):
        """!
        Sets how often the 6DoF should write to the external sensor: once per cycle i.e. output
        data rate, or just once.

        @param config: **int** The write mode

        Possible values:
            - HUB_WRITE_MODE_SINGLE
            - HUB_WRITE_MODE_CYCLE
        """
        if config not in [self.HUB_WRITE_MODE_SINGLE, self.HUB_WRITE_MODE_CYCLE]:
            return
        
        self._mem_bank_set(self.SENSOR_HUB_BANK)

        master_config = self._i2c.read_byte(self.address, self.REG_MASTER_CONFIG)
        master_config &= ~self.MASTER_CONFIG_MASK_WRITE_ONCE
        master_config |= (config << self.MASTER_CONFIG_SHIFT_WRITE_ONCE)
        self._i2c.write_byte(self.address, self.REG_MASTER_CONFIG, master_config)

        self._mem_bank_set(self.USER_BANK)

    def set_hub_pass_through(self, enable = True):
        """!
        Allows the primary I2C data lines to communicate through the auxiliary I2C lines.

        @param enable: **bool** Enable or disable the pass through
        """

        self._mem_bank_set(self.SENSOR_HUB_BANK)

        master_config = self._i2c.read_byte(self.address, self.REG_MASTER_CONFIG)
        master_config &= ~self.MASTER_CONFIG_SHIFT_PASS_THROUGH_MODE
        master_config |= (enable << self.MASTER_CONFIG_SHIFT_PASS_THROUGH_MODE)
        self._i2c.write_byte(self.address, self.REG_MASTER_CONFIG, master_config)

        self._mem_bank_set(self.USER_BANK)

    def set_hub_fifo_batching(self, enable = True):
        """!
        Sets sensor hub FIFO batching

        @param enable: **bool** Enable or disable the FIFO batching
        """
        if enable != 1 and enable != 0:
            return

        self._mem_bank_set(self.SENSOR_HUB_BANK)

        slv0_config = self._i2c.read_byte(self.address, self.REG_SLV0_CONFIG)

        slv0_config &= ~self.SLV0_CONFIG_MASK_BATCH_EXT_SENS0_EN
        slv0_config |= (enable << self.SLV0_CONFIG_SHIFT_BATCH_EXT_SENS0_EN)

        self._i2c.write_byte(self.address, self.REG_SLV0_CONFIG, slv0_config)

        self._mem_bank_set(self.USER_BANK)


    def set_hub_pull_ups(self, enable = True):
        """!
        Enables/Disables internal pullups on SDX/SCX lines

        @param enable: **bool** Enable or disable the pullups
        """
        if enable != 1 and enable != 0:
            return
        
        self._mem_bank_set(self.SENSOR_HUB_BANK)

        master_config = self._i2c.read_byte(self.address, self.REG_MASTER_CONFIG)
        master_config &= ~self.MASTER_CONFIG_MASK_SHUB_PU_EN
        master_config |= (enable << self.MASTER_CONFIG_SHIFT_SHUB_PU_EN)
        self._i2c.write_byte(self.address, self.REG_MASTER_CONFIG, master_config)

        self._mem_bank_set(self.USER_BANK)

    def reset_sensor_hub(self):
        """!
        Resets all settings in the "Master Config" register
        """
        self._mem_bank_set(self.SENSOR_HUB_BANK)

        master_config = self._i2c.read_byte(self.address, self.REG_MASTER_CONFIG)
        master_config |= self.MASTER_CONFIG_MASK_RST_MASTER_REGS
        self._i2c.write_byte(self.address, self.REG_MASTER_CONFIG, master_config)
        master_config &= ~self.MASTER_CONFIG_MASK_RST_MASTER_REGS
        self._i2c.write_byte(self.address, self.REG_MASTER_CONFIG, master_config)

        self._mem_bank_set(self.USER_BANK)


    # Self Test Functions
    def set_accel_self_test(self, val):
        """!
        Linear acceleration sensor self-test enable.

        @param val: **int** Change the values of st_xl in reg CTRL5_C

        Possible values:
            - SELF_TEST_DISABLE
            - SELF_TEST_POSITIVE
            - SELF_TEST_NEGATIVE
        """
        if val not in [self.SELF_TEST_DISABLE, self.SELF_TEST_POSITIVE, self.SELF_TEST_NEGATIVE]:
            return
        
        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL5_C)

        reg_val &= ~self.CTRL5_C_MASK_ST_XL
        reg_val |= (val << self.CTRL5_C_SHIFT_ST_XL)

        self._i2c.write_byte(self.address, self.REG_CTRL5_C, reg_val)

    def set_gyro_self_test(self, val):
        """!
        Angular rate sensor self-test enable

        @param val: **int** Change the values of st_g in reg CTRL5_C

        Possible values:
            - SELF_TEST_DISABLE
            - SELF_TEST_POSITIVE
            - SELF_TEST_NEGATIVE
        """
        if val not in [self.SELF_TEST_DISABLE, self.SELF_TEST_POSITIVE, self.SELF_TEST_NEGATIVE]:
            return
        
        reg_val = self._i2c.read_byte(self.address, self.REG_CTRL5_C)

        reg_val &= ~self.CTRL5_C_MASK_ST_G
        reg_val |= (val << self.CTRL5_C_SHIFT_ST_G)

        self._i2c.write_byte(self.address, self.REG_CTRL5_C, reg_val)

    # Status Checking Functions

    def check_status(self):
        """!
        Checks if data is ready for both the acclerometer and the gyroscope

        @return **bool** If data is ready for both sensors
        """
        status = self._i2c.read_byte(self.address, self.REG_STATUS)

        if status & self.STATUS_MASK_XLDA and status & self.STATUS_MASK_GDA:
            return True
        
        return False
    
    def check_accel_status(self):
        """!
        Checks if data is ready for the accelerometer

        @return **bool** If data is ready for the accelerometer
        """
        status = self._i2c.read_byte(self.address, self.REG_STATUS)

        if status & self.STATUS_MASK_XLDA:
            return True
        
        return False
    
    def check_gyro_status(self):
        """!
        Checks if data is ready for the gyroscope
        """
        status = self._i2c.read_byte(self.address, self.REG_STATUS)

        if status & self.STATUS_MASK_GDA:
            return True
        
        return False
    
    def check_temp_status(self):
        """!
        Checks if data is ready for the temperature sensor
        """
        status = self._i2c.read_byte(self.address, self.REG_STATUS)

        if status & self.STATUS_MASK_TDA:
            return True
        
        return False
