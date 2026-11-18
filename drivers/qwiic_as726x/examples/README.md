# Sparkfun AS726X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic As726X Ex1 Basic
`qwiic_as726x_ex1_basic.py`

This example prints all measurements based on whether the device is AS7262 or AS7263

The key methods showcased by this example are:
- `take_measurements()`
- The various `get_calibrated_...()` methods
- `get_temperature_f()`

## Qwiic As726X Ex2 Settings
`qwiic_as726x_ex2_settings.py`

This example shows how to set custom Gain and Measurement Mode settings with begin()

The key methods showcased by this example are:
- `begin()`

## Qwiic As726X Ex3 Bulb
`qwiic_as726x_ex3_bulb.py`

This example shows how to take 4-channel measurements with the bulb enabled

The key methods showcased by this example are:
- `take_measurements_with_bulb()`


