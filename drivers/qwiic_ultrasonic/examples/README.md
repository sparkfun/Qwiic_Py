# Sparkfun Ultrasonic Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

## Example 1: Basic Readings
`qwiic_ultrasonic_ex1_basic_readings.py`

This example demonstrates basic bringup of the Qwiic Ultrasonic HC-SR04 to to print distance measurements (in mm) every tenth of a second.

The key method showcased by this example is `trigger_and_read()`

## Example 2: Change I2C Address
`qwiic_ultrasonic_ex2_change_address.py`

This example demonstrates how to change the I2C address on the Qwiic Ultrasonic HC-SR04. The user is prompted for a new I2C address in the legal range 0x20 to 0x2F. Then, the address of the sensor is changed to the user's selection. 

The key method showcased by this example is `change_address()`
