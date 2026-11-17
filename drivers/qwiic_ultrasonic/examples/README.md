# Sparkfun Ultrasonic Py Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_ultrasonic_py/issues). 

## Example 1: Basic Readings
This example demonstrates basic bringup of the Qwiic Ultrasonic HC-SR04 to to print distance measurements (in mm) every tenth of a second.

The key method showcased by this example is [trigger_and_read()](https://docs.sparkfun.com/qwiic_ultrasonic_py/classqwiic__ultrasonic_1_1_qwiic_ultrasonic.html#a3ab08f0d5ed5b2b1c34bcee954927e6b)

## Example 2: Change I2C Address
This example demonstrates how to change the I2C address on the Qwiic Ultrasonic HC-SR04. The user is prompted for a new I2C address in the legal range 0x20 to 0x2F. Then, the address of the sensor is changed to the user's selection. 

The key method showcased by this example is [change_address()](https://docs.sparkfun.com/qwiic_ultrasonic_py/classqwiic__ultrasonic_1_1_qwiic_ultrasonic.html#a027312bc157eb37aeff0529013a3dc4a)