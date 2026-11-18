# Sparkfun AS6212 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

## Example 1: Basic Readings
`qwiic_as6212_ex1_basic_readings.py`

Configures the AS6212 alert settings (consecutive faults, polarity, interrupt mode, conversion cycle time and T_HIGH/T_LOW thresholds), then reads the temperature and alert status, putting the sensor to sleep between readings.

The key methods showcased by this example are:

- `set_consecutive_faults()`
- `set_alert_polarity()`
- `set_interrupt_mode()`
- `set_conversion_cycletime()`
- `set_high_temp_f()`
- `set_low_temp_f()`
- `read_low_temp_f()`
- `read_high_temp_f()`
- `set_sleep_mode()`
- `read_temp_f()`
- `get_alert_status()`

## Example 2: Single Shot
`qwiic_as6212_ex2_single_shot.py`

Puts the sensor into sleep mode, then triggers a single conversion for each reading and times how long it takes. This keeps power use to a minimum.

The key methods showcased by this example are:

- `set_sleep_mode()`
- `trigger_single_shot_conversion()`
- `get_single_shot_status()`
- `read_temp_f()`
