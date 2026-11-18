# SparkFun MAX3010X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Ex1 Basic Readings
`qwiic_max3010x_ex1_basic_readings.py`

Simple example for the qwiic MAX3010x device
 Outputs all Red/IR/Green values.

The key methods showcased by this example are:
- `get_ir()`
- `get_green()`

## Ex2 Presence Sensing
`qwiic_max3010x_ex2_presence_sensing.py`

Simple example for the qwiic MAX3010x device
 This takes an average reading at power up and if the reading changes more than 100,
 then print 'Something is there!'.

The key methods showcased by this example are:
- `set_pulse_amplitude_red()`
- `set_pulse_amplitude_green()`
- `get_ir()`


## Ex3 Temperature Sense
`qwiic_max3010x_ex3_temperature_sense.py`

Simple example for the qwiic MAX3010x device
 This demo outputs the onboard temperature sensor.
 The temp sensor is accurate to +/-1 C but
 has an astonishing precision of 0.0625 C.

The key methods showcased by this example are:
- `read_temperature()`
- `read_temperature_f()`

## Ex4 Heartbeat Plotter
`qwiic_max3010x_ex4_heartbeat_plotter.py`

NOTE: This example uses matplotlib, so it only runs on CPython (Linux/Raspberry Pi), not on MicroPython or CircuitPython.
 Shows the user's heart beat on a graphical plotter
 Using Matplotlib
 To learn more about plotting data in python check out this tutorial:
 https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/
 The example code below was built using the code from the previously mentioned tutorial.
 Thanks Shawn Hymel!

## Ex5 Heartrate
`qwiic_max3010x_ex5_heart_rate.py`

Simple example for the qwiic MAX3010x device
 This is a demo to show the reading of heart rate or beats per minute (BPM) using
 a Penpheral Beat Amplitude (PBA) algorithm.

The key methods showcased by this example are:
- `set_pulse_amplitude_red()`
- `set_pulse_amplitude_green()`
- `check_for_beat()`


## Ex6 Fifo Readings
`qwiic_max3010x_ex6_fifo_readings.py`

Simple example for the qwiic MAX3010x device
 Outputs all Red/IR/Green values at  about 5Hz by polling the FIFO
 Note, the Hz is slowed down by printing to the python terminal,
 It can be drmatically speed up if printing is omitted or intermittent

The key methods showcased by this example are:
- `available()`
- `get_fifo_red()`
- `get_fifo_ir()`
- `get_fifo_green()`
