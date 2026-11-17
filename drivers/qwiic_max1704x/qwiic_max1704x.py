#-------------------------------------------------------------------------------
# qwiic_max1704x.py
#
# Python library for the SparkFun max1704x boards, available here:
# https://www.sparkfun.com/products/20680
# https://www.sparkfun.com/products/17715
# 
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
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
qwiic_max1704x
============
Python module for the [SparkFun Qwiic MAX1704X](https://www.sparkfun.com/products/20680, https://www.sparkfun.com/products/17715)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_MAX1704x_Fuel_Gauge_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic MAX1704X"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x36]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicMAX1704X(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Device types:
    kDeviceTypeMAX17043 = 0
    kDeviceTypeMAX17044 = 1
    kDeviceTypeMAX17048 = 2
    kDeviceTypeMAX17049 = 3

    # Register Map
    kRegVcell = 0x02          # R - 12-bit A/D measurement of battery voltage
    kRegSoc = 0x04            # R - 16-bit state of charge (SOC)
    kRegMode = 0x06           # W - Sends special commands to IC
    kRegVersion = 0x08        # R - Returns IC version
    kRegHibRt = 0x0A          # R/W - (MAX17048/49) Thresholds for entering hibernate
    kRegConfig = 0x0C         # R/W - Battery compensation (default 0x971C)
    kRegCValrt = 0x14         # R/W - (MAX17048/49) Configures vcell range to generate alerts (default 0x00FF)
    kRegCRate = 0x16          # R - (MAX17048/49) Charge rate 0.208%/hr
    kRegVResetId = 0x18       # R/W - (MAX17048/49) Reset voltage and ID (default 0x96__)
    kRegStatus = 0x1A         # R/W - (MAX17048/49) Status of ID (default 0x01__)
    kRegCommand = 0xFE        # W - Sends special commands to IC

    # MAX17043 Mode Coms
    kModeQuickStart = 0x4000  # On the MAX17048/49 this also clears the EnSleep bit

    # MAX17048 Mode Coms
    kModeEnSleep = 0x2000  # Enables sleep mode (the SLEEP bit in the CONFIG reg engages sleep)
    kModeHibStat = 0x1000  # Indicates when the IC is in hibernate mode

    # VResetId Shifts and Masks (Only applicable for Max17048/49)
    kVResetIdVResetShift = 9
    kVResetIdVResetMask = 0x7F << kVResetIdVResetShift

    kVResetIdComparatorDisShift = 8
    kVResetIdComparatorDisMask = 0x01 << kVResetIdComparatorDisShift

    # Status Shifts and Masks (Only applicable for Max17048/49)
    kStatusShift = 8
    kStatusMask = 0x7F << kStatusShift

    kStatusRiShift = 8
    kStatusRiMask = 0x01 << kStatusRiShift

    kStatusVhShift = 9
    kStatusVhMask = 0x01 << kStatusVhShift

    kStatusVlShift = 10
    kStatusVlMask = 0x01 << kStatusVlShift

    kStatusVrShift = 11
    kStatusVrMask = 0x01 << kStatusVrShift

    kStatusHdShift = 12
    kStatusHdMask = 0x01 << kStatusHdShift

    kStatusScShift = 13
    kStatusScMask = 0x01 << kStatusScShift

    kStatusEnVrShift = 14
    kStatusEnVrMask = 0x01 << kStatusEnVrShift

    # Config Shifts and Masks
    kConfigAlertShift = 5
    kConfigAlertMask = 0x01 << kConfigAlertShift

    kConfigSocAlertShift = 6
    kConfigSocAlertMask = 0x01 << kConfigSocAlertShift

    kConfigSleepShift = 7
    kConfigSleepMask = 0x01 << kConfigSleepShift

    kConfigThresholdShift = 0
    kConfigThresholdMask = 0x1F << kConfigThresholdShift

    kConfigCompShift = 8
    kConfigCompMask = 0xFF << kConfigCompShift

    # MAX17048 Hibernate Modes
    kMax17048HibRtEnHib = 0xFFFF  # always use hibernate mode
    kMax17048HibRtDisHib = 0x0000  # disable hibernate mode

    def __init__(self, address=None, i2c_driver=None, device_type = kDeviceTypeMAX17043):
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

        # Default to MAX17043, and full-scale for MAX17043
        self._device = self.kDeviceTypeMAX17043
        self._full_scale = 5.12
        self.set_device(device_type)

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        # TODO: If the device has a product ID register, that should be
        # checked in addition to the ACK
        if not self._i2c.isDeviceConnected(self.address):
            return False
        
        version = self.read16(self.address, self.kRegVersion)

        # Extra test - but only for MAX17048/9
        if self._device >= self.kDeviceTypeMAX17048:
            # Get version should return 0x001_
            # Supported on 48/49
            if version & (1 << 4) == 0:
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


    def set_device(self, device_type):
        """!
        Set the device type. Do this after instantiation but before .begin()

        @param int device_type: The device type to set
        """
        self._device = device_type

        # Define the full-scale voltage for VCELL based on the device
        if device_type == self.kDeviceTypeMAX17044:
            self._full_scale = 10.24  # MAX17044 VCELL is 12-bit, 2.50mV per LSB
        elif device_type == self.kDeviceTypeMAX17048:
            self._full_scale = 5.12  # MAX17048 VCELL is 16-bit, 78.125uV/cell per LSB
        elif device_type == self.kDeviceTypeMAX17049:
            self._full_scale = 10.24  # MAX17049 VCELL is 16-bit, 78.125uV/cell per LSB (i.e. 156.25uV per LSB)
        else:  # Default is the MAX17043
            self._full_scale = 5.12  # MAX17043 VCELL is 12-bit, 1.25mV per LSB
    
    def quick_start(self):
        """!
        A quick-start allows the MAX17043 to restart fuel-gauge calculations in the
        same manner as initial power-up of the IC. If an application's power-up
        sequence is exceedingly noisy such that excess error is introduced into the
        IC's "first guess" of SOC, the host can issue a quick-start to reduce the
        error. A quick-start is initiated by a rising edge on the QSTRT pin, or
        through software by writing 4000h to MODE register.

        Note: on the MAX17048/49 this will also clear / disable EnSleep bit
        """
        self.write16(self.address, self.kRegMode, self.kModeQuickStart)

    def get_voltage(self):
        """!
        Get the MAX17043's voltage reading.
        Output: floating point value between 0-5V in 1.25mV increments.

        @return **float** The voltage as a floating point value
        """
        vcell = self.read16(self.address, self.kRegVcell)
        
        if self._device <= self.kDeviceTypeMAX17044:
            # On the MAX17043/44: vCell is a 12-bit register where each bit represents:
            # 1.25mV on the MAX17043
            # 2.5mV on the MAX17044
            vcell = vcell >> 4 # Align the 12 bits
            divider = 4096.0 / self._full_scale
            return vcell / divider
        else:
            # On the MAX17048/49: vCell is a 16-bit register where each bit represents:
            # 78.125uV on the MAX17048
            # 156.25uV on the MAX17049
            divider = 65536.0 / self._full_scale
            return vcell / divider

    def get_soc(self):
        """!
        get_soc() - Get the MAX17043's state-of-charge (SOC) reading, as calculated
        by the IC's "ModelGauge" algorithm.
        The first update is available approximately 1s after POR of the IC.
        Output: floating point value between 0-100, representing a percentage of
        full charge.

        @return **float** The state of charge as a percentage
        """

        soc = self.read16(self.address, self.kRegSoc)
        percent = (soc & 0xFF00) >> 8
        percent += (soc & 0x00FF) / 256.0
        return percent

    def get_version(self):
        """!
        Get the MAX17043's version number.
        Output: 16-bit value representing the version number.

        @return **int** The version number
        """
        return self.read16(self.address, self.kRegVersion)

    def get_id(self):
        """!
        get_id() - (MAX17048/49) Returns 8-bit OTP bits set at factory. Can be used to
        'to distinguish multiple cell types in production'.

        Writes to these bits are ignored.
        """
        
        if self._device <= self.kDeviceTypeMAX17044:
            return 0
        
        vreset_id = self.read16(self.address, self.kRegVResetId)
        return vreset_id & 0xFF

    def set_reset_voltage_threshold(self, threshold):
        """!
        set_reset_voltage_threshold(threshold) - (MAX17048/49) Set the 7-bit VRESET value.
        A 7-bit value that controls the comparator for detecting when
        a battery is detached and re-connected. 40mV per bit. Default is 3.0V.
        For captive batteries, set to 2.5V. For
        removable batteries, set to at least 300mV below the
        application's empty voltage, according to the desired
        reset threshold for your application.
        Input: [threshold] - Should be a value between 0-127.
        Output: 0 on success, positive integer on fail.

        @param int threshold: The threshold value to set

        @return  True if successful, otherwise False
        
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        if threshold < 0 or threshold > 127:
            return False
        
        vreset_id = self.read16(self.address, self.kRegVResetId)
        vreset_id &= (~self.kVResetIdVResetMask)
        vreset_id |= threshold << self.kVResetIdVResetShift
        
        self.write16(self.address, self.kRegVResetId, vreset_id)

    def set_reset_voltage_volts(self, threshold_volts):
        """!
        Helper function to set the reset voltage threshold in volts

        @param float threshold_volts: The threshold voltage to set

        @return **bool** True if successful, otherwise False
        """

        thresh = int(max(min(threshold_volts, 5.08), 0.0) / 0.04)

        return self.set_reset_voltage_threshold(thresh)

    def enable_comparator(self):
        """!
        enable_comparator() - (MAX17048/49) Set bit in VRESET/ID reg
        Comparator is enabled by default. (Re)enable the analog comparator, uses 0.5uA.

        @return **bool** True if successful, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        vreset_id = self.read16(self.address, self.kRegVResetId)
        vreset_id &= (~self.kVResetIdComparatorDisMask)
        self.write16(self.address, self.kRegVResetId, vreset_id)

    def disable_comparator(self):
        """!
        disable_comparator() - (MAX17048/49) Clear bit in VRESET/ID reg
        Disable the analog comparator, saves 0.5uA in hibernate mode.

        @return **bool** True if successful, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        vreset_id = self.read16(self.address, self.kRegVResetId)
        vreset_id |= self.kVResetIdComparatorDisMask
        self.write16(self.address, self.kRegVResetId, vreset_id)

    def get_change_rate(self):
        """!
        get_change_rate() - (MAX17048/49) Get rate of change per hour in %
        Output: (signed) Float (that is the 0.208% * CRATE register value)
        A positive rate is charging, negative is discharge.
        """
            
        if self._device <= self.kDeviceTypeMAX17044:
            return 0
        
        crate = self.read16(self.address, self.kRegCRate)

        # convert from unsinged to signed 16-bit
        if crate > 32767:
            crate -= 65536

        return crate * 0.208
    
    # TODO: If these next two fns aren't used, remove them
    def get_status(self):
        """!
        (MAX17048/49) Get the 7 bits of status register

        @return **int** 7-bit value indicating various alerts
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return 0

        status = self.read16(self.address, self.kRegStatus)
        return (status & self.kStatusMask) >> self.kStatusShift
    
    def clear_status_reg_bits(self, mask):
        """!
        clear_status_reg_bits() - (MAX17048/49) Clear the specified mask in the status reg

        @param int mask: The mask to clear
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False

        status = self.read16(self.address, self.kRegStatus)
        status &= ~mask
        self.write16(self.address, self.kRegStatus, status)

    def is_reset(self, clear = False):
        """!
        is_reset() - (MAX17048/49) Check if the reset bit is set in the status register

        @param bool clear: If True, the reset bit is cleared

        @return **bool** True if the reset bit is set, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False

        status = self.read16(self.address, self.kRegStatus)
        reset = (status & self.kStatusRiMask) == self.kStatusRiMask

        if clear and reset:
            self.clear_status_reg_bits(self.kStatusRiMask)
        
        return reset
        
    def is_voltage_high(self, clear = False):
        """!
        is_voltage_high() - (MAX17048/49) Check if the voltage high bit is set in the status register

        @param bool clear: If True, the voltage high bit is cleared

        @return **bool** True if the voltage high bit is set, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False

        status = self.read16(self.address, self.kRegStatus)
        vh = (status & self.kStatusVhMask) == self.kStatusVhMask

        if clear and vh:
            self.clear_status_reg_bits(self.kStatusVhMask)
        
        return vh

    def is_voltage_low(self, clear = False):
        """!
        is_voltage_low() - (MAX17048/49) Check if the voltage low bit is set in the status register

        @param bool clear: If True, the voltage low bit is cleared

        @return **bool** True if the voltage low bit is set, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False

        status = self.read16(self.address, self.kRegStatus)
        vl = (status & self.kStatusVlMask) == self.kStatusVlMask

        if clear and vl:
            self.clear_status_reg_bits(self.kStatusVlMask)
        
        return vl
    
    def is_voltage_reset(self, clear = False):
        """!
        is_voltage_reset() - (MAX17048/49) Check if the voltage reset bit is set in the status register

        @param bool clear: If True, the voltage reset bit is cleared

        @return **bool** True if the voltage reset bit is set, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False

        status = self.read16(self.address, self.kRegStatus)
        vr = (status & self.kStatusVrMask) == self.kStatusVrMask

        if clear and vr:
            self.clear_status_reg_bits(self.kStatusVrMask)
        
        return vr
    
    def is_low(self, clear = False):
        """!
        is_low() - (MAX17048/49) Check if the low bit is set in the status register

        @param bool clear: If True, the low bit is cleared

        @return **bool** True if the low bit is set, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False

        status = self.read16(self.address, self.kRegStatus)
        hd = (status & self.kStatusHdMask) == self.kStatusHdMask

        if clear and hd:
            self.clear_status_reg_bits(self.kStatusHdMask)
        
        return hd
    
    def is_change(self,clear = False):
        """!
        is_change() - (MAX17048/49) Check if the change bit is set in the status register

        @param bool clear: If True, the change bit is cleared

        @return **bool** True if the change bit is set, otherwise False
        """
        if self._device <= self.kDeviceTypeMAX17044:
            return False

        status = self.read16(self.address, self.kRegStatus)
        sc = (status & self.kStatusScMask) >> self.kStatusScShift

        if clear and sc:
            self.clear_status_reg_bits(self.kStatusScMask)
        
        return sc
    
    def clear_alert(self):
        """!
        clearAlert() - Clear the MAX1704X's ALRT alert flag.
        """

        config = self.read16(self.address, self.kRegConfig)
        config &= ~self.kConfigAlertMask
        self.write16(self.address, self.kRegConfig, config)

    def get_alert(self, clear = False):
        """!
        get_alert() - Check if the MAX1704X's ALRT alert interrupt has been triggered.

        @param bool clear: If True, the alert flag will be cleared if it was set

        @return  True if the alert interrupt is/was triggered, otherwise False
        
        """
        
        config = self.read16(self.address, self.kRegConfig)
        alert = (config & self.kConfigAlertMask) == self.kConfigAlertMask

        if clear and alert:
            config &= ~self.kConfigAlertMask
            self.write16(self.address, self.kRegConfig, config)
        
        return alert

    def enable_soc_alert(self):
        """!
        enable_soc_alert() - (MAX17048/49) Enable the SOC change alert

        @return **bool** True if successful, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        config = self.read16(self.address, self.kRegConfig)
        config |= self.kConfigSocAlertMask
        self.write16(self.address, self.kRegConfig, config)

        # TODO: this check below existed for the arduino lib, but not sure it's needed
        config = self.read16(self.address, self.kRegConfig)
        return (config & self.kConfigSocAlertMask) == self.kConfigSocAlertMask
    
    def disable_soc_alert(self):
        """!
        disable_soc_alert() - (MAX17048/49) Disable the SOC change alert

        @return **bool** True if successful, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        config = self.read16(self.address, self.kRegConfig)
        config &= ~self.kConfigSocAlertMask
        self.write16(self.address, self.kRegConfig, config)

        # TODO: this check below existed for the arduino lib, but not sure it's needed
        config = self.read16(self.address, self.kRegConfig)
        return (config & self.kConfigSocAlertMask) == 0
    
    def enable_alert(self):
        """!
        enable_alert() - Enable the MAX1704X's VRESET Alert

        EnVr (enable voltage reset alert) when set to 1 asserts
        the ALRT pin when a voltage-reset event occurs under
        the conditions described by the VRESET/ ID register.
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False

        status = self.read16(self.address, self.kRegStatus)
        status |= self.kStatusEnVrMask

        self.write16(self.address, self.kRegStatus, status)
    
    def disable_alert(self):
        """!
        disable_alert() - Disable the MAX1704X's VRESET Alert

        EnVr (enable voltage reset alert) when set to 1 asserts
        the ALRT pin when a voltage-reset event occurs under
        the conditions described by the VRESET/ ID register.
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False

        status = self.read16(self.address, self.kRegStatus)
        status &= ~self.kStatusEnVrMask

        self.write16(self.address, self.kRegStatus, status)
    
    def get_threshold(self):
        """!
        get_threshold() - Get the MAX17043's current percentage threshold that will
        trigger an alert.

        @return **int** An integer value between 1 and 32, representing a % that will trigger an alert interrupt.
        """

        config = self.read16(self.address, self.kRegConfig)
        thresh = (config & self.kConfigThresholdMask) >> self.kConfigThresholdShift

        # It has an LSb weight of 1%, and can be programmed from 1% to 32%.
        # The value is (32 - ATHD)%, e.g.: 00000=32%, 00001=31%, 11111=1%.
        # Let's convert our percent to that first:
        return 32 - thresh


    def set_threshold(self, percent=4):
        """!
        set_threshold() - Set the MAX17043's percentage threshold that will
        trigger an alert.

        @param int percent: The percentage value that will trigger an alert interrupt.
            Any value between 1 and 32 is valid. Default value is 0x1C == 4%
        """

        if percent < 1 or percent > 32:
            return False
        
        #   The alert threshold is a 5-bit value that sets the state of charge level
        #   where an interrupt is generated on the ALRT pin.

        #   It has an LSb weight of 1%, and can be programmed from 1% to 32%.
        #   The value is (32 - ATHD)%, e.g.: 00000=32%, 00001=31%, 11111=1%.
        #   Let's convert our percent to that first:
        percent = max(min(percent, 32.0), 0.0)
        thresh = 32 - percent

        config = self.read16(self.address, self.kRegConfig)
        config &= ~self.kConfigThresholdMask
        config |= thresh << self.kConfigThresholdShift

        self.write16(self.address, self.kRegConfig, config)
    
    def sleep(self):
        """!
        sleep() - Set the MAX17043 into sleep mode.

        In sleep mode, the IC halts all operations, reducing current
        consumption to below 1uA. After exiting sleep mode,
        the IC continues normal operation. In sleep mode, the
        IC does not detect self-discharge. If the battery changes
        state while the IC sleeps, the IC cannot detect it, causing
        SOC error. Wake up the IC before charging or discharging.

        @return **bool** True if successful, otherwise False
        """

        if self._device > self.kDeviceTypeMAX17044:
            self.write16(self.address, self.kRegMode, self.kModeEnSleep)
        
        config = self.read16(self.address, self.kRegConfig)
        if config & self.kConfigSleepMask:
            return False # Already asleep
        
        config |= self.kConfigSleepMask
        self.write16(self.address, self.kRegConfig, config)

        return True
    
    def wake(self):
        """!
        wake() - Wake the MAX17043 up from sleep.

        @return **bool** True if successful, otherwise False
        """

        # Read config reg, so we don't modify any other values:
        config_reg = self.read16(self.address, self.kRegConfig)
        if not (config_reg & self.kConfigSleepMask):
            return False  # Already awake, do nothing but return an error

        config_reg &= ~self.kConfigSleepMask  # Clear sleep bit

        self.write16(self.address, self.kRegConfig, config_reg)

        if self._device > self.kDeviceTypeMAX17044:
            # On the MAX17048, we should also clear the EnSleep bit in the MODE register
            # Strictly, this will clear the QuickStart bit too.
            self.write16(self.address, self.kRegMode, 0x0000)
        
        return True
    

    def reset(self):
        """!
        Issue a Power-on-reset command to the MAX17043. This function
        will reset every register in the MAX17043 to its default value.
        """

        # Writing a value of 0x5400 to the CMD Register causes
        # the device to completely reset as if power had been
        # removed (see the Power-On Reset (POR) section). The
        # reset occurs when the last bit has been clocked in. The
        # IC does not respond with an I2C ACK after this command
        # sequence.
        # Output: Positive integer on success, 0 on fail.

        # TODO: will this upset our driver since we don't get an ack?
        self.write16(self.address, self.kRegCommand, 0x5400)


    def get_compensation(self):
        """!
        get_compensation() - Get the ModelGauge compensation value - an obscure
        8-bit value set to 0x97 by default.

        @return **int** The compensation value
        """
        return ( self.read16(self.address, self.kRegConfig) & 0xFF00 ) >> 8
    
    def set_compensation(self, newCompensation):
        """!
        set_compensation(newCompensation) - Set the 8-bit compensation value. This
        is an obscure 8-bit value that has some effect on Maxim's ModelGauge
        algorithm. The POR value of RCOMP is 0x97.

        From the datasheet: "Contact Maxim for instructions for optimization."
        For best performance, the host microcontroller must measure
        battery temperature periodically, and compensate
        the RCOMP ModelGauge parameter accordingly, at least
        once per minute. Each custom model defines constants
        RCOMP0 (default is 0x97), TempCoUp (default is -0.5),
        and TempCoDown (default is -5.0). To calculate the new
        value of CONFIG.RCOMP:

        // T is battery temperature (degrees Celsius)
        if (T > 20) { RCOMP = RCOMP0 + (T - 20) x TempCoUp;}
        else { RCOMP = RCOMP0 + (T - 20) x TempCoDown; }

        : param newCompensation: The new compensation value to set
        : type newCompensation: int

        : return: True if successful, otherwise False
        : rtype: bool
        """

        config = self.read16(self.address, self.kRegConfig)
        config &= ~self.kConfigCompMask
        config |= newCompensation << self.kConfigCompShift
        self.write16(self.address, self.kRegConfig, config)
    
    def set_valrt_max(self, threshold = 0xFF):
        """!
        Set the MAX17048/49 VALRT Maximum threshold

        This register is divided into two thresholds: Voltage alert
        maximum (VALRT.MAX) and minimum (VALRT. MIN).
        Both registers have 1 LSb = 20mV. The IC alerts while
        VCELL > VALRT.MAX or VCELL < VALRT.MIN

        @param int threshold: The threshold value to set
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        if threshold < 0 or threshold > 0xFFFF:
            return False
        

        valrt = self.read16(self.address, self.kRegCValrt)
        valrt &= 0xFF00

        valrt |= threshold
        self.write16(self.address, self.kRegCValrt, valrt)
    

    def set_valrt_max_volts(self, threshold_volts = 5.1):
        """!
        Helper function to set the MAX17048/49 VALRT Maximum threshold in volts

        @param float threshold_volts: The threshold voltage to set

        @return **bool** True if successful, otherwise False
        """

        thresh = int(max(min(threshold_volts, 5.1), 0.0) / 0.02)

        return self.set_valrt_max(thresh)

    def get_valrt_max(self):
        """!
        Get the MAX17048/49 VALRT Maximum threshold
        LSb = 20mV

        @return **int** The threshold value
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return 0
        
        valrt = self.read16(self.address, self.kRegCValrt)
        return valrt & 0x00FF

    def set_valrt_min(self, threshold = 0x00 ):
        """!
        Set the MAX17048/49 VALRT Minimum threshold

        This register is divided into two thresholds: Voltage alert
        maximum (VALRT.MAX) and minimum (VALRT. MIN).
        Both registers have 1 LSb = 20mV. The IC alerts while
        VCELL > VALRT.MAX or VCELL < VALRT.MIN

        @param int threshold: The threshold value to set
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        if threshold < 0 or threshold > 0xFFFF:
            return False
        
        valrt = self.read16(self.address, self.kRegCValrt)
        valrt &= 0x00FF

        valrt |= threshold << 8
        self.write16(self.address, self.kRegCValrt, valrt)
    
    def set_valrt_min_volts(self, threshold_volts = 0.0):
        """!
        Helper function to set the MAX17048/49 VALRT Minimum threshold in volts

        @param float threshold_volts: The threshold voltage to set

        @return **bool** True if successful, otherwise False
        """

        thresh = int(max(min(threshold_volts, 5.1), 0.0) / 0.02)

        return self.set_valrt_min(thresh)

    def get_valrt_min(self):
        """!
        Get the MAX17048/49 VALRT Minimum threshold
        LSb = 20mV

        @return **int** The threshold value
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return 0
        
        valrt = self.read16(self.address, self.kRegCValrt)
        return (valrt & 0xFF00) >> 8

    def is_hibernating(self):
        """!
        is_hibernating() - (MAX17048/49) Check if the IC is in hibernate mode

        @return **bool** True if the IC is in hibernate mode, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        mode = self.read16(self.address, self.kRegMode)
        return (mode & self.kModeHibStat) == self.kModeHibStat
    
    def get_hibrt_act_thr(self):
        """!
        get_hibrt_act_thr() - (MAX17048/49)   Read and return the MAX17048/49 HIBRT Active Threshold
        LSb = 1.25mV

        @return **int** The hibernate threshold
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return 0
        
        hibrt = self.read16(self.address, self.kRegHibRt)
        return hibrt & 0xFF
    
    def set_hibrt_act_thr(self, threshold):
        """!
        Set the MAX17048/49 HIBRT Active Threshold
        LSb = 1.25mV
        """
        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        if threshold < 0 or threshold > 0xFF:
            return False
        
        hibrt = self.read16(self.address, self.kRegHibRt)
        hibrt &= 0xFF00

        hibrt |= threshold
        self.write16(self.address, self.kRegHibRt, hibrt)

        return True
    
    def get_hibrt_act_thr_volts(self, threshold_volts):
        """!
        Helper function to set the MAX17048/49 HIBRT ACT Threshold in volts

        @param float threshold_volts: The threshold voltage to set

        @return **bool** True if successful, otherwise False
        """
            
        thresh = int(max(min(threshold_volts, 0.31875), 0.0) / 0.00125)

        return self.set_hibrt_act_thr(thresh)
    
    def get_hibrt_hib_thr(self):
        """!
        get_hibrt_hib_thr() - (MAX17048/49)   Read and return the MAX17048/49 HIBRT Hibernate Threshold
        LSb = 1.25mV

        @return **int** The hibernate threshold
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return 0
        
        hibrt = self.read16(self.address, self.kRegHibRt)
        return (hibrt & 0xFF00) >> 8
    
    def set_hibrt_hib_thr(self, threshold):
        """!
        Set the MAX17048/49 HIBRT Hibernate Threshold
        LSb = 1.25mV
        """
        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        if threshold < 0 or threshold > 0xFF:
            return False
        
        hibrt = self.read16(self.address, self.kRegHibRt)
        hibrt &= 0x00FF

        hibrt |= threshold << 8
        self.write16(self.address, self.kRegHibRt, hibrt)

        return True

    def get_hibrt_hib_thr_percent(self, threshold_percent):
        """!
        Helper function to set the MAX17048/49 HIBRT Hibernate Threshold in percent
        LSb = 0.208%/hr

        @param float threshold_percent: The threshold percentage to set

        @return **bool** True if successful, otherwise False
        """

        thresh = int(max(min(threshold_percent, 53.04), 0.0) / 0.208)

        return self.set_hibrt_hib_thr(thresh)
    
    def enable_hibernate(self):
        """!
        enable_hibernate() - (MAX17048/49) Enable hibernate mode

        @return **bool** True if successful, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        self.write16(self.address, self.kRegHibRt, self.kModeEnHib)

        return True
    
    def disable_hibernate(self):
        """!
        disable_hibernate() - (MAX17048/49) Disable hibernate mode

        @return **bool** True if successful, otherwise False
        """

        if self._device <= self.kDeviceTypeMAX17044:
            return False
        
        self.write16(self.address, self.kRegHibRt, self.kModeDisHib)
        return True
    
    def write16(self, address, register, data):
        """!
        Write 16-bit data to a register (big-endian)

        @param int register: The register to write to
        @param int data: The data to write
        """

        bytes_to_write = [(data >> 8) & 0xFF, data & 0xFF]
        self._i2c.write_block(address, register, bytes_to_write)
    
    def read16(self, address, register):
        """!
        Read 16-bit data from a register (big-endian)

        @param int register: The register to read from

        @return **int** The data read
        """

        bytes_read = self._i2c.read_block(address, register, 2)
        return (bytes_read[0] << 8) | bytes_read[1]
