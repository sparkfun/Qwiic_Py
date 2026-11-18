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

__version__ = "3.0.0"

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

        @param x: **float, optional** X value, defaults to 0.0
        @param y: **float, optional** Y value, defaults to 0.0
        @param h: **float, optional** Heading value, defaults to 0.0
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
    REG_PRODUCT_ID = 0x00
    REG_HW_VERSION = 0x01
    REG_FW_VERSION = 0x02
    REG_SCALAR_LINEAR = 0x04
    REG_SCALAR_ANGULAR = 0x05
    REG_IMU_CALIB = 0x06
    REG_RESET = 0x07
    REG_SIGNAL_PROCESS = 0x0E
    REG_SELF_TEST = 0x0F
    REG_OFF_XL = 0x10
    REG_OFF_XH = 0x11
    REG_OFF_YL = 0x12
    REG_OFF_YH = 0x13
    REG_OFF_HL = 0x14
    REG_OFF_HH = 0x15
    REG_STATUS = 0x1F
    REG_POS_XL = 0x20
    REG_POS_XH = 0x21
    REG_POS_YL = 0x22
    REG_POS_YH = 0x23
    REG_POS_HL = 0x24
    REG_POS_HH = 0x25
    REG_VEL_XL = 0x26
    REG_VEL_XH = 0x27
    REG_VEL_YL = 0x28
    REG_VEL_YH = 0x29
    REG_VEL_HL = 0x2A
    REG_VEL_HH = 0x2B
    REG_ACC_XL = 0x2C
    REG_ACC_XH = 0x2D
    REG_ACC_YL = 0x2E
    REG_ACC_YH = 0x2F
    REG_ACC_HL = 0x30
    REG_ACC_HH = 0x31
    REG_POS_STD_XL = 0x32
    REG_POS_STD_XH = 0x33
    REG_POS_STD_YL = 0x34
    REG_POS_STD_YH = 0x35
    REG_POS_STD_HL = 0x36
    REG_POS_STD_HH = 0x37
    REG_VEL_STD_XL = 0x38
    REG_VEL_STD_XH = 0x39
    REG_VEL_STD_YL = 0x3A
    REG_VEL_STD_YH = 0x3B
    REG_VEL_STD_HL = 0x3C
    REG_VEL_STD_HH = 0x3D
    REG_ACC_STD_XL = 0x3E
    REG_ACC_STD_XH = 0x3F
    REG_ACC_STD_YL = 0x40
    REG_ACC_STD_YH = 0x41
    REG_ACC_STD_HL = 0x42
    REG_ACC_STD_HH = 0x43

    # Product ID register value
    PRODUCT_ID = 0x5F

    # Conversion factors
    METER_TO_INCH = 39.37
    INCH_TO_METER = 1.0 / METER_TO_INCH
    RADIAN_TO_DEGREE = 180.0 / 3.14159
    DEGREE_TO_RADIAN = 3.14159 / 180.0

    # Conversion factor for the linear position registers. 16-bit signed
    # registers with a max value of 10 meters (394 inches) gives a resolution
    # of about 0.0003 mps (0.012 ips)
    METER_TO_INT16 = 32768.0 / 10.0
    INT16_TO_METER = 1.0 / METER_TO_INT16

    # Conversion factor for the linear velocity registers. 16-bit signed
    # registers with a max value of 5 mps (197 ips) gives a resolution of about
    # 0.00015 mps (0.006 ips)
    MPS_TO_INT16 = 32768.0 / 5.0
    INT16_TO_MPS = 1.0 / MPS_TO_INT16

    # Conversion factor for the linear acceleration registers. 16-bit signed
    # registers with a max value of 157 mps^2 (16 g) gives a resolution of
    # about 0.0048 mps^2 (0.49 mg)
    MPSS_TO_INT16 = 32768.0 / (16.0 * 9.80665)
    INT16_TO_MPSS = 1.0 / MPSS_TO_INT16

    # Conversion factor for the angular position registers. 16-bit signed
    # registers with a max value of pi radians (180 degrees) gives a resolution
    # of about 0.00096 radians (0.0055 degrees)
    RAD_TO_INT16 = 32768.0 / 3.14159
    INT16_TO_RAD = 1.0 / RAD_TO_INT16

    # Conversion factor for the angular velocity registers. 16-bit signed
    # registers with a max value of 34.9 rps (2000 dps) gives a resolution of
    # about 0.0011 rps (0.061 degrees per second)
    RPS_TO_INT16 = 32768.0 / (2000.0 * DEGREE_TO_RADIAN)
    INT16_TO_RPS = 1.0 / RPS_TO_INT16

    # Conversion factor for the angular acceleration registers. 16-bit signed
    # registers with a max value of 3141 rps^2 (180000 dps^2) gives a
    # resolution of about 0.096 rps^2 (5.5 dps^2)
    RPSS_TO_INT16 = 32768.0 / (3.14159 * 1000.0)
    INT16_TO_RPSS = 1.0 / RPSS_TO_INT16
    
    # Minimum scalar value for the linear and angular scalars
    MIN_SCALAR = 0.872

    # Maximum scalar value for the linear and angular scalars
    MAX_SCALAR = 1.127

    # Enumerations for linear units used by the OTOS driver
    LINEAR_UNIT_METERS = 0
    LINEAR_UNIT_INCHES = 1

    # Enumerations for angular units used by the OTOS driver
    ANGULAR_UNIT_RADIANS = 0
    ANGULAR_UNIT_DEGREES = 1

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

        # Units to be used by the public pose functions. Everything uses meters and
        # radians internally, so this just determines what conversion factor is
        # applied to the public functions
        self._linear_unit = self.LINEAR_UNIT_INCHES
        self._angular_unit = self.ANGULAR_UNIT_DEGREES

        # Conversion factors from meters and radians to the current linear and
        # angular units
        self._meter_to_unit = self.METER_TO_INCH
        self._rad_to_unit = self.RADIAN_TO_DEGREE

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        if not self._i2c.is_device_connected(self.address):
            return False
        
        # Something ACK'd, check if the product ID is correct
        prodid = self._i2c.read_byte(self.address, self.REG_PRODUCT_ID)
        return prodid == self.PRODUCT_ID

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected nothing else is needed!
        return self.is_connected()

    def get_version_info(self):
        """!
        Gets the hardware and firmware version numbers from the OTOS

        @return **list** Hardware and firmware version numbers
        """
        # Read the hardware and firmware version registers
        return self._i2c.read_block(self.address, self.REG_HW_VERSION, 2)

    def self_test(self):
        """!
        Performs a self-test on the OTOS

        @return **bool** True if successful, otherwise False
        """
        # Write the self-test register to start the self test
        self._i2c.write_byte(self.address, self.REG_SELF_TEST, 0x01)
        
        # Loop until self-test is done, should only take ~20ms in firmware v1.0
        for i in range(10):
            # Give a short delay between reads
            self._i2c.delay_ms(5)

            # Read the self-test register
            reg_value = self._i2c.read_byte(self.address, self.REG_SELF_TEST)

            # Check if the self-test is done
            if ((reg_value >> 1) & 0x01) == 0:
                break

        # Check if the self-test passed
        return True if ((reg_value >> 2) & 0x01) == 1 else False

    def calibrate_imu(self, num_samples = 255, wait_until_done = True):
        """!
        Calibrates the IMU on the OTOS, which removes the accelerometer and
        gyroscope offsets

        @param num_samples: **int, optional** Number of samples to take for calibration. Each
        sample takes about 2.4ms, so fewer samples can be taken for faster
        calibration, defaults to 255
        @param wait_until_done: **bool, optional** hether to wait until the calibration is complete.
        Set false to calibrate asynchronously, see get_imu_calibration_progress(),
        defaults to True

        @return **bool** True if successful, otherwise False
        """
        # Write the number of samples to the device
        self._i2c.write_byte(self.address, self.REG_IMU_CALIB, num_samples)
        
        # Wait 1 sample period (2.4ms) to ensure the register updates
        self._i2c.delay_ms(3)

        # Do we need to wait until the calibration finishes?
        if not wait_until_done:
            return True
        
        # Wait for the calibration to finish, which is indicated by the IMU
        # calibration register reading zero, or until we reach the maximum
        # number of read attempts
        for num_attempts in range(num_samples, 0, -1):
            # Read the gryo calibration register value
            calibration_value = self._i2c.read_byte(self.address, self.REG_IMU_CALIB)

            # Check if calibration is done
            if calibration_value == 0:
                return True

            # Give a short delay between reads. As of firmware v1.0, samples take
            # 2.4ms each, so 3ms should guarantee the next sample is done. This
            # also ensures the max attempts is not exceeded in normal operation
            self._i2c.delay_ms(3)

        # Max number of attempts reached, calibration failed
        return False

    def get_imu_calibration_progress(self):
        """!
        Gets the progress of the IMU calibration. Used for asynchronous
        calibration with calibrate_imu()

        @return **int** Number of samples remaining for calibration
        """
        # Read the IMU calibration register
        return self._i2c.read_byte(self.address, self.REG_IMU_CALIB)

    def get_linear_unit(self):
        """!
        Gets the linear unit used by all methods using a pose

        @return **int** Linear unit
        """
        return self._linear_unit

    def set_linear_unit(self, unit):
        """!
        Sets the linear unit used by all methods using a pose

        @param unit: **int** Linear unit
        """
        # Check if this unit is already set
        if unit == self._linear_unit:
            return

        # Store new unit
        self._linear_unit = unit

        # Compute conversion factor to new units
        self._meter_to_unit = 1.0 if unit == self.LINEAR_UNIT_METERS else self.METER_TO_INCH

    def get_angular_unit(self):
        """!
        Gets the angular unit used by all methods using a pose

        @return **int** Angular unit
        """
        return self._angular_unit

    def set_angular_unit(self, unit):
        """!
        Sets the angular unit used by all methods using a pose

        @param unit: **int** Angular unit
        """
        # Check if this unit is already set
        if unit == self._angular_unit:
            return

        # Store new unit
        self._angular_unit = unit

        # Compute conversion factor to new units
        self._rad_to_unit = 1.0 if unit == self.ANGULAR_UNIT_RADIANS else self.RADIAN_TO_DEGREE

    def get_linear_scalar(self):
        """!
        Gets the linear scalar used by the OTOS

        @return **float** Linear scalar
        """
        # Read the linear scalar from the device
        raw_scalar = self._i2c.read_byte(self.address, self.REG_SCALAR_LINEAR)

        # Convert to signed 8-bit integer
        if raw_scalar > 127:
            raw_scalar = raw_scalar - 256

        # Convert to float, multiples of 0.1%
        return raw_scalar * 0.001 + 1.0

    def set_linear_scalar(self, scalar):
        """!
        Sets the linear scalar used by the OTOS. Can be used to compensate
        for scaling issues with the sensor measurements

        @param scalar: **float** Linear scalar, must be between 0.872 and 1.127

        @return **bool** True if successful, otherwise False
        """
        # Check if the scalar is out of bounds
        if scalar < self.MIN_SCALAR or scalar > self.MAX_SCALAR:
            return False

        # Convert to integer, multiples of 0.1%
        raw_scalar = round((scalar - 1.0) * 1000)

        # Write the scalar to the device
        self._i2c.write_byte(self.address, self.REG_SCALAR_LINEAR, raw_scalar)

    def get_angular_scalar(self):
        """!
        Gets the angular scalar used by the OTOS

        @return **float** Angular scalar
        """
        # Read the angular scalar from the device
        raw_scalar = self._i2c.read_byte(self.address, self.REG_SCALAR_ANGULAR)

        # Convert to signed 8-bit integer
        if raw_scalar > 127:
            raw_scalar = raw_scalar - 256

        # Convert to float, multiples of 0.1%
        return raw_scalar * 0.001 + 1.0

    def set_angular_scalar(self, scalar):
        """!
        Sets the angular scalar used by the OTOS. Can be used to compensate
        for scaling issues with the sensor measurements

        @param scalar: **float** Angular scalar, must be between 0.872 and 1.127

        @return **bool** True if successful, otherwise False
        """
        # Check if the scalar is out of bounds
        if scalar < self.MIN_SCALAR or scalar > self.MAX_SCALAR:
            return False

        # Convert to integer, multiples of 0.1%
        raw_scalar = round((scalar - 1.0) * 1000)

        # Write the scalar to the device
        self._i2c.write_byte(self.address, self.REG_SCALAR_ANGULAR, raw_scalar)

    def reset_tracking(self):
        """!
        Resets the tracking algorithm, which resets the position to the origin,
        but can also be used to recover from some rare tracking errors
        """
        # Set tracking reset bit
        self._i2c.write_byte(self.address, self.REG_RESET, 0x01)

    def get_signal_process_config(self):
        """!
        Gets the signal processing configuration from the OTOS

        @return **int** Signal processing configuration
        """
        # Read the signal process register
        return self._i2c.read_byte(self.address, self.REG_SIGNAL_PROCESS)

    def set_signal_process_config(self, config):
        """!
        Sets the signal processing configuration for the OTOS

        @param config: **int** Signal processing configuration
        """
        # Write the signal process register
        self._i2c.write_byte(self.address, self.REG_SIGNAL_PROCESS, config)

    def get_status(self):
        """!
        Gets the status register from the OTOS, which includes warnings
        and errors reported by the sensor

        @return **int** Status register value
        """
        return self._i2c.read_byte(self.address, self.REG_STATUS)

    def get_offset(self):
        """!
        Gets the offset of the OTOS

        @return **Pose2D** Offset of the sensor relative to the center of the robot
        """
        return self._read_pose_regs(self.REG_OFF_XL, self.INT16_TO_METER, self.INT16_TO_RAD)

    def set_offset(self, pose):
        """!
        Gets the offset of the OTOS. This is useful if your sensor is
        mounted off-center from a robot. Rather than returning the position of
        the sensor, the OTOS will return the position of the robot

        @param pose: **Pose2D** Offset of the sensor relative to the center of the robot
        """
        self._write_pose_regs(self.REG_OFF_XL, pose, self.METER_TO_INT16, self.RAD_TO_INT16)

    def get_position(self):
        """!
        Gets the position measured by the OTOS

        @return **Pose2D** Position measured by the OTOS
        """
        return self._read_pose_regs(self.REG_POS_XL, self.INT16_TO_METER, self.INT16_TO_RAD)

    def set_position(self, pose):
        """!
        Sets the position measured by the OTOS. This is useful if your
        robot does not start at the origin, or you have another source of
        location information (eg. vision odometry); the OTOS will continue
        tracking from this position

        @param pose: **Pose2D** New position for the OTOS to track from
        """
        self._write_pose_regs(self.REG_POS_XL, pose, self.METER_TO_INT16, self.RAD_TO_INT16)

    def get_velocity(self):
        """!
        Gets the velocity measured by the OTOS

        @return **Pose2D** Velocity measured by the OTOS
        """
        return self._read_pose_regs(self.REG_VEL_XL, self.INT16_TO_MPS, self.INT16_TO_RPS)

    def get_acceleration(self):
        """!
        Gets the acceleration measured by the OTOS

        @return **Pose2D** Acceleration measured by the OTOS
        """
        return self._read_pose_regs(self.REG_ACC_XL, self.INT16_TO_MPSS, self.INT16_TO_RPSS)

    def get_position_std_dev(self):
        """!
        Gets the standard deviation of the measured position

        These values are just the square root of the diagonal elements of
        the covariance matrices of the Kalman filters used in the firmware, so
        they are just statistical quantities and do not represent actual error!

        @return **Pose2D** Standard deviation of the position measured by the OTOS
        """
        return self._read_pose_regs(self.REG_POS_STD_XL, self.INT16_TO_METER, self.INT16_TO_RAD)

    def get_velocity_std_dev(self):
        """!
        Gets the standard deviation of the measured velocity

        These values are just the square root of the diagonal elements of
        the covariance matrices of the Kalman filters used in the firmware, so
        they are just statistical quantities and do not represent actual error!

        @return **Pose2D** Standard deviation of the velocity measured by the OTOS
        """
        return self._read_pose_regs(self.REG_VEL_STD_XL, self.INT16_TO_MPS, self.INT16_TO_RPS)

    def get_acceleration_std_dev(self):
        """!
        Gets the standard deviation of the measured acceleration

        These values are just the square root of the diagonal elements of
        the covariance matrices of the Kalman filters used in the firmware, so
        they are just statistical quantities and do not represent actual error!

        @return **Pose2D** Standard deviation of the acceleration measured by the OTOS
        """
        return self._read_pose_regs(self.REG_ACC_STD_XL, self.INT16_TO_MPSS, self.INT16_TO_RPSS)

    def get_pos_vel_acc(self):
        """!
        Gets the position, velocity, and acceleration measured by the
        OTOS in a single burst read

        @return **tuple of Pose2D** Position, velocity, and acceleration measured by the OTOS
        """
        # Read all pose registers
        raw_data = self._i2c.read_block(self.address, self.REG_POS_XL, 18)
        
        # Convert raw data to pose units
        pos = self._regs_to_pose(raw_data[0:6], self.INT16_TO_METER, self.INT16_TO_RAD)
        vel = self._regs_to_pose(raw_data[6:12], self.INT16_TO_MPS, self.INT16_TO_RPS)
        acc = self._regs_to_pose(raw_data[12:18], self.INT16_TO_MPSS, self.INT16_TO_RPSS)

        return (pos, vel, acc)

    def get_pos_vel_acc_std_dev(self):
        """!
        Gets the standard deviation of the measured position, velocity,
        and acceleration in a single burst read

        @return **tuple of Pose2D** Standard deviation of the position, velocity, and acceleration
        measured by the OTOS
        """
        # Read all pose registers
        raw_data = self._i2c.read_block(self.address, self.REG_POS_STD_XL, 18)
        
        # Convert raw data to pose units
        pos = self._regs_to_pose(raw_data[0:6], self.INT16_TO_METER, self.INT16_TO_RAD)
        vel = self._regs_to_pose(raw_data[6:12], self.INT16_TO_MPS, self.INT16_TO_RPS)
        acc = self._regs_to_pose(raw_data[12:18], self.INT16_TO_MPSS, self.INT16_TO_RPSS)

        return (pos, vel, acc)

    def get_pos_vel_acc_and_std_dev(self):
        """!
        Gets the position, velocity, acceleration, and standard deviation
        of each in a single burst read

        @return **tuple of Pose2D** Position, velocity, acceleration, and standard deviation of
        each measured by the OTOS
        """
        # Read all pose registers
        raw_data = self._i2c.read_block(self.address, self.REG_POS_XL, 36)
        
        # Convert raw data to pose units
        pos = self._regs_to_pose(raw_data[0:6], self.INT16_TO_METER, self.INT16_TO_RAD)
        vel = self._regs_to_pose(raw_data[6:12], self.INT16_TO_MPS, self.INT16_TO_RPS)
        acc = self._regs_to_pose(raw_data[12:18], self.INT16_TO_MPSS, self.INT16_TO_RPSS)
        pos_std_dev = self._regs_to_pose(raw_data[18:24], self.INT16_TO_METER, self.INT16_TO_RAD)
        vel_std_dev = self._regs_to_pose(raw_data[24:30], self.INT16_TO_MPS, self.INT16_TO_RPS)
        acc_std_dev = self._regs_to_pose(raw_data[30:36], self.INT16_TO_MPSS, self.INT16_TO_RPSS)

        return (pos, vel, acc, pos_std_dev, vel_std_dev, acc_std_dev)

    def _read_pose_regs(self, reg, raw_to_xy, raw_to_h):
        """!
        Function to read raw pose registers and convert to specified units

        @param reg: **int** Register to read from
        @param raw_to_xy: **float** Conversion factor from raw units to XY units
        @param raw_to_h: **float** Conversion factor from raw units to heading units

        @return **Pose2D** Pose structure containing the pose read from the registers
        """
        # Read the raw pose data
        raw_data = self._i2c.read_block(self.address, reg, 6)
        
        return self._regs_to_pose(raw_data, raw_to_xy, raw_to_h)

    def _write_pose_regs(self, reg, pose, xy_to_raw, h_to_raw):
        """!
        Function to write raw pose registers and convert from specified units

        @param reg: **int** Register to write to
        @param pose: **Pose2D** Pose structure containing the pose to write to the registers
        @param xy_to_raw: **float** Conversion factor from XY units to raw units
        @param h_to_raw: **float** Conversion factor from heading units to raw units
        """
        # Store raw data in a temporary buffer
        raw_data = self._pose_to_regs(pose, xy_to_raw, h_to_raw)

        # Write the raw data to the device
        self._i2c.write_block(self.address, reg, raw_data)

    def _regs_to_pose(self, raw_data, raw_to_xy, raw_to_h):
        """!
        Function to convert raw pose registers to a pose structure

        @param raw_data: **list of int** Raw data from the pose registers
        @param raw_to_xy: **float** Conversion factor from raw units to XY units
        @param raw_to_h: **float** Conversion factor from raw units to heading units

        @return **Pose2D** Pose structure containing the pose read from the registers
        """
        # Store raw data
        raw_x = (raw_data[1] << 8) | raw_data[0]
        raw_y = (raw_data[3] << 8) | raw_data[2]
        raw_h = (raw_data[5] << 8) | raw_data[4]

        # Convert raw data to signed 16-bit integers
        if raw_x > 32767:
            raw_x = raw_x - 65536
        if raw_y > 32767:
            raw_y = raw_y - 65536
        if raw_h > 32767:
            raw_h = raw_h - 65536

        # Store in pose and convert to units
        x = raw_x * raw_to_xy * self._meter_to_unit
        y = raw_y * raw_to_xy * self._meter_to_unit
        h = raw_h * raw_to_h * self._rad_to_unit

        return Pose2D(x, y, h)

    def _pose_to_regs(self, pose, xy_to_raw, h_to_raw):
        """!
        Function to convert a pose structure to raw pose registers

        @param pose: **Pose2D** Pose structure containing the pose to write to the registers
        @param xy_to_raw: **float** Conversion factor from XY units to raw units
        @param h_to_raw: **float** Conversion factor from heading units to raw units

        @return **list of int** Raw data to write to the pose registers
        """
        # Convert pose units to raw data
        raw_x = round(pose.x * xy_to_raw / self._meter_to_unit)
        raw_y = round(pose.y * xy_to_raw / self._meter_to_unit)
        raw_h = round(pose.h * h_to_raw / self._rad_to_unit)

        # Store raw data in buffer
        raw_data = [0] * 6
        raw_data[0] = raw_x & 0xFF
        raw_data[1] = (raw_x >> 8) & 0xFF
        raw_data[2] = raw_y & 0xFF
        raw_data[3] = (raw_y >> 8) & 0xFF
        raw_data[4] = raw_h & 0xFF
        raw_data[5] = (raw_h >> 8) & 0xFF

        return raw_data
