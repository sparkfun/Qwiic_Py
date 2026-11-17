# Sparkfun BME280 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_lsm6dso_py/issues). 

## Example 1: Basic Readings
This example demonstrates basic bringup of the LSM6DSO to extract gyroscope, accelerometer, and temperature readings. Each second it will print the current measurement. The user has the option to uncomment different methods to experiment with different ways of extracting the components of acceleration and gyro.

The key methods showcased by this example are: 
- [read_float_accel_x()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#a300c3e6fc41213d1310169425405a6db) as well as the corresponding y and z methods
- [read_float_gyro_x()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#aa9cbaf29d6021a60d7c7d46a2edac889) as well as the corresponding y and z methods
- [read_float_accel_all()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#ab40213e457ed65a1dc4676115cf86f46)
- [read_float_gyro_all()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#a0a6287248cac3fa966e17f4286df222c)
- [read_float_accel_gyro_all()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#af19015da9121a416bc918e9597cca8ac)
- [read_temp_c()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#a1f08edda2d6c37661be6fd6138795186)


## Example 2: Settings
This example demonstrates how to set the various settings of the LSM6DSO. The range and data rate of both the accelerometer and gyroscope are set before the measurements are again periodically printed. Measurements are printed much faster than example 1 to demonstrate the settings taking effect.

The key methods showcased by this example are:
- [set_accel_range()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#af5d0cb9b68ae39ea1b26f33356b99fe2)
- [set_gyro_range()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#a269266885c506ec4f6358c301108be58)
- [set_accel_data_rate()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#a9626aeee7400f515e6d6825b85c4c86c)
- [set_gyro_data_rate()](https://docs.sparkfun.com/qwiic_lsm6dso_py/classqwiic__lsm6dso_1_1_qwiic_l_s_m6_d_s_o.html#ab3dcd26cb56a42191225684b25d3e410)
