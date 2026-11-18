# Sparkfun Proximity Sensor (VCNL4040) Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: The abnormal numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
`qwiic_proximity_ex1_basic_readings.py`

Sets up the VCNL4040 and prints the proximity value.

The key methods showcased by this example are:

- `begin()`
- `get_proximity()`

## Example 2: Presence Sensing
`qwiic_proximity_ex2_presence_sensing.py`

Averages 8 proximity readings as a baseline, then reports when something comes close to the sensor (a 5% change) and when it goes away.

The key methods showcased by this example are:

- `set_led_current()`
- `set_prox_integration_time()`
- `get_proximity()`

## Example 3: Ambient Light
`qwiic_proximity_ex3_ambient_light.py`

Powers down the proximity sensor and prints the ambient light value.

The key methods showcased by this example are:

- `power_off_proximity()`
- `power_on_ambient()`
- `get_ambient()`

## Example 4: All Readings
`qwiic_proximity_ex4_all_readings.py`

Enables the proximity, ambient and white light channels and prints all three values.

The key methods showcased by this example are:

- `power_on_proximity()`
- `power_on_ambient()`
- `enable_white_channel()`
- `get_proximity()`
- `get_ambient()`
- `get_white()`

## Example 5: Advanced Settings
`qwiic_proximity_ex5_advanced_settings.py`

Sets the integration times, the proximity interrupt thresholds and type, and enables the proximity logic output mode, so the INT pin goes low whenever a reading is outside the thresholds.

The key methods showcased by this example are:

- `set_prox_integration_time()`
- `set_ambient_integration_time()`
- `set_prox_high_threshold()`
- `set_prox_low_threshold()`
- `set_prox_interrupt_type()`
- `enable_prox_logic_mode()`

## Example 8: Connection Check
`qwiic_proximity_ex8_connection_check.py`

Checks the sensor is still connected before every reading, and prints "Not Connected" when it isn't.

The key methods showcased by this example are:

- `is_connected()`
- `power_on_proximity()`
- `get_proximity()`
