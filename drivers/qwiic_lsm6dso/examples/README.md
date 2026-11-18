# Sparkfun LSM6DSO Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

## Example 1: Basic Readings
`qwiic_lsm6dso_ex1_basic_readings.py`

This example demonstrates basic bringup of the LSM6DSO to extract gyroscope, accelerometer, and temperature readings. Each second it will print the current measurement. The user has the option to uncomment different methods to experiment with different ways of extracting the components of acceleration and gyro.

The key methods showcased by this example are: 
- `read_float_accel_x()` as well as the corresponding y and z methods
- `read_float_gyro_x()` as well as the corresponding y and z methods
- `read_float_accel_all()`
- `read_float_gyro_all()`
- `read_float_accel_gyro_all()`
- `read_temp_c()`


## Example 2: Settings
`qwiic_lsm6dso_ex2_settings.py`

This example demonstrates how to set the various settings of the LSM6DSO. The range and data rate of both the accelerometer and gyroscope are set before the measurements are again periodically printed. Measurements are printed much faster than example 1 to demonstrate the settings taking effect.

The key methods showcased by this example are:
- `set_accel_range()`
- `set_gyro_range()`
- `set_accel_data_rate()`
- `set_gyro_data_rate()`
