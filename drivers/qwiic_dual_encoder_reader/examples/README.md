# SparkFun Qwiic Dual Encoder Reader Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues)

## Example 1: Read Counts
`qwiic_dual_encoder_reader_ex1_read_counts.py`

Prints the counts of both encoders every 300 ms.

The key methods showcased by this example are:

- `get_count1()`
- `get_count2()`

## Example 2: Reset Counts
`qwiic_dual_encoder_reader_ex2_reset_counts.py`

Prints the counts of both encoders for about 3 seconds, then sets both counts back to zero, and repeats.

The key methods showcased by this example are:

- `get_count1()`
- `get_count2()`
- `set_count1()`
- `set_count2()`
