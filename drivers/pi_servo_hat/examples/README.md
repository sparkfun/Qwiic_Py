# SparkFun Pi Servo HAT Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

> [!NOTE]
> Many cheap servo motors indicate incorrect ranges of rotation in their datasheets. Often it takes a bit of experimentation to determine the true ranges of a servo. When in doubt, disconnecting the servo and hooking an oscilloscope or logic analyzer to the PWM signal pin of the Pi Servo HAT is a good way to check that you are delivering the PWM signal you would expect to your servo. This is helpful to trace any issues to either the Pi Servo HAT hardware/software or to the servo itself. If your servo needs pulses other than 1 ms to 2 ms for its full range, pass them as `PiServoHAT(min_pt=..., max_pt=...)` or call `set_pulse_time()`.

## Example 1: Full Sweep 90 Degree Servo
`pi_servo_hat_ex1_full_sweep_90_deg_servo.py`

This example should be used with a 90 degree (range of rotation) servo on channel 0 of the Pi Servo HAT. It sweeps the servo the full 90 degrees.

The extended code (commented out) at the end of the example could be used to test the full range of the servo motion. However, users should be wary as they can damage their servo by giving it a position outside the standard range of motion.

The key methods showcased by this example are:

- `begin()`
- `restart()`
- `move_servo_position()`

## Example 2: Full Sweep 180 Degree Servo
`pi_servo_hat_ex2_full_sweep_180_deg_servo.py`

This example should be used with a 180 degree (range of rotation) servo on channel 0 of the Pi Servo HAT. It sweeps the servo the full 180 degrees.

The extended code (commented out) at the end of the example could be used to test the full range of the servo motion. However, users should be wary as they can damage their servo by giving it a position outside the standard range of motion.

The key methods showcased by this example are:

- `move_servo_position()`

## Example 3: Get Position 180 Degree Servo
`pi_servo_hat_ex3_get_position_180_deg_servo.py`

This example should be used with a 180 degree (range of rotation) servo on channel 0 of the Pi Servo HAT. It sweeps the servo forward and back while printing the estimated servo position.

The key methods showcased by this example are:

- `get_servo_position()`

## Example 4: Change PWM Frequency 180 Degree Servo
`pi_servo_hat_ex4_change_pwm_frequency_180_deg_servo.py`

This example should be used with a 180 degree (range of rotation) servo on channel 0 of the Pi Servo HAT. It sweeps the servo at PWM frequencies of 50, 100 and 200 Hz while printing the estimated servo position.

The key methods showcased by this example are:

- `set_pwm_frequency()`
