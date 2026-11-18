# Sparkfun Titan GPS Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic
`qwiic_titan_gps_ex1_basic.py`

In this example NMEA data is requested from the GPS module and the recieved Latitude, Longitude, and Time data is printed to the screen.

The key methods and attributes showcased by this example are: 
- `get_nmea_data()`
- `gnss_messages`

## Example 2: All Data
`qwiic_titan_gps_ex2_all_data.py`

In this example, much like the first, NMEA data is requested from the SparkFun
GPS Breakout Board. All data that is retrieved is the printed to the screen.

The key methods and attributes showcased by this example are: 
- `get_nmea_data()`
- `gnss_messages`
