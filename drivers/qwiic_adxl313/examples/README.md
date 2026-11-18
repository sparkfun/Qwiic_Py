# SparkFun ADXL313 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues)

NOTE: The numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Example 1: Basic Readings
`qwiic_adxl313_ex1_basic_readings.py`

Puts the ADXL313 in measure mode and prints the raw acceleration on each axis whenever new data is ready.

The key methods showcased by this example are:

- `measure_mode_on()`
- `data_ready()`
- `read_accel()`

## Example 2: Set Range
`qwiic_adxl313_ex2_set_range.py`

Sets the measurement range (0.5, 1, 2 or 4 g) while in standby, then prints readings as in Example 1.

The key methods showcased by this example are:

- `standby()`
- `set_range()`

## Example 3: Auto Sleep
`qwiic_adxl313_ex3_auto_sleep.py`

Sets up activity and inactivity detection and autosleep, then prints readings only while the sensor is awake.

The key methods showcased by this example are:

- `set_activity_x()`, `set_activity_threshold()`
- `set_inactivity_x()`, `set_inactivity_threshold()`, `set_time_inactivity()`
- `activity_int()`, `inactivity_int()`
- `autosleep_on()`
- `update_int_source_statuses()`

## Example 4: Low Power Mode
`qwiic_adxl313_ex4_low_power_mode.py`

Turns on low power mode with a 12.5 Hz bandwidth, then prints readings.

The key methods showcased by this example are:

- `low_power_on()`
- `set_bandwidth()`

## Example 5: Standby
`qwiic_adxl313_ex5_standby.py`

Alternates between measure mode, printing readings, and 5 seconds in standby mode.

The key methods showcased by this example are:

- `measure_mode_on()`
- `standby()`

## Example 6: Interrupt
`qwiic_adxl313_ex6_interrupt.py`

Sets up autosleep and maps the activity and inactivity interrupts to the INT1 pin, then prints readings only while the sensor is awake.

The key methods showcased by this example are:

- `set_interrupt_mapping()`
- `data_ready_int()`
- `is_interrupt_enabled()`

## Example 7: FIFO
`qwiic_adxl313_ex7_fifo.py`

Sets up the FIFO in stream mode with a watermark of 30 samples. Each time the watermark is reached, it reads every sample in the FIFO and prints them, with the time since the last read.

The key methods showcased by this example are:

- `set_fifo_mode()`
- `set_fifo_samples_threshold()`
- `watermark_int()`
- `clear_fifo()`
- `get_fifo_entries_amount()`
