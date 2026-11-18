# SparkFun SGP40 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

NOTE: The abnormal numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Example 1: Basic Readings
`qwiic_sgp40_ex1_basic_readings.py`

This example demonstrates basic bringup of the SGP40 to print the Volatile Organic Compound (VOC) Index.

The key method showcased by this example is `get_voc_index()`

## Example 2: Function Test
`qwiic_sgp40_ex2_function_test.py`

This example demonstrates how to perform a self-test, turn the heater off, and perform a soft reset on the SGP40.

The key methods showcased by this example are:

- `measure_test()`
- `heater_off()`
- `soft_reset()`
