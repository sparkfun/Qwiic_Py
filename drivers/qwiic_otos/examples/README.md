# Sparkfun OTOS Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_otos_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Otos Ex1 Basic Readings
This example demonstrates how to read the position and heading from the
 SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

The key methods showcased by this example are:
- [resetTracking()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#af10d67665906b6cb5e9f66d25b358a4f)
- [getPosition()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#a507b45aeb4223a732c6e995b64f0e796)

## Qwiic Otos Ex2 Set Units
This example demonstrates how to change the units of the SparkFun Qwiic
 Optical Tracking Odometry Sensor (OTOS).

 The OTOS library defaults to inches and degrees, but you can change the
 units to suit the needs of your project.

The key methods showcased by this example are:
- [setLinearUnit()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#a6373a18efaa75a35abb7e3171013617f)
- [setAngularUnit()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#ac2668f8297ed977b005c6577ce58bca0)

## Qwiic Otos Ex3 Calibration
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
- [setLinearScalar()](http://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#a044cce1266b0870ede4c6d6ad0e24f22)
- [setAngularScalar()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#a0cfe24386907cff6b721ce088b566a95)
- [calibrateImu()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#a6966d47e4b0276882e4575ad512d5b4e)

## Qwiic Otos Ex4 Set Offsets And Position
This example demonstrates how to set the offset and position of the SparkFun
 Qwiic Optical Tracking Odometry Sensor (OTOS).

 If your OTOS is mounted to a robot and is not centered, you can specify the
 offset for the sensor relative to the center of the robot; rather than
 returning the position of the sensor, the OTOS will calculate and return the
 position of the robot's center. If you know where your robot is located,
 such as the starting location or from another sensor, you can send that
 position to the OTOS and it will continue to track from there.

The key methods showcased by this example are:
- [setOffset()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#a578d51d9c510a07fe59698ac3ff7a25d)
- [setPosition()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#ad7921cc40d3ea207340b53622f3a63a5)

## Qwiic Otos Ex5 Velocity And Acceleration
This example demonstrates how to read the velocity and acceleration from the
 SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

 The primary purpose of the OTOS is to track position, but it also provides
 velocity and acceleration measurements for more advanced applications. Note
 that these measurements can be noisy and inaccurate, especially if the
 sensor is not flat to the ground.

The key methods showcased by this example are:
- [getVelocity()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#a2d5b5f6fc45e28f7c611af7606bb632e)
- [getAcceleration()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#a205c550fbe558fd314ba2a5d80ea2ac8)

## Qwiic Otos Ex6 Standard Deviation
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
- [getPositionStdDev()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#abc2101cf659e26f03d9f6a472ab30177)

## Qwiic Otos Ex7 Get Version
This example demonstrates how to get the hardware and firmware version
 numbers from the SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

 There may be future hardware and/or firmware changes of the OTOS, so you can
 use this example to check which version you have. See the product page or
 hardware repository to see what the latest version is:
 https://www.sparkfun.com/products/24904
 https://github.com/sparkfun/SparkFun_Optical_Tracking_Odometry_Sensor

The key methods showcased by this example are:
- [getVersionInfo()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#a0e4ba26222411f6109b59f7a65e09ad5)

## Qwiic Otos Ex8 Self Test
This example demonstrates how to perform a self test of the SparkFun Qwiic
 Optical Tracking Odometry Sensor (OTOS).

 The self test triggers the OTOS to perform a series of tests to ensure the
 sensor is functioning correctly. This is performed during QC testing, but
 you can also perform this test yourself.

The key methods showcased by this example are:
- [selfTest()](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html#ac7b2f0230c1fa2b3494a06f75f156a64)
