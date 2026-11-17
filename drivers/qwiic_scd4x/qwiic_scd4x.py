#-------------------------------------------------------------------------------
# qwiic_scd4x.py
#
# Python library for the SparkFun Qwiic SCD4x CO2 Sensor, available here:
# https://www.sparkfun.com/products/22396
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
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
qwiic_scd4x
============
Python module for the [SparkFun Qwiic SCD4x C02 sensor]https://www.sparkfun.com/products/22396
This is a port of the existing [Arduino Library]https://github.com/sparkfun/SparkFun_SCD4x_Arduino_Library
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
_DEFAULT_NAME = "Qwiic SCD4x"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [ 0x62]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicSCD4x(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Basic Commands
    kComStartPeriodicMeasurement = 0x21b1
    kComReadMeasurement = 0xec05  # execution time: 1ms
    kComStopPeriodicMeasurement = 0x3f86  # execution time: 500ms

    # On-chip output signal compensation
    kComSetTemperatureOffset = 0x241d  # execution time: 1ms
    kComGetTemperatureOffset = 0x2318  # execution time: 1ms
    kComSetSensorAltitude = 0x2427  # execution time: 1ms
    kComGetSensorAltitude = 0x2322  # execution time: 1ms
    kComSetAmbientPressure = 0xe000  # execution time: 1ms

    # Field calibration
    kComPerformForcedCalibration = 0x362f  # execution time: 400ms
    kComSetAutomaticSelfCalibrationEnabled = 0x2416  # execution time: 1ms
    kComGetAutomaticSelfCalibrationEnabled = 0x2313  # execution time: 1ms

    # Low power
    kComStartLowPowerPeriodicMeasurement = 0x21ac
    kComGetDataReadyStatus = 0xe4b8  # execution time: 1ms

    # Advanced features
    kComPersistSettings = 0x3615  # execution time: 800ms
    kComGetSerialNumber = 0x3682  # execution time: 1ms
    kComPerformSelfTest = 0x3639  # execution time: 10000ms
    kComPerformFactoryReset = 0x3632  # execution time: 1200ms
    kComReinit = 0x3646  # execution time: 20ms
    kComGetFeatureSetVersion = 0x202F  # execution time: 1ms

    # Low power single shot - SCD41 only
    kComMeasureSingleShot = 0x219d  # execution time: 5000ms
    kComMeasureSingleShotRhtOnly = 0x2196  # execution time: 50ms

    # Sensor types 
    kTypeSCD40 = 0
    kTypeSCD41 = 1
    kTypeSDC4xInvalid = 2

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

        self._sensorType = self.kTypeSCD40
        self._doingPeriodicMeasurement = False

        # Set by read_measurement
        self._co2 = 0
        self._humidity = 0
        self._temperature = 0

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self, measBegin = True, autoCalibrate = True, skipStopPeriodicMeasurement = False, pollAndSetDeviceType = True):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        # If periodic measurements are already running, get_serial_number will fail...
        # To be safe, let's stop period measurements before we do anything else
        # The user can override this by setting skipStopPeriodicMeasurements to True
        if skipStopPeriodicMeasurement == False:
            self.stop_periodic_measurement()

        success = True

        serial_number = self.get_serial_number()
        success &= (serial_number is not None)
        
        if pollAndSetDeviceType:
            success &= self.get_feature_set_version()
        
        success &= self.set_automatic_self_calibration_enabled(autoCalibrate)
        success &= (self.get_automatic_self_calibration_enabled() == autoCalibrate)

        if measBegin:
            self.start_periodic_measurement()

        return True

    def start_periodic_measurement(self):
        """!
        Start periodic measurements. See 3.5.1
        signal update interval is 5 seconds.
        """
        self.send_command(self.kComStartPeriodicMeasurement)
        self._doingPeriodicMeasurement = True

    def stop_periodic_measurement(self, delayMillis = 500):
        """!
        stop_periodic_measurement can be called before begin() if required
        Note that the sensor will only respond to other commands after waiting 500 ms after issuing the stop_periodic_measurement command.

        @param int delayMillis: The delay in milliseconds to wait after stopping the measurement
        """
        self.send_command(self.kComStopPeriodicMeasurement)
        self._doingPeriodicMeasurement = False
        time.sleep(delayMillis / 1000)
    
    def read_measurement(self):
        """!
        Get 9 bytes from SCD4x. See 3.5.2
        Updates the internal CO2, humidity, and temperature values
        Returns true if data is read successfully
        Read sensor output. The measurement data can only be read out once per signal update interval as the
        buffer is emptied upon read-out. If no data is available in the buffer, the sensor returns a NACK.
        To avoid a NACK response, the get_data_ready_status can be issued to check data status
        (see chapter 3.8.2 for further details).

        @return  `True` if successful, otherwise `False`
        :rtype
        
        """
        if self.get_data_ready_status() == False:
            return False

        self.send_command(self.kComReadMeasurement)

        time.sleep(0.001) # specified by datasheet

        bytes_read = self._i2c.readBlock(self.address, None, 9) # By passing "None" we perform a general read. Requires new version of qwiic_i2c
        co2_bytes = bytes_read[0:3]
        temperature_bytes = bytes_read[3:6]
        humidity_bytes = bytes_read[6:9]

        # Check CRC's
        for bytes in [co2_bytes, humidity_bytes, temperature_bytes]:
            if self.compute_crc8(bytes[0:2]) != bytes[2]:
                return False
        
        # Convert to 16-bit values
        self._co2 = (co2_bytes[0] << 8) | co2_bytes[1]
        self._humidity = (humidity_bytes[0] << 8) | humidity_bytes[1]
        self._temperature = (temperature_bytes[0] << 8) | temperature_bytes[1]

        # Perform conversions on the values (see 3.5.2)
        self._temperature = -45 + (self._temperature * 175 / 65536)
        self._humidity = self._humidity * 100 / 65536

        return True

    # TODO: Arduino lib has booleans tracking whether to refresh these automatically, we can add this if needed, but might be best to 
    #       force users to just call read_measurement() to explicitly refresh all of these at once so they are coherent
    def get_co2(self):
        """!
        Get the CO2 value. Call read_measurement() first to update the value

        @return **int** The CO2 value
        """
        return self._co2

    def get_humidity(self):
        """!
        Get the humidity value. Call read_measurement() first to update the value

        @return **int** The humidity value
        """
        return self._humidity
    
    def get_temperature(self):
        """!
        Get the temperature value. Call read_measurement() first to update the value

        @return **int** The temperature value
        """
        return self._temperature
    
    def set_temperature_offset(self, offset, delayMillis = 1):
        """!
        Set the temperature offset (C). See 3.6.1
        Max command duration: 1ms
        The user can set delayMillis to zero if they want the function to return immediately.
        The temperature offset has no influence on the SCD4x CO2 accuracy.
        Setting the temperature offset of the SCD4x inside the customer device correctly allows the user
        to leverage the RH and T output signal.

        @param int offset: The temperature offset to set. Must be between 0 and 175
        @param int delayMillis: The delay in milliseconds to wait after setting the offset

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._doingPeriodicMeasurement:
            return False

        if offset < 0 or offset >= 175:
            return False
        
        offset_word = int(offset * 65536 / 175) # Toffset [°C] * 2^16 / 175
        self.send_command(self.kComSetTemperatureOffset, offset_word)
        
        if delayMillis > 0:
            time.sleep(delayMillis / 1000)

        return True
    
    def get_temperature_offset(self):
        """!
        Get the temperature offset (C). See 3.6.2

        @return **int** The temperature offset or None if unsuccessful
        """
        if self._doingPeriodicMeasurement:
            return None
        
        offset = self.read_register(self.kComGetTemperatureOffset)
        if offset is None:
            return None
        
        return offset * 175 / 65536 # TODO: Arduino uses 65535 here but datasheet and other functions says 65536

    def set_sensor_altitude(self, altitude, delayMillis = 1):
        """!
        Set the sensor altitude (metres above sea level). See 3.6.3
        Max command duration: 1ms
        The user can set delayMillis to zero if they want the function to return immediately.
        Reading and writing of the sensor altitude must be done while the SCD4x is in idle mode.
        Typically, the sensor altitude is set once after device installation. To save the setting to the EEPROM,
        the persist setting (see chapter 3.9.1) command must be issued.
        Per default, the sensor altitude is set to 0 meter above sea-level.

        @param int altitude: The altitude to set
        @param int delayMillis: The delay in milliseconds to wait after setting the altitude
        """
        if self._doingPeriodicMeasurement:
            return False
        
        self.send_command(self.kComSetSensorAltitude, altitude)

        if delayMillis > 0:
            time.sleep(delayMillis / 1000)

    def get_sensor_altitude(self):
        """!
        Get the sensor altitude (metres above sea level). See 3.6.4

        @return **int** The sensor altitude or None if unsuccessful
        """
        if self._doingPeriodicMeasurement:
            return None
        
        return self.read_register(self.kComGetSensorAltitude)
    
    def set_ambient_pressure(self, pressure, delayMillis = 1):
        """!
        Set the ambient pressure (Pa). See 3.6.5
        Max command duration: 1ms

        Define the ambient pressure in Pascals, so RH and CO2 are compensated for atmospheric pressure
        set_ambient_pressure overrides set_sensor_altitude

        The user can set delayMillis to zero if they want the function to return immediately.
        The set_ambient_pressure command can be sent during periodic measurements to enable continuous pressure compensation.
        set_ambient_pressure overrides set_sensor_altitude

        @param int pressure: The pressure to set. Must be between 0 and 6553500
        @param int delayMillis: The delay in milliseconds to wait after setting the pressure
        """
        if pressure < 0 or pressure >= 6553500:
            return False

        pressure_word = int(pressure / 100)
        self.send_command(self.kComSetAmbientPressure, pressure_word)
        if delayMillis > 0:
            time.sleep(delayMillis / 1000)

        return True

    def perform_forced_recalibration(self, concentration):
        """!
        Perform forced recalibration. See 3.7.1
        To successfully conduct an accurate forced recalibration, the following steps need to be carried out:
        1. Operate the SCD4x in the operation mode later used in normal sensor operation (periodic measurement,
        low power periodic measurement or single shot) for > 3 minutes in an environment with homogenous and
        constant CO2 concentration.
        2. Issue stop_periodic_measurement. Wait 500 ms for the stop command to complete.
        3. Subsequently issue the perform_forced_recalibration command and optionally read out the FRC correction
        (i.e. the magnitude of the correction) after waiting for 400 ms for the command to complete.
        A return value of 0xffff indicates that the forced recalibration has failed.

        @param int concentration: The concentration to recalibrate to

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._doingPeriodicMeasurement:
            return False
        
        self.send_command(self.kComPerformForcedCalibration, concentration)
        
        time.sleep(0.4) # specified by datasheet
        
        read_bytes = self._i2c.readBlock(self.address, None, 3) # By passing "None" we perform a general read. Requires new version of qwiic_i2c
        
        if self.compute_crc8(read_bytes[0:2]) != read_bytes[2]:
            return False
        
        correction = ((read_bytes[0] << 8) | read_bytes[1]) - 32768 # FRC correction [ppm CO2] = word[0] – 0x8000

        return (correction != 0xFFFF)
    
    def start_low_power_periodic_measurement(self):
        """!
        Start low power periodic measurements. See 3.8.1
        Signal update interval will be 30 seconds instead of 5

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._doingPeriodicMeasurement:
            return False
        
        self.send_command(self.kComStartLowPowerPeriodicMeasurement)
        self._doingPeriodicMeasurement = True
        return True

    def get_data_ready_status(self):
        """!
        Returns true when data is available. See 3.8.2

        @return **bool** `True` if data is ready, otherwise `False`
        """
        response = self.read_register(self.kComGetDataReadyStatus)
        if response is None:
            return False
        
        # If the least significant 11 bits of word[0] are 0 → data not ready
        # else → data ready for read-out
        return (response & 0x07FF) != 0
    
    def persist_settings(self, delayMillis = 800):
        """!
        Persist settings: copy settings (e.g. temperature offset) from RAM to EEPROM. See 3.9.1
        
        Configuration settings such as the temperature offset, sensor altitude and the ASC enabled/disabled parameter
        are by default stored in the volatile memory (RAM) only and will be lost after a power-cycle. The persist_settings
        command stores the current configuration in the EEPROM of the SCD4x, making them persistent across power-cycling.
        
        WARNING: To avoid unnecessary wear of the EEPROM, the persist_settings command should only be sent when persistence is required
        and if actual changes to the configuration have been made. The EEPROM is guaranteed to endure at least 2000 write
        cycles before failure.

        @param int delayMillis: The delay in milliseconds to wait after persisting the settings

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._doingPeriodicMeasurement:
            return False
        
        self.send_command(self.kComPersistSettings)
        if delayMillis > 0:
            time.sleep(delayMillis / 1000)
        
        return True

    def get_serial_number(self):
        """!
        Get the serial number of the sensor

        @param int serialNumber: The serial number of the sensor

        @return **str** Serial Number if successful, otherwise `None`
        """
        if self._doingPeriodicMeasurement:
            return None
        
        self.send_command(self.kComGetSerialNumber)
        
        time.sleep(0.001) # specified by datasheet

        bytes_read = self._i2c.readBlock(self.address, None, 9) # By passing "None" we perform a general read. Requires new version of qwiic_i2c
        
        # Bytes are returned as 3 big-endian words, each with a CRC8 byte after
        bytes_to_crc0 = bytes_read[0:3]
        bytes_to_crc1 = bytes_read[3:6]
        bytes_to_crc2 = bytes_read[6:9]

        serial = ""

        for bytes in [bytes_to_crc0, bytes_to_crc1, bytes_to_crc2]:
            if self.compute_crc8(bytes[0:2]) != bytes[2]:
                return None
            serial += self.convert_hex_to_ascii(bytes[0] >> 4)
            serial += self.convert_hex_to_ascii(bytes[0] & 0x0F)
            serial += self.convert_hex_to_ascii(bytes[1] >> 4)
            serial += self.convert_hex_to_ascii(bytes[1] & 0x0F)
        
        return serial
    
    def convert_hex_to_ascii(self, digit):
        """!
        Convert a hex digit to its ASCII representation

        @param int digit: The hex digit to convert

        @return **str** The ASCII representation of the hex digit
        """
        if digit <= 9:
            return chr(digit + 0x30)
        else:
            return chr(digit + 0x41 - 10)  # Use upper case for A-F
        
    def perform_self_test(self):
        """!
        Perform self test. Takes 10 seconds to complete. See 3.9.3
        The perform_self_test feature can be used as an end-of-line test to check sensor functionality
        and the customer power supply to the sensor.

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._doingPeriodicMeasurement:
            return False
        
        response = self.read_register(self.kComPerformSelfTest, 10000)

        return response == 0x0000
    
    def perform_factory_reset(self, delayMillis = 1200):
        """!
        Peform factory reset. See 3.9.4
        The perform_factory_reset command resets all configuration settings stored in the EEPROM
        and erases the FRC and ASC algorithm history.

        @param int delayMillis: The delay in milliseconds to wait after performing the factory reset

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._doingPeriodicMeasurement:
            return False
        
        self.send_command(self.kComPerformFactoryReset)

        if delayMillis > 0:
            time.sleep(delayMillis / 1000)
        
        return True
    
    def reinit(self, delayMillis = 20):
        """!
        Re-initialize the sensor, load settings from EEPROM. See 3.9.5

        The reinit command reinitializes the sensor by reloading user settings from EEPROM.
        Before sending the reinit command, the stop measurement command must be issued.
        If the reinit command does not trigger the desired re-initialization,
        a power-cycle should be applied to the SCD4x

        @param int delayMillis: The delay in milliseconds to wait after re-initializing

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._doingPeriodicMeasurement:
            return False
        
        self.send_command(self.kComReinit)

        if delayMillis > 0:
            time.sleep(delayMillis / 1000)
        
        return True

    def measure_single_shot(self):
        """!
        SCD41 only. Request a single low-power measurement. Data will be ready in 5 seconds. See 3.10.1

        In addition to periodic measurement modes, the SCD41 features a single shot measurement mode,
        i.e. allows for on-demand measurements.
        The typical communication sequence is as follows:
        1. The sensor is powered up.
        2. The I2C master sends a single shot command and waits for the indicated max. command duration time.
        3. The I2C master reads out data with the read measurement sequence (chapter 3.5.2).
        4. Steps 2-3 are repeated as required by the application.

        @return **bool** `True` if successful, otherwise `False`
        """

        if self._sensorType != self.kTypeSCD41:
            return False

        if self._doingPeriodicMeasurement:
            return False
        
        self.send_command(self.kComMeasureSingleShot)

        return True
    
    def measure_single_shot_rht_only(self):
        """!
        On-demand measurement of relative humidity and temperature only. SCD41 only. Data will be ready in 50ms

        The sensor output is read using the read_measurement command (chapter 3.5.2).
        CO2 output is returned as 0 ppm.

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._sensorType != self.kTypeSCD41:
            return False
        
        if self._doingPeriodicMeasurement:
            return False
        
        self.send_command(self.kComMeasureSingleShotRhtOnly)

        return True

    def get_sensor_type(self):
        """!
        Get the sensor type. Allowable versions are kTypeSCD40, kTypeSCD41, and kTypeSDC4xInvalid

        @return **int** The sensor type
        """
        return self._sensorType
    
    def set_sensor_type(self, sensorType):
        """!
        Set the sensor type. Allowable versions are kTypeSCD40, kTypeSCD41, and kTypeSDC4xInvalid

        @param int sensorType: The sensor type to set
        """
        if sensorType == self.kTypeSCD40 or sensorType == self.kTypeSCD41 or sensorType == self.kTypeSDC4xInvalid:
            self._sensorType = sensorType

    def get_feature_set_version(self):
        """!
        Save the feature set version/sensor type of the sensor.

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._doingPeriodicMeasurement:
            return False
        
        feature_set = self.read_register(self.kComGetFeatureSetVersion)
        
        if feature_set is None:
            return False
        
        read_type = ( (feature_set & 0x1000) >> 12 )

        if read_type == self.kTypeSCD40:
            self._sensorType = self.kTypeSCD40
        elif read_type == self.kTypeSCD41:
            self._sensorType = self.kTypeSCD41
        else:
            self._sensorType = self.kTypeSDC4xInvalid
        
        return True

    def set_automatic_self_calibration_enabled(self, enabled, delayMillis = 1):
        """!
        Enable/disable automatic self calibration. See 3.7.2
        Set the current state (enabled / disabled) of the automatic self-calibration. By default, ASC is enabled.
        To save the setting to the EEPROM, the persist_setting (see chapter 3.9.1) command must be issued.

        @param bool enabled: `True` to enable, `False` to disable
        @param int delayMillis: The delay in milliseconds to wait after setting the calibration

        @return **bool** `True` if successful, otherwise `False`
        """
        if self._doingPeriodicMeasurement:
            return False
        
        enabled_word = 0x0001 if enabled else 0x0000
        self.send_command(self.kComSetAutomaticSelfCalibrationEnabled, enabled_word)
        time.sleep(delayMillis / 1000)
        return True
    
    def get_automatic_self_calibration_enabled(self):
        """!
        Check if automatic self calibration is enabled. See 3.7.3

        @return  `True` if enabled, otherwise `False`
        
        """
        if self._doingPeriodicMeasurement:
            return False
        
        return ( self.read_register(self.kComGetAutomaticSelfCalibrationEnabled) == 0x0001 )
        
    def compute_crc8(self, data):
        """!
        Given a list of bytes, this calculate CRC8 for those bytes
        CRC is only calc'd on the data portion (two bytes) of the four bytes being sent
        From: http://www.sunshine2k.de/articles/coding/crc/understanding_crc.html
        Tested with: http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
        x^8+x^5+x^4+1 = 0x31

        @param list of int data: The data to compute the CRC for

        @return **int** The computed CRC8 value
        """
        crc = 0xFF  # Init with 0xFF

        for byte in data:
            crc ^= byte  # XOR-in the next input byte

            for i in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1

        return crc & 0xFF  # Ensure CRC is within 8-bit range

    def send_command(self, command, arguments = None): 
        """!
        Sends a command along with arguments and CRC

        @param int command: The command to send
        @param int arguments: A 16 bit value containing the arguments to send
        """

        bytes_to_write = [command >> 8, command & 0xFF]
        
        if arguments is not None:
            arguments_to_wrte = [int(arguments) >> 8, int(arguments) & 0xFF]
            crc = self.compute_crc8(arguments_to_wrte)
            bytes_to_write += [arguments_to_wrte[0], arguments_to_wrte[1], crc]
        
        # we don't have an explicit way in the I2C drivers to write not to a specific register, 
        # but if we write the first as the register it should behave the same
        self._i2c.writeBlock(self.address, bytes_to_write[0], bytes_to_write[1:])

    def read_register(self, registerAddress, delayMillis = 1):
        """!
        Read a register from the sensor. Gets two bytes from SCD4x plus CRC

        @param int registerAddress: The address of the register to read
        @param int delayMillis: The delay in milliseconds to wait after reading the register

        @return **int** The value of the register if successful, otherwise `None`
        """
        self.send_command(registerAddress)
        
        time.sleep(delayMillis / 1000)

        bytes_read = self._i2c.readBlock(self.address, None, 3) # By passing "None" we perform a general read. Requires new version of qwiic_i2c
        
        if self.compute_crc8(bytes_read[0:2]) != bytes_read[2]:
            return None
        
        return (bytes_read[0] << 8) | bytes_read[1]
