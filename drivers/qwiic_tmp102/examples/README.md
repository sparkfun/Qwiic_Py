# Sparkfun TMP102 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_tmp102_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example1-Gettemperature
Simple Example for the Qwiic TMP102 Device

The key methods showcased by this example are: 
- [set_fault()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#a344274d651723491c358b6d94a0a5309)
- [set_alert_polarity()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#a3474e054fccda8ddde2e0f30cfe9570f)
- [set_alert_mode()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#a3bf679ecd81acde07dac06dc0c669f82)
- [set_conversion_rate()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#a227f41d274da19b293424c4866475873)
- [set_extended_mode()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#a96024ea22ff9a381c3d391038c0a4da8)
- [set_high_temp_f()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#af5890245c9d35a2bc6c0349ef87b8081)
- [set_low_temp_f()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#acfd545a8aef7abde61091ada16dbbe17)
- [wakeup()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#a3458195c0618a415928085abbee4377b)
- [read_temp_f()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#ae73d5f968d98d748113d2d4c4943dd41)
- [alert()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#a26120555525346ab140cf6a46a09061a)
- [sleep()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#adec143eb2a7ef012cd7299cfb93ccbf9)

## Example2 One-Shot Temperature Reading
This sketch connects to the TMP102 temperature sensor and enables the
 one-shot temperature measurement mode using the one_shot() function.
 The function returns 0 until the temperature measurement is ready to
 read (takes around 25ms). After the measurment is read, the TMP102 is
 placed back into sleep mode before the loop is repeated. This can be 
 useful to save power or increase the continuous conversion rate from
 8Hz up to a maximum of 40Hz.

 This code is beerware; if you see me (or any other SparkFun employee) at
 the local, and you've found our code helpful, please buy us a round!

 Distributed as-is; no warranty is given.

The key methods showcased by this example are: 
- [one_shot()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#ac6ddcc1f60857d3ff39711667802d4a3)
- [read_temp_c()](https://docs.sparkfun.com/qwiic_tmp102_py/classqwiic__tmp102_1_1_qwiic_tmp102_sensor.html#a7ae43b44590dfaee186782d1bbfa9d1f)

