# Sparkfun VL53L5CX Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Distance Array
`qwiic_vl53l5cx_ex1_distance_array.py`

This example shows how to read all 64 distance readings at once.

The key methods showcased by this example are: 
- `set_resolution()`
- `start_ranging()`
- `check_data_ready()`
- `get_ranging_data()`

## Example 3: Set Frequency
`qwiic_vl53l5cx_ex3_set_freq.py`

This example shows how to increase output frequency.

 Default is 1Hz.
 Using 4x4, min frequency is 1Hz and max is 60Hz
 Using 8x8, min frequency is 1Hz and max is 15Hz

The key methods showcased by this example are: 
- `set_ranging_frequency_hz()`
- `get_ranging_frequency_hz()`

## Example 6: Settings
`qwiic_vl53l5cx_ex6_settings.py`

This example shows how to change the ranging mode, power mode, integration time, sharpener and target order.

The key methods showcased by this example are: 
- `set_ranging_mode()`
- `set_power_mode()`
- `set_integration_time_ms()`
- `set_sharpener_percent()`
- `set_target_order()`

## Example 8: Set Address
`qwiic_vl53l5cx_ex8_set_address.py`

This example shows how to set a custom address for the VL53L5CX.

The key methods showcased by this example are: 
- `set_i2c_address()`
