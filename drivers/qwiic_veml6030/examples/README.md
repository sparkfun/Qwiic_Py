# Sparkfun VEML6030 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: The abnormal numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
`qwiic_veml6030_ex1_basic_readings.py`

This example demonstrates basic bringup of the VEML6030 to read and print ambient light measurements in lux every second.

The key method showcased by this example is:
- `read_light()`

## Example 2: Settings
`qwiic_veml6030_ex2_settings.py`

This example demonstrates how to change basic settings of the VEML6030. Gain and integration time are both manually set and then checked. Finally ambient light is read and printed with a period equal to the integration time.

The key methods showcased by this example are:
- `set_gain()`
- `set_integ_time()`

## Example 3: Threshold Interrupts
`qwiic_veml6030_ex3_threshold_interrupts.py`

This example demonstrates how to set up threshold interrupts for the VEML6030. First, the low threshold is set to 20 lux and the high threshold is set to 200 lux. Then, the threshold settings are read and confirmed. Finally, the ambient light is printed every integration time period, as well as a message if either the high or low threshold interrupts have occurred.

The key methods showcased by this example are:
- `set_int_low_thresh()`
- `set_int_high_thresh()`
- `read_low_thresh()`
- `read_high_thresh()`
- `read_interrupt()`

## Example 4: Power Saving
`qwiic_veml6030_ex4_power_saving.py`

This example demonstrates how to enter power saving mode on the VEML6030. The sensor is set to minimum current consumption settings and then the lux is printed very 4.1 seconds. This period is specified in page 9 of the datasheet for the refresh time when in power saving mode 4. 

The key methods showcased by this example are:
- `set_pow_sav_mode()`
- `read_pow_sav_mode()`
- `enable_pow_save()`
- `read_pow_sav_enabled()`