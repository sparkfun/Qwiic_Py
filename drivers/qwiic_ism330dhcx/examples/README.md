# Sparkfun ISM330DHCX Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic
`qwiic_ism330dhcx_ex1_basic.py`

This example shows the basic settings and functions for retrieving accelerometer and gyroscopic data.


The key methods showcased by this example are: 
- `set_device_config()`
- `set_block_data_update()`
- `set_accel_data_rate()`
- `set_accel_full_scale()`
- `set_gyro_data_rate()`
- `set_gyro_full_scale()`
- `set_accel_filter_lp2()`
- `set_accel_slope_filter()`
- `set_gyro_filter_lp1()`
- `set_gyro_lp1_bandwidth()`
- `check_status()`
- `get_accel()`
- `get_gyro()`
