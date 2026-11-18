# SparkFun Qwiic Relay Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Example 1: Single
`qwiic_relay_ex1_single.py`

This example shows the basics of using the single relay.

The key methods showcased by this example are:

- `set_relay_on()`
- `set_relay_off()`
- `get_relay_state()`

## Example 2: Dual
`qwiic_relay_ex2_dual.py`

This example shows the basics of using the dual solid state relay, and how to pass a relay number to `get_relay_state()`.

The key methods showcased by this example are:

- `set_relay_on()`
- `set_relay_off()`
- `get_relay_state()`

## Example 3: Quad
`qwiic_relay_ex3_quad.py`

This example shows the basics of using the quad relays.

The key methods showcased by this example are:

- `set_all_relays_on()`
- `set_all_relays_off()`

## Example 4: PWM
`qwiic_relay_ex4_pwm.py`

This example shows how to set and get the slow PWM value. Slow PWM works only on the solid state relays.

The key methods showcased by this example are:

- `set_slow_pwm()`
- `get_slow_pwm()`
