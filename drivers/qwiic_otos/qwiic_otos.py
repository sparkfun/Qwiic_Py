#-------------------------------------------------------------------------------
# qwiic_otos.py
#
# Python library for the SparkFun Qwiic Optical Tracking Odometry Sensor,
# available here:
# https://www.sparkfun.com/products/24904
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, May 2024
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
qwiic_otos
============
Python module for the [SparkFun Qwiic Optical Tracking Odometry Sensor](https://www.sparkfun.com/products/24904)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_OTOS_Arduino_Library)
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
_DEFAULT_NAME = "Qwiic OTOS"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x17]

class Pose2D:
    """!
    2D pose structure, including x and y coordinates and heading angle
    Note: Although pose is traditionally used for position and orientation, this
    structure is also used for velocity and accleration by the OTOS driver
    """

    def __init__(self, x=0.0, y=0.0, h=0.0):
        """!
        Initializes the pose structure

        @param float, optional x: X value, defaults to 0.0
        @param float, optional y: Y value, defaults to 0.0
        @param float, optional h: Heading value, defaults to 0.0
        """
        self.x = x
        self.y = y
        self.h = h

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicOTOS(object):
    """!
    Class for the SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).
    Includes methods to communicate with the sensor, such as getting the tracked
    location, configuring the sensor, etc. This class is a base class that must
    be derived to implement the delay function and I2C communication bus.
    """
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # OTOS register map
    kRegProductId = 0x00
    kRegHwVersion = 0x01
    kRegFwVersion = 0x02
    kRegScalarLinear = 0x04
    kRegScalarAngular = 0x05
    kRegImuCalib = 0x06
    kRegReset = 0x07
    kRegSignalProcess = 0x0E
    kRegSelfTest = 0x0F
    kRegOffXL = 0x10
    kRegOffXH = 0x11
    kRegOffYL = 0x12
    kRegOffYH = 0x13
    kRegOffHL = 0x14
    kRegOffHH = 0x15
    kRegStatus = 0x1F
    kRegPosXL = 0x20
    kRegPosXH = 0x21
    kRegPosYL = 0x22
    kRegPosYH = 0x23
    kRegPosHL = 0x24
    kRegPosHH = 0x25
    kRegVelXL = 0x26
    kRegVelXH = 0x27
    kRegVelYL = 0x28
    kRegVelYH = 0x29
    kRegVelHL = 0x2A
    kRegVelHH = 0x2B
    kRegAccXL = 0x2C
    kRegAccXH = 0x2D
    kRegAccYL = 0x2E
    kRegAccYH = 0x2F
    kRegAccHL = 0x30
    kRegAccHH = 0x31
    kRegPosStdXL = 0x32
    kRegPosStdXH = 0x33
    kRegPosStdYL = 0x34
    kRegPosStdYH = 0x35
    kRegPosStdHL = 0x36
    kRegPosStdHH = 0x37
    kRegVelStdXL = 0x38
    kRegVelStdXH = 0x39
    kRegVelStdYL = 0x3A
    kRegVelStdYH = 0x3B
    kRegVelStdHL = 0x3C
    kRegVelStdHH = 0x3D
    kRegAccStdXL = 0x3E
    kRegAccStdXH = 0x3F
    kRegAccStdYL = 0x40
    kRegAccStdYH = 0x41
    kRegAccStdHL = 0x42
    kRegAccStdHH = 0x43

    # Product ID register value
    kProductId = 0x5F

    # Conversion factors
    kMeterToInch = 39.37
    kInchToMeter = 1.0 / kMeterToInch
    kRadianToDegree = 180.0 / 3.14159
    kDegreeToRadian = 3.14159 / 180.0

    # Conversion factor for the linear position registers. 16-bit signed
    # registers with a max value of 10 meters (394 inches) gives a resolution
    # of about 0.0003 mps (0.012 ips)
    kMeterToInt16 = 32768.0 / 10.0
    kInt16ToMeter = 1.0 / kMeterToInt16

    # Conversion factor for the linear velocity registers. 16-bit signed
    # registers with a max value of 5 mps (197 ips) gives a resolution of about
    # 0.00015 mps (0.006 ips)
    kMpsToInt16 = 32768.0 / 5.0
    kInt16ToMps = 1.0 / kMpsToInt16

    # Conversion factor for the linear acceleration registers. 16-bit signed
    # registers with a max value of 157 mps^2 (16 g) gives a resolution of
    # about 0.0048 mps^2 (0.49 mg)
    kMpssToInt16 = 32768.0 / (16.0 * 9.80665)
    kInt16ToMpss = 1.0 / kMpssToInt16

    # Conversion factor for the angular position registers. 16-bit signed
    # registers with a max value of pi radians (180 degrees) gives a resolution
    # of about 0.00096 radians (0.0055 degrees)
    kRadToInt16 = 32768.0 / 3.14159
    kInt16ToRad = 1.0 / kRadToInt16

    # Conversion factor for the angular velocity registers. 16-bit signed
    # registers with a max value of 34.9 rps (2000 dps) gives a resolution of
    # about 0.0011 rps (0.061 degrees per second)
    kRpsToInt16 = 32768.0 / (2000.0 * kDegreeToRadian)
    kInt16ToRps = 1.0 / kRpsToInt16

    # Conversion factor for the angular acceleration registers. 16-bit signed
    # registers with a max value of 3141 rps^2 (180000 dps^2) gives a
    # resolution of about 0.096 rps^2 (5.5 dps^2)
    kRpssToInt16 = 32768.0 / (3.14159 * 1000.0)
    kInt16ToRpss = 1.0 / kRpssToInt16
    
    # Minimum scalar value for the linear and angular scalars
    kMinScalar = 0.872

    # Maximum scalar value for the linear and angular scalars
    kMaxScalar = 1.127

    # Enumerations for linear units used by the OTOS driver
    kLinearUnitMeters = 0
    kLinearUnitInches = 1

    # Enumerations for angular units used by the OTOS driver
    kAngularUnitRadians = 0
    kAngularUnitDegrees = 1

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

        # Units to be used by the public pose functions. Everything uses meters and
        # radians internally, so this just determines what conversion factor is
        # applied to the public functions
        self._linearUnit = self.kLinearUnitInches
        self._angularUnit = self.kAngularUnitDegrees

        # Conversion factors from meters and radians to the current linear and
        # angular units
        self._meterToUnit = self.kMeterToInch
        self._radToUnit = self.kRadianToDegree

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        if(self._i2c.isDeviceConnected(self.address) == False):
            return False
        
        # Something ACK'd, check if the product ID is correct
        prodid = self._i2c.readByte(self.address, self.kRegProductId)
        return prodid == self.kProductId

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected nothing else is needed!
        return self.is_connected()

    def getVersionInfo(self):
        """!
        Gets the hardware and firmware version numbers from the OTOS

        @return **list** Hardware and firmware version numbers
        """
        # Read the hardware and firmware version registers
        return self._i2c.read_block(self.address, self.kRegHwVersion, 2)

    def selfTest(self):
        """!
        Performs a self-test on the OTOS

        @return **bool** True if successful, otherwise False
        """
        # Write the self-test register to start the self test
        self._i2c.write_byte(self.address, self.kRegSelfTest, 0x01)
        
        # Loop until self-test is done, should only take ~20ms in firmware v1.0
        for i in range(10):
            # Give a short delay between reads
            time.sleep(0.005)

            # Read the self-test register
            regValue = self._i2c.read_byte(self.address, self.kRegSelfTest)

            # Check if the self-test is done
            if ((regValue >> 1) & 0x01) == 0:
                break

        # Check if the self-test passed
        return True if ((regValue >> 2) & 0x01) == 1 else False

    def calibrateImu(self, numSamples = 255, waitUntilDone = True):
        """!
        Calibrates the IMU on the OTOS, which removes the accelerometer and
        gyroscope offsets

        @param int, optional numSamples: Number of samples to take for calibration. Each
        sample takes about 2.4ms, so fewer samples can be taken for faster
        calibration, defaults to 255
        @param bool, optional waitUntilDone: hether to wait until the calibration is complete.
        Set false to calibrate asynchronously, see getImuCalibrationProgress(),
        defaults to True

        @return **bool** True if successful, otherwise False
        """
        # Write the number of samples to the device
        self._i2c.write_byte(self.address, self.kRegImuCalib, numSamples)
        
        # Wait 1 sample period (2.4ms) to ensure the register updates
        time.sleep(0.003)

        # Do we need to wait until the calibration finishes?
        if not waitUntilDone:
            return True
        
        # Wait for the calibration to finish, which is indicated by the IMU
        # calibration register reading zero, or until we reach the maximum
        # number of read attempts
        for numAttempts in range(numSamples, 0, -1):
            # Read the gryo calibration register value
            calibrationValue = self._i2c.read_byte(self.address, self.kRegImuCalib)

            # Check if calibration is done
            if calibrationValue == 0:
                return True

            # Give a short delay between reads. As of firmware v1.0, samples take
            # 2.4ms each, so 3ms should guarantee the next sample is done. This
            # also ensures the max attempts is not exceeded in normal operation
            time.sleep(0.003)

        # Max number of attempts reached, calibration failed
        return False

    def getImuCalibrationProgress(self):
        """!
        Gets the progress of the IMU calibration. Used for asynchronous
        calibration with calibrateImu()

        @return **int** Number of samples remaining for calibration
        """
        # Read the IMU calibration register
        return self._i2c.read_byte(self.address, self.kRegImuCalib)

    def getLinearUnit(self):
        """!
        Gets the linear unit used by all methods using a pose

        @return **int** Linear unit
        """
        return self._linearUnit

    def setLinearUnit(self, unit):
        """!
        Sets the linear unit used by all methods using a pose

        @param int unit: Linear unit
        """
        # Check if this unit is already set
        if unit == self._linearUnit:
            return

        # Store new unit
        self._linearUnit = unit

        # Compute conversion factor to new units
        self._meterToUnit = 1.0 if unit == self.kLinearUnitMeters else self.kMeterToInch

    def getAngularUnit(self):
        """!
        Gets the angular unit used by all methods using a pose

        @return **int** Angular unit
        """
        return self._angularUnit

    def setAngularUnit(self, unit):
        """!
        Sets the angular unit used by all methods using a pose

        @param int unit: Angular unit
        """
        # Check if this unit is already set
        if unit == self._angularUnit:
            return

        # Store new unit
        self._angularUnit = unit

        # Compute conversion factor to new units
        self._radToUnit = 1.0 if unit == self.kAngularUnitRadians else self.kRadianToDegree

    def getLinearScalar(self):
        """!
        Gets the linear scalar used by the OTOS

        @return **float** Linear scalar
        """
        # Read the linear scalar from the device
        rawScalar = self._i2c.read_byte(self.address, self.kRegScalarLinear)

        # Convert to signed 8-bit integer
        if rawScalar > 127:
            rawScalar = rawScalar - 256

        # Convert to float, multiples of 0.1%
        return rawScalar * 0.001 + 1.0

    def setLinearScalar(self, scalar):
        """!
        Sets the linear scalar used by the OTOS. Can be used to compensate
        for scaling issues with the sensor measurements

        @param float scalar: Linear scalar, must be between 0.872 and 1.127

        @return **bool** True if successful, otherwise False
        """
        # Check if the scalar is out of bounds
        if scalar < self.kMinScalar or scalar > self.kMaxScalar:
            return False

        # Convert to integer, multiples of 0.1%
        rawScalar = round((scalar - 1.0) * 1000)

        # Write the scalar to the device
        self._i2c.write_byte(self.address, self.kRegScalarLinear, rawScalar)

    def getAngularScalar(self):
        """!
        Gets the angular scalar used by the OTOS

        @return **float** Angular scalar
        """
        # Read the linear scalar from the device
        rawScalar = self._i2c.read_byte(self.address, self.kRegScalarAngular)

        # Convert to signed 8-bit integer
        if rawScalar > 127:
            rawScalar = rawScalar - 256

        # Convert to float, multiples of 0.1%
        return rawScalar * 0.001 + 1.0

    def setAngularScalar(self, scalar):
        """!
        Sets the angular scalar used by the OTOS. Can be used to compensate
        for scaling issues with the sensor measurements

        @param float scalar: Angular scalar, must be between 0.872 and 1.127

        @return **bool** True if successful, otherwise False
        """
        # Check if the scalar is out of bounds
        if scalar < self.kMinScalar or scalar > self.kMaxScalar:
            return False

        # Convert to integer, multiples of 0.1%
        rawScalar = round((scalar - 1.0) * 1000)

        # Write the scalar to the device
        self._i2c.write_byte(self.address, self.kRegScalarAngular, rawScalar)

    def resetTracking(self):
        """!
        Resets the tracking algorithm, which resets the position to the origin,
        but can also be used to recover from some rare tracking errors
        """
        # Set tracking reset bit
        self._i2c.write_byte(self.address, self.kRegReset, 0x01)

    def getSignalProcessConfig(self):
        """!
        Gets the signal processing configuration from the OTOS

        @return **int** Signal processing configuration
        """
        # Read the signal process register
        return self._i2c.read_byte(self.address, self.kRegSignalProcess)

    def setSignalProcessConfig(self, config):
        """!
        Sets the signal processing configuration for the OTOS

        @param int config: Signal processing configuration
        """
        # Write the signal process register
        self._i2c.write_byte(self.address, self.kRegSignalProcess, config)

    def getStatus(self):
        """!
        Gets the status register from the OTOS, which includes warnings
        and errors reported by the sensor

        @return **int** Status register value
        """
        return self._i2c.read_byte(self.address, self.kRegStatus)

    def getOffset(self):
        """!
        Gets the offset of the OTOS

        @return **Pose2D** Offset of the sensor relative to the center of the robot
        """
        return self._readPoseRegs(self.kRegOffXL, self.kInt16ToMeter, self.kInt16ToRad)

    def setOffset(self, pose):
        """!
        Gets the offset of the OTOS. This is useful if your sensor is
        mounted off-center from a robot. Rather than returning the position of
        the sensor, the OTOS will return the position of the robot

        @param Pose2D pose: Offset of the sensor relative to the center of the robot
        """
        self._writePoseRegs(self.kRegOffXL, pose, self.kMeterToInt16, self.kRadToInt16)

    def getPosition(self):
        """!
        Gets the position measured by the OTOS

        @return **Pose2D** Position measured by the OTOS
        """
        return self._readPoseRegs(self.kRegPosXL, self.kInt16ToMeter, self.kInt16ToRad)

    def setPosition(self, pose):
        """!
        Sets the position measured by the OTOS. This is useful if your
        robot does not start at the origin, or you have another source of
        location information (eg. vision odometry); the OTOS will continue
        tracking from this position

        @param Pose2D pose: New position for the OTOS to track from
        """
        self._writePoseRegs(self.kRegPosXL, pose, self.kMeterToInt16, self.kRadToInt16)

    def getVelocity(self):
        """!
        Gets the velocity measured by the OTOS

        @return **Pose2D** Velocity measured by the OTOS
        """
        return self._readPoseRegs(self.kRegVelXL, self.kInt16ToMps, self.kInt16ToRps)

    def getAcceleration(self):
        """!
        Gets the acceleration measured by the OTOS

        @return **Pose2D** Acceleration measured by the OTOS
        """
        return self._readPoseRegs(self.kRegAccXL, self.kInt16ToMpss, self.kInt16ToRpss)

    def getPositionStdDev(self):
        """!
        Gets the standard deviation of the measured position

        These values are just the square root of the diagonal elements of
        the covariance matrices of the Kalman filters used in the firmware, so
        they are just statistical quantities and do not represent actual error!

        @return **Pose2D** Standard deviation of the position measured by the OTOS
        """
        return self._readPoseRegs(self.kRegPosStdXL, self.kInt16ToMeter, self.kInt16ToRad)

    def getVelocityStdDev(self):
        """!
        Gets the standard deviation of the measured velocity

        These values are just the square root of the diagonal elements of
        the covariance matrices of the Kalman filters used in the firmware, so
        they are just statistical quantities and do not represent actual error!

        @return **Pose2D** Standard deviation of the velocity measured by the OTOS
        """
        return self._readPoseRegs(self.kRegVelStdXL, self.kInt16ToMps, self.kInt16ToRps)

    def getAccelerationStdDev(self):
        """!
        Gets the standard deviation of the measured acceleration

        These values are just the square root of the diagonal elements of
        the covariance matrices of the Kalman filters used in the firmware, so
        they are just statistical quantities and do not represent actual error!

        @return **Pose2D** Standard deviation of the acceleration measured by the OTOS
        """
        return self._readPoseRegs(self.kRegAccStdXL, self.kInt16ToMpss, self.kInt16ToRpss)

    def getPosVelAcc(self):
        """!
        Gets the position, velocity, and acceleration measured by the
        OTOS in a single burst read

        @return **tuple of Pose2D** Position, velocity, and acceleration measured by the OTOS
        """
        # Read all pose registers
        rawData = self._i2c.read_block(self.address, self.kRegPosXL, 18)
        
        # Convert raw data to pose units
        pos = self._regsToPose(rawData[0:6], self.kInt16ToMeter, self.kInt16ToRad)
        vel = self._regsToPose(rawData[6:12], self.kInt16ToMps, self.kInt16ToRps)
        acc = self._regsToPose(rawData[12:18], self.kInt16ToMpss, self.kInt16ToRpss)

        return (pos, vel, acc)

    def getPosVelAccStdDev(self):
        """!
        Gets the standard deviation of the measured position, velocity,
        and acceleration in a single burst read

        @return **tuple of Pose2D** Standard deviation of the position, velocity, and acceleration
        measured by the OTOS
        """
        # Read all pose registers
        rawData = self._i2c.read_block(self.address, self.kRegPosStdXL, 18)
        
        # Convert raw data to pose units
        pos = self._regsToPose(rawData[0:6], self.kInt16ToMeter, self.kInt16ToRad)
        vel = self._regsToPose(rawData[6:12], self.kInt16ToMps, self.kInt16ToRps)
        acc = self._regsToPose(rawData[12:18], self.kInt16ToMpss, self.kInt16ToRpss)

        return (pos, vel, acc)

    def getPosVelAccAndStdDev(self):
        """!
        Gets the position, velocity, acceleration, and standard deviation
        of each in a single burst read

        @return **tuple of Pose2D** Position, velocity, acceleration, and standard deviation of
        each measured by the OTOS
        """
        # Read all pose registers
        rawData = self._i2c.read_block(self.address, self.kRegPosXL, 36)
        
        # Convert raw data to pose units
        pos = self._regsToPose(rawData[0:6], self.kInt16ToMeter, self.kInt16ToRad)
        vel = self._regsToPose(rawData[6:12], self.kInt16ToMps, self.kInt16ToRps)
        acc = self._regsToPose(rawData[12:18], self.kInt16ToMpss, self.kInt16ToRpss)
        posStdDev = self._regsToPose(rawData[18:24], self.kInt16ToMeter, self.kInt16ToRad)
        velStdDev = self._regsToPose(rawData[24:30], self.kInt16ToMps, self.kInt16ToRps)
        accStdDev = self._regsToPose(rawData[30:36], self.kInt16ToMpss, self.kInt16ToRpss)

        return (pos, vel, acc, posStdDev, velStdDev, accStdDev)

    def _readPoseRegs(self, reg, rawToXY, rawToH):
        """!
        Function to read raw pose registers and convert to specified units

        @param int reg: Register to read from
        @param float rawToXY: Conversion factor from raw units to XY units
        @param float rawToH: Conversion factor from raw units to heading units

        @return **Pose2D** Pose structure containing the pose read from the registers
        """
        # Read the raw pose data
        rawData = self._i2c.read_block(self.address, reg, 6)
        
        return self._regsToPose(rawData, rawToXY, rawToH)

    def _writePoseRegs(self, reg, pose, xyToRaw, hToRaw):
        """!
        Function to write raw pose registers and convert from specified units

        @param int reg: Register to write to
        @param Pose2D pose: Pose structure containing the pose to write to the registers
        @param float xyToRaw: Conversion factor from XY units to raw units
        @param float hToRaw: Conversion factor from heading units to raw units
        """
        # Store raw data in a temporary buffer
        rawData = self._poseToRegs(pose, xyToRaw, hToRaw)

        # Write the raw data to the device
        self._i2c.write_block(self.address, reg, rawData)

    def _regsToPose(self, rawData, rawToXY, rawToH):
        """!
        Function to convert raw pose registers to a pose structure

        @param list of int rawData: Raw data from the pose registers
        @param float rawToXY: Conversion factor from raw units to XY units
        @param float rawToH: Conversion factor from raw units to heading units

        @return **Pose2D** Pose structure containing the pose read from the registers
        """
        # Store raw data
        rawX = (rawData[1] << 8) | rawData[0]
        rawY = (rawData[3] << 8) | rawData[2]
        rawH = (rawData[5] << 8) | rawData[4]

        # Convert raw data to signed 16-bit integers
        if rawX > 32767:
            rawX = rawX - 65536
        if rawY > 32767:
            rawY = rawY - 65536
        if rawH > 32767:
            rawH = rawH - 65536

        # Store in pose and convert to units
        x = rawX * rawToXY * self._meterToUnit
        y = rawY * rawToXY * self._meterToUnit
        h = rawH * rawToH * self._radToUnit

        return Pose2D(x, y, h)

    def _poseToRegs(self, pose, xyToRaw, hToRaw):
        """!
        Function to convert a pose structure to raw pose registers

        @param Pose2D pose: Pose structure containing the pose to write to the registers
        @param float xyToRaw: Conversion factor from XY units to raw units
        @param float hToRaw: Conversion factor from heading units to raw units

        @return **list of int** Raw data to write to the pose registers
        """
        # Convert pose units to raw data
        rawX = round(pose.x * xyToRaw / self._meterToUnit)
        rawY = round(pose.y * xyToRaw / self._meterToUnit)
        rawH = round(pose.h * hToRaw / self._radToUnit)

        # Store raw data in buffer
        rawData = [0] * 6
        rawData[0] = rawX & 0xFF
        rawData[1] = (rawX >> 8) & 0xFF
        rawData[2] = rawY & 0xFF
        rawData[3] = (rawY >> 8) & 0xFF
        rawData[4] = rawH & 0xFF
        rawData[5] = (rawH >> 8) & 0xFF

        return rawData
