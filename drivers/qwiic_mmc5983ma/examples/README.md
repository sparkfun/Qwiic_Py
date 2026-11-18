# Sparkfun MMC5983MA Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
`qwiic_mmc5983ma_ex1_basic_readings.py`

Demonstrates how to get basic data from the MMC5983MA Magnetometer

The key functions showcased by this example are:
- `get_measurement_xyz_gauss()`

## Example 2: Calibration
`qwiic_mmc5983ma_ex2_calibration.py`

Demonstrates how to calibrate the MMC5983MA Magnetometer

The key functions showcased by this example are:
- `calibrate_offsets()`
- `get_offsets()`

## Example 3: Compass
`qwiic_mmc5983ma_ex3_compass.py`

Demonstrates how to use the MMC5983MA Magnetometer as a compass

The key functions showcased by this example are:
- `get_measurement_x_gauss()`
- `get_measurement_y_gauss()`
