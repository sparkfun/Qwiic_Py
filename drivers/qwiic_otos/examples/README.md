# Sparkfun OTOS Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
`qwiic_otos_ex1_basic_readings.py`

This example demonstrates how to read the position and heading from the
 SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

The key methods showcased by this example are:
- `reset_tracking()`
- `get_position()`

## Example 2: Set Units
`qwiic_otos_ex2_set_units.py`

This example demonstrates how to change the units of the SparkFun Qwiic
 Optical Tracking Odometry Sensor (OTOS).

 The OTOS library defaults to inches and degrees, but you can change the
 units to suit the needs of your project.

The key methods showcased by this example are:
- `set_linear_unit()`
- `set_angular_unit()`

## Example 3: Calibration
`qwiic_otos_ex3_calibration.py`

This example demonstrates how to calibrate the SparkFun Qwiic Optical
 Tracking Odometry Sensor (OTOS).

 This example should be used to calibrate the linear and angular scalars of
 the OTOS to get the most accurate tracking performance. The linear scalar
 can be used to compensate for scaling issues with the x and y measurements,
 while the angular scalar can be used to compensate for scaling issues with
 the heading measurement. Note that if the heading measurement is off, that
 can also cause the x and y measurements to be off, so it's recommended to
 calibrate the angular scalar first.
 
The key methods showcased by this example are:
- `set_linear_scalar()`
- `set_angular_scalar()`
- `calibrate_imu()`

## Example 4: Set Offsets And Position
`qwiic_otos_ex4_set_offsets_and_position.py`

This example demonstrates how to set the offset and position of the SparkFun
 Qwiic Optical Tracking Odometry Sensor (OTOS).

 If your OTOS is mounted to a robot and is not centered, you can specify the
 offset for the sensor relative to the center of the robot; rather than
 returning the position of the sensor, the OTOS will calculate and return the
 position of the robot's center. If you know where your robot is located,
 such as the starting location or from another sensor, you can send that
 position to the OTOS and it will continue to track from there.

The key methods showcased by this example are:
- `set_offset()`
- `set_position()`

## Example 5: Velocity And Acceleration
`qwiic_otos_ex5_velocity_and_acceleration.py`

This example demonstrates how to read the velocity and acceleration from the
 SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

 The primary purpose of the OTOS is to track position, but it also provides
 velocity and acceleration measurements for more advanced applications. Note
 that these measurements can be noisy and inaccurate, especially if the
 sensor is not flat to the ground.

The key methods showcased by this example are:
- `get_velocity()`
- `get_acceleration()`

## Example 6: Standard Deviation
`qwiic_otos_ex6_standard_deviation.py`

This example demonstrates how to read the standard deviation of the
 measurements of the SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

 The OTOS uses Kalman filters to estimate the position, velocity, and
 acceleration of the x, y, and heading. The square root of the diagonal
 elements of the covariance matrices are provided for the standard deviation
 of each measurement. THEY DO NOT REPRESENT THE ACTUAL TRACKING ERROR! These
 are statistical quantities that assume a correct model of the system, but
 there could be unmodelled error sources that cause the physical error to
 become larger than these statistical error (eg. improper calibration, or
 tilting the OTOS to not be flat against the tracking surface). These are
 provided primarily for anyone wanting to perform sensor fusion with
 additional sensors.

The key methods showcased by this example are:
- `get_position_std_dev()`

## Example 7: Get Version
`qwiic_otos_ex7_get_version.py`

This example demonstrates how to get the hardware and firmware version
 numbers from the SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

 There may be future hardware and/or firmware changes of the OTOS, so you can
 use this example to check which version you have. See the product page or
 hardware repository to see what the latest version is:
 https://www.sparkfun.com/products/24904
 https://github.com/sparkfun/SparkFun_Optical_Tracking_Odometry_Sensor

The key methods showcased by this example are:
- `get_version_info()`

## Example 8: Self Test
`qwiic_otos_ex8_self_test.py`

This example demonstrates how to perform a self test of the SparkFun Qwiic
 Optical Tracking Odometry Sensor (OTOS).

 The self test triggers the OTOS to perform a series of tests to ensure the
 sensor is functioning correctly. This is performed during QC testing, but
 you can also perform this test yourself.

The key methods showcased by this example are:
- `self_test()`
