# Sparkfun SGP40 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_sgp40_py/issues). 

NOTE: The abnormal numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
This example demonstrates basic bringup of the SGP40 to print the Volatile Organic Compound (VOC) Index.

The key method showcased by this example is [get_VOC_index()](https://docs.sparkfun.com/qwiic_sgp40_py/classqwiic__sgp40_1_1qwiic__sgp40_1_1_qwiic_s_g_p40.html#a576db58d961d914e8dfbcf0e5d16208c)

## Example 2: Function Test
This example demonstrates how to perform a self-test, turn the heater off, and perform a soft reset on the SGP40. 

The key methods showcased by this example are:

- [measure_test()](https://docs.sparkfun.com/qwiic_sgp40_py/classqwiic__sgp40_1_1qwiic__sgp40_1_1_qwiic_s_g_p40.html#ac6934101f5bc41a404ebdfb9039adf26)
- [heater_off()](https://docs.sparkfun.com/qwiic_sgp40_py/classqwiic__sgp40_1_1qwiic__sgp40_1_1_qwiic_s_g_p40.html#a156643482236cca7d1f411c47fcc74a8)
- [soft_reset()](https://docs.sparkfun.com/qwiic_sgp40_py/classqwiic__sgp40_1_1qwiic__sgp40_1_1_qwiic_s_g_p40.html#a3307442d5b8f693ad1c2450debfd1076)