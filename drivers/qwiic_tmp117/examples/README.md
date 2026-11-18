# Sparkfun TMP117 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic
`qwiic_tmp117_ex1_basic.py`

This script configures the TMP117 temperature sensor and prints the
 temperature in degrees celsius and fahrenheit with a 500ms delay for
 easier readings.

The key methods showcased by this example are: 
- `data_ready()`
- `read_temp_c()`
- `read_temp_f()`

## Example 2: Alert Statuses
`qwiic_tmp117_ex2_alert_statuses.py`

This script sets the TMP117 temperature sensor's high limit,
 low limit, and alert function mode. Once set, we read the 
 temperature in C and checks alert status. If we are outside
 of the boundary, we will output a message indicating
 that we are beyond the limit.

The key methods showcased by this example are: 
- `set_high_limit()`
- `set_low_limit()`
- `get_alert_function_mode()`
- `get_high_low_alert()`

## Example 3: Set Offset Temp
`qwiic_tmp117_ex3_set_offset_temp.py`

This script configures the TMP117 temperature sensor and allows the user to
 set the offset temperature for System Correction.

The key methods showcased by this example are: 
- `get_temperature_offset()`
- `set_temperature_offset()`

## Example 4: Set Conv Mode
`qwiic_tmp117_ex4_set_conv_mode.py`

This script can get and set the conversion mode to
 Continuous Conversion, Shutdown, or One-Shot

The key methods showcased by this example are: 
- `set_continuous_conversion_mode()`
- `set_shutdown_mode()`
- `set_one_shot_mode()`

## Example 5: Set Alert Limits
`qwiic_tmp117_ex5_set_alert_limits.py`

This script can set and get the Alert Function Mode, Low Temperature 
 Limit, and High Temperature Limit for the sensor. These limits can
 be set within +/- 256°C. When the temperature goes above/below the 
 specified temperature limits, it will cause the alert pins to go
 high. To access these registers, please reference Example 2: Alert Statuses.

The key methods showcased by this example are: 
- `set_low_limit()`
- `set_high_limit()`
- `set_alert_function_mode()`

## Example 6: Set Conv Cycle
`qwiic_tmp117_ex6_set_conv_cycle.py`

This script can set and get the Conversion Times in Continuous Conversion mode
 for the Sensor. A chart for the averaging modes and the conversion times can
 be found in the table below or in the Datasheet on page 27 table 7.

The key methods showcased by this example are: 
- `set_conversion_average_mode()`
- `set_conversion_cycle_bit()`

## Example 7: Set Address
`qwiic_tmp117_ex7_set_address.py`

This script allows the user to change the address of the device and to
 change the Wire port for I2C Communications. The address can be physically
 changed with an external jumper on the back of the sensor. 
 
 See the "Address Select" section in the hookup guide for more information:
 https://learn.sparkfun.com/tutorials/qwiic-tmp117-high-precision-digital-temperature-sensor-hookup-guide

The key methods showcased by this example are: 
- `get_address()`
