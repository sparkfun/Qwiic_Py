# SparkFun SCD4X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Qwiic Scd4X Ex1 Basic
`qwiic_scd4x_ex1_basic.py`

This example prints the current CO2 level, relative humidity, and temperature in C.

The key methods showcased by this example are:
- `read_measurement()`
- `get_co2()`
- `get_temperature()`
- `get_humidity()`

## Qwiic Scd4X Ex2 Low Power
`qwiic_scd4x_ex2_low_power.py`

This example uses low-power measurements and
 prints the current CO2 level, relative humidity, and temperature in C.

The key methods showcased by this example are:
- `start_low_power_periodic_measurement()`

## Qwiic Scd4X Ex3 Disable Auto Calibration
`qwiic_scd4x_ex3_disable_auto_calibration.py`

This example disables automatic calibration and
 prints the current CO2 level, relative humidity, and temperature in C.

The key methods showcased by this example are:
- `begin()`

## Qwiic Scd4X Ex4 Skip Stop Periodic
`qwiic_scd4x_ex4_skip_stop_periodic.py`

This example skips the stop_periodic_measurement() call in begin() and
 prints the current CO2 level, relative humidity, and temperature in C.

The key methods showcased by this example are:
- `stop_periodic_measurement()`

## Qwiic Scd4X Ex6 Signal Compensation
`qwiic_scd4x_ex6_signal_compensation.py`

This example shows how to set the three signal compensation settings:
 temperature offset, sensor altitude, and ambient pressure.

The key methods showcased by this example are:
- `set_temperature_offset()`
- `set_sensor_altitude()`
- `set_ambient_pressure()`
- `get_serial_number()`

## Qwiic Scd4X Ex7 Test And Reset
`qwiic_scd4x_ex7_test_and_reset.py`

This example shows how to perform a self test and factory reset on the SCD4x sensor.

The key methods showcased by this example are:
- `perform_self_test()`
- `perform_factory_reset()`

## Qwiic Scd4X Ex8 Scd41 Single Shot
`qwiic_scd4x_ex8_scd41_single_shot.py`

This example shows how to perform single-shot data acquisition on the SCD41 sensor.

The key methods showcased by this example are:
- `measure_single_shot_rht_only()`

## Qwiic Scd4X Ex9 Sensor Type
`qwiic_scd4x_ex9_sensor_type.py`

This example determines and prints the device type then exits

The key methods showcased by this example are:
- `get_feature_set_version()`
- `get_sensor_type()`
