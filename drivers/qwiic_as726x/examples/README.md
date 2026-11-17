# Sparkfun AS726X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_as726x_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic As726X Ex1 Basic
This example prints all measurements based on whether the device is AS7262 or AS7263

The key methods showcased by this example are:
- [take_measurements()](https://docs.sparkfun.com/qwiic_as726x_py/classqwiic__as726x_1_1_qwiic_a_s726x.html#abaa761d3f43a42dffb84ad802a0d89e4)
- The various [get_calibrated_...()](https://docs.sparkfun.com/qwiic_as726x_py/classqwiic__as726x_1_1_qwiic_a_s726x.html#a2125cb7746b49359a91fcfb1e7afbe52) methods
- [get_temperature_f()](https://docs.sparkfun.com/qwiic_as726x_py/classqwiic__as726x_1_1_qwiic_a_s726x.html#a7b4a42a6a5a168a82a038360cf81ea9c)

## Qwiic As726X Ex2 Settings
This example shows how to set custom Gain and Measurement Mode settings with begin()

The key methods showcased by this example are:
- [begin()](https://docs.sparkfun.com/qwiic_as726x_py/classqwiic__as726x_1_1_qwiic_a_s726x.html#a1511744c9efad6cee70cc4aa8ff51d0f)

## Qwiic As726X Ex3 Bulb
This example shows how to take 4-channel measurements with the bulb enabled

The key methods showcased by this example are:
- [take_measurements_with_bulb()](https://docs.sparkfun.com/qwiic_as726x_py/classqwiic__as726x_1_1_qwiic_a_s726x.html#aa42605739ce59684f20af5a2f0419858)


