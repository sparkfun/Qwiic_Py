# SparkFun Qwiic EEPROM Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Example 1: Basic Read Write
`qwiic_eeprom_ex1_basic_read_write.py`

This example writes and reads back a byte, a 32-bit signed int and a float.

The key methods showcased by this example are:

- `write_byte()`, `read_byte()`
- `write_int()`, `read_int()`
- `write_float()`, `read_float()`

## Example 2: Settings
`qwiic_eeprom_ex2_settings.py`

This example sets the memory size, page size and page write time for a particular EEPROM, and turns off polling for write completion.

The key methods showcased by this example are:

- `set_memory_size()`, `get_memory_size()`
- `set_page_size()`, `get_page_size()`
- `disable_poll_for_write_complete()`
- `set_page_write_time()`

## Example 3: Advanced I2C
`qwiic_eeprom_ex3_advanced_i2c.py`

This example talks to an EEPROM at a non-default I2C address (0x51, with the A0 address bit set).

The key methods showcased by this example are:

- `QwiicEEPROM(address)`

## Example 4: User Options
`qwiic_eeprom_ex4_user_options.py`

This example stores a group of settings in EEPROM, loads them at startup (or writes defaults to a blank EEPROM), and records a new baud rate typed by the user.

The key methods showcased by this example are:

- `write_int()`, `read_int()`
- `write_byte()`, `read_byte()`
- `write_float()`, `read_float()`

## Example 5: Interface Test
`qwiic_eeprom_ex5_interface_test.py`

This example erases the EEPROM, then times and checks reads and writes of bytes, ints, floats, lists and strings at random locations. It erases the whole EEPROM.

The key methods showcased by this example are:

- `erase()`
- `write()`, `read()`
- `write_string()`, `read_string()`
