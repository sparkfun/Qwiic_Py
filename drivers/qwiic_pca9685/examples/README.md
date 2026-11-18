# SparkFun Qwiic PCA9685 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

## Example 1: Servo Sweep
`qwiic_pca9685_ex1_servo_sweep.py`

This example sets the PWM frequency to 50 Hz and sweeps the pulse on channel 0 between 1 ms and 2 ms, which moves a servo back and forth. For servo control in degrees, see the `pi_servo_hat` driver, which is built on this one.

The key methods showcased by this example are:

- `set_pre_scale()`
- `set_channel_word()`
