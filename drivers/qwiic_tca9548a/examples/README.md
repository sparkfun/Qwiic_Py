# Sparkfun TCA9548A Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_tca9548a_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Tca9548A Ex1
Simple example for the Qwiic 8 Channel Mux. This example alternates between enableing channels 0 & 1 and ports 2 & 3 and listing the enable status of channels. It lists the devices found on each port.

The key methods showcased by this example are: 
- [disable_all()](https://docs.sparkfun.com/qwiic_tca9548a_py/classqwiic__tca9548a_1_1_qwiic_t_c_a9548_a.html#afaad9d1ae741d14c080f34b597919541)
- [enable_channels()](https://docs.sparkfun.com/qwiic_tca9548a_py/classqwiic__tca9548a_1_1_qwiic_t_c_a9548_a.html#a26fc69208d04b5414885a293e7c8f365)
- [list_channels()](https://docs.sparkfun.com/qwiic_tca9548a_py/classqwiic__tca9548a_1_1_qwiic_t_c_a9548_a.html#a15d4dbb9e373e8e9dc3247e48bad7592)

## Qwiic Tca9548A Ex2
Example for the Qwiic 8 Channel Mux interfacing with two Qwiic VL53L1X Distance Sensors. This example shows how to interface with two sensors that have the same I2C address by enabling different mux channels at different times.
