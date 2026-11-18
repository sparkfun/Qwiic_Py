# Sparkfun AS7343 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic As7343 Ex1 Basic Readings
`qwiic_as7343_ex1_basic_readings.py`

This example shows how to setup the AS7343 sensor with default settings and
 print out 4 channels from the sensor (Red, Green, Blue, and NIR).

## Qwiic As7343 Ex2 All Channels
`qwiic_as7343_ex2_all_channels.py`

This example shows how to setup the AS7343 sensor with default settings and
 print out all the spectral data from the sensor.

## Qwiic As7343 Ex3 Gain
`qwiic_as7343_ex3_gain.py`

This example shows how to setup the AS7343 sensor with a specific Spectral 
 Engines Gain Setting (aka "AGAIN").

## Qwiic As7343 Ex5 Flicker Detection
`qwiic_as7343_ex5_flicker_detection.py`

This example shows how to use the Flicker Detection feature of the AS7343 sensor.
 It sets up the sensor with default settings and prints out the flicker detection
 results to the serial monitor.

## Qwiic As7343 Ex6 Sleep
`qwiic_as7343_ex6_sleep.py`

This example shows how to setup the AS7343 sensor with default settings and
   print out all the spectral data from the sensor, putting it to "sleep" inbetween
   measurements to save power.
  
   Note, the AS7343 datasheet refers to each mode of operation as Sleep, Idle,
   and Active. Although there is no direct control of a power mode, we can turn off
   the Measurement and the Power ON bits in the Enable register to put the device
     into a low power state (~350uA).

## Qwiic As7343 Ex7 Web Bar Graphs
`qwiic_as7343_ex7_web_bar_graphs.py`

This example shows how to setup the AS7343 sensor with the SparkFun Web Serial
 Bar Graphs Demo. It prints the spectral data in a format that the
 [SparkFun WebSerialPlotter](https://github.com/sparkfun/SparkFun_WebSerialPlotter)
 can display as bar graphs.
