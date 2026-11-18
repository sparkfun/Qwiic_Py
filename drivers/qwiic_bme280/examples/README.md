# Sparkfun BME280 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: The abnormal numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
`qwiic_bme280_ex1_basic_readings.py`

This example demonstrates basic bringup of the BME280 to extract humidity, pressure, altitude, and temperature.

The key methods showcased by this example are: 

- `read_humidity()`
- `read_pressure()`
- `get_altitude_feet()`
- `get_temperature_fahrenheit()`


## Example 4: Settings
`qwiic_bme280_ex4_settings.py`

This example shows how to change the various filter and oversample settings of the BME280. It sets several filtering and oversampling settings and then performs the same readings as in Example 1. 

The key methods showcased by this example are:

- `set_filter()`
- `set_standby_time()`
- `set_temperature_oversample()`
- `set_humidity_oversample()`
- `set_mode()`


## Example 5: Read All Registers
`qwiic_bme280_ex5_read_all_registers.py`

This example configures the BME280 to read all measurements. It also displays the BME280's physical memory and what the driver perceives the calibration words to be.

This method showcases direct I2C reads as well as the `calibration` dictionary