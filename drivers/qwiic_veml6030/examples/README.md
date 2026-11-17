# Sparkfun VEML6030 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_veml6030_py/issues). 

NOTE: The abnormal numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
This example demonstrates basic bringup of the VEML6030 to read and print ambient light measurements in lux every second.

The key method showcased by this example is [read_light()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#acd1cc61adaf25315b4dfb37d5bb1697d)

## Example 2: Settings
This example demonstrates how to change basic settings of the VEML6030. Gain and integration time are both manually set and then checked. Finally ambient light is read and printed with a period equal to the integration time.

The key methods showcased by this example are:
- [set_gain()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#a2a07076e8d5edea5f6ee781328c6032d)
- [set_integ_time()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#aeba91ad95e4548efbcf0e447676d1539)

## Example 3: Threshold Interrupts
This example demonstrates how to set up threshold interrupts for the VEML6030. First, the low threshold is set to 20 lux and the high threshold is set to 200 lux. Then, the threshold settings are read and confirmed. Finally, the ambient light is printed every integration time period, as well as a message if either the high or low threshold interrupts have occurred.

The key methods showcased by this example are:
- [set_int_low_thresh()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#a0559f3cb0aeacc522f7e7c2740ee802c)
- [set_int_high_thresh()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#a59c8e64395b85e33846d1b62853e2558)
- [read_low_thresh()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#a0c2d78a6ae369222b9243692799dbdec)
- [read_high_thresh()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#ac3a0badece94a5519e92c22a0103b868)
- [read_interrupt()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#a1e59fe263f1163db54edf815e06c9c69)

## Example 4: Power Saving
This example demonstrates how to enter power saving mode on the VEML6030. The sensor is set to minimum current consumption settings and then the lux is printed very 4.1 seconds. This period is specified in page 9 of the datasheet for the refresh time when in power saving mode 4. 

The key methods showcased by this example are:
- [set_pow_sav_mode()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#aa2bacce96ea2175c316ce3067aba3813)
- [read_pow_sav_mode()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#adfad56621faa24774651a2f2de442c95)
- [enable_pow_save()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#a6beaf964dd89c41ce2c31e8571f42f36)
- [read_pow_sav_enabled()](https://docs.sparkfun.com/qwiic_veml6030_py/classqwiic__veml6030_1_1_qwiic_v_e_m_l6030.html#a9ca7a37b8242c0887667c1663c212114)