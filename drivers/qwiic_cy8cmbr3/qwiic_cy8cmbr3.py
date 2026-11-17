#-------------------------------------------------------------------------------
# qwiic_cy8cmbr3.py
#
# Python library for the SparkFun Qwiic Capacitive Soil Moisture Sensor, available here:
# https://www.sparkfun.com/products/30480
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, January 2026
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2026 SparkFun Electronics
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
qwiic_cy8cmbr3
============
Python module for the [SparkFun Qwiic Capacitive Soil Moisture Sensor](https://www.sparkfun.com/products/30480)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_CY8CMBR3_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic CY8CMBR3"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x37] 
# Add the other allowable addresses (0x08 to 0x77) to the end of the list
_AVAILABLE_I2C_ADDRESS.extend(list(range(0x08, 0x78)))

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicCY8CMBR3(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS
    default_address = _AVAILABLE_I2C_ADDRESS[0]

    # Register Map
    kRegSensorEn = 0x00
    kRegFssEn = 0x02
    kRegToggleEn = 0x04
    kRegLedOnEn = 0x06
    kRegSensitivity0 = 0x08
    kRegSensitivity1 = 0x09
    kRegSensitivity2 = 0x0A
    kRegSensitivity3 = 0x0B
    kRegBaseThreshold0 = 0x0C
    kRegBaseThreshold1 = 0x0D
    kRegFingerThreshold2 = 0x0E
    kRegFingerThreshold3 = 0x0F
    kRegFingerThreshold4 = 0x10
    kRegFingerThreshold5 = 0x11
    kRegFingerThreshold6 = 0x12
    kRegFingerThreshold7 = 0x13
    kRegFingerThreshold8 = 0x14
    kRegFingerThreshold9 = 0x15
    kRegFingerThreshold10 = 0x16
    kRegFingerThreshold11 = 0x17
    kRegFingerThreshold12 = 0x18
    kRegFingerThreshold13 = 0x19
    kRegFingerThreshold14 = 0x1A
    kRegFingerThreshold15 = 0x1B
    kRegSensorDebounce = 0x1C
    kRegButtonHys = 0x1D
    kRegButtonLbr = 0x1F
    kRegButtonNnt = 0x20
    kRegButtonNt = 0x21
    kRegProxEn = 0x26
    kRegProxCfg = 0x27
    kRegProxCfg2 = 0x28
    kRegProxTouchTh0 = 0x2A
    kRegProxTouchTh1 = 0x2C
    kRegProxResolution0 = 0x2E
    kRegProxResolution1 = 0x2F
    kRegProxHys = 0x30
    kRegProxLbr = 0x32
    kRegProxNnt = 0x33
    kRegProxNt = 0x34
    kRegProxPositiveTh0 = 0x35
    kRegProxPositiveTh1 = 0x36
    kRegProxNegativeTh0 = 0x39
    kRegProxNegativeTh1 = 0x3A
    kRegLedOnTime = 0x3D
    kRegBuzzerCfg = 0x3E
    kRegBuzzerOnTime = 0x3F
    kRegGpoCfg = 0x40
    kRegPwmDutyCycleCfg0 = 0x41
    kRegPwmDutyCycleCfg1 = 0x42
    kRegPwmDutyCycleCfg2 = 0x43
    kRegPwmDutyCycleCfg3 = 0x44
    kRegPwmDutyCycleCfg4 = 0x45
    kRegPwmDutyCycleCfg5 = 0x46
    kRegPwmDutyCycleCfg6 = 0x47
    kRegPwmDutyCycleCfg7 = 0x48
    kRegSpoCfg = 0x4C
    kRegDeviceCfg0 = 0x4D
    kRegDeviceCfg1 = 0x4E
    kRegDeviceCfg2 = 0x4F
    kRegDeviceCfg3 = 0x50
    kRegI2cAddr = 0x51
    kRegRefreshCtrl = 0x52
    kRegStateTimeout = 0x55
    kRegSliderCfg = 0x5D
    kRegSlider1Cfg = 0x61
    kRegSlider1Resolution = 0x62
    kRegSlider1Threshold = 0x63
    kRegSlider2Cfg = 0x67
    kRegSlider2Resolution = 0x68
    kRegSlider2Threshold = 0x69
    kRegSliderLbr = 0x71
    kRegSliderNnt = 0x72
    kRegSliderNt = 0x73
    kRegScratchpad0 = 0x7A
    kRegScratchpad1 = 0x7B
    kRegConfigCrc = 0x7E
    kRegGpoOutputState = 0x80
    kRegSensorId = 0x82
    kRegCtrlCmd = 0x86
    kRegCtrlCmdStatus = 0x88
    kRegCtrlCmdErr = 0x89
    kRegSystemStatus = 0x8A
    kRegPrevCtrlCmdCode = 0x8C
    kRegFamilyId = 0x8F
    kRegDeviceId = 0x90
    kRegDeviceRev = 0x92
    kRegCalcCrc = 0x94
    kRegTotalWorkingSns = 0x97
    kRegSnsCpHigh = 0x98
    kRegSnsVddShort = 0x9A
    kRegSnsGndShort = 0x9C
    kRegSnsSnsShort = 0x9E
    kRegCmodShieldTest = 0xA0
    kRegButtonStat = 0xAA
    kRegLatchedButtonStat = 0xAC
    kRegProxStat = 0xAE
    kRegLatchedProxStat = 0xAF
    kRegSlider1Position = 0xB0
    kRegLiftoffSlider1Position = 0xB1
    kRegSlider2Position = 0xB2
    kRegLiftoffSlider2Position = 0xB3
    kRegSyncCounter0 = 0xB9
    kRegDiffCnt0 = 0xBA
    kRegDiffCnt1 = 0xBC
    kRegDiffCnt2 = 0xBE
    kRegDiffCnt3 = 0xC0
    kRegDiffCnt4 = 0xC2
    kRegDiffCnt5 = 0xC4
    kRegDiffCnt6 = 0xC6
    kRegDiffCnt7 = 0xC8
    kRegDiffCnt8 = 0xCA
    kRegDiffCnt9 = 0xCC
    kRegDiffCnt10 = 0xCE
    kRegDiffCnt11 = 0xD0
    kRegDiffCnt12 = 0xD2
    kRegDiffCnt13 = 0xD4
    kRegDiffCnt14 = 0xD6
    kRegDiffCnt15 = 0xD8
    kRegGpoData = 0xDA
    kRegSyncCounter1 = 0xDB
    kRegDebugSensorId = 0xDC
    kRegDebugCp = 0xDD
    kRegDebugDiffCnt0 = 0xDE
    kRegDebugBaseline0 = 0xE0
    kRegDebugRawCnt0 = 0xE2
    kRegDebugAvgRawCnt0 = 0xE4
    kRegSyncCounter2 = 0xE7

    # Note: Currently since the only supported SparkFun products use the CY8CMBR3102, only CS0 and GPO0 are used. 
    # If other sensors or GPOs are used in the future, additional shifts and masks can be added here.
    # Shifts and Masks
    # SENSOR_EN: Capacitive sensor enable/disable configuration.
    kSensorEnShiftCs0 = 0
    kSensorEnMaskCs0 = 0b01
    kSensorEnShiftCs1 = 1
    kSensorEnMaskCs1 = 0b10

    # TOGGLE_EN: GPO toggle enable/disable.
    kToggleEnShiftGpo0 = 0
    kToggleEnMaskGpo0 = 0b01

    # LED_ON_EN: GPO extended LED ON duration enable/disable.
    kLedOnEnShiftGpo0 = 0
    kLedOnEnMaskGpo0 = 0b01

    # SENSITIVITY0: Sensitivities (units: counts/pF) for button sensors 0 - 3
    kSensitivity0ShiftCs0 = 0
    kSensitivity0MaskCs0 = 0b11

    # GPO_CFG: GPO configuration
    kGpoCfgShiftGpo0GpoCtl = 0
    kGpoCfgMaskGpo0GpoCtl = 1 << kGpoCfgShiftGpo0GpoCtl
    kGpoCfgShiftGpo0GpoPwm = 1
    kGpoCfgMaskGpo0GpoPwm = 1 << kGpoCfgShiftGpo0GpoPwm
    kGpoCfgShiftGpo0DriveMode = 2
    kGpoCfgMaskGpo0DriveMode = 1 << kGpoCfgShiftGpo0DriveMode
    kGpoCfgShiftGpo0ActiveState = 3
    kGpoCfgMaskGpo0ActiveState = 1 << kGpoCfgShiftGpo0ActiveState

    # SPO_CFG: Special purpose output configuration
    kSpoCfgShiftSpo0 = 0
    kSpoCfgMaskSpo0 = 0b00000111
    kSpoCfgShiftSpo1 = 4
    kSpoCfgMaskSpo1 = 0b01110000

    # GPO_OUTPUT_STATE: GPO output state control
    kGpoOutputStateShiftGpo0 = 0
    kGpoOutputStateMaskGpo0 = 0b01

    # GPO_DATA: Current GPO state values
    kGpoDataShiftGpo0 = 0
    kGpoDataMaskGpo0 = 0b01

    # Auto-Reset Enable
    kAutoResetShiftButtonSldArst = 4
    kAutoResetMaskButtonSldArst = 0b11 << kAutoResetShiftButtonSldArst

    kAutoResetShiftProximityArst = 6
    kAutoResetMaskProximityArst = 0b11 << kAutoResetShiftProximityArst


    # Value Variables 
    # IDs
    kDefaultCY8CMBR3102FamilyID = 0x9A # When polling the FAMILY_ID register, this should be returned on boot.
    kDefaultCY8CMBR3102DeviceID = 0xA01 # When polling the DEVICE_ID register, this should be returned on boot.

    # Sensitivities
    # Sensitivity values (counts per pF)
    kCsSensitivity500CountsPerPf = 0  # 50 counts/0.1pF
    kCsSensitivity250CountsPerPf = 1  # 50 counts/0.2pF
    kCsSensitivity167CountsPerPf = 2  # 50 counts/0.3pF
    kCsSensitivity125CountsPerPf = 3  # 50 counts/0.4pF

    # Refresh Intervals
    kRefreshInterval20ms = 1
    kRefreshInterval40ms = 2
    kRefreshInterval60ms = 3
    kRefreshInterval80ms = 4
    kRefreshInterval100ms = 5
    kRefreshInterval120ms = 6
    kRefreshInterval140ms = 7
    kRefreshInterval160ms = 8
    kRefreshInterval180ms = 9
    kRefreshInterval200ms = 10
    kRefreshInterval220ms = 11
    kRefreshInterval240ms = 12
    kRefreshInterval260ms = 13
    kRefreshInterval280ms = 14
    kRefreshInterval300ms = 15
    kRefreshInterval320ms = 16
    kRefreshInterval340ms = 17
    kRefreshInterval360ms = 18
    kRefreshInterval380ms = 19
    kRefreshInterval400ms = 20
    kRefreshInterval420ms = 21
    kRefreshInterval440ms = 22
    kRefreshInterval460ms = 23
    kRefreshInterval480ms = 24
    kRefreshInterval500ms = 25

    # Auto Reset Timeouts
    kAutoResetTimeoutDisabled = 0
    kAutoResetTimeout5Seconds = 1
    kAutoResetTimeout20Seconds = 2

    # Commands
    kCtrlCmdNoOp = 0
    kCtrlCmdSaveConfig = 2
    kCtrlCmdCalcCrc = 3
    kCtrlCmdDeepSleep = 7
    kCtrlCmdResetLatch = 8
    kCtrlCmdAlpResetPs0 = 9
    kCtrlCmdAlpResetPs1 = 10
    kCtrlCmdSwReset = 255
    
    def __init__(self, address=None, i2c_driver=None, enableDebug=False):
        """!
        Constructor

        @param int, optional address: The I2C address to use for the device
            If not provided, the default address is used
        @param I2CDriver, optional i2c_driver: An existing i2c driver object
            If not provided, a driver object is created
        """
        self.enableDebug = enableDebug

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
        # Check ID registers to confirm connected
        family_id = self.get_family_id()
        device_id = self.get_device_id()
        if (family_id != self.kDefaultCY8CMBR3102FamilyID or
            device_id != self.kDefaultCY8CMBR3102DeviceID):
            return False
        
        return True

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False
        
        if not self.enable(0, True):
            return False

        if not self.enable(1, False):
            return False
        
        if not self.set_sensitivity_cs0(self.kCsSensitivity500CountsPerPf):
            return False

        if not self.set_refresh_interval(self.kRefreshInterval100ms):
            return False
        
        if not self.set_spo0_config(5):  # Set as GPO0
            return False

        if not self.set_gpo_config(controlByHost=True, pwmOutput=False, strongDrive=True, activeHigh=False):
            return False
        
        if not self.set_auto_reset_enable():
            return False
        
        # Save the configuration to non-volatile memory and reset
        if not self.save_config():
            return False
    
        if not self.reset():
            return False

        if not self.led_off():
            return False

        if not self.set_sensor_id(0):
            return False
        
        return True

    def get_family_id(self):
        """!
        Reads and returns the Family ID register

        @return **int** The Family ID value
        """
        # Read the Family ID register
        family_id = self._read_byte_with_retry(self.kRegFamilyId)
        
        return family_id
    
    def get_device_id(self):
        """!
        Reads and returns the Device ID register

        @return **int** The Device ID value
        """
        # Read the Device ID register
        device_id = self._read_word_with_retry(self.kRegDeviceId)
        
        return device_id
    
    def enable(self, cs = 0, enable=True):
        """!
        Enables or disables the capacitive sensor 0 (CS0)

        @param cs: The capacitive sensor number (only 0 and 1 are supported)
        @param enable: If `True`, enables CS0
            If `False`, disables CS0

        @return Returns `True` if successful, otherwise `False`
        """
        sensorEnVal = self._read_word_with_retry(self.kRegSensorEn)

        if cs == 0:
            # Configure CS0 enable/disable
            if enable:
                sensorEnVal |= self.kSensorEnMaskCs0
            else:
                sensorEnVal &= ~self.kSensorEnMaskCs0
        
        elif cs == 1:
            # Configure CS1 enable/disable
            if enable:
                sensorEnVal |= self.kSensorEnMaskCs1
            else:
                sensorEnVal &= ~self.kSensorEnMaskCs1
        
        else:
            self.debug_print("Invalid capacitive sensor number.")
            return False  # Invalid capacitive sensor number

        # Write the sensor enable value to the SENSOR_EN register
        self._write_word_with_retry(self.kRegSensorEn, sensorEnVal)

        return True

    def set_auto_reset_enable(self, enable=True, timeout=kAutoResetTimeout5Seconds):
        """!
        Enables or disables the auto-reset feature for buttons and sliders

        @param enable: If `True`, enables auto-reset
            If `False`, disables auto-reset
        @param timeout: The auto-reset timeout to set
            Use one of the kAutoResetTimeout* constants defined in this class

        @return Returns `True` if successful, otherwise `False`
        """
        # Ensure valid inputs
        if timeout < self.kAutoResetTimeoutDisabled or timeout > self.kAutoResetTimeout20Seconds:
            self.debug_print("Invalid auto-reset timeout value.")
            return False  # Invalid auto-reset timeout value
        
        deviceCfg2Val = self._read_byte_with_retry(self.kRegDeviceCfg2)

        if enable:
            deviceCfg2Val &= ~self.kAutoResetMaskProximityArst
            deviceCfg2Val |= (timeout << self.kAutoResetShiftProximityArst) & self.kAutoResetMaskProximityArst

            deviceCfg2Val &= ~self.kAutoResetMaskButtonSldArst
            deviceCfg2Val |= (timeout << self.kAutoResetShiftButtonSldArst) & self.kAutoResetMaskButtonSldArst
        else:
            deviceCfg2Val &= ~self.kAutoResetMaskProximityArst
            deviceCfg2Val |= (self.kAutoResetTimeoutDisabled << self.kAutoResetShiftProximityArst) & self.kAutoResetMaskProximityArst

            deviceCfg2Val &= ~self.kAutoResetMaskButtonSldArst
            deviceCfg2Val |= (self.kAutoResetTimeoutDisabled << self.kAutoResetShiftButtonSldArst) & self.kAutoResetMaskButtonSldArst

        # Write the updated device configuration value back to the DEVICE_CFG2 register
        self._write_byte_with_retry(self.kRegDeviceCfg2, deviceCfg2Val)

        return True

    def set_spo0_config(self, config):
        """!
        Sets the SPO0 configuration

        @param enable: If `True`, enables SPO0
            If `False`, disables SPO0
        @param mode: The SPO0 mode to set
        @param threshold: The SPO0 threshold to set

        @return Returns `True` if successful, otherwise `False`
        """
        # Ensure valid inputs
        spoCfgVal = self._read_byte_with_retry(self.kRegSpoCfg)
        spoCfgVal &= ~self.kSpoCfgMaskSpo0
        spoCfgVal |= (config << self.kSpoCfgShiftSpo0) & self.kSpoCfgMaskSpo0

        # Write the SPO0 configuration to the device
        self._write_byte_with_retry(self.kRegSpoCfg, spoCfgVal)

        return True

    def set_sensitivity_cs0(self, sensitivity):
        """!
        Sets the sensitivity for the capacitive sensor 0 (CS0)

        @param sensitivity: The sensitivity value to set
            Use one of the kCsSensitivity* constants defined in this class

        @return Returns `True` if successful, otherwise `False`
        """
        if sensitivity < self.kCsSensitivity500CountsPerPf or sensitivity > self.kCsSensitivity125CountsPerPf:
            self.debug_print("Invalid sensitivity value.")
            return False  # Invalid sensitivity value
        
        # Read the current SENSITIVITY register value
        sensVal = self._read_byte_with_retry(self.kRegSensitivity0)

        # Clear the bits associated with the capacitive sensor
        sensVal &= ~self.kSensitivity0MaskCs0

        # Set the new sensitivity value
        sensVal |= (sensitivity << self.kSensitivity0ShiftCs0) & self.kSensitivity0MaskCs0

        # Write the updated sensitivity value back to the register
        self._write_byte_with_retry(self.kRegSensitivity0, sensVal)

        return True
    
    def set_refresh_interval(self, interval):
        """!
        Sets the refresh interval for the capacitive sensor

        @param interval: The refresh interval value to set
            Use one of the kRefreshInterval* constants defined in this class

        @return Returns `True` if successful, otherwise `False`
        """
        if interval < self.kRefreshInterval20ms or interval > self.kRefreshInterval500ms:
            self.debug_print("Invalid refresh interval value.")
            return False  # Invalid refresh interval value
        
        # Write the refresh interval value to the REFRESH_CTRL register
        self._write_byte_with_retry(self.kRegRefreshCtrl, interval)

        return True
    
    def set_gpo_config(self, controlByHost, pwmOutput, strongDrive, activeHigh):
        """!
        Configures the GPO0 settings

        @param controlByHost: If `True`, GPO0 is controlled by the host
            If `False`, GPO0 is controlled by the device
        @param pwmOutput: If `True`, GPO0 outputs PWM signal
            If `False`, GPO0 outputs digital signal
        @param strongDrive: If `True`, GPO0 uses strong drive mode
            If `False`, GPO0 uses weak drive mode
        @param activeHigh: If `True`, GPO0 is active high
            If `False`, GPO0 is active low

        @return Returns `True` if successful, otherwise `False`
        """
        gpoCfgVal = self._read_byte_with_retry(self.kRegGpoCfg)

        # Configure control by host/device
        if controlByHost:
            gpoCfgVal |= self.kGpoCfgMaskGpo0GpoCtl
        else:
            gpoCfgVal &= ~self.kGpoCfgMaskGpo0GpoCtl
        
        # Configure PWM/digital output
        if pwmOutput:
            gpoCfgVal |= self.kGpoCfgMaskGpo0GpoPwm
        else:
            gpoCfgVal &= ~self.kGpoCfgMaskGpo0GpoPwm

        # Configure strong/weak drive mode
        if strongDrive:
            gpoCfgVal |= self.kGpoCfgMaskGpo0DriveMode
        else:
            gpoCfgVal &= ~self.kGpoCfgMaskGpo0DriveMode
        
        # Configure active high/low
        if activeHigh:
            gpoCfgVal |= self.kGpoCfgMaskGpo0ActiveState
        else:
            gpoCfgVal &= ~self.kGpoCfgMaskGpo0ActiveState
       
        # Write the GPO configuration value to the GPO_CFG register
        self._write_byte_with_retry(self.kRegGpoCfg, gpoCfgVal)

        return True
    
    def led_on(self, enable=True):
        """!
        Sets the GPO0 output state to turn on/off an LED

        @param enable: If `True`, turns on the LED
            If `False`, turns off the LED

        @return Returns `True` if successful, otherwise `False`
        """
        gpoOutputVal = self._read_byte_with_retry(self.kRegGpoOutputState)

        if enable:
            gpoOutputVal &= ~self.kGpoOutputStateMaskGpo0  # Active low
        else:
            gpoOutputVal |= self.kGpoOutputStateMaskGpo0

        # Write the GPO output state value to the GPO_OUTPUT_STATE register
        self._write_byte_with_retry(self.kRegGpoOutputState, gpoOutputVal)

        return True
    
    def led_off(self):
        """!
        Turns off the LED connected to GPO0

        @return Returns `True` if successful, otherwise `False`
        """
        return self.led_on(False)
    
    def get_debug_sensor_id(self):
        """!
        Reads and returns the Debug Sensor ID register

        @return **int** The Debug Sensor ID value
        """
        # Read the Debug Sensor ID register
        debugSensorId = self._read_byte_with_retry(self.kRegDebugSensorId)
        
        return debugSensorId
    
    def set_sensor_id(self, sensor_id=0):
        """!
        Sets the Sensor ID register

        @param sensor_id: The Sensor ID value to set

        @return Returns `True` if successful, otherwise `False`
        """
        # Write the Sensor ID value to the SENSOR_ID register
        self._write_byte_with_retry(self.kRegSensorId, sensor_id)

        # Wait until the debug sensor ID matches the set sensor ID
        while (self.get_debug_sensor_id() != sensor_id):
            pass  # Optionally, add a timeout here to avoid infinite loops

        return True
    
    def get_capacitance_pf(self):
        """!
        Reads and returns the capacitance value from CS0 in picofarads (pF)

        @return **float** The capacitance value in pF or 0 on error
        """
        # From datasheet 1.5.123 DEBUG_CP register (measurement is updated whenever there is a change in value of SENSOR_ID register)
        # So, we'll first set the sensor ID to something else and then back to the desired sensorId to force an update.
        if not self.set_sensor_id(1):
            return 0.0
        
        # Now set it back to our target sensor (CS0)
        if not self.set_sensor_id(0):
            return 0.0

        # Read the capacitance value from the DebugCp register
        capacitancePf = self._read_byte_with_retry(self.kRegDebugCp)

        return capacitancePf

    def get_diff_count(self):
        """!
        Reads and returns the difference count value from CS0

        @return **int** The difference count value
        """
        # Read the difference count value from the DIFF_CNT0 register
        diffCount = self._read_word_with_retry(self.kRegDiffCnt0)

        return diffCount
    
    def get_diff_pf(self):
        """!
        Reads and returns the difference count value from CS0 in picofarads (pF)

        @return **float** The difference count value in pF
        """
        # Read the difference count value from the DIFF_CNT0 register
        diffCount = self.get_diff_count()

        # Read the sensitivity setting for CS0
        sensVal = self._read_byte_with_retry(self.kRegSensitivity0)
        sensitivitySetting = (sensVal & self.kSensitivity0MaskCs0) >> self.kSensitivity0ShiftCs0

        # Map sensitivity setting to counts per pF
        if sensitivitySetting == self.kCsSensitivity500CountsPerPf:
            countsPerPf = 500
        elif sensitivitySetting == self.kCsSensitivity250CountsPerPf:
            countsPerPf = 250
        elif sensitivitySetting == self.kCsSensitivity167CountsPerPf:
            countsPerPf = 167
        elif sensitivitySetting == self.kCsSensitivity125CountsPerPf:
            countsPerPf = 125
        else:
            self.debug_print("Invalid sensitivity setting.")
            return 0.0  # Invalid sensitivity setting

        # Calculate capacitance in pF
        capacitancePf = diffCount / countsPerPf

        return capacitancePf
    
    def get_baseline_count(self):
        """!
        Reads and returns the baseline count value from CS0

        @return **int** The baseline count value
        """
        if not self.set_sensor_id(0):
            return 0

        # Read the baseline count value from the DebugBaseline0 register
        baselineCount = self._read_word_with_retry(self.kRegDebugBaseline0)

        return baselineCount
    
    def check_saturation(self, rawCount):
        """!
        Checks if the raw count value indicates saturation

        @param rawCount: The raw count value to check

        @return **bool** `True` if saturated, otherwise `False`
        """
        # Read the current sensitivity setting for CS0
        sensVal = self._read_byte_with_retry(self.kRegSensitivity0)
        sensitivitySetting = (sensVal & self.kSensitivity0MaskCs0) >> self.kSensitivity0ShiftCs0

        if sensitivitySetting == self.kCsSensitivity500CountsPerPf:
            saturationThreshold = 4094
        elif sensitivitySetting == self.kCsSensitivity250CountsPerPf:
            saturationThreshold = 2046
        elif sensitivitySetting == self.kCsSensitivity167CountsPerPf:
            saturationThreshold = 1022
        elif sensitivitySetting == self.kCsSensitivity125CountsPerPf:
            saturationThreshold = 1022
    
        return rawCount == saturationThreshold
    
    def get_raw_count(self, autoCalibrate=False):
        """!
        Reads and returns the raw count value from CS0

        @param autoCalibrate: If `True`, performs auto-calibration if saturation is detected.

        Note:
        Do not touch the sensor while auto-calibration is occurring.
        It will range the sensor to a very high capacitance value which will not
        be recoverable by future auto-calibrations until the sensor is manually reset.
        ONLY ENABLE IF AWARE OF THE CONSEQUENCES OF A SOFTWARE RESET!

        @return **int** The raw count value
        """
        if not self.set_sensor_id(0):
            return 0

        # Read the raw count value from the DebugRawCnt0 register
        rawCount = self._read_word_with_retry(self.kRegDebugRawCnt0)

        # If autocalibration is enabled, we'll call reset() if the raw count is at maximum (saturated)
        if autoCalibrate:
            if self.check_saturation(rawCount):
                self.debug_print("Raw count saturated, performing software reset for auto-calibration.")
                self.reset()

        return rawCount
    
    def is_ctrl_command_complete(self):
        """!
        Determines if the last control command has completed

        @return **bool** `True` if the last command is complete, otherwise `False`
        """
        ctrlCmd = self._read_byte_with_retry(self.kRegCtrlCmd)

        # If CTRL_CMD is 0, then the last command is complete
        return (ctrlCmd == self.kCtrlCmdNoOp)
    
    def send_ctrl_command(self, command, waitForCompletion=True):
        """!
        Sends a control command to the device

        @param command: The control command to send
        @param waitForCompletion: If `True`, waits for the command to complete

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Write the command to the CTRL_CMD register
        if not self._write_byte_with_retry(self.kRegCtrlCmd, command):
            self.debug_print(f"Failed to write control command to CTRL_CMD register: 0x{command:X}")
            return False

        if not waitForCompletion:
            return True

        # Wait for the command to complete
        while not self.is_ctrl_command_complete():
            pass  # Optionally, add a timeout here to avoid infinite loops

        # Read the CTRL_CMD_ERR register to check for errors
        ctrlCmdErr = self._read_byte_with_retry(self.kRegCtrlCmdErr)
        if ctrlCmdErr is None:
            return False

        if ctrlCmdErr != 0:  # Assuming 0 means no error
            self.debug_print(f"Control Command Error: {ctrlCmdErr}")
            return False

        self.debug_print(f"Control Command 0x{command:X} executed successfully!")
        return True  # Return true to indicate success
    
    def save_config(self):
        """!
        Saves the current configuration to non-volatile memory

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Calculate the CRC (using the CALC_CRC register) for the current configuration and load it in the CONFIG_CRC register
        if not self.send_ctrl_command(self.kCtrlCmdCalcCrc):
            return False

        # Read the calculated CRC from the CALC_CRC register
        calcCrc = self._read_word_with_retry(self.kRegCalcCrc)
        if calcCrc is None:
            return False

        # Write the calculated CRC to the CONFIG_CRC register
        if not self._write_word_with_retry(self.kRegConfigCrc, calcCrc):
            return False

        # Send the SAVE_CONFIG command to save the current configuration to non-volatile memory
        if not self.send_ctrl_command(self.kCtrlCmdSaveConfig):
            return False

        return True  # Return true to indicate success
    
    def set_i2c_address(self, new_address):
        """!
        Sets a new I2C address for the device

        @param new_address: The new I2C address to set

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        if new_address not in self.available_addresses:
            self.debug_print("Invalid I2C address.")
            return False  # Invalid I2C address

        # Write the new I2C address to the I2C_ADDR register
        if not self._write_byte_with_retry(self.kRegI2cAddr, new_address):
            return False

        # Save the configuration to non-volatile memory
        if not self.save_config():
            return False
        
        # Reset but do not wait for completion as the address will change directly after
        if not self.reset(waitForCompletion=False):
            return False

        # Update the instance's address to the new address
        self.address = new_address

        # wait for the command to complete on the new address
        completionRetries = 10
        from time import sleep
        while completionRetries > 0:
            if self.is_ctrl_command_complete():
                break
            completionRetries -= 1
            sleep(0.1)  # Small delay before retrying

        return True  # Return true to indicate success
    
    def reset(self, waitForCompletion=True):
        """!
        Performs a software reset of the device

        @param waitForCompletion: If `True`, waits for the reset to complete

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Send the SW_RESET command to perform a software reset
        if not self.send_ctrl_command(self.kCtrlCmdSwReset, waitForCompletion):
            return False

        return True  # Return true to indicate success

    def _read_byte_with_retry(self, register, retries=5):
        """!
        Reads a byte from the specified register with retry logic

        @param register: The register address to read from
        @param retries: The number of retry attempts

        @return **int or None** The byte value read from the register or None on failure
        """
        for attempt in range(retries):
            try:
                value = self._i2c.read_byte(self.address, register)
                return value
            except Exception as e:
                self.debug_print(f"Read attempt {attempt + 1} failed: {e}")

    def _read_word_with_retry(self, register, retries=5):
        """!
        Reads a word from the specified register with retry logic

        @param register: The register address to read from
        @param retries: The number of retry attempts

        @return **int or None** The word value read from the register or None on failure
        """
        for attempt in range(retries):
            try:
                value = self._i2c.read_word(self.address, register)
                return value
            except Exception as e:
                self.debug_print(f"Read word attempt {attempt + 1} failed: {e}")
        
    def _write_byte_with_retry(self, register, value, retries=5):
        """!
        Writes a byte to the specified register with retry logic

        @param register: The register address to write to
        @param value: The byte value to write
        @param retries: The number of retry attempts

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        for attempt in range(retries):
            try:
                self._i2c.write_byte(self.address, register, value)
                return True
            except Exception as e:
                self.debug_print(f"Write attempt {attempt + 1} failed: {e}")
        return False
    
    def _write_word_with_retry(self, register, value, retries=5):
        """!
        Writes a word to the specified register with retry logic

        @param register: The register address to write to
        @param value: The word value to write
        @param retries: The number of retry attempts

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        for attempt in range(retries):
            try:
                self._i2c.write_word(self.address, register, value)
                return True
            except Exception as e:
                self.debug_print(f"Write word attempt {attempt + 1} failed: {e}")
        return False

    def debug_print(self, str):
        """!
        Prints debug information to the console if debugging is enabled

        @param str: The string to print
        """
        if self.enableDebug:
            print("QwiicCY8CMBR3: " + str)
