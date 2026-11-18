# SparkFun Qwiic TCA9548A Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

## Example 1: Scan Channels
`qwiic_tca9548a_ex1_scan_channels.py`

Simple example for the Qwiic 8 Channel Mux. This example alternates between enabling channels 0 and 1 and channels 2 and 3, prints the enabled channels, and lists the devices found on each pair.

The key methods showcased by this example are:

- `disable_all()`
- `enable_channels()`
- `list_channels()`

## Example 2: Two Distance Sensors
`qwiic_tca9548a_ex2_two_distance_sensors.py`

Example for the Qwiic 8 Channel Mux interfacing with two Qwiic VL53L1X Distance Sensors. This example shows how to interface with two sensors that have the same I2C address by enabling different mux channels at different times. It needs the `qwiic_vl53l1x` driver too.

The key methods showcased by this example are:

- `disable_all()`
- `enable_channels()`

## Example 3: Enable Channels
`qwiic_tca9548a_ex3_enable_channels.py`

This example enables channels 0 and 4, then channel 7, printing the enabled channels after each step.

The key methods showcased by this example are:

- `enable_channels()`
- `list_channels()`

## Example 4: Disable Channels
`qwiic_tca9548a_ex4_disable_channels.py`

This example disables channels 0 and 4, printing the enabled channels before and after.

The key methods showcased by this example are:

- `disable_channels()`
- `list_channels()`
