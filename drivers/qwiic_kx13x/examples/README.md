# SparkFun KX13X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues)

NOTE: The numbering of examples is to retain consistency with the Arduino library from which this was ported.

Each example uses the KX132. For the KX134, follow the comments in the example to use `QwiicKX134`, its `KX134_RANGE*` constants and `kx134_accel`.

## Example 1: Basic Readings
`qwiic_kx13x_ex1_basic_readings.py`

Resets the accelerometer, sets its range and prints the acceleration on each axis whenever new data is ready.

The key methods showcased by this example are:

- `software_reset()`
- `enable_accel()`
- `set_range()`
- `enable_data_engine()`
- `data_ready()`
- `get_accel_data()`

## Example 3: Buffer
`qwiic_kx13x_ex3_buffer.py`

Shows how to set up the sample buffer, and how to route the buffer's interrupt to a physical interrupt pin.

The key methods showcased by this example are:

- `enable_buffer_and_interrupt()`
- `enable_phys_interrupt()`
- `route_hardware_interrupt()`
- `set_buffer_operation_and_resolution()`
- `get_sample_level()`
- `get_raw_accel_buffer_data()`
- `conv_accel_data()`

## Example 4: Tap
`qwiic_kx13x_ex4_tap.py`

Shows how to enable the tap engine and detect single taps.

The key methods showcased by this example are:

- `enable_tap_engine()`
- `tap_detected()`
- `get_direction()`
- `unknown_tap()`
- `double_tap_detected()`
- `clear_interrupt()`
