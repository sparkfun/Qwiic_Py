# Sparkfun BME280 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_bme280_py/issues). 

NOTE: The abnormal numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
This example demonstrates basic bringup of the BME280 to extract humidity, pressure, altitude, and temperature.

The key methods showcased by this example are: 

- [read_humidity()](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a601d62c86ef837f61c3e452a3f390b9d)
- [read_pressure()](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#af799265b51181bd65cae6983c245c513)
- [get_altitude_feet()](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#af5b0a1f1c2355f72d2182ed0c036ef8e)
- [get_temperature_fahrenheit()](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a31603e97db007558964618800b055a61)

These methods are invoked via reading their corresponding properties([humidity](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#ace5c02deec66d7096a322f68bd19e35d), [pressure](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a169132f58174ba65b2ef1148858a93f7), [altitude_feet](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#aa6b842360817379f6c9026767b4c51cb), and [temperature_fahrenheit](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a42eb4ab7f10b8188d9174384feb2e328))

## Example 4: Settings
This example shows how to change the various filter and oversample settings of the BME280. It sets several filtering and oversampling settings and then performs the same readings as in Example 1. 

The key methods showcased by this example are:

- [set_filter()](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a5f32790df30c3c23c82b2aa2f43fc378)
- [set_standby_time()](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#ac92bbaf17893b45805678d05af28cff8)
- [set_tempature_oversample()](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a4cb331d973e88bb6e85c03ead63b042f)
- [set_humidity_oversample()](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a510a98a4a15cdf4d634aaacfbde6139c)
- [set_mode()](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a4cb378ab043d8dfa7c3c6c48e19bab84)

These methods are invoked via reading their corresponding properties ([filter](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#abd7049904b69e17438de6c1bfad899b4), [standby_time](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a16991516b62efcb3400ce1a6ead3f8a3), [tempature_oversample](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#aaa2c92f61e6c0360c2d480074ed73b3a), [humidity_oversample](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a7b7bf88a522fced77db96301b5fced51), [mode](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#aec55ad7625fa470e5f7f4d0e415ec96e))

## Example 5: Read All Registers
This example configures the BME280 to read all measurements. It also displays the BME280's physical memory and what the driver perceives the calibration words to be.

This method showcases direct I2C reads as well as the use of the [calibration property](https://docs.sparkfun.com/qwiic_bme280_py/classqwiic__bme280_1_1_qwiic_bme280.html#a61ff5a498e96023a6c82cb99ca6a093b)