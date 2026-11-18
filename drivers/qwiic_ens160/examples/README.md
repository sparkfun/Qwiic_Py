# SparkFun ENS160 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Qwiic Ens160 Ex1 Basic
`qwiic_ens160_ex1_basic.py`

This example shows basic data retrieval from the SparkFun Indoor Air Quality Sensor - ENS160.

The key methods showcased by this example are:
- `set_operating_mode()`
- `get_flags()`
- `check_data_status()`
- `get_aqi()`
- `get_tvoc()`
- `get_eco2()`

## Qwiic Ens160 Ex4 Bme280 Temp Rh Compensation
`qwiic_ens160_ex4_bme280_temp_rh_compensation.py`

This example shows how to give the ENS160 Temperature and Relative Humidity
  Data for compensation with the BME280. Note that the values that are given for compensation are not
  populated in their registers until the Air Quality Sensor is set to "Standard" operation
  and when data is ready (i.e. the data ready bit is set). Also note that there will be some
  rounding of the temperature and relative humidity values when they're given to the sensor
  and again when they're read back.

 SparkFun Environmental Combo Breakout: https://www.sparkfun.com/products/22858
 SparkFun Atmospheric Sensor Breakout: https://www.sparkfun.com/products/15440

The key methods showcased by this example are:
- `set_temp_compensation_celsius()`
- `set_rh_compensation()`
- `get_rh()`
- `get_temp_celsius()`

This example also needs the [BME280 driver](https://github.com/sparkfun/Qwiic_Py/tree/main/drivers/qwiic_bme280) (`qwiic_bme280`).

## Qwiic Ens160 Ex6 Burn In
`qwiic_ens160_ex6_burn_in.py`

This example demonstrates the warm up phase of the ENS160. After the "burn-in" phase
  the readings from the ENS160 will be more accurate. Before any data is given, the
  the sensor waits for the status flag to return "Initial Start Up" or "Normal Operation".
  This time take approximately three minutes.

## Qwiic Ens160 Ex7 Raw Resistance
`qwiic_ens160_ex7_raw_resistance.py`

This example retreieves the raw resistance of the plates. This would be used
  in the case that you want to process these values yourself.

The key methods showcased by this example are:
- `get_raw_resistance()`
