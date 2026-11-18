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

__version__ = "3.0.0"

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
    DEFAULT_ADDRESS = _AVAILABLE_I2C_ADDRESS[0]

    # Register Map
    REG_SENSOR_EN = 0x00
    REG_FSS_EN = 0x02
    REG_TOGGLE_EN = 0x04
    REG_LED_ON_EN = 0x06
    REG_SENSITIVITY0 = 0x08
    REG_SENSITIVITY1 = 0x09
    REG_SENSITIVITY2 = 0x0A
    REG_SENSITIVITY3 = 0x0B
    REG_BASE_THRESHOLD0 = 0x0C
    REG_BASE_THRESHOLD1 = 0x0D
    REG_FINGER_THRESHOLD2 = 0x0E
    REG_FINGER_THRESHOLD3 = 0x0F
    REG_FINGER_THRESHOLD4 = 0x10
    REG_FINGER_THRESHOLD5 = 0x11
    REG_FINGER_THRESHOLD6 = 0x12
    REG_FINGER_THRESHOLD7 = 0x13
    REG_FINGER_THRESHOLD8 = 0x14
    REG_FINGER_THRESHOLD9 = 0x15
    REG_FINGER_THRESHOLD10 = 0x16
    REG_FINGER_THRESHOLD11 = 0x17
    REG_FINGER_THRESHOLD12 = 0x18
    REG_FINGER_THRESHOLD13 = 0x19
    REG_FINGER_THRESHOLD14 = 0x1A
    REG_FINGER_THRESHOLD15 = 0x1B
    REG_SENSOR_DEBOUNCE = 0x1C
    REG_BUTTON_HYS = 0x1D
    REG_BUTTON_LBR = 0x1F
    REG_BUTTON_NNT = 0x20
    REG_BUTTON_NT = 0x21
    REG_PROX_EN = 0x26
    REG_PROX_CFG = 0x27
    REG_PROX_CFG2 = 0x28
    REG_PROX_TOUCH_TH0 = 0x2A
    REG_PROX_TOUCH_TH1 = 0x2C
    REG_PROX_RESOLUTION0 = 0x2E
    REG_PROX_RESOLUTION1 = 0x2F
    REG_PROX_HYS = 0x30
    REG_PROX_LBR = 0x32
    REG_PROX_NNT = 0x33
    REG_PROX_NT = 0x34
    REG_PROX_POSITIVE_TH0 = 0x35
    REG_PROX_POSITIVE_TH1 = 0x36
    REG_PROX_NEGATIVE_TH0 = 0x39
    REG_PROX_NEGATIVE_TH1 = 0x3A
    REG_LED_ON_TIME = 0x3D
    REG_BUZZER_CFG = 0x3E
    REG_BUZZER_ON_TIME = 0x3F
    REG_GPO_CFG = 0x40
    REG_PWM_DUTY_CYCLE_CFG0 = 0x41
    REG_PWM_DUTY_CYCLE_CFG1 = 0x42
    REG_PWM_DUTY_CYCLE_CFG2 = 0x43
    REG_PWM_DUTY_CYCLE_CFG3 = 0x44
    REG_PWM_DUTY_CYCLE_CFG4 = 0x45
    REG_PWM_DUTY_CYCLE_CFG5 = 0x46
    REG_PWM_DUTY_CYCLE_CFG6 = 0x47
    REG_PWM_DUTY_CYCLE_CFG7 = 0x48
    REG_SPO_CFG = 0x4C
    REG_DEVICE_CFG0 = 0x4D
    REG_DEVICE_CFG1 = 0x4E
    REG_DEVICE_CFG2 = 0x4F
    REG_DEVICE_CFG3 = 0x50
    REG_I2C_ADDR = 0x51
    REG_REFRESH_CTRL = 0x52
    REG_STATE_TIMEOUT = 0x55
    REG_SLIDER_CFG = 0x5D
    REG_SLIDER1_CFG = 0x61
    REG_SLIDER1_RESOLUTION = 0x62
    REG_SLIDER1_THRESHOLD = 0x63
    REG_SLIDER2_CFG = 0x67
    REG_SLIDER2_RESOLUTION = 0x68
    REG_SLIDER2_THRESHOLD = 0x69
    REG_SLIDER_LBR = 0x71
    REG_SLIDER_NNT = 0x72
    REG_SLIDER_NT = 0x73
    REG_SCRATCHPAD0 = 0x7A
    REG_SCRATCHPAD1 = 0x7B
    REG_CONFIG_CRC = 0x7E
    REG_GPO_OUTPUT_STATE = 0x80
    REG_SENSOR_ID = 0x82
    REG_CTRL_CMD = 0x86
    REG_CTRL_CMD_STATUS = 0x88
    REG_CTRL_CMD_ERR = 0x89
    REG_SYSTEM_STATUS = 0x8A
    REG_PREV_CTRL_CMD_CODE = 0x8C
    REG_FAMILY_ID = 0x8F
    REG_DEVICE_ID = 0x90
    REG_DEVICE_REV = 0x92
    REG_CALC_CRC = 0x94
    REG_TOTAL_WORKING_SNS = 0x97
    REG_SNS_CP_HIGH = 0x98
    REG_SNS_VDD_SHORT = 0x9A
    REG_SNS_GND_SHORT = 0x9C
    REG_SNS_SNS_SHORT = 0x9E
    REG_CMOD_SHIELD_TEST = 0xA0
    REG_BUTTON_STAT = 0xAA
    REG_LATCHED_BUTTON_STAT = 0xAC
    REG_PROX_STAT = 0xAE
    REG_LATCHED_PROX_STAT = 0xAF
    REG_SLIDER1_POSITION = 0xB0
    REG_LIFTOFF_SLIDER1_POSITION = 0xB1
    REG_SLIDER2_POSITION = 0xB2
    REG_LIFTOFF_SLIDER2_POSITION = 0xB3
    REG_SYNC_COUNTER0 = 0xB9
    REG_DIFF_CNT0 = 0xBA
    REG_DIFF_CNT1 = 0xBC
    REG_DIFF_CNT2 = 0xBE
    REG_DIFF_CNT3 = 0xC0
    REG_DIFF_CNT4 = 0xC2
    REG_DIFF_CNT5 = 0xC4
    REG_DIFF_CNT6 = 0xC6
    REG_DIFF_CNT7 = 0xC8
    REG_DIFF_CNT8 = 0xCA
    REG_DIFF_CNT9 = 0xCC
    REG_DIFF_CNT10 = 0xCE
    REG_DIFF_CNT11 = 0xD0
    REG_DIFF_CNT12 = 0xD2
    REG_DIFF_CNT13 = 0xD4
    REG_DIFF_CNT14 = 0xD6
    REG_DIFF_CNT15 = 0xD8
    REG_GPO_DATA = 0xDA
    REG_SYNC_COUNTER1 = 0xDB
    REG_DEBUG_SENSOR_ID = 0xDC
    REG_DEBUG_CP = 0xDD
    REG_DEBUG_DIFF_CNT0 = 0xDE
    REG_DEBUG_BASELINE0 = 0xE0
    REG_DEBUG_RAW_CNT0 = 0xE2
    REG_DEBUG_AVG_RAW_CNT0 = 0xE4
    REG_SYNC_COUNTER2 = 0xE7

    # Note: Currently since the only supported SparkFun products use the CY8CMBR3102, only CS0 and GPO0 are used. 
    # If other sensors or GPOs are used in the future, additional shifts and masks can be added here.
    # Shifts and Masks
    # SENSOR_EN: Capacitive sensor enable/disable configuration.
    SENSOR_EN_SHIFT_CS0 = 0
    SENSOR_EN_MASK_CS0 = 0b01
    SENSOR_EN_SHIFT_CS1 = 1
    SENSOR_EN_MASK_CS1 = 0b10

    # TOGGLE_EN: GPO toggle enable/disable.
    TOGGLE_EN_SHIFT_GPO0 = 0
    TOGGLE_EN_MASK_GPO0 = 0b01

    # LED_ON_EN: GPO extended LED ON duration enable/disable.
    LED_ON_EN_SHIFT_GPO0 = 0
    LED_ON_EN_MASK_GPO0 = 0b01

    # SENSITIVITY0: Sensitivities (units: counts/pF) for button sensors 0 - 3
    SENSITIVITY0_SHIFT_CS0 = 0
    SENSITIVITY0_MASK_CS0 = 0b11

    # GPO_CFG: GPO configuration
    GPO_CFG_SHIFT_GPO0_GPO_CTL = 0
    GPO_CFG_MASK_GPO0_GPO_CTL = 1 << GPO_CFG_SHIFT_GPO0_GPO_CTL
    GPO_CFG_SHIFT_GPO0_GPO_PWM = 1
    GPO_CFG_MASK_GPO0_GPO_PWM = 1 << GPO_CFG_SHIFT_GPO0_GPO_PWM
    GPO_CFG_SHIFT_GPO0_DRIVE_MODE = 2
    GPO_CFG_MASK_GPO0_DRIVE_MODE = 1 << GPO_CFG_SHIFT_GPO0_DRIVE_MODE
    GPO_CFG_SHIFT_GPO0_ACTIVE_STATE = 3
    GPO_CFG_MASK_GPO0_ACTIVE_STATE = 1 << GPO_CFG_SHIFT_GPO0_ACTIVE_STATE

    # SPO_CFG: Special purpose output configuration
    SPO_CFG_SHIFT_SPO0 = 0
    SPO_CFG_MASK_SPO0 = 0b00000111
    SPO_CFG_SHIFT_SPO1 = 4
    SPO_CFG_MASK_SPO1 = 0b01110000

    # GPO_OUTPUT_STATE: GPO output state control
    GPO_OUTPUT_STATE_SHIFT_GPO0 = 0
    GPO_OUTPUT_STATE_MASK_GPO0 = 0b01

    # GPO_DATA: Current GPO state values
    GPO_DATA_SHIFT_GPO0 = 0
    GPO_DATA_MASK_GPO0 = 0b01

    # Auto-Reset Enable
    AUTO_RESET_SHIFT_BUTTON_SLD_ARST = 4
    AUTO_RESET_MASK_BUTTON_SLD_ARST = 0b11 << AUTO_RESET_SHIFT_BUTTON_SLD_ARST

    AUTO_RESET_SHIFT_PROXIMITY_ARST = 6
    AUTO_RESET_MASK_PROXIMITY_ARST = 0b11 << AUTO_RESET_SHIFT_PROXIMITY_ARST


    # Value Variables 
    # IDs
    DEFAULT_CY8CMBR3102_FAMILY_ID = 0x9A # When polling the FAMILY_ID register, this should be returned on boot.
    DEFAULT_CY8CMBR3102_DEVICE_ID = 0xA01 # When polling the DEVICE_ID register, this should be returned on boot.

    # Sensitivities
    # Sensitivity values (counts per pF)
    CS_SENSITIVITY_500_COUNTS_PER_PF = 0  # 50 counts/0.1pF
    CS_SENSITIVITY_250_COUNTS_PER_PF = 1  # 50 counts/0.2pF
    CS_SENSITIVITY_167_COUNTS_PER_PF = 2  # 50 counts/0.3pF
    CS_SENSITIVITY_125_COUNTS_PER_PF = 3  # 50 counts/0.4pF

    # Refresh Intervals
    REFRESH_INTERVAL_20MS = 1
    REFRESH_INTERVAL_40MS = 2
    REFRESH_INTERVAL_60MS = 3
    REFRESH_INTERVAL_80MS = 4
    REFRESH_INTERVAL_100MS = 5
    REFRESH_INTERVAL_120MS = 6
    REFRESH_INTERVAL_140MS = 7
    REFRESH_INTERVAL_160MS = 8
    REFRESH_INTERVAL_180MS = 9
    REFRESH_INTERVAL_200MS = 10
    REFRESH_INTERVAL_220MS = 11
    REFRESH_INTERVAL_240MS = 12
    REFRESH_INTERVAL_260MS = 13
    REFRESH_INTERVAL_280MS = 14
    REFRESH_INTERVAL_300MS = 15
    REFRESH_INTERVAL_320MS = 16
    REFRESH_INTERVAL_340MS = 17
    REFRESH_INTERVAL_360MS = 18
    REFRESH_INTERVAL_380MS = 19
    REFRESH_INTERVAL_400MS = 20
    REFRESH_INTERVAL_420MS = 21
    REFRESH_INTERVAL_440MS = 22
    REFRESH_INTERVAL_460MS = 23
    REFRESH_INTERVAL_480MS = 24
    REFRESH_INTERVAL_500MS = 25

    # Auto Reset Timeouts
    AUTO_RESET_TIMEOUT_DISABLED = 0
    AUTO_RESET_TIMEOUT_5_SECONDS = 1
    AUTO_RESET_TIMEOUT_20_SECONDS = 2

    # Commands
    CTRL_CMD_NO_OP = 0
    CTRL_CMD_SAVE_CONFIG = 2
    CTRL_CMD_CALC_CRC = 3
    CTRL_CMD_DEEP_SLEEP = 7
    CTRL_CMD_RESET_LATCH = 8
    CTRL_CMD_ALP_RESET_PS0 = 9
    CTRL_CMD_ALP_RESET_PS1 = 10
    CTRL_CMD_SW_RESET = 255
    
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
        # Check ID registers to confirm connected
        family_id = self.get_family_id()
        device_id = self.get_device_id()
        if (family_id != self.DEFAULT_CY8CMBR3102_FAMILY_ID or
            device_id != self.DEFAULT_CY8CMBR3102_DEVICE_ID):
            return False
        
        return True

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
        
        if not self.set_sensitivity_cs0(self.CS_SENSITIVITY_500_COUNTS_PER_PF):
            return False

        if not self.set_refresh_interval(self.REFRESH_INTERVAL_100MS):
            return False
        
        if not self.set_spo0_config(5):  # Set as GPO0
            return False

        if not self.set_gpo_config(control_by_host=True, pwm_output=False, strong_drive=True, active_high=False):
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
        family_id = self._read_byte_with_retry(self.REG_FAMILY_ID)
        
        return family_id
    
    def get_device_id(self):
        """!
        Reads and returns the Device ID register

        @return **int** The Device ID value
        """
        # Read the Device ID register
        device_id = self._read_word_with_retry(self.REG_DEVICE_ID)
        
        return device_id
    
    def enable(self, cs = 0, enable=True):
        """!
        Enables or disables the capacitive sensor 0 (CS0)

        @param cs: The capacitive sensor number (only 0 and 1 are supported)
        @param enable: If `True`, enables CS0
            If `False`, disables CS0

        @return Returns `True` if successful, otherwise `False`
        """
        sensorEnVal = self._read_word_with_retry(self.REG_SENSOR_EN)

        if cs == 0:
            # Configure CS0 enable/disable
            if enable:
                sensorEnVal |= self.SENSOR_EN_MASK_CS0
            else:
                sensorEnVal &= ~self.SENSOR_EN_MASK_CS0
        
        elif cs == 1:
            # Configure CS1 enable/disable
            if enable:
                sensorEnVal |= self.SENSOR_EN_MASK_CS1
            else:
                sensorEnVal &= ~self.SENSOR_EN_MASK_CS1
        
        else:
            return False  # Invalid capacitive sensor number

        # Write the sensor enable value to the SENSOR_EN register
        self._write_word_with_retry(self.REG_SENSOR_EN, sensorEnVal)

        return True

    def set_auto_reset_enable(self, enable=True, timeout=AUTO_RESET_TIMEOUT_5_SECONDS):
        """!
        Enables or disables the auto-reset feature for buttons and sliders

        @param enable: If `True`, enables auto-reset
            If `False`, disables auto-reset
        @param timeout: The auto-reset timeout to set
            Use one of the AUTO_RESET_TIMEOUT_* constants defined in this class

        @return Returns `True` if successful, otherwise `False`
        """
        # Ensure valid inputs
        if timeout < self.AUTO_RESET_TIMEOUT_DISABLED or timeout > self.AUTO_RESET_TIMEOUT_20_SECONDS:
            return False  # Invalid auto-reset timeout value
        
        deviceCfg2Val = self._read_byte_with_retry(self.REG_DEVICE_CFG2)

        if enable:
            deviceCfg2Val &= ~self.AUTO_RESET_MASK_PROXIMITY_ARST
            deviceCfg2Val |= (timeout << self.AUTO_RESET_SHIFT_PROXIMITY_ARST) & self.AUTO_RESET_MASK_PROXIMITY_ARST

            deviceCfg2Val &= ~self.AUTO_RESET_MASK_BUTTON_SLD_ARST
            deviceCfg2Val |= (timeout << self.AUTO_RESET_SHIFT_BUTTON_SLD_ARST) & self.AUTO_RESET_MASK_BUTTON_SLD_ARST
        else:
            deviceCfg2Val &= ~self.AUTO_RESET_MASK_PROXIMITY_ARST
            deviceCfg2Val |= (self.AUTO_RESET_TIMEOUT_DISABLED << self.AUTO_RESET_SHIFT_PROXIMITY_ARST) & self.AUTO_RESET_MASK_PROXIMITY_ARST

            deviceCfg2Val &= ~self.AUTO_RESET_MASK_BUTTON_SLD_ARST
            deviceCfg2Val |= (self.AUTO_RESET_TIMEOUT_DISABLED << self.AUTO_RESET_SHIFT_BUTTON_SLD_ARST) & self.AUTO_RESET_MASK_BUTTON_SLD_ARST

        # Write the updated device configuration value back to the DEVICE_CFG2 register
        self._write_byte_with_retry(self.REG_DEVICE_CFG2, deviceCfg2Val)

        return True

    def set_spo0_config(self, config):
        """!
        Sets the SPO0 configuration

        @param config: The 3-bit SPO0 function value (bits 2:0 of the SPO_CFG
            register; see the CY8CMBR3 register reference)

        @return Returns `True` if successful, otherwise `False`
        """
        # Ensure valid inputs
        spoCfgVal = self._read_byte_with_retry(self.REG_SPO_CFG)
        spoCfgVal &= ~self.SPO_CFG_MASK_SPO0
        spoCfgVal |= (config << self.SPO_CFG_SHIFT_SPO0) & self.SPO_CFG_MASK_SPO0

        # Write the SPO0 configuration to the device
        self._write_byte_with_retry(self.REG_SPO_CFG, spoCfgVal)

        return True

    def set_sensitivity_cs0(self, sensitivity):
        """!
        Sets the sensitivity for the capacitive sensor 0 (CS0)

        @param sensitivity: The sensitivity value to set
            Use one of the CS_SENSITIVITY_* constants defined in this class

        @return Returns `True` if successful, otherwise `False`
        """
        if sensitivity < self.CS_SENSITIVITY_500_COUNTS_PER_PF or sensitivity > self.CS_SENSITIVITY_125_COUNTS_PER_PF:
            return False  # Invalid sensitivity value
        
        # Read the current SENSITIVITY register value
        sensVal = self._read_byte_with_retry(self.REG_SENSITIVITY0)

        # Clear the bits associated with the capacitive sensor
        sensVal &= ~self.SENSITIVITY0_MASK_CS0

        # Set the new sensitivity value
        sensVal |= (sensitivity << self.SENSITIVITY0_SHIFT_CS0) & self.SENSITIVITY0_MASK_CS0

        # Write the updated sensitivity value back to the register
        self._write_byte_with_retry(self.REG_SENSITIVITY0, sensVal)

        return True
    
    def set_refresh_interval(self, interval):
        """!
        Sets the refresh interval for the capacitive sensor

        @param interval: The refresh interval value to set
            Use one of the REFRESH_INTERVAL_* constants defined in this class

        @return Returns `True` if successful, otherwise `False`
        """
        if interval < self.REFRESH_INTERVAL_20MS or interval > self.REFRESH_INTERVAL_500MS:
            return False  # Invalid refresh interval value
        
        # Write the refresh interval value to the REFRESH_CTRL register
        self._write_byte_with_retry(self.REG_REFRESH_CTRL, interval)

        return True
    
    def set_gpo_config(self, control_by_host, pwm_output, strong_drive, active_high):
        """!
        Configures the GPO0 settings

        @param control_by_host: If `True`, GPO0 is controlled by the host
            If `False`, GPO0 is controlled by the device
        @param pwm_output: If `True`, GPO0 outputs PWM signal
            If `False`, GPO0 outputs digital signal
        @param strong_drive: If `True`, GPO0 uses strong drive mode
            If `False`, GPO0 uses weak drive mode
        @param active_high: If `True`, GPO0 is active high
            If `False`, GPO0 is active low

        @return Returns `True` if successful, otherwise `False`
        """
        gpoCfgVal = self._read_byte_with_retry(self.REG_GPO_CFG)

        # Configure control by host/device
        if control_by_host:
            gpoCfgVal |= self.GPO_CFG_MASK_GPO0_GPO_CTL
        else:
            gpoCfgVal &= ~self.GPO_CFG_MASK_GPO0_GPO_CTL
        
        # Configure PWM/digital output
        if pwm_output:
            gpoCfgVal |= self.GPO_CFG_MASK_GPO0_GPO_PWM
        else:
            gpoCfgVal &= ~self.GPO_CFG_MASK_GPO0_GPO_PWM

        # Configure strong/weak drive mode
        if strong_drive:
            gpoCfgVal |= self.GPO_CFG_MASK_GPO0_DRIVE_MODE
        else:
            gpoCfgVal &= ~self.GPO_CFG_MASK_GPO0_DRIVE_MODE
        
        # Configure active high/low
        if active_high:
            gpoCfgVal |= self.GPO_CFG_MASK_GPO0_ACTIVE_STATE
        else:
            gpoCfgVal &= ~self.GPO_CFG_MASK_GPO0_ACTIVE_STATE
       
        # Write the GPO configuration value to the GPO_CFG register
        self._write_byte_with_retry(self.REG_GPO_CFG, gpoCfgVal)

        return True
    
    def led_on(self, enable=True):
        """!
        Sets the GPO0 output state to turn on/off an LED

        @param enable: If `True`, turns on the LED
            If `False`, turns off the LED

        @return Returns `True` if successful, otherwise `False`
        """
        gpoOutputVal = self._read_byte_with_retry(self.REG_GPO_OUTPUT_STATE)

        if enable:
            gpoOutputVal &= ~self.GPO_OUTPUT_STATE_MASK_GPO0  # Active low
        else:
            gpoOutputVal |= self.GPO_OUTPUT_STATE_MASK_GPO0

        # Write the GPO output state value to the GPO_OUTPUT_STATE register
        self._write_byte_with_retry(self.REG_GPO_OUTPUT_STATE, gpoOutputVal)

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
        debugSensorId = self._read_byte_with_retry(self.REG_DEBUG_SENSOR_ID)
        
        return debugSensorId
    
    def set_sensor_id(self, sensor_id=0):
        """!
        Sets the Sensor ID register

        @param sensor_id: The Sensor ID value to set

        @return Returns `True` if successful, otherwise `False`
        """
        # Write the Sensor ID value to the SENSOR_ID register
        self._write_byte_with_retry(self.REG_SENSOR_ID, sensor_id)

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
        capacitancePf = self._read_byte_with_retry(self.REG_DEBUG_CP)

        return capacitancePf

    def get_diff_count(self):
        """!
        Reads and returns the difference count value from CS0

        @return **int** The difference count value
        """
        # Read the difference count value from the DIFF_CNT0 register
        diffCount = self._read_word_with_retry(self.REG_DIFF_CNT0)

        return diffCount
    
    def get_diff_pf(self):
        """!
        Reads and returns the difference count value from CS0 in picofarads (pF)

        @return **float** The difference count value in pF
        """
        # Read the difference count value from the DIFF_CNT0 register
        diffCount = self.get_diff_count()

        # Read the sensitivity setting for CS0
        sensVal = self._read_byte_with_retry(self.REG_SENSITIVITY0)
        sensitivitySetting = (sensVal & self.SENSITIVITY0_MASK_CS0) >> self.SENSITIVITY0_SHIFT_CS0

        # Map sensitivity setting to counts per pF
        if sensitivitySetting == self.CS_SENSITIVITY_500_COUNTS_PER_PF:
            countsPerPf = 500
        elif sensitivitySetting == self.CS_SENSITIVITY_250_COUNTS_PER_PF:
            countsPerPf = 250
        elif sensitivitySetting == self.CS_SENSITIVITY_167_COUNTS_PER_PF:
            countsPerPf = 167
        elif sensitivitySetting == self.CS_SENSITIVITY_125_COUNTS_PER_PF:
            countsPerPf = 125
        else:
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
        baselineCount = self._read_word_with_retry(self.REG_DEBUG_BASELINE0)

        return baselineCount
    
    def check_saturation(self, raw_count):
        """!
        Checks if the raw count value indicates saturation

        @param raw_count: The raw count value to check

        @return **bool** `True` if saturated, otherwise `False`
        """
        # Read the current sensitivity setting for CS0
        sensVal = self._read_byte_with_retry(self.REG_SENSITIVITY0)
        sensitivitySetting = (sensVal & self.SENSITIVITY0_MASK_CS0) >> self.SENSITIVITY0_SHIFT_CS0

        if sensitivitySetting == self.CS_SENSITIVITY_500_COUNTS_PER_PF:
            saturationThreshold = 4094
        elif sensitivitySetting == self.CS_SENSITIVITY_250_COUNTS_PER_PF:
            saturationThreshold = 2046
        elif sensitivitySetting == self.CS_SENSITIVITY_167_COUNTS_PER_PF:
            saturationThreshold = 1022
        elif sensitivitySetting == self.CS_SENSITIVITY_125_COUNTS_PER_PF:
            saturationThreshold = 1022
    
        return raw_count == saturationThreshold
    
    def get_raw_count(self, auto_calibrate=False):
        """!
        Reads and returns the raw count value from CS0

        @param auto_calibrate: If `True`, performs auto-calibration if saturation is detected.

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
        raw_count = self._read_word_with_retry(self.REG_DEBUG_RAW_CNT0)

        # If autocalibration is enabled, we'll call reset() if the raw count is at maximum (saturated)
        if auto_calibrate:
            if self.check_saturation(raw_count):
                self.reset()

        return raw_count
    
    def is_ctrl_command_complete(self):
        """!
        Determines if the last control command has completed

        @return **bool** `True` if the last command is complete, otherwise `False`
        """
        ctrlCmd = self._read_byte_with_retry(self.REG_CTRL_CMD)

        # If CTRL_CMD is 0, then the last command is complete
        return (ctrlCmd == self.CTRL_CMD_NO_OP)
    
    def send_ctrl_command(self, command, wait_for_completion=True):
        """!
        Sends a control command to the device

        @param command: The control command to send
        @param wait_for_completion: If `True`, waits for the command to complete

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Write the command to the CTRL_CMD register
        if not self._write_byte_with_retry(self.REG_CTRL_CMD, command):
            return False

        if not wait_for_completion:
            return True

        # Wait for the command to complete
        while not self.is_ctrl_command_complete():
            pass  # Optionally, add a timeout here to avoid infinite loops

        # Read the CTRL_CMD_ERR register to check for errors
        ctrlCmdErr = self._read_byte_with_retry(self.REG_CTRL_CMD_ERR)
        if ctrlCmdErr is None:
            return False

        if ctrlCmdErr != 0:  # Assuming 0 means no error
            return False

        return True  # Return true to indicate success
    
    def save_config(self):
        """!
        Saves the current configuration to non-volatile memory

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Calculate the CRC (using the CALC_CRC register) for the current configuration and load it in the CONFIG_CRC register
        if not self.send_ctrl_command(self.CTRL_CMD_CALC_CRC):
            return False

        # Read the calculated CRC from the CALC_CRC register
        calcCrc = self._read_word_with_retry(self.REG_CALC_CRC)
        if calcCrc is None:
            return False

        # Write the calculated CRC to the CONFIG_CRC register
        if not self._write_word_with_retry(self.REG_CONFIG_CRC, calcCrc):
            return False

        # Send the SAVE_CONFIG command to save the current configuration to non-volatile memory
        if not self.send_ctrl_command(self.CTRL_CMD_SAVE_CONFIG):
            return False

        return True  # Return true to indicate success
    
    def set_i2c_address(self, new_address):
        """!
        Sets a new I2C address for the device

        @param new_address: The new I2C address to set

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        if new_address not in self.available_addresses:
            return False  # Invalid I2C address

        # Write the new I2C address to the I2C_ADDR register
        if not self._write_byte_with_retry(self.REG_I2C_ADDR, new_address):
            return False

        # Save the configuration to non-volatile memory
        if not self.save_config():
            return False
        
        # Reset but do not wait for completion as the address will change directly after
        if not self.reset(wait_for_completion=False):
            return False

        # Update the instance's address to the new address
        self.address = new_address

        # wait for the command to complete on the new address
        completionRetries = 10
        while completionRetries > 0:
            if self.is_ctrl_command_complete():
                break
            completionRetries -= 1
            self._i2c.delay_ms(100)  # Small delay before retrying

        return True  # Return true to indicate success
    
    def reset(self, wait_for_completion=True):
        """!
        Performs a software reset of the device

        @param wait_for_completion: If `True`, waits for the reset to complete

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Send the SW_RESET command to perform a software reset
        if not self.send_ctrl_command(self.CTRL_CMD_SW_RESET, wait_for_completion):
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
            except Exception:
                pass  # Try again

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
            except Exception:
                pass  # Try again
        
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
            except Exception:
                pass  # Try again
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
            except Exception:
                pass  # Try again
        return False
