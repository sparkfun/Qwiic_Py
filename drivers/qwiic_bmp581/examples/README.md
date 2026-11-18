# SparkFun BMP581 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Qwiic Bmp581 Ex1 Basic
`qwiic_bmp581_ex1_basic.py`

This example demonstrates how to read basic temperature and pressure values from the Qwiic BMP581

The key methods showcased by this example are:
- `get_sensor_data()`

## Qwiic Bmp581 Ex4 Filtering
`qwiic_bmp581_ex4_filtering.py`

This example demonstrates how to use filtering to smooth temperature and pressure measurements.

The key methods showcased by this example are:
- `set_iir_config()`

## Qwiic Bmp581 Ex5 Oversampling
`qwiic_bmp581_ex5_oversampling.py`

This example demonstrates how to use oversampling to increase resolution and decrease noise
 in temperature and pressure measurements.

The key methods showcased by this example are:
- `set_osr_multipliers()`
- `set_odr_frequency()`
- `get_osr_odr_eff()`

## Qwiic Bmp581 Ex7 Nvm
`qwiic_bmp581_ex7_nvm.py`

This example demonstrates how to write data to the 6 bytes of user-programmable non-volatile memory (NVM) of the Qwiic BMP581 and read it back

The key methods showcased by this example are:
- `nvm_write()`
- `nvm_read()`

## Qwiic Bmp581 Ex8 Low Power
`qwiic_bmp581_ex8_low_power.py`

This example demonstrates how to put the Qwiic BMP581 in deep standby between single forced-mode measurements to minimize power consumption

The key methods showcased by this example are:
- `set_power_mode()`
