# Sparkfun Soil Moisture Sensor Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_bme280_py/issues). 

## Example 1: Basic Readings
This example demonstrates basic bringup of the Qwiic Soil Moisture Sensor to print moisture level and toggle the LED on and off.

The key methods showcased by this example are: 

- [read_moisture_level()](https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/classqwiic__soil__moisture__sensor_1_1_qwiic_soil_moisture_sensor.html#a21ef69d794e2786b5eb3ef7881ba95db)
- [led_on()](https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/classqwiic__soil__moisture__sensor_1_1_qwiic_soil_moisture_sensor.html#a344fb9aa9120ca97555afc052aa94aa4)
- [led_off()](https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/classqwiic__soil__moisture__sensor_1_1_qwiic_soil_moisture_sensor.html#a9799401c60ab796e346a49718a98f601)


## Example 2: Change I2C Address
This example demonstrates how to change the I2C address on the Qwiic Soil Moisture Sensor. The user is prompted for a new I2C address in the legal range 0x08 to 0x3F. Then, the address of the sensor is changed to the user's selection. 

The key method showcased by this example is [change_address()](https://docs.sparkfun.com/qwiic_soil_moisture_sensor_py/classqwiic__soil__moisture__sensor_1_1_qwiic_soil_moisture_sensor.html#ad3b91fdbd9f8190798af7ee2227d4d63)