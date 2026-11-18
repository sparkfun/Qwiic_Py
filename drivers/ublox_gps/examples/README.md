# Sparkfun u-blox GPS Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

Examples 1 to 5 use the serial port `/dev/serial0` at 38400 baud. Change the port if your module is connected over USB (for example `/dev/ttyACM0`).

## Example 1: Geo Coords
`ublox_gps_ex1_geo_coords.py`

Gets and prints latitude, longitude and heading of motion.

The key method showcased by this example is `geo_coords()`

## Example 2: GPS Time
`ublox_gps_ex2_gps_time.py`

Prints the UTC date and time and whether they are valid.

The key method showcased by this example is `date_time()`

## Example 3: Dead Reckoning
`ublox_gps_ex3_dead_reckoning.py`

Prints the vehicle attitude (roll, pitch, heading and their accuracies) from a dead reckoning module. See the [hookup guide](https://learn.sparkfun.com/tutorials/sparkfun-gps-rtk-dead-reckoning-zed-f9r-hookup-guide) for where to attach the module and how to calibrate it.

The key method showcased by this example is `veh_attitude()`

## Example 4: Stream NMEA
`ublox_gps_ex4_stream_nmea.py`

Prints the NMEA sentences from the module.

The key method showcased by this example is `stream_nmea()`

## Example 5: Configuration Settings
`ublox_gps_ex5_configuration_settings.py`

Reads a configuration item (the NMEA protocol version, key `0x20930001`) with the u-blox configuration interface. Works on modules with the configuration interface (F9 and M9 series).

The key method showcased by this example is `ubx_get_val()`

## Example 6: Using SPI
`ublox_gps_ex6_using_spi.py`

Does the same as Example 1 over SPI: pass a `spidev.SpiDev()` port and the driver sets it up for the u-blox module.
