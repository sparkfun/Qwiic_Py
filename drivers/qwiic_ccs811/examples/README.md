# SparkFun CCS811 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

NOTE: The numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Example 1: Basic Readings
`qwiic_ccs811_ex1_basic_readings.py`

This example reads equivalent CO2 and TVOC from the CCS811 once a second. On a Raspberry Pi it also checks that the I2C clock is slow enough for the CCS811.

The key methods showcased by this example are:

- `begin()`
- `is_rpi_i2c_baudrate_ok()`
- `read_algorithm_results()`
- `get_co2()`
- `get_tvoc()`


## Example 3: NTC Compensated
`qwiic_ccs811_ex3_ntc_compensated.py`

This example reads the temperature from an NTC thermistor connected to the CCS811 and uses it to compensate the CO2 and TVOC readings. The Qwiic CCS811 doesn't support this, but other SparkFun CCS811 boards do.

The key methods showcased by this example are:

- `set_reference_resistance()`
- `data_available()`
- `read_ntc()`
- `get_resistance()`
- `get_temperature()`
- `set_environmental_data()`
- `check_status_error()`
- `get_error_register()`


## Example 7: Set Environmental Readings
`qwiic_ccs811_ex7_set_environmental_readings.py`

This example sends random humidity and temperature values to the CCS811 for compensation, then prints the CO2 and TVOC readings.

The key methods showcased by this example are:

- `set_environmental_data()`
- `data_available()`
- `read_algorithm_results()`
