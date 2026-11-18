# Sparkfun VL53L1X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

Each example takes a measurement the same way: `start_ranging()`, wait for `check_for_data_ready()`, `get_distance()`, then `clear_interrupt()` to arm the sensor for the next measurement, and `stop_ranging()`.

## Example 1: Read Distance
`qwiic_vl53l1x_ex1_read_distance.py`

This example prints the distance to an object. If you are getting weird
readings, be sure the vacuum tape has been removed from the sensor.

The key methods showcased by this example are: 
- `begin()`
- `start_ranging()`
- `check_for_data_ready()`
- `get_distance()`
- `clear_interrupt()`
- `stop_ranging()`

## Example 2: Set Distance Mode
`qwiic_vl53l1x_ex2_set_distance_mode.py`

This example configures the sensor to short distance mode and then
prints the distance to an object. If you are getting weird readings,
be sure the vacuum tape has been removed from the sensor.

The key methods showcased by this example are: 
- `set_distance_mode()`

## Example 3: Status and Rate
`qwiic_vl53l1x_ex3_status_and_rate.py`

This example configures the sensor to short distance mode and then
prints the distance to an object. The output also includes a
running average of the last 10 readings along with some statistics,
like signal rate and frequency (of the measurements).

If you are getting weird readings, be sure the vacuum tape has been
removed from the sensor.

The key methods showcased by this example are: 
- `get_signal_rate()`
- `get_range_status()`

## Example 4: Set Intermeasurement Period
`qwiic_vl53l1x_ex4_set_intermeasurement_period.py`

This example configures the inter-measurement period of the sensor
and then prints the distance to an object. If you are getting weird
readings, be sure the vacuum tape has been removed from the sensor.

The key methods showcased by this example are: 
- `set_inter_measurement_in_ms()`
- `get_inter_measurement_in_ms()`
