# Sparkfun FS3000 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic
`qwiic_fs3000_ex1_basic.py`

Read values of air velocity from the FS3000 sensor, print them to terminal.
   Prints raw data, m/s and mph.
   Note, the response time on the sensor is 125ms.

The key methods showcased by this example are:
- `set_range()`
- `read_raw()`
- `read_meters_per_second()`
- `read_miles_per_hour()`
