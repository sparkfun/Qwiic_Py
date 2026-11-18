# SparkFun Qwiic RFID Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues)

NOTE: The numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Example 1: Get Tag
`qwiic_rfid_ex1_get_tag.py`

Reads the latest tag and prints its ID and how long ago it was scanned.

The key methods showcased by this example are:

- `get_tag()`
- `get_prec_req_time()`

## Example 2: Get All Tags
`qwiic_rfid_ex2_get_all_tags.py`

Every 10 seconds, reads every tag in the reader's buffer and prints their IDs and scan times.

The key methods showcased by this example are:

- `get_all_tags()`
- `get_all_prec_times()`

## Example 3: Change I2C Address
`qwiic_rfid_ex3_change_i2c_address.py`

Takes a new I2C address from the user and changes the reader's address.

The key methods showcased by this example are:

- `change_address()`
