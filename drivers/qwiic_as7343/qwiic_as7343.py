#-------------------------------------------------------------------------------
# qwiic_as7343.py
#
# Python library for the SparkFun Qwiic AS7343, available here:
# https://www.sparkfun.com/products/TODO
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, May 2025
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2025 SparkFun Electronics
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
qwiic_as7343
============
Python module for the [SparkFun Qwiic AS7343](https://www.sparkfun.com/products/TODO)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_AS7343_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic AS7343"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x39] 

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicAS7343(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # --------- Constant Variables ---------
    NUM_CHANNELS = 18
    DEFAULT_AS7343_DEVICE_ID = 0x81; 
    
    # ----------- Register Bank Settings -----------
    REG_BANK0 = 0x00  # Register bank 0 (default)
    REG_BANK1 = 0x01  # Register bank 1

    # ----------- Sensor Channels -----------
    # Use these to access each channel individually from the _data array in the class.
    # The channels are defined in the datasheet as FZ, FY, FXL, NIR, 2xVIS, FD, F1-F8.
    # When AutoSmux is set to 18 channels, the channels are in this order:
    # Cycle 1: FZ, FY, FXL, NIR, 2xVIS, FD
    # Cycle 2: F2, F3, F4, F6, 2xVIS, FD
    # Cycle 3: F1, F7, F8, F5, 2xVIS, FD
    CH_BLUE_FZ_450NM = 0x00  # Blue peak wavelength 450 nanometers (cycle 1)
    CH_GREEN_FY_555NM = 0x01  # Green (wide bandwidth) peak wavelength 555 nanometers (cycle 1)
    CH_ORANGE_FXL_600NM = 0x02  # Orange peak wavelength 600 nanometers (cycle 1)
    CH_NIR_855NM = 0x03  # NIR peak wavelength 855 nanometers (cycle 1)
    CH_VIS1 = 0x04  # VIS (cycle 1)
    CH_FD1 = 0x05  # Flicker Detection (cycle 1)
    CH_DARK_BLUE_F2_425NM = 0x06  # Dark Blue peak wavelength 425 nanometers (cycle 2)
    CH_LIGHT_BLUE_F3_475NM = 0x07  # Light Blue peak wavelength 475 nanometers (cycle 2)
    CH_BLUE_F4_515NM = 0x08  # Blue peak wavelength 515 nanometers (cycle 2)
    CH_BROWN_F6_640NM = 0x09  # Brown peak wavelength 640 nanometers (cycle 2)
    CH_VIS2 = 0x0A  # VIS (cycle 2)
    CH_FD2 = 0x0B  # Flicker Detection (cycle 2)
    CH_PURPLE_F1_405NM = 0x0C  # Purple peak wavelength 405 nanometers (cycle 3)
    CH_RED_F7_690NM = 0x0D  # Red peak wavelength 690 nanometers (cycle 3)
    CH_DARK_RED_F8_745NM = 0x0E  # Dark Red peak wavelength 745 nanometers (cycle 3)
    CH_GREEN_F5_550NM = 0x0F  # Green (Narrow bandwidth) peak wavelength 550 nanometers (cycle 3)
    CH_VIS3 = 0x10  # VIS (cycle 3)
    CH_FD3 = 0x11  # Flicker Detection (cycle 3)

    # ----------- Sensor Gain Settings -----------
    AGAIN_0_5 = 0x00  # 0.5x gain
    AGAIN_1 = 0x01
    AGAIN_2 = 0x02
    AGAIN_4 = 0x03
    AGAIN_8 = 0x04
    AGAIN_16 = 0x05
    AGAIN_32 = 0x06
    AGAIN_64 = 0x07
    AGAIN_128 = 0x08
    AGAIN_256 = 0x09
    AGAIN_512 = 0x0A
    AGAIN_1024 = 0x0B
    AGAIN_2048 = 0x0C

    # ----------- Flicker Detection Gain Settings -----------
    FD_GAIN_0_5 = 0x00  # 0.5x gain
    FD_GAIN_1 = 0x01
    FD_GAIN_2 = 0x02
    FD_GAIN_4 = 0x03
    FD_GAIN_8 = 0x04
    FD_GAIN_16 = 0x05
    FD_GAIN_32 = 0x06
    FD_GAIN_64 = 0x07
    FD_GAIN_128 = 0x08
    FD_GAIN_256 = 0x09
    FD_GAIN_512 = 0x0A
    FD_GAIN_1024 = 0x0B
    FD_GAIN_2048 = 0x0C

    # ----------- FIFO Threshold Settings -----------
    FIFO_THRESHOLD_LVL_1 = 0x00
    FIFO_THRESHOLD_LVL_4 = 0x01
    FIFO_THRESHOLD_LVL_8 = 0x02
    FIFO_THRESHOLD_LVL_16 = 0x03

    # ----------- Spectral Threshold Channel -----------
    SPECTRAL_THRESHOLD_CHANNEL_0 = 0x00
    SPECTRAL_THRESHOLD_CHANNEL_1 = 0x01
    SPECTRAL_THRESHOLD_CHANNEL_2 = 0x02
    SPECTRAL_THRESHOLD_CHANNEL_3 = 0x03
    SPECTRAL_THRESHOLD_CHANNEL_4 = 0x04
    SPECTRAL_THRESHOLD_CHANNEL_5 = 0x05

    # ----------- Automatic Channel Read-out -----------
    AUTO_SMUX_6_CHANNELS = 0x00  # 6 channel readout
    AUTO_SMUX_12_CHANNELS = 0x02  # 12 channel readout
    AUTO_SMUX_18_CHANNELS = 0x03  # 18 channel readout

    # ----------- GPIO Mode Settings -----------
    GPIO_MODE_INPUT = 0x00  # GPIO set to input mode
    GPIO_MODE_OUTPUT = 0x01  # GPIO set to output mode

    # ----------- GPIO Output Settings -----------
    GPIO_OUTPUT_LOW = 0x00  # GPIO set to low
    GPIO_OUTPUT_HIGH = 0x01  # GPIO set to high

    # Register Definitions:
    # ----------- AUX ID Register ----------- 
    REG_AUX_ID = 0x58

    SHIFT_AUX_ID = 0

    MASK_AUX_ID = 0b1111 << SHIFT_AUX_ID

    # ----------- REV ID Register ----------- 
    REG_REV_ID = 0x59

    SHIFT_REV_ID = 0
    
    MASK_REV_ID = 0b111 << SHIFT_REV_ID

    # ----------- ID Register ----------- 
    REG_ID = 0x5A
    # Register is a single 8bit value

    # ----------- CFG12 Register -----------
    REG_CFG12 = 0x66

    SHIFT_CFG12_RESERVED = 0
    SHIFT_CFG12_SP_TH_CH = 5

    MASK_CFG12_RESERVED = 0b11111 << SHIFT_CFG12_RESERVED
    MASK_CFG12_SP_TH_CH = 0b111 << SHIFT_CFG12_SP_TH_CH

    # ----------- Enable Register ----------- 
    REG_ENABLE = 0x80

    SHIFT_ENABLE_PON = 0
    SHIFT_ENABLE_SP_EN = 1
    SHIFT_ENABLE_WEN = 3
    SHIFT_ENABLE_SMUX_EN = 4
    SHIFT_ENABLE_FDEN = 6
    SHIFT_ENABLE_ENABLE = 8

    MASK_ENABLE_PON = 0b1 << SHIFT_ENABLE_PON
    MASK_ENABLE_SP_EN = 0b1 << SHIFT_ENABLE_SP_EN
    MASK_ENABLE_WEN = 0b1 << SHIFT_ENABLE_WEN
    MASK_ENABLE_SMUX_EN = 0b1 << SHIFT_ENABLE_SMUX_EN
    MASK_ENABLE_FDEN = 0b1 << SHIFT_ENABLE_FDEN
    MASK_ENABLE_ENABLE = 0b1 << SHIFT_ENABLE_ENABLE

    # ----------- ATime Register -----------
    REG_A_TIME = 0x81 # Register Address, register is a single uint8_t.

    # ----------- WTime Register -----------
    REG_W_TIME = 0x83 # Register Address, register is a single uint8_t.


    # ----------- SP TH L Register -----------
    REG_SP_TH_L = 0x84

    SHIFT_SP_TH_L_SP_TH_LSB = 0
    SHIFT_SP_TH_L_SP_TH_MSB = 8

    MASK_SP_TH_L_SP_TH_LSB = 0xFF << SHIFT_SP_TH_L_SP_TH_LSB
    MASK_SP_TH_L_SP_TH_MSB = 0xFF << SHIFT_SP_TH_L_SP_TH_MSB

    # ----------- SP TH H Register -----------
    REG_SP_TH_H = 0x86

    SHIFT_SP_TH_H_SP_TH_LSB = 0
    SHIFT_SP_TH_H_SP_TH_MSB = 8

    MASK_SP_TH_H_SP_TH_LSB = 0xFF << SHIFT_SP_TH_H_SP_TH_LSB
    MASK_SP_TH_H_SP_TH_MSB = 0xFF << SHIFT_SP_TH_H_SP_TH_MSB

    # ----------- Status Register -----------
    REG_STATUS = 0x93

    SHIFT_STATUS_SINT = 0
    SHIFT_STATUS_FINT = 2
    SHIFT_STATUS_AINT = 3
    SHIFT_STATUS_ASAT = 7

    MASK_STATUS_SINT = 0b1 << SHIFT_STATUS_SINT
    MASK_STATUS_FINT = 0b1 << SHIFT_STATUS_FINT
    MASK_STATUS_AINT = 0b1 << SHIFT_STATUS_AINT
    MASK_STATUS_ASAT = 0b1 << SHIFT_STATUS_ASAT

    # ----------- A Status Register -----------
    REG_A_STATUS = 0x94

    SHIFT_A_STATUS_AGAIN_STATUS = 0
    SHIFT_A_STATUS_ASAT_STATUS = 7

    MASK_A_STATUS_AGAIN_STATUS = 0b1111 << SHIFT_A_STATUS_AGAIN_STATUS
    MASK_A_STATUS_ASAT_STATUS = 0b1 << SHIFT_A_STATUS_ASAT_STATUS

    # ----------- Data Registers -----------
    REG_DATA0 = 0x95
    REG_DATA1 = 0x97
    REG_DATA2 = 0x99
    REG_DATA3 = 0x9B
    REG_DATA4 = 0x9D
    REG_DATA5 = 0x9F
    REG_DATA6 = 0xA1
    REG_DATA7 = 0xA3
    REG_DATA8 = 0xA5
    REG_DATA9 = 0xA7
    REG_DATA10 = 0xA9
    REG_DATA11 = 0xAB
    REG_DATA12 = 0xAD
    REG_DATA13 = 0xAF
    REG_DATA14 = 0xB1
    REG_DATA15 = 0xB3
    REG_DATA16 = 0xB5
    REG_DATA17 = 0xB7

    SHIFT_DATA_LSB = 0
    SHIFT_DATA_MSB = 8

    MASK_DATA_LSB = 0xFF << SHIFT_DATA_LSB
    MASK_DATA_MSB = 0xFF << SHIFT_DATA_MSB

    # ----------- Status 2 Register -----------
    REG_STATUS2 = 0x90

    SHIFT_STATUS2_FDSAT_DIG = 0
    SHIFT_STATUS2_FDSAT_ANA = 1
    SHIFT_STATUS2_ASAT_ANA = 3
    SHIFT_STATUS2_ASAT_DIG = 4
    SHIFT_STATUS2_AVALID = 6

    MASK_STATUS2_FDSAT_DIG = 0b1 << SHIFT_STATUS2_FDSAT_DIG
    MASK_STATUS2_FDSAT_ANA = 0b1 << SHIFT_STATUS2_FDSAT_ANA
    MASK_STATUS2_ASAT_ANA = 0b1 << SHIFT_STATUS2_ASAT_ANA
    MASK_STATUS2_ASAT_DIG = 0b1 << SHIFT_STATUS2_ASAT_DIG
    MASK_STATUS2_AVALID = 0b1 << SHIFT_STATUS2_AVALID

    # ----------- Status 3 Register -----------
    REG_STATUS3 = 0x91

    SHIFT_STATUS3_INT_SP_L = 4
    SHIFT_STATUS3_INT_SP_H = 5

    MASK_STATUS3_INT_SP_L = 0b1 << SHIFT_STATUS3_INT_SP_L
    MASK_STATUS3_INT_SP_H = 0b1 << SHIFT_STATUS3_INT_SP_H

    # ----------- Status 4 Register -----------
    REG_STATUS4 = 0xBC

    SHIFT_STATUS4_INT_BUSY = 0
    SHIFT_STATUS4_SAI_ACT = 1
    SHIFT_STATUS4_SP_TRIG = 2
    SHIFT_STATUS4_FD_TRIG = 4
    SHIFT_STATUS4_OV_TEMP = 5
    SHIFT_STATUS4_FIFO_OV = 7

    MASK_STATUS4_INT_BUSY = 0b1 << SHIFT_STATUS4_INT_BUSY
    MASK_STATUS4_SAI_ACT = 0b1 << SHIFT_STATUS4_SAI_ACT
    MASK_STATUS4_SP_TRIG = 0b1 << SHIFT_STATUS4_SP_TRIG
    MASK_STATUS4_FD_TRIG = 0b1 << SHIFT_STATUS4_FD_TRIG
    MASK_STATUS4_OV_TEMP = 0b1 << SHIFT_STATUS4_OV_TEMP
    MASK_STATUS4_FIFO_OV = 0b1 << SHIFT_STATUS4_FIFO_OV

    # ----------- Status 5 Register -----------
    REG_STATUS5 = 0x93

    SHIFT_STATUS5_SINT_SMUX = 2
    SHIFT_STATUS5_SINT_FD = 3
    SHIFT_STATUS5_RESERVED = 4
    SHIFT_STATUS5_RESERVED_ONE = 6

    MASK_STATUS5_SINT_SMUX = 0b1 << SHIFT_STATUS5_SINT_SMUX
    MASK_STATUS5_SINT_FD = 0b1 << SHIFT_STATUS5_SINT_FD
    MASK_STATUS5_RESERVED = 0b11 << SHIFT_STATUS5_RESERVED
    MASK_STATUS5_RESERVED_ONE = 0b111 << SHIFT_STATUS5_RESERVED_ONE

    # ----------- FD Status Register -----------
    REG_FD_STATUS = 0xE3

    SHIFT_FD_STATUS_FD_100HZ_DET = 0
    SHIFT_FD_STATUS_FD_120HZ_DET = 1
    SHIFT_FD_STATUS_FD_100HZ_VALID = 2
    SHIFT_FD_STATUS_FD_120HZ_VALID = 3
    SHIFT_FD_STATUS_FD_SATURATION = 4
    SHIFT_FD_STATUS_FD_MEAS_VALID = 5

    MASK_FD_STATUS_FD_100HZ_DET = 0b1 << SHIFT_FD_STATUS_FD_100HZ_DET
    MASK_FD_STATUS_FD_120HZ_DET = 0b1 << SHIFT_FD_STATUS_FD_120HZ_DET
    MASK_FD_STATUS_FD_100HZ_VALID = 0b1 << SHIFT_FD_STATUS_FD_100HZ_VALID
    MASK_FD_STATUS_FD_120HZ_VALID = 0b1 << SHIFT_FD_STATUS_FD_120HZ_VALID
    MASK_FD_STATUS_FD_SATURATION = 0b1 << SHIFT_FD_STATUS_FD_SATURATION
    MASK_FD_STATUS_FD_MEAS_VALID = 0b1 << SHIFT_FD_STATUS_FD_MEAS_VALID

    # ----------- Cfg0 Register -----------
    REG_CFG0 = 0xBF

    SHIFT_CFG0_WLONG = 2
    SHIFT_CFG0_REG_BANK = 4
    SHIFT_CFG0_LOW_POWER = 5

    MASK_CFG0_WLONG = 0b1 << SHIFT_CFG0_WLONG
    MASK_CFG0_REG_BANK = 0b1 << SHIFT_CFG0_REG_BANK
    MASK_CFG0_LOW_POWER = 0b1 << SHIFT_CFG0_LOW_POWER

    # ----------- Cfg1 Register -----------
    REG_CFG1 = 0xC6

    SHIFT_CFG1_AGAIN = 0

    MASK_CFG1_AGAIN = 0b11111 << SHIFT_CFG1_AGAIN

    # ----------- Cfg3 Register -----------
    REG_CFG3 = 0xC7

    SHIFT_CFG3_SAI = 4

    MASK_CFG3_SAI = 0b1 << SHIFT_CFG3_SAI

    # ----------- Cfg6 Register -----------
    REG_CFG6 = 0xF5

    SHIFT_CFG6_SMUX_CMD = 3

    MASK_CFG6_SMUX_CMD = 0b11 << SHIFT_CFG6_SMUX_CMD

    # ----------- Cfg8 Register -----------
    REG_CFG8 = 0xC9

    SHIFT_CFG8_FIFO_TH = 6

    MASK_CFG8_FIFO_TH = 0b11 << SHIFT_CFG8_FIFO_TH

    # ----------- Cfg9 Register -----------
    REG_CFG9 = 0xCA

    SHIFT_CFG9_SIENC_SMUX = 5
    SHIFT_CFG9_SIENC_FD = 7

    MASK_CFG9_SIENC_SMUX = 0b1 << SHIFT_CFG9_SIENC_SMUX
    MASK_CFG9_SIENC_FD = 0b1 << SHIFT_CFG9_SIENC_FD

    # ----------- Cfg10 Register -----------
    REG_CFG10 = 0x65

    SHIFT_CFG10_FD_PERS = 0

    MASK_CFG10_FD_PERS = 0b111 << SHIFT_CFG10_FD_PERS

    # ----------- Pers Register -----------
    REG_PERS = 0xCF

    SHIFT_PERS_APERS = 0

    MASK_PERS_APERS = 0b1111 << SHIFT_PERS_APERS

    # ----------- Gpio Register -----------
    REG_GPIO = 0x6B

    SHIFT_GPIO_IN = 0
    SHIFT_GPIO_OUT = 1
    SHIFT_GPIO_IN_EN = 2
    SHIFT_GPIO_INV = 3

    MASK_GPIO_IN = 0b1 << SHIFT_GPIO_IN
    MASK_GPIO_OUT = 0b1 << SHIFT_GPIO_OUT
    MASK_GPIO_IN_EN = 0b1 << SHIFT_GPIO_IN_EN
    MASK_GPIO_INV = 0b1 << SHIFT_GPIO_INV

    # ----------- AStep Register -----------
    REG_A_STEP = 0xD4

    SHIFT_A_STEP_L = 0
    SHIFT_A_STEP_H = 8

    MASK_A_STEP_L = 0xFF << SHIFT_A_STEP_L
    MASK_A_STEP_H = 0xFF << SHIFT_A_STEP_H

    # ----------- Cfg20 Register -----------
    REG_CFG20 = 0xD6

    SHIFT_CFG20_AUTO_SMUX = 5
    SHIFT_CFG20_FD_FIFO8B = 7

    MASK_CFG20_AUTO_SMUX = 0b11 << SHIFT_CFG20_AUTO_SMUX
    MASK_CFG20_FD_FIFO8B = 0b1 << SHIFT_CFG20_FD_FIFO8B

    # ----------- Led Register -----------
    REG_LED = 0xCD

    SHIFT_LED_DRIVE = 0
    SHIFT_LED_ACT = 7

    MASK_LED_DRIVE = 0b1111111 << SHIFT_LED_DRIVE
    MASK_LED_ACT = 0b1 << SHIFT_LED_ACT

    # ----------- Agc Gain Max Register -----------
    REG_AGC_GAIN_MAX = 0xD7

    SHIFT_AGC_GAIN_MAX = 4

    MASK_AGC_GAIN_MAX = 0b1111 << SHIFT_AGC_GAIN_MAX

    # ----------- Az Config Register -----------
    REG_AZ_CONFIG = 0xDE

    # Register is a single 8-bit value

    # ----------- Fd Time1 Register -----------
    REG_FD_TIME1 = 0xE0

    # Register is a single 8-bit value

    # ----------- Fd Time2 Register -----------
    REG_FD_TIME2 = 0xE2

    SHIFT_FD_TIME2_FD_TIME_H = 0
    SHIFT_FD_TIME2_FD_GAIN = 3

    MASK_FD_TIME2_FD_TIME_H = 0b111 << SHIFT_FD_TIME2_FD_TIME_H
    MASK_FD_TIME2_FD_GAIN = 0b11111 << SHIFT_FD_TIME2_FD_GAIN

    # ----------- Fd Time Cfg0 Register -----------
    REG_FD_TIME_CFG0 = 0xDF

    SHIFT_FD_TIME_CFG0_FIFO_WRITE_FD = 7

    MASK_FD_TIME_CFG0_FIFO_WRITE_FD = 0b1 << SHIFT_FD_TIME_CFG0_FIFO_WRITE_FD

    # ----------- Int Enab Register -----------
    REG_INT_ENAB = 0xF9

    SHIFT_INT_ENAB_SEIN = 0
    SHIFT_INT_ENAB_FIEN = 2
    SHIFT_INT_ENAB_SP_IEN = 3
    SHIFT_INT_ENAB_ASIEN = 7

    MASK_INT_ENAB_SEIN = 0b1 << SHIFT_INT_ENAB_SEIN
    MASK_INT_ENAB_FIEN = 0b1 << SHIFT_INT_ENAB_FIEN
    MASK_INT_ENAB_SP_IEN = 0b1 << SHIFT_INT_ENAB_SP_IEN
    MASK_INT_ENAB_ASIEN = 0b1 << SHIFT_INT_ENAB_ASIEN

    # ----------- Control Register -----------
    REG_CONTROL = 0xFA

    SHIFT_CONTROL_CLEAR_SAI_ACT = 0
    SHIFT_CONTROL_FIFO_CLR = 1
    SHIFT_CONTROL_SP_MAN_AZ = 2
    SHIFT_CONTROL_SW_RESET = 3

    MASK_CONTROL_CLEAR_SAI_ACT = 0b1 << SHIFT_CONTROL_CLEAR_SAI_ACT
    MASK_CONTROL_FIFO_CLR = 0b1 << SHIFT_CONTROL_FIFO_CLR
    MASK_CONTROL_SP_MAN_AZ = 0b1 << SHIFT_CONTROL_SP_MAN_AZ
    MASK_CONTROL_SW_RESET = 0b1 << SHIFT_CONTROL_SW_RESET

    # ----------- Fifo Map Register -----------
    REG_FIFO_MAP = 0xFC

    SHIFT_FIFO_MAP_FIFO_WRITE_A_STATUS = 0
    SHIFT_FIFO_MAP_FIFO_WRITE_CH0_DATA = 1
    SHIFT_FIFO_MAP_FIFO_WRITE_CH1_DATA = 2
    SHIFT_FIFO_MAP_FIFO_WRITE_CH2_DATA = 3
    SHIFT_FIFO_MAP_FIFO_WRITE_CH3_DATA = 4
    SHIFT_FIFO_MAP_FIFO_WRITE_CH4_DATA = 5
    SHIFT_FIFO_MAP_FIFO_WRITE_CH5_DATA = 6

    MASK_FIFO_MAP_FIFO_WRITE_A_STATUS = 0b1 << SHIFT_FIFO_MAP_FIFO_WRITE_A_STATUS
    MASK_FIFO_MAP_FIFO_WRITE_CH0_DATA = 0b1 << SHIFT_FIFO_MAP_FIFO_WRITE_CH0_DATA
    MASK_FIFO_MAP_FIFO_WRITE_CH1_DATA = 0b1 << SHIFT_FIFO_MAP_FIFO_WRITE_CH1_DATA
    MASK_FIFO_MAP_FIFO_WRITE_CH2_DATA = 0b1 << SHIFT_FIFO_MAP_FIFO_WRITE_CH2_DATA
    MASK_FIFO_MAP_FIFO_WRITE_CH3_DATA = 0b1 << SHIFT_FIFO_MAP_FIFO_WRITE_CH3_DATA
    MASK_FIFO_MAP_FIFO_WRITE_CH4_DATA = 0b1 << SHIFT_FIFO_MAP_FIFO_WRITE_CH4_DATA
    MASK_FIFO_MAP_FIFO_WRITE_CH5_DATA = 0b1 << SHIFT_FIFO_MAP_FIFO_WRITE_CH5_DATA

    # ----------- Fifo Lvl Register -----------
    REG_FIFO_LVL = 0xFD

    # Register is a single 8-bit value

    # ----------- FData Register -----------
    REG_F_DATA = 0xFE

    SHIFT_F_DATA_L = 0
    SHIFT_F_DATA_H = 8

    MASK_F_DATA_L = 0xFF << SHIFT_F_DATA_L
    MASK_F_DATA_H = 0xFF << SHIFT_F_DATA_H


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

        self._data = [None] * self.NUM_CHANNELS

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        if not self._i2c.is_device_connected(self.address):
            return False

        # Check that Part Number Identifier is correct (read only and should always be 0x81)
        if self.get_device_id() != self.DEFAULT_AS7343_DEVICE_ID:
            return False
        
        return True

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        return self.is_connected()

    def set_register_bank(self, bank):
        """!
        Sets the register bank for the device

        @param bank: **int** The register bank to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the bank is valid
        if bank not in [self.REG_BANK0, self.REG_BANK1]:
            return False

        # Read the current cfg0 register
        cfg0 = self._i2c.read_byte(self.address, self.REG_CFG0)

        # Clear the register bank bits
        cfg0 &= ~self.MASK_CFG0_REG_BANK

        # Set the new register bank
        cfg0 |= (bank << self.SHIFT_CFG0_REG_BANK) & self.MASK_CFG0_REG_BANK

        # Write the new cfg0 register value
        self._i2c.write_byte(self.address, self.REG_CFG0, cfg0)
        return True

    def read_register(self, register):
        """!
        Reads a single byte from the specified register

        @param register: **int** The register to read from

        @return **int** The value read from the register
        """
        
        # Set the register bank as needed to access the specified register.
        # if the desired register is equal to or greater than 0x80, set bank 0.
        # Otherwise, set bank 1.
        if register >= 0x80:
            self.set_register_bank(self.REG_BANK0)
        else:
            self.set_register_bank(self.REG_BANK1)

        # Read the register value
        return self._i2c.read_byte(self.address, register)
    
    def get_device_id(self):
        """!
        Gets the device ID of the AS7343

        @return **int** The device ID
        """
        # Read the device ID register
        return self.read_register(self.REG_ID)
    
    def power_on(self, enable=True):
        """!
        Powers on the AS7343

        @param enable: **bool** `True` to power on, `False` to power off

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current enable register
        enable_reg = self.read_register(self.REG_ENABLE)

        # Set the power on bit
        if enable:
            enable_reg |= self.MASK_ENABLE_PON
        else:
            enable_reg &= ~self.MASK_ENABLE_PON

        # Write the new enable register value
        self._i2c.write_byte(self.address, self.REG_ENABLE, enable_reg)
        return True
    
    def power_off(self):
        """!
        Powers off the AS7343

        @return **bool** `True` if successful, otherwise `False`
        """
        return self.power_on(False)
    
    def spectral_measurement_enable(self, enable=True):
        """!
        Enables or disables spectral measurement

        @param enable: **bool** `True` to enable, `False` to disable

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current enable register
        enable_reg = self.read_register(self.REG_ENABLE)

        # Set the spectral measurement enable bit
        if enable:
            enable_reg |= self.MASK_ENABLE_SP_EN
        else:
            enable_reg &= ~self.MASK_ENABLE_SP_EN

        # Write the new enable register value
        self._i2c.write_byte(self.address, self.REG_ENABLE, enable_reg)
        return True
    
    def spectral_measurement_disable(self):
        """!
        Disables spectral measurement

        @return **bool** `True` if successful, otherwise `False`
        """
        return self.spectral_measurement_enable(False)
    
    def read_all_spectral_data(self):
        """!
        Reads all spectral data from the AS7343

        @return None
        """
        
        # Set the register bank to bank 0 to access the data registers
        self.set_register_bank(self.REG_BANK0)

        # Read the spectral data registers
        for i in range(self.NUM_CHANNELS):
            self._data[i] = (self._i2c.read_word(self.address, self.REG_DATA0 + (i * 2)))

    
    def get_data(self, channel):
        """!
        Gets the data for a specific channel

        @param channel: **int** The channel to get data from

        @return **int** The data for the specified channel or `None` if invalid
        """
        # Check if the channel is valid
        if channel < 0 or channel >= self.NUM_CHANNELS:
            return None

        # Return the data for the specified channel
        return self._data[channel]
        
    def set_auto_smux(self, auto_smux):
        """!
        Sets the automatic SMUX mode

        @param auto_smux: **int** The automatic SMUX mode to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the auto SMUX mode is valid
        if auto_smux not in [self.AUTO_SMUX_6_CHANNELS, self.AUTO_SMUX_12_CHANNELS, self.AUTO_SMUX_18_CHANNELS]:
            return False

        # Read the current cfg20 register
        cfg20 = self.read_register(self.REG_CFG20)

        # Clear the automatic SMUX bits
        cfg20 &= ~self.MASK_CFG20_AUTO_SMUX

        # Set the new automatic SMUX mode
        cfg20 |= (auto_smux << self.SHIFT_CFG20_AUTO_SMUX) & self.MASK_CFG20_AUTO_SMUX

        # Write the new cfg20 register value
        self._i2c.write_byte(self.address, self.REG_CFG20, cfg20)
        return True
    
    def set_led_on(self, led_on = True):
        """!
        Sets the LED state

        @param led_on: **bool** `True` to turn on the LED, `False` to turn it off

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current LED register
        led_reg = self.read_register(self.REG_LED)

        # Set the LED state
        if led_on:
            led_reg |= self.MASK_LED_ACT
        else:
            led_reg &= ~self.MASK_LED_ACT

        # Write the new LED register value
        self._i2c.write_byte(self.address, self.REG_LED, led_reg)
        return True
    
    def set_led_off(self):
        """!
        Turns off the LED

        @return **bool** `True` if successful, otherwise `False`
        """
        return self.set_led_on(False)
    
    def set_led_drive(self, drive):
        """!
        Sets the LED drive current

        @param drive: **int** The LED drive current to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the drive current is valid
        if drive < 0 or drive > 127:
            return False

        # Read the current LED register
        led_reg = self.read_register(self.REG_LED)

        # Set the LED drive current
        led_reg &= ~self.MASK_LED_DRIVE
        led_reg |= (drive << self.SHIFT_LED_DRIVE) & self.MASK_LED_DRIVE

        # Write the new LED register value
        self._i2c.write_byte(self.address, self.REG_LED, led_reg)
        return True
    
    def get_red(self):
        """!
        Gets the red channel data

        @return **int** The red channel data
        """
        return self.get_data(self.CH_RED_F7_690NM)
    
    def get_green(self):
        """!
        Gets the green channel data

        @return **int** The green channel data
        """
        return self.get_data(self.CH_GREEN_F5_550NM)
    
    def get_blue(self):
        """!
        Gets the blue channel data

        @return **int** The blue channel data
        """
        return self.get_data(self.CH_BLUE_FZ_450NM)
    
    def get_nir(self):
        """!
        Gets the NIR channel data

        @return **int** The NIR channel data
        """
        return self.get_data(self.CH_NIR_855NM)
    
    # TODO: Check endianness for these write_words
    def set_spectral_int_threshold_high(self, sp_th_h):
        """!
        Sets the spectral intensity threshold high value

        @param sp_th_h: The spectral intensity threshold high value (16-bit, 0 to 65535)

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the spectral intensity threshold high value is valid
        if sp_th_h < 0 or sp_th_h > 0xFFFF:
            return False
    
        # Right the full 16-bit value to the register
        self._i2c.write_word(self.address, self.REG_SP_TH_H, sp_th_h)
        return True
    
    def set_spectral_int_threshold_low(self, sp_th_l):
        """!
        Sets the spectral intensity threshold low value

        @param sp_th_l: The spectral intensity threshold low value (16-bit, 0 to 65535)

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the spectral intensity threshold low value is valid
        if sp_th_l < 0 or sp_th_l > 0xFFFF:
            return False
    
        # Right the full 16-bit value to the register
        self._i2c.write_word(self.address, self.REG_SP_TH_L, sp_th_l)
        return True
    
    def spectral_int_enable(self, enable=True):
        """!
        Enables or disables spectral intensity measurement

        @param enable: **bool** `True` to enable, `False` to disable

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current cfg20 register
        int_enab = self.read_register(self.REG_INT_ENAB)

        # Set the spectral intensity enable bit
        if enable:
            int_enab |= self.MASK_INT_ENAB_SP_IEN
        else:
            int_enab &= ~self.MASK_INT_ENAB_SP_IEN

        # Write the new INT_ENAB register value
        self._i2c.write_byte(self.address, self.REG_INT_ENAB, int_enab)
        return True
    
    def spectral_int_disable(self):
        """!
        Disables spectral intensity measurement

        @return **bool** `True` if successful, otherwise `False`
        """
        return self.spectral_int_enable(False)
    
    def set_spectral_threshold_channel(self, channel):
        """!
        Sets the spectral threshold channel

        @param channel: **int** The spectral threshold channel to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the spectral threshold channel is valid
        if channel not in [self.SPECTRAL_THRESHOLD_CHANNEL_0, self.SPECTRAL_THRESHOLD_CHANNEL_1,
                           self.SPECTRAL_THRESHOLD_CHANNEL_2, self.SPECTRAL_THRESHOLD_CHANNEL_3,
                           self.SPECTRAL_THRESHOLD_CHANNEL_4, self.SPECTRAL_THRESHOLD_CHANNEL_5]:
            return False

        # Read the current cfg12 register
        cfg12 = self.read_register(self.REG_CFG12)

        # Clear the spectral threshold channel bits
        cfg12 &= ~self.MASK_CFG12_SP_TH_CH

        # Set the new spectral threshold channel
        cfg12 |= (channel << self.SHIFT_CFG12_SP_TH_CH) & self.MASK_CFG12_SP_TH_CH

        # Write the new cfg12 register value
        self._i2c.write_byte(self.address, self.REG_CFG12, cfg12)
        return True

    def get_system_interrupt_status(self):
        """!
        Gets the system interrupt status

        @return **bool** The system interrupt status
        """
        # Read the status register
        status = self.read_register(self.REG_STATUS)

        # Check if the system interrupt is set
        return (status & self.MASK_STATUS_SINT) == self.MASK_STATUS_SINT
    
    def get_spectral_channel_interrupt_status(self):
        """!
        Gets the spectral channel interrupt status

        @return **int** The spectral channel interrupt status
        """
        # Read the status register
        status = self.read_register(self.REG_STATUS)

        # Check if the spectral channel interrupt is set
        return (status & self.MASK_STATUS_AINT) == self.MASK_STATUS_AINT
    
    def get_spectral_interrupt_high_status(self):
        """!
        Gets the spectral interrupt high status

        @return **int** The spectral interrupt high status
        """
        # Read the status3 register
        status3 = self.read_register(self.REG_STATUS3)

        # Check if the spectral interrupt high is set
        return (status3 & self.MASK_STATUS3_INT_SP_H) == self.MASK_STATUS3_INT_SP_H
    
    def get_spectral_trigger_error_status(self):
        """!
        Gets the spectral trigger error status

        @return **int** The spectral trigger error status
        """
        # Read the status4 register
        status4 = self.read_register(self.REG_STATUS4)

        # Check if the spectral trigger error is set
        return (status4 & self.MASK_STATUS4_SP_TRIG) == self.MASK_STATUS4_SP_TRIG
    
    def set_wait_time(self, wait_time):
        """!
        Sets the wait time for the AS7343

        @param wait_time: **int** The wait time to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the wait time is valid
        if wait_time < 0 or wait_time > 255:
            return False

        # Write the new wait time to the register
        self._i2c.write_byte(self.address, self.REG_W_TIME, wait_time)
        return True
    
    def get_wait_time(self):
        """!
        Gets the wait time for the AS7343

        @return **int** The wait time
        """
        # Read the wait time register
        return self.read_register(self.REG_W_TIME)
    
    def wait_time_enable(self, enable=True):
        """!
        Enables or disables the wait time

        @param enable: **bool** `True` to enable, `False` to disable

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current enable register
        enable_reg = self.read_register(self.REG_ENABLE)

        # Set the wait time enable bit
        if enable:
            enable_reg |= self.MASK_ENABLE_WEN
        else:
            enable_reg &= ~self.MASK_ENABLE_WEN

        # Write the new enable register value
        self._i2c.write_byte(self.address, self.REG_ENABLE, enable_reg)
        return True
    
    def wait_time_disable(self):
        """!
        Disables the wait time

        @return **bool** `True` if successful, otherwise `False`
        """
        return self.wait_time_enable(False)
    
    def get_spectral_valid_status(self):
        """!
        Gets the spectral valid status

        @return **int** The spectral valid status
        """
        # Read the status2 register
        status2 = self.read_register(self.REG_STATUS2)

        # Check if the spectral valid status is set
        return (status2 & self.MASK_STATUS2_AVALID) == self.MASK_STATUS2_AVALID
    
    def read_int_enable_reg(self):
        """!
        Reads the interrupt enable register

        @return **int** The interrupt enable register value
        """
        # Read the interrupt enable register
        return self.read_register(self.REG_INT_ENAB)
    
    def set_gpio_mode(self, mode):
        """!
        Sets the GPIO mode

        @param mode: **int** The GPIO mode to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the GPIO mode is valid
        if mode not in [self.GPIO_MODE_INPUT, self.GPIO_MODE_OUTPUT]:
            return False

        # Read the current GPIO register
        gpio_reg = self.read_register(self.REG_GPIO)

        # Set the GPIO mode
        gpio_reg &= ~self.MASK_GPIO_IN_EN
        
        if mode == self.GPIO_MODE_INPUT:
            gpio_reg |= self.MASK_GPIO_IN_EN

        # Write the new GPIO register value
        self._i2c.write_byte(self.address, self.REG_GPIO, gpio_reg)
        return True
    
    def get_gpio_input_status(self):
        """!
        Gets the GPIO input status

        @return **int** The GPIO input status
        """
        # Read the GPIO register
        gpio_reg = self.read_register(self.REG_GPIO)

        # Check if the GPIO input status is set
        return (gpio_reg & self.MASK_GPIO_IN) == self.MASK_GPIO_IN
    
    def set_gpio_output(self, output):
        """!
        Sets the GPIO output

        @param output: **int** The GPIO output to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the GPIO output is valid
        if output not in [self.GPIO_OUTPUT_LOW, self.GPIO_OUTPUT_HIGH]:
            return False

        # Read the current GPIO register
        gpio_reg = self.read_register(self.REG_GPIO)

        # Set the GPIO output
        gpio_reg &= ~self.MASK_GPIO_OUT
        gpio_reg |= (output << self.SHIFT_GPIO_OUT) & self.MASK_GPIO_OUT

        # Write the new GPIO register value
        self._i2c.write_byte(self.address, self.REG_GPIO, gpio_reg)
        return True

    def reset(self):
        """!
        Resets the AS7343

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current control register
        control_reg = self.read_register(self.REG_CONTROL)

        # Set the reset bit
        control_reg |= self.MASK_CONTROL_SW_RESET

        # Write the new control register value
        self._i2c.write_byte(self.address, self.REG_CONTROL, control_reg)
        return True 

    def set_spectral_int_persistence(self, persistence):
        """!
        Sets the spectral intensity persistence

        @param persistence: **int** The spectral intensity persistence to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the spectral intensity persistence is valid
        if persistence < 0 or persistence > 0x0F:
            return False

        # Read the current persistence register
        pers_reg = self.read_register(self.REG_PERS)

        # Set the spectral intensity persistence
        pers_reg &= ~self.MASK_PERS_APERS
        pers_reg |= (persistence << self.SHIFT_PERS_APERS) & self.MASK_PERS_APERS

        # Write the new persistence register value
        self._i2c.write_byte(self.address, self.REG_PERS, pers_reg)
        return True
    
    def clear_spectral_channel_interrupt(self):
        """!
        Clears the spectral channel interrupt

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current status register
        status_reg = self.read_register(self.REG_STATUS)

        # Clear the AINT bit by writing a 1 to it
        status_reg |= self.MASK_STATUS_AINT

        # Write the new status register value
        self._i2c.write_byte(self.address, self.REG_STATUS, status_reg)
        return True

    def set_a_gain(self, gain):
        """!
        Sets the A gain

        @param gain: **int** The A gain to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the A gain is valid
        if gain < self.AGAIN_0_5 or gain > self.AGAIN_2048:
            return False

        # Read the current cfg1 register
        cfg1 = self.read_register(self.REG_CFG1)

        # Set the A gain
        cfg1 &= ~self.MASK_CFG1_AGAIN
        cfg1 |= (gain << self.SHIFT_CFG1_AGAIN) & self.MASK_CFG1_AGAIN

        # Write the new cfg1 register value
        self._i2c.write_byte(self.address, self.REG_CFG1, cfg1)
        return True
    
    def flicker_detection_enable(self, enable=True):
        """!
        Enables or disables flicker detection

        @param enable: **bool** `True` to enable, `False` to disable
        """
        # Read the current enable register
        enable_reg = self.read_register(self.REG_ENABLE)

        # Set the flicker detection enable bit
        if enable:
            enable_reg |= self.MASK_ENABLE_FDEN
        else:
            enable_reg &= ~self.MASK_ENABLE_FDEN

        # Write the new enable register value
        self._i2c.write_byte(self.address, self.REG_ENABLE, enable_reg)
    
    def flicker_detection_disable(self):
        """!
        Disables flicker detection
        """
        return self.flicker_detection_enable(False)
    
    def get_fd_valid_status(self):
        """!
        Gets the flicker detection valid status

        @return **bool** The flicker detection valid status
        """
        # Read the fd status register
        fd_status = self.read_register(self.REG_FD_STATUS)

        # Check if the flicker detection valid status is set
        return (fd_status & self.MASK_FD_STATUS_FD_MEAS_VALID) == self.MASK_FD_STATUS_FD_MEAS_VALID
    
    def get_fd_saturation_status(self):
        """!
        Gets the flicker detection saturation status

        @return **bool** The flicker detection saturation status
        """
        # Read the fd status register
        fd_status = self.read_register(self.REG_FD_STATUS)

        # Check if the flicker detection saturation status is set
        return (fd_status & self.MASK_FD_STATUS_FD_SATURATION) == self.MASK_FD_STATUS_FD_SATURATION
    
    def get_fd_frequency(self):
        """!
        Gets the flicker detection frequency

        @return **int** The flicker detection frequency
        """
        # Read the fd status register
        fd_status = self.read_register(self.REG_FD_STATUS)

        # See which frequency bit is set (fd_100hz_det or fd_120hz_det) and check
        # its corresponding valid bit (fd_100hz_valid or fd_120hz_valid) to determine the frequency
        # return the frequency value
        if (fd_status & self.MASK_FD_STATUS_FD_100HZ_DET) == self.MASK_FD_STATUS_FD_100HZ_DET and \
           (fd_status & self.MASK_FD_STATUS_FD_100HZ_VALID) == self.MASK_FD_STATUS_FD_100HZ_VALID:
            return 100
        elif (fd_status & self.MASK_FD_STATUS_FD_120HZ_DET) == self.MASK_FD_STATUS_FD_120HZ_DET and \
             (fd_status & self.MASK_FD_STATUS_FD_120HZ_VALID) == self.MASK_FD_STATUS_FD_120HZ_VALID:
            return 120
        else:
            return 0
