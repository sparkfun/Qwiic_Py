# Sparkfun MicroPressure Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic
`qwiic_micropressure_ex1_basic.py`

Basic test of the Qwiic MicroPressure Sensor. Prints the pressure in each of the supported units (`PRESSURE_PSI`, `PRESSURE_PA`, `PRESSURE_KPA`, `PRESSURE_TORR`, `PRESSURE_INHG`, `PRESSURE_ATM`, `PRESSURE_BAR`).

The key methods showcased by this example are: 
- `read_pressure()`
