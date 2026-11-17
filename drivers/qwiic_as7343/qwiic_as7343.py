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
    kNumChannels = 18
    kDefaultAS7343DeviceID = 0x81; 
    
    # ----------- Register Bank Settings -----------
    kRegBank0 = 0x00  # Register bank 0 (default)
    kRegBank1 = 0x01  # Register bank 1

    # ----------- Sensor Channels -----------
    # Use these to access each channel individually from the _data array in the class.
    # The channels are defined in the datasheet as FZ, FY, FXL, NIR, 2xVIS, FD, F1-F8.
    # When AutoSmux is set to 18 channels, the channels are in this order:
    # Cycle 1: FZ, FY, FXL, NIR, 2xVIS, FD
    # Cycle 2: F2, F3, F4, F6, 2xVIS, FD
    # Cycle 3: F1, F7, F8, F5, 2xVIS, FD
    kChBlueFz450nm = 0x00  # Blue peak wavelength 450 nanometers (cycle 1)
    kChGreenFy555nm = 0x01  # Green (wide bandwidth) peak wavelength 555 nanometers (cycle 1)
    kChOrangeFxl600nm = 0x02  # Orange peak wavelength 600 nanometers (cycle 1)
    kChNir855nm = 0x03  # NIR peak wavelength 855 nanometers (cycle 1)
    kChVis1 = 0x04  # VIS (cycle 1)
    kChFd1 = 0x05  # Flicker Detection (cycle 1)
    kChDarkBlueF2425nm = 0x06  # Dark Blue peak wavelength 425 nanometers (cycle 2)
    kChLightBlueF3475nm = 0x07  # Light Blue peak wavelength 475 nanometers (cycle 2)
    kChBlueF4515nm = 0x08  # Blue peak wavelength 515 nanometers (cycle 2)
    kChBrownF6640nm = 0x09  # Brown peak wavelength 640 nanometers (cycle 2)
    kChVis2 = 0x0A  # VIS (cycle 2)
    kChFd2 = 0x0B  # Flicker Detection (cycle 2)
    kChPurpleF1405nm = 0x0C  # Purple peak wavelength 405 nanometers (cycle 3)
    kChRedF7690nm = 0x0D  # Red peak wavelength 690 nanometers (cycle 3)
    kChDarkRedF8745nm = 0x0E  # Dark Red peak wavelength 745 nanometers (cycle 3)
    kChGreenF5550nm = 0x0F  # Green (Narrow bandwidth) peak wavelength 550 nanometers (cycle 3)
    kChVis3 = 0x10  # VIS (cycle 3)
    kChFd3 = 0x11  # Flicker Detection (cycle 3)

    # ----------- Sensor Gain Settings -----------
    kAgain0_5 = 0x00  # 0.5x gain
    kAgain1 = 0x01
    kAgain2 = 0x02
    kAgain4 = 0x03
    kAgain8 = 0x04
    kAgain16 = 0x05
    kAgain32 = 0x06
    kAgain64 = 0x07
    kAgain128 = 0x08
    kAgain256 = 0x09
    kAgain512 = 0x0A
    kAgain1024 = 0x0B
    kAgain2048 = 0x0C

    # ----------- Flicker Detection Gain Settings -----------
    kFdGain0_5 = 0x00  # 0.5x gain
    kFdGain1 = 0x01
    kFdGain2 = 0x02
    kFdGain4 = 0x03
    kFdGain8 = 0x04
    kFdGain16 = 0x05
    kFdGain32 = 0x06
    kFdGain64 = 0x07
    kFdGain128 = 0x08
    kFdGain256 = 0x09
    kFdGain512 = 0x0A
    kFdGain1024 = 0x0B
    kFdGain2048 = 0x0C

    # ----------- FIFO Threshold Settings -----------
    kFifoThresholdLvl1 = 0x00
    kFifoThresholdLvl4 = 0x01
    kFifoThresholdLvl8 = 0x02
    kFifoThresholdLvl16 = 0x03

    # ----------- Spectral Threshold Channel -----------
    kSpectralThresholdChannel0 = 0x00
    kSpectralThresholdChannel1 = 0x01
    kSpectralThresholdChannel2 = 0x02
    kSpectralThresholdChannel3 = 0x03
    kSpectralThresholdChannel4 = 0x04
    kSpectralThresholdChannel5 = 0x05

    # ----------- Automatic Channel Read-out -----------
    kAutoSmux6Channels = 0x00  # 6 channel readout
    kAutoSmux12Channels = 0x02  # 12 channel readout
    kAutoSmux18Channels = 0x03  # 18 channel readout

    # ----------- GPIO Mode Settings -----------
    kGpioModeInput = 0x00  # GPIO set to input mode
    kGpioModeOutput = 0x01  # GPIO set to output mode

    # ----------- GPIO Output Settings -----------
    kGpioOutputLow = 0x00  # GPIO set to low
    kGpioOutputHigh = 0x01  # GPIO set to high

    # Register Definitions:
    # ----------- AUX ID Register ----------- 
    kRegAuxID = 0x58

    kShiftAuxID = 0

    kMaskAuxID = 0b1111 << kShiftAuxID

    # ----------- REV ID Register ----------- 
    kRegRevID = 0x59

    kShiftRevID = 0
    
    kMaskRevID = 0b111 << kShiftRevID

    # ----------- ID Register ----------- 
    kRegID = 0x5A
    # Register is a single 8bit value

    # ----------- CFG12 Register -----------
    kRegCfg12 = 0x66

    kShiftCfg12Reserved = 0
    kShiftCfg12SpThCh = 5

    kMaskCfg12Reserved = 0b11111 << kShiftCfg12Reserved
    kMaskCfg12SpThCh = 0b111 << kShiftCfg12SpThCh

    # ----------- Enable Register ----------- 
    kRegEnable = 0x80

    kShiftEnablePon = 0
    kShiftEnableSpEn = 1
    kShiftEnableWen = 3
    kShiftEnableSmuxEn = 4
    kShiftEnableFden = 6
    kShiftEnableEnable = 8

    kMaskEnablePon = 0b1 << kShiftEnablePon
    kMaskEnableSpEn = 0b1 << kShiftEnableSpEn
    kMaskEnableWen = 0b1 << kShiftEnableWen
    kMaskEnableSmuxEn = 0b1 << kShiftEnableSmuxEn
    kMaskEnableFden = 0b1 << kShiftEnableFden
    kMaskEnableEnable = 0b1 << kShiftEnableEnable

    # ----------- ATime Register -----------
    kRegATime = 0x81 # Register Address, register is a single uint8_t.

    # ----------- WTime Register -----------
    kRegWTime = 0x83 # Register Address, register is a single uint8_t.


    # ----------- SP TH L Register -----------
    kRegSpThL = 0x84

    kShiftSpThLSpThLsb = 0
    kShiftSpThLSpThMsb = 8

    kMaskSpThLSpThLsb = 0xFF << kShiftSpThLSpThLsb
    kMaskSpThLSpThMsb = 0xFF << kShiftSpThLSpThMsb

    # ----------- SP TH H Register -----------
    kRegSpThH = 0x86

    kShiftSpThHSpThLsb = 0
    kShiftSpThHSpThMsb = 8

    kMaskSpThHSpThLsb = 0xFF << kShiftSpThHSpThLsb
    kMaskSpThHSpThMsb = 0xFF << kShiftSpThHSpThMsb

    # ----------- Status Register -----------
    kRegStatus = 0x93

    kShiftStatusSint = 0
    kShiftStatusFint = 2
    kShiftStatusAint = 3
    kShiftStatusAsat = 7

    kMaskStatusSint = 0b1 << kShiftStatusSint
    kMaskStatusFint = 0b1 << kShiftStatusFint
    kMaskStatusAint = 0b1 << kShiftStatusAint
    kMaskStatusAsat = 0b1 << kShiftStatusAsat

    # ----------- A Status Register -----------
    kRegAStatus = 0x94

    kShiftAStatusAgainStatus = 0
    kShiftAStatusAsatStatus = 7

    kMaskAStatusAgainStatus = 0b1111 << kShiftAStatusAgainStatus
    kMaskAStatusAsatStatus = 0b1 << kShiftAStatusAsatStatus

    # ----------- Data Registers -----------
    kRegData0 = 0x95
    kRegData1 = 0x97
    kRegData2 = 0x99
    kRegData3 = 0x9B
    kRegData4 = 0x9D
    kRegData5 = 0x9F
    kRegData6 = 0xA1
    kRegData7 = 0xA3
    kRegData8 = 0xA5
    kRegData9 = 0xA7
    kRegData10 = 0xA9
    kRegData11 = 0xAB
    kRegData12 = 0xAD
    kRegData13 = 0xAF
    kRegData14 = 0xB1
    kRegData15 = 0xB3
    kRegData16 = 0xB5
    kRegData17 = 0xB7

    kShiftDataLsb = 0
    kShiftDataMsb = 8

    kMaskDataLsb = 0xFF << kShiftDataLsb
    kMaskDataMsb = 0xFF << kShiftDataMsb

    # ----------- Status 2 Register -----------
    kRegStatus2 = 0x90

    kShiftStatus2FdsatDig = 0
    kShiftStatus2FdsatAna = 1
    kShiftStatus2AsatAna = 3
    kShiftStatus2AsatDig = 4
    kShiftStatus2Avalid = 6

    kMaskStatus2FdsatDig = 0b1 << kShiftStatus2FdsatDig
    kMaskStatus2FdsatAna = 0b1 << kShiftStatus2FdsatAna
    kMaskStatus2AsatAna = 0b1 << kShiftStatus2AsatAna
    kMaskStatus2AsatDig = 0b1 << kShiftStatus2AsatDig
    kMaskStatus2Avalid = 0b1 << kShiftStatus2Avalid

    # ----------- Status 3 Register -----------
    kRegStatus3 = 0x91

    kShiftStatus3IntSpL = 4
    kShiftStatus3IntSpH = 5

    kMaskStatus3IntSpL = 0b1 << kShiftStatus3IntSpL
    kMaskStatus3IntSpH = 0b1 << kShiftStatus3IntSpH

    # ----------- Status 4 Register -----------
    kRegStatus4 = 0xBC

    kShiftStatus4IntBusy = 0
    kShiftStatus4SaiAct = 1
    kShiftStatus4SpTrig = 2
    kShiftStatus4FdTrig = 4
    kShiftStatus4OvTemp = 5
    kShiftStatus4FifoOv = 7

    kMaskStatus4IntBusy = 0b1 << kShiftStatus4IntBusy
    kMaskStatus4SaiAct = 0b1 << kShiftStatus4SaiAct
    kMaskStatus4SpTrig = 0b1 << kShiftStatus4SpTrig
    kMaskStatus4FdTrig = 0b1 << kShiftStatus4FdTrig
    kMaskStatus4OvTemp = 0b1 << kShiftStatus4OvTemp
    kMaskStatus4FifoOv = 0b1 << kShiftStatus4FifoOv

    # ----------- Status 5 Register -----------
    kRegStatus5 = 0x93

    kShiftStatus5SintSmux = 2
    kShiftStatus5SintFd = 3
    kShiftStatus5Reserved = 4
    kShiftStatus5ReservedOne = 6

    kMaskStatus5SintSmux = 0b1 << kShiftStatus5SintSmux
    kMaskStatus5SintFd = 0b1 << kShiftStatus5SintFd
    kMaskStatus5Reserved = 0b11 << kShiftStatus5Reserved
    kMaskStatus5ReservedOne = 0b111 << kShiftStatus5ReservedOne

    # ----------- FD Status Register -----------
    kRegFdStatus = 0xE3

    kShiftFdStatusFd100HzDet = 0
    kShiftFdStatusFd120HzDet = 1
    kShiftFdStatusFd100HzValid = 2
    kShiftFdStatusFd120HzValid = 3
    kShiftFdStatusFdSaturation = 4
    kShiftFdStatusFdMeasValid = 5

    kMaskFdStatusFd100HzDet = 0b1 << kShiftFdStatusFd100HzDet
    kMaskFdStatusFd120HzDet = 0b1 << kShiftFdStatusFd120HzDet
    kMaskFdStatusFd100HzValid = 0b1 << kShiftFdStatusFd100HzValid
    kMaskFdStatusFd120HzValid = 0b1 << kShiftFdStatusFd120HzValid
    kMaskFdStatusFdSaturation = 0b1 << kShiftFdStatusFdSaturation
    kMaskFdStatusFdMeasValid = 0b1 << kShiftFdStatusFdMeasValid

    # ----------- Cfg0 Register -----------
    kRegCfg0 = 0xBF

    kShiftCfg0Wlong = 2
    kShiftCfg0RegBank = 4
    kShiftCfg0LowPower = 5

    kMaskCfg0Wlong = 0b1 << kShiftCfg0Wlong
    kMaskCfg0RegBank = 0b1 << kShiftCfg0RegBank
    kMaskCfg0LowPower = 0b1 << kShiftCfg0LowPower

    # ----------- Cfg1 Register -----------
    kRegCfg1 = 0xC6

    kShiftCfg1Again = 0

    kMaskCfg1Again = 0b11111 << kShiftCfg1Again

    # ----------- Cfg3 Register -----------
    kRegCfg3 = 0xC7

    kShiftCfg3Sai = 4

    kMaskCfg3Sai = 0b1 << kShiftCfg3Sai

    # ----------- Cfg6 Register -----------
    kRegCfg6 = 0xF5

    kShiftCfg6SmuxCmd = 3

    kMaskCfg6SmuxCmd = 0b11 << kShiftCfg6SmuxCmd

    # ----------- Cfg8 Register -----------
    kRegCfg8 = 0xC9

    kShiftCfg8FifoTh = 6

    kMaskCfg8FifoTh = 0b11 << kShiftCfg8FifoTh

    # ----------- Cfg9 Register -----------
    kRegCfg9 = 0xCA

    kShiftCfg9SiencSmux = 5
    kShiftCfg9SiencFd = 7

    kMaskCfg9SiencSmux = 0b1 << kShiftCfg9SiencSmux
    kMaskCfg9SiencFd = 0b1 << kShiftCfg9SiencFd

    # ----------- Cfg10 Register -----------
    kRegCfg10 = 0x65

    kShiftCfg10FdPers = 0

    kMaskCfg10FdPers = 0b111 << kShiftCfg10FdPers

    # ----------- Pers Register -----------
    kRegPers = 0xCF

    kShiftPersApers = 0

    kMaskPersApers = 0b1111 << kShiftPersApers

    # ----------- Gpio Register -----------
    kRegGpio = 0x6B

    kShiftGpioIn = 0
    kShiftGpioOut = 1
    kShiftGpioInEn = 2
    kShiftGpioInv = 3

    kMaskGpioIn = 0b1 << kShiftGpioIn
    kMaskGpioOut = 0b1 << kShiftGpioOut
    kMaskGpioInEn = 0b1 << kShiftGpioInEn
    kMaskGpioInv = 0b1 << kShiftGpioInv

    # ----------- AStep Register -----------
    kRegAStep = 0xD4

    kShiftAStepL = 0
    kShiftAStepH = 8

    kMaskAStepL = 0xFF << kShiftAStepL
    kMaskAStepH = 0xFF << kShiftAStepH

    # ----------- Cfg20 Register -----------
    kRegCfg20 = 0xD6

    kShiftCfg20AutoSmux = 5
    kShiftCfg20FdFifo8b = 7

    kMaskCfg20AutoSmux = 0b11 << kShiftCfg20AutoSmux
    kMaskCfg20FdFifo8b = 0b1 << kShiftCfg20FdFifo8b

    # ----------- Led Register -----------
    kRegLed = 0xCD

    kShiftLedDrive = 0
    kShiftLedAct = 7

    kMaskLedDrive = 0b1111111 << kShiftLedDrive
    kMaskLedAct = 0b1 << kShiftLedAct

    # ----------- Agc Gain Max Register -----------
    kRegAgcGainMax = 0xD7

    kShiftAgcGainMax = 4

    kMaskAgcGainMax = 0b1111 << kShiftAgcGainMax

    # ----------- Az Config Register -----------
    kRegAzConfig = 0xDE

    # Register is a single 8-bit value

    # ----------- Fd Time1 Register -----------
    kRegFdTime1 = 0xE0

    # Register is a single 8-bit value

    # ----------- Fd Time2 Register -----------
    kRegFdTime2 = 0xE2

    kShiftFdTime2FdTimeH = 0
    kShiftFdTime2FdGain = 3

    kMaskFdTime2FdTimeH = 0b111 << kShiftFdTime2FdTimeH
    kMaskFdTime2FdGain = 0b11111 << kShiftFdTime2FdGain

    # ----------- Fd Time Cfg0 Register -----------
    kRegFdTimeCfg0 = 0xDF

    kShiftFdTimeCfg0FifoWriteFd = 7

    kMaskFdTimeCfg0FifoWriteFd = 0b1 << kShiftFdTimeCfg0FifoWriteFd

    # ----------- Int Enab Register -----------
    kRegIntEnab = 0xF9

    kShiftIntEnabSein = 0
    kShiftIntEnabFien = 2
    kShiftIntEnabSpIen = 3
    kShiftIntEnabAsien = 7

    kMaskIntEnabSein = 0b1 << kShiftIntEnabSein
    kMaskIntEnabFien = 0b1 << kShiftIntEnabFien
    kMaskIntEnabSpIen = 0b1 << kShiftIntEnabSpIen
    kMaskIntEnabAsien = 0b1 << kShiftIntEnabAsien

    # ----------- Control Register -----------
    kRegControl = 0xFA

    kShiftControlClearSaiAct = 0
    kShiftControlFifoClr = 1
    kShiftControlSpManAz = 2
    kShiftControlSwReset = 3

    kMaskControlClearSaiAct = 0b1 << kShiftControlClearSaiAct
    kMaskControlFifoClr = 0b1 << kShiftControlFifoClr
    kMaskControlSpManAz = 0b1 << kShiftControlSpManAz
    kMaskControlSwReset = 0b1 << kShiftControlSwReset

    # ----------- Fifo Map Register -----------
    kRegFifoMap = 0xFC

    kShiftFifoMapFifoWriteAStatus = 0
    kShiftFifoMapFifoWriteCh0Data = 1
    kShiftFifoMapFifoWriteCh1Data = 2
    kShiftFifoMapFifoWriteCh2Data = 3
    kShiftFifoMapFifoWriteCh3Data = 4
    kShiftFifoMapFifoWriteCh4Data = 5
    kShiftFifoMapFifoWriteCh5Data = 6

    kMaskFifoMapFifoWriteAStatus = 0b1 << kShiftFifoMapFifoWriteAStatus
    kMaskFifoMapFifoWriteCh0Data = 0b1 << kShiftFifoMapFifoWriteCh0Data
    kMaskFifoMapFifoWriteCh1Data = 0b1 << kShiftFifoMapFifoWriteCh1Data
    kMaskFifoMapFifoWriteCh2Data = 0b1 << kShiftFifoMapFifoWriteCh2Data
    kMaskFifoMapFifoWriteCh3Data = 0b1 << kShiftFifoMapFifoWriteCh3Data
    kMaskFifoMapFifoWriteCh4Data = 0b1 << kShiftFifoMapFifoWriteCh4Data
    kMaskFifoMapFifoWriteCh5Data = 0b1 << kShiftFifoMapFifoWriteCh5Data

    # ----------- Fifo Lvl Register -----------
    kRegFifoLvl = 0xFD

    # Register is a single 8-bit value

    # ----------- FData Register -----------
    kRegFData = 0xFE

    kShiftFDataL = 0
    kShiftFDataH = 8

    kMaskFDataL = 0xFF << kShiftFDataL
    kMaskFDataH = 0xFF << kShiftFDataH


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

        self._data = [None] * self.kNumChannels

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        if not self._i2c.isDeviceConnected(self.address):
            print("Device not connected")
            return False

        # Check that Part Number Identifier is correct (read only and should always be 0x81)
        if self.get_device_id() != self.kDefaultAS7343DeviceID:
            print("Device ID mismatch")
            return False
        
        return True

    connected = property(is_connected)

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

        @param int bank: The register bank to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the bank is valid
        if bank not in [self.kRegBank0, self.kRegBank1]:
            return False

        # Read the current cfg0 register
        cfg0 = self._i2c.read_byte(self.address, self.kRegCfg0)

        # Clear the register bank bits
        cfg0 &= ~self.kMaskCfg0RegBank

        # Set the new register bank
        cfg0 |= (bank << self.kShiftCfg0RegBank) & self.kMaskCfg0RegBank

        # Write the new cfg0 register value
        self._i2c.write_byte(self.address, self.kRegCfg0, cfg0)
        return True

    def read_register(self, register):
        """!
        Reads a single byte from the specified register

        @param int register: The register to read from

        @return **int** The value read from the register
        """
        
        # Set the register bank as needed to access the specified register.
        # if the desired register is equal to or greater than 0x80, set bank 0.
        # Otherwise, set bank 1.
        if register >= 0x80:
            self.set_register_bank(self.kRegBank0)
        else:
            self.set_register_bank(self.kRegBank1)

        # Read the register value
        return self._i2c.read_byte(self.address, register)
    
    def get_device_id(self):
        """!
        Gets the device ID of the AS7343

        @return **int** The device ID
        """
        # Read the device ID register
        return self.read_register(self.kRegID)
    
    def power_on(self, enable=True):
        """!
        Powers on the AS7343

        @param bool enable: `True` to power on, `False` to power off

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current enable register
        enable_reg = self.read_register(self.kRegEnable)

        # Set the power on bit
        if enable:
            enable_reg |= self.kMaskEnablePon
        else:
            enable_reg &= ~self.kMaskEnablePon

        # Write the new enable register value
        self._i2c.write_byte(self.address, self.kRegEnable, enable_reg)
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

        @param bool enable: `True` to enable, `False` to disable

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current enable register
        enable_reg = self.read_register(self.kRegEnable)

        # Set the spectral measurement enable bit
        if enable:
            enable_reg |= self.kMaskEnableSpEn
        else:
            enable_reg &= ~self.kMaskEnableSpEn

        # Write the new enable register value
        self._i2c.write_byte(self.address, self.kRegEnable, enable_reg)
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
        self.set_register_bank(self.kRegBank0)

        # Read the spectral data registers
        for i in range(self.kNumChannels):
            self._data[i] = (self._i2c.read_word(self.address, self.kRegData0 + (i * 2)))

    
    def get_data(self, channel):
        """!
        Gets the data for a specific channel

        @param int channel: The channel to get data from

        @return **int** The data for the specified channel or `None` if invalid
        """
        # Check if the channel is valid
        if channel < 0 or channel >= self.kNumChannels:
            return None

        # Return the data for the specified channel
        return self._data[channel]
        
    def set_auto_smux(self, auto_smux):
        """!
        Sets the automatic SMUX mode

        @param int auto_smux: The automatic SMUX mode to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the auto SMUX mode is valid
        if auto_smux not in [self.kAutoSmux6Channels, self.kAutoSmux12Channels, self.kAutoSmux18Channels]:
            return False

        # Read the current cfg20 register
        cfg20 = self.read_register(self.kRegCfg20)

        # Clear the automatic SMUX bits
        cfg20 &= ~self.kMaskCfg20AutoSmux

        # Set the new automatic SMUX mode
        cfg20 |= (auto_smux << self.kShiftCfg20AutoSmux) & self.kMaskCfg20AutoSmux

        # Write the new cfg20 register value
        self._i2c.write_byte(self.address, self.kRegCfg20, cfg20)
        return True
    
    def set_led_on(self, led_on = True):
        """!
        Sets the LED state

        @param bool led_on: `True` to turn on the LED, `False` to turn it off

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current LED register
        led_reg = self.read_register(self.kRegLed)

        # Set the LED state
        if led_on:
            led_reg |= self.kMaskLedAct
        else:
            led_reg &= ~self.kMaskLedAct

        # Write the new LED register value
        self._i2c.write_byte(self.address, self.kRegLed, led_reg)
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

        @param int drive: The LED drive current to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the drive current is valid
        if drive < 0 or drive > 127:
            return False

        # Read the current LED register
        led_reg = self.read_register(self.kRegLed)

        # Set the LED drive current
        led_reg &= ~self.kMaskLedDrive
        led_reg |= (drive << self.kShiftLedDrive) & self.kMaskLedDrive

        # Write the new LED register value
        self._i2c.write_byte(self.address, self.kRegLed, led_reg)
        return True
    
    def get_red(self):
        """!
        Gets the red channel data

        @return **int** The red channel data
        """
        return self.get_data(self.kChRedF7690nm)
    
    def get_green(self):
        """!
        Gets the green channel data

        @return **int** The green channel data
        """
        return self.get_data(self.kChGreenF5550nm)
    
    def get_blue(self):
        """!
        Gets the blue channel data

        @return **int** The blue channel data
        """
        return self.get_data(self.kChBlueFz450nm)
    
    def get_nir(self):
        """!
        Gets the NIR channel data

        @return **int** The NIR channel data
        """
        return self.get_data(self.kChNir855nm)
    
    # TODO: Check endianness for these write_words
    def set_spectral_int_threshold_high(self, spThH):
        """!
        Sets the spectral intensity threshold high value

        @param 16-bit positive int spThH: The spectral intensity threshold high value

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the spectral intensity threshold high value is valid
        if spThH < 0 or spThH > 0xFFFF:
            return False
    
        # Right the full 16-bit value to the register
        self._i2c.write_word(self.address, self.kRegSpThH, spThH)
        return True
    
    def set_spectral_int_threshold_low(self, spThL):
        """!
        Sets the spectral intensity threshold low value

        @param 16-bit positive int spThL: The spectral intensity threshold low value

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the spectral intensity threshold low value is valid
        if spThL < 0 or spThL > 0xFFFF:
            return False
    
        # Right the full 16-bit value to the register
        self._i2c.write_word(self.address, self.kRegSpThL, spThL)
        return True
    
    def spectral_int_enable(self, enable=True):
        """!
        Enables or disables spectral intensity measurement

        @param bool enable: `True` to enable, `False` to disable

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current cfg20 register
        intEnab = self.read_register(self.kRegIntEnab)

        # Set the spectral intensity enable bit
        if enable:
            intEnab |= self.kMaskIntEnabSpIen
        else:
            intEnab &= ~self.kMaskIntEnabSpIen

        # Write the new INT_ENAB register value
        self._i2c.write_byte(self.address, self.kRegIntEnab, intEnab)
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

        @param int channel: The spectral threshold channel to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the spectral threshold channel is valid
        if channel not in [self.kSpectralThresholdChannel0, self.kSpectralThresholdChannel1,
                           self.kSpectralThresholdChannel2, self.kSpectralThresholdChannel3,
                           self.kSpectralThresholdChannel4, self.kSpectralThresholdChannel5]:
            return False

        # Read the current cfg12 register
        cfg12 = self.read_register(self.kRegCfg12)

        # Clear the spectral threshold channel bits
        cfg12 &= ~self.kMaskCfg12SpThCh

        # Set the new spectral threshold channel
        cfg12 |= (channel << self.kShiftCfg12SpThCh) & self.kMaskCfg12SpThCh

        # Write the new cfg12 register value
        self._i2c.write_byte(self.address, self.kRegCfg12, cfg12)
        return True

    def get_system_interrupt_status(self):
        """!
        Gets the system interrupt status

        @return **bool** The system interrupt status
        """
        # Read the status register
        status = self.read_register(self.kRegStatus)

        # Check if the system interrupt is set
        return (status & self.kMaskStatusSint) == self.kMaskStatusSint
    
    def get_spectral_channel_interrupt_status(self):
        """!
        Gets the spectral channel interrupt status

        @return **int** The spectral channel interrupt status
        """
        # Read the status register
        status = self.read_register(self.kRegStatus)

        # Check if the spectral channel interrupt is set
        return (status & self.kMaskStatusAint) == self.kMaskStatusAint
    
    def get_spectral_interrupt_high_status(self):
        """!
        Gets the spectral interrupt high status

        @return **int** The spectral interrupt high status
        """
        # Read the status3 register
        status3 = self.read_register(self.kRegStatus3)

        # Check if the spectral interrupt high is set
        return (status3 & self.kMaskStatus3IntSpH) == self.kMaskStatus3IntSpH
    
    def get_spectral_trigger_error_status(self):
        """!
        Gets the spectral trigger error status

        @return **int** The spectral trigger error status
        """
        # Read the status4 register
        status4 = self.read_register(self.kRegStatus4)

        # Check if the spectral trigger error is set
        return (status4 & self.kMaskStatus4SpTrig) == self.kMaskStatus4SpTrig
    
    def set_wait_time(self, wait_time):
        """!
        Sets the wait time for the AS7343

        @param int wait_time: The wait time to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the wait time is valid
        if wait_time < 0 or wait_time > 255:
            return False

        # Write the new wait time to the register
        self._i2c.write_byte(self.address, self.kRegWTime, wait_time)
        return True
    
    def get_wait_time(self):
        """!
        Gets the wait time for the AS7343

        @return **int** The wait time
        """
        # Read the wait time register
        return self.read_register(self.kRegWTime)
    
    def wait_time_enable(self, enable=True):
        """!
        Enables or disables the wait time

        @param bool enable: `True` to enable, `False` to disable

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current enable register
        enable_reg = self.read_register(self.kRegEnable)

        # Set the wait time enable bit
        if enable:
            enable_reg |= self.kMaskEnableWen
        else:
            enable_reg &= ~self.kMaskEnableWen

        # Write the new enable register value
        self._i2c.write_byte(self.address, self.kRegEnable, enable_reg)
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
        status2 = self.read_register(self.kRegStatus2)

        # Check if the spectral valid status is set
        return (status2 & self.kMaskStatus2Avalid) == self.kMaskStatus2Avalid
    
    def read_int_enable_reg(self):
        """!
        Reads the interrupt enable register

        @return **int** The interrupt enable register value
        """
        # Read the interrupt enable register
        return self.read_register(self.kRegIntEnab)
    
    def set_gpio_mode(self, mode):
        """!
        Sets the GPIO mode

        @param int mode: The GPIO mode to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the GPIO mode is valid
        if mode not in [self.kGpioModeInput, self.kGpioModeOutput]:
            return False

        # Read the current GPIO register
        gpio_reg = self.read_register(self.kRegGpio)

        # Set the GPIO mode
        gpio_reg &= ~self.kMaskGpioInEn
        
        if mode == self.kGpioModeInput:
            gpio_reg |= self.kMaskGpioInEn

        # Write the new GPIO register value
        self._i2c.write_byte(self.address, self.kRegGpio, gpio_reg)
        return True
    
    def get_gpio_input_status(self):
        """!
        Gets the GPIO input status

        @return **int** The GPIO input status
        """
        # Read the GPIO register
        gpio_reg = self.read_register(self.kRegGpio)

        # Check if the GPIO input status is set
        return (gpio_reg & self.kMaskGpioIn) == self.kMaskGpioIn
    
    def set_gpio_output(self, output):
        """!
        Sets the GPIO output

        @param int output: The GPIO output to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the GPIO output is valid
        if output not in [self.kGpioOutputLow, self.kGpioOutputHigh]:
            return False

        # Read the current GPIO register
        gpio_reg = self.read_register(self.kRegGpio)

        # Set the GPIO output
        gpio_reg &= ~self.kMaskGpioOut
        gpio_reg |= (output << self.kShiftGpioOut) & self.kMaskGpioOut

        # Write the new GPIO register value
        self._i2c.write_byte(self.address, self.kRegGpio, gpio_reg)
        return True

    def reset(self):
        """!
        Resets the AS7343

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current control register
        control_reg = self.read_register(self.kRegControl)

        # Set the reset bit
        control_reg |= self.kMaskControlSwReset

        # Write the new control register value
        self._i2c.write_byte(self.address, self.kRegControl, control_reg)
        return True 

    def set_spectral_int_persistence(self, persistence):
        """!
        Sets the spectral intensity persistence

        @param int persistence: The spectral intensity persistence to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the spectral intensity persistence is valid
        if persistence < 0 or persistence > 0x0F:
            return False

        # Read the current persistence register
        pers_reg = self.read_register(self.kRegPers)

        # Set the spectral intensity persistence
        pers_reg &= ~self.kMaskPersApers
        pers_reg |= (persistence << self.kShiftPersApers) & self.kMaskPersApers

        # Write the new persistence register value
        self._i2c.write_byte(self.address, self.kRegPers, pers_reg)
        return True
    
    def clear_spectral_channel_interrupt(self):
        """!
        Clears the spectral channel interrupt

        @return **bool** `True` if successful, otherwise `False`
        """
        # Read the current status register
        status_reg = self.read_register(self.kRegStatus)

        # Clear the AINT bit by writing a 1 to it
        status_reg |= self.kMaskStatusAint

        # Write the new status register value
        self._i2c.write_byte(self.address, self.kRegStatus, status_reg)
        return True

    def set_a_gain(self, gain):
        """!
        Sets the A gain

        @param int gain: The A gain to set

        @return **bool** `True` if successful, otherwise `False`
        """
        # Check if the A gain is valid
        if gain < self.kAgain0_5 or gain > self.kAgain2048:
            return False

        # Read the current cfg1 register
        cfg1 = self.read_register(self.kRegCfg1)

        # Set the A gain
        cfg1 &= ~self.kMaskCfg1Again
        cfg1 |= (gain << self.kShiftCfg1Again) & self.kMaskCfg1Again

        # Write the new cfg1 register value
        self._i2c.write_byte(self.address, self.kRegCfg1, cfg1)
        return True
    
    def flicker_detection_enable(self, enable=True):
        """!
        Enables or disables flicker detection

        @param bool enable: `True` to enable, `False` to disable
        """
        # Read the current enable register
        enable_reg = self.read_register(self.kRegEnable)

        # Set the flicker detection enable bit
        if enable:
            enable_reg |= self.kMaskEnableFden
        else:
            enable_reg &= ~self.kMaskEnableFden

        # Write the new enable register value
        self._i2c.write_byte(self.address, self.kRegEnable, enable_reg)
    
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
        fd_status = self.read_register(self.kRegFdStatus)

        # Check if the flicker detection valid status is set
        return (fd_status & self.kMaskFdStatusFdMeasValid) == self.kMaskFdStatusFdMeasValid
    
    def get_fd_saturation_status(self):
        """!
        Gets the flicker detection saturation status

        @return **bool** The flicker detection saturation status
        """
        # Read the fd status register
        fd_status = self.read_register(self.kRegFdStatus)

        # Check if the flicker detection saturation status is set
        return (fd_status & self.kMaskFdStatusFdSaturation) == self.kMaskFdStatusFdSaturation
    
    def get_fd_frequency(self):
        """!
        Gets the flicker detection frequency

        @return **int** The flicker detection frequency
        """
        # Read the fd status register
        fd_status = self.read_register(self.kRegFdStatus)

        # See which frequency bit is set (fd_100hz_det or fd_120hz_det) and check
        # its corresponding valid bit (fd_100hz_valid or fd_120hz_valid) to determine the frequency
        # return the frequency value
        if (fd_status & self.kMaskFdStatusFd100HzDet) == self.kMaskFdStatusFd100HzDet and \
           (fd_status & self.kMaskFdStatusFd100HzValid) == self.kMaskFdStatusFd100HzValid:
            return 100
        elif (fd_status & self.kMaskFdStatusFd120HzDet) == self.kMaskFdStatusFd120HzDet and \
             (fd_status & self.kMaskFdStatusFd120HzValid) == self.kMaskFdStatusFd120HzValid:
            return 120
        else:
            return 0
