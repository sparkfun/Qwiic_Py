# Sparkfun TMP102 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Get Temperature
`qwiic_tmp102_ex1_get_temperature.py`

Configures the TMP102 alert settings, then reads the temperature and alert state, putting the sensor to sleep between readings.

The key methods showcased by this example are: 

- `set_fault()`
- `set_alert_polarity()`
- `set_alert_mode()`
- `set_conversion_rate()`
- `set_extended_mode()`
- `set_high_temp_f()`
- `set_low_temp_f()`
- `wakeup()`
- `read_temp_f()`
- `alert()`
- `sleep()`

## Example 2: One-Shot Temperature Reading
`qwiic_tmp102_ex2_one_shot_temperature_reading.py`

This example enables the one-shot temperature measurement mode using the `one_shot()` method.
The method returns 0 until the temperature measurement is ready to
read (takes around 25ms). After the measurement is read, the TMP102 is
placed back into sleep mode before the loop is repeated. This can be 
useful to save power or increase the continuous conversion rate from
8Hz up to a maximum of 40Hz.

The key methods showcased by this example are: 

- `one_shot()`
- `read_temp_c()`
- `sleep()`
