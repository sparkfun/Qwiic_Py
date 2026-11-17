# Sparkfun PiServoHat Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/piservohat_py/issues). 

> [!NOTE]
> Many cheap servo motors indicate incorrect ranges of rotation in their datasheets. Often it takes a bit of experimentation to determine the true ranges of a servo. When in doubt, disconnecting the servo and hooking an oscilliscope or logic analyzer to the PWM signal pin of the PiServoHat is a good way to check that you are delivering the PWM signal you would expect to you servo. This is helpful to trace any issues to either the use of the PiServoHat hardware/software or to the servo itself. 

## Ex1 Full Sweep With 90 Deg Servo
This example should be used with a 90 degree (range of rotation) servo
on channel 0 of the Pi Servo Hat. It sweeps the servo the full 90 degrees.

The extended code (commented out), at the end of the example could be
used to test the full range of the servo motion. However, users should
be wary as they can damage their servo by giving it a position outside
the standard range of motion.

The key methods showcased by this example are:
- [restart()](https://docs.sparkfun.com/piservohat_py/classpi__servo__hat_1_1_pi_servo_hat.html#a2b0a7d33628b812ae6f7cdf127dd022c)
- [move_servo_position()](https://docs.sparkfun.com/piservohat_py/classpi__servo__hat_1_1_pi_servo_hat.html#aef748fe65cad023d697080799bcba81a)

## Ex2 Full Sweep With 180 Deg Servo
This example should be used with a 180 degree (range of rotation) servo
on channel 0 of the Pi Servo Hat. It sweeps the servo the full 180 degrees.

The extended code (commented out), at the end of the example could be
used to test the full range of the servo motion. However, users should
be wary as they can damage their servo by giving it a position outside
the standard range of motion.

## Ex3 Get Position 180 Deg Servo
This example should be used with a 180 degree (range of rotation) servo
on channel 0 of the Pi Servo Hat. It sweeps the servo forward and back while printing the current servo position.

The extended code (commented out), at the end of the example could be
used to test the full range of the servo motion. However, users should
be wary as they can damage their servo by giving it a position outside
the standard range of motion.

The key methods showcased by this example are:
- [get_servo_position()](https://docs.sparkfun.com/piservohat_py/classpi__servo__hat_1_1_pi_servo_hat.html#a903e801c1693ea63fde33a23174183ac)

## Ex4 Change PWM Frequency 180 Deg Servo
This example should be used with a 180 degree (range of rotation) servo
on channel 0 of the Pi Servo Hat.

The extended code (commented out), at the end of the example could be
used to test the full range of the servo motion. However, users should
be wary as they can damage their servo by giving it a position outside
the standard range of motion

The key methods showcased by this example are:
- [set_pwm_frequency()](https://docs.sparkfun.com/piservohat_py/classpi__servo__hat_1_1_pi_servo_hat.html#a1dbb53c9f4d0b752c518d5b7e7e3ee1b)
