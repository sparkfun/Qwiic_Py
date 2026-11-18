import qwiic_pca9685
import qwiic_i2c
import sys


print("\nSparkFun PCA9685 Example 1\n")
my_pwm = qwiic_pca9685.QwiicPCA9685()

if not my_pwm.is_connected():
	print("The Qwiic PCA9685 device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

my_pwm.begin()

# Sets PWM Frequency to 50 Hz
my_pwm.set_pre_scale(50)

# Sets start time of PWM pulse on Channel 0 to 0s
my_pwm.set_channel_word(0, 1, 0)

while True:
	# Increments start time of PWM pulse on Channel 0 to i (1ms to 2ms)
	for i in range(205, 410):
		my_pwm.set_channel_word(0, 0, i)
		# Delay .05 s
		qwiic_i2c.delay_ms(50)

	# Decrements start time of PWM pulse on Channel 0 to i (2ms to 1ms)
	for i in range(410, 205, -1):
		my_pwm.set_channel_word(0, 0, i)
		# Delay .05 s
		qwiic_i2c.delay_ms(50)

	qwiic_i2c.delay_ms(1000)
