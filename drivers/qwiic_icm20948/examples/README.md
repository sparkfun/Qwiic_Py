# Sparkfun 9DOF Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
`qwiic_icm20948_ex1_basic_readings.py`

Simple Example for the Qwiic ICM20948 Device. It prints the raw accelerometer, gyroscope and magnetometer readings whenever new data is ready.

The key methods showcased by this example are: 
- `data_ready()`
- `get_agmt()`, which updates the `ax_raw`, `ay_raw`, `az_raw`, `gx_raw`, `gy_raw`, `gz_raw`, `mx_raw`, `my_raw` and `mz_raw` attributes
