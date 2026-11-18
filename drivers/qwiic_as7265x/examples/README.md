# Sparkfun AS7265X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic As7265X Ex1 Basic
`qwiic_as7265x_ex1_basic.py`

This example takes all 18 readings, 372nm to 966nm, over I2C and outputs
 them to the serial port.

The key methods showcased by this example are:
- The various `get_calibrated_...()` functions.
- `take_measurements()`

## Qwiic As7265X Ex2 Leds
`qwiic_as7265x_ex2_leds.py`

This example takes all 18 readings and blinks the illumination LEDs 
 as it goes. We recommend you point the Triad away from your eyes, the LEDs are *bright*.

The key methods showcased by this example are:
- `disable_indicator()`
- `take_measurements_with_bulb()`

## Qwiic As7265X Ex3 Settings
`qwiic_as7265x_ex3_settings.py`

This example shows how to change the gain, mode, and LED drive currents

The key methods showcased by this example are:
- `set_measurement_mode()`
- `set_integration_cycles()`
- `set_bulb_current()`
- `enable_interrupt()`

## Qwiic As7265X Ex4 Read Raw
`qwiic_as7265x_ex4_read_raw.py`

This example shows how to output the raw sensor values. This is probably never needed since the 
 calibrated values are tuned to each sensor. But it does run faster (2 bytes per channel instead of 4)

The key methods showcased by this example are the various `get_...()` functions.

## Qwiic As7265X Ex5 Max Read Rate
`qwiic_as7265x_ex5_max_read_rate.py`

This example shows how to setup the sensor for max, calibrated read rate.

## Qwiic As7265X Ex6 Read Temp
`qwiic_as7265x_ex6_read_temp.py`

This example shows how to read the temperature of the ICs

The key methods showcased by this example are:
- `get_temperature()`
- `get_temperature_average()`

## Qwiic As7265X Ex7 Get Version
`qwiic_as7265x_ex7_get_version.py`

This example shows how to read the temperature of the ICs

The key methods showcased by this example are:
- `get_device_type()`
- `get_hardware_version()`
- `get_major_firmware_version()`
- `get_patch_firmware_version()`
- `get_build_firmware_version()`


