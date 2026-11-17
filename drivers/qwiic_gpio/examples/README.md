# Sparkfun GPIO Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_gpio_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Gpio Ex1A Write
This script sets up a GPIO 0 as an output and toggles
   the output HIGH and LOW.
 
   This device sinks current. When an output is LOW then current will flow.

The key methods showcased by this example are:
- [pinMode()](https://docs.sparkfun.com/qwiic_gpio_py/classqwiic__gpio_1_1_qwiic_g_p_i_o.html#a88956a5327174e453c9f247ae7ea2a07)
- [digitalWrite()](https://docs.sparkfun.com/qwiic_gpio_py/classqwiic__gpio_1_1_qwiic_g_p_i_o.html#a4cd696748424967345528fabe4fc22fa)

## Qwiic Gpio Ex1B Write Port
This script flips all 8 outputs on and off every second.
- [pinModePort()](https://docs.sparkfun.com/qwiic_gpio_py/classqwiic__gpio_1_1_qwiic_g_p_i_o.html#a0f80b0d4eb2872e5bbdd1eefffcf04cc)
- [digitalWritePort()](https://docs.sparkfun.com/qwiic_gpio_py/classqwiic__gpio_1_1_qwiic_g_p_i_o.html#a52c93eb9bb28236c9b6fffe3456e2249)

## Qwiic Gpio Ex2A Read
This script allows the user to read a value from GPIO 0
- [digitalRead()](https://docs.sparkfun.com/qwiic_gpio_py/classqwiic__gpio_1_1_qwiic_g_p_i_o.html#a98403a1293a99ff4411cc6a4cca5e691)

## Qwiic Gpio Ex2B Read Port
This script allows the user to read the status of all 8 GPIO simultaneously
- [digitalReadPort()](https://docs.sparkfun.com/qwiic_gpio_py/classqwiic__gpio_1_1_qwiic_g_p_i_o.html#a6d86c74b1969a08272de93aeaeb128c5)

## Qwiic Gpio Ex3A Inversion
This script shows how to invert the input signal on a pin
- [invertPin()](https://docs.sparkfun.com/qwiic_gpio_py/classqwiic__gpio_1_1_qwiic_g_p_i_o.html#af3e28ee15c8bf6dd94d307f3d05c5430)

## Qwiic Gpio Ex3B Inversion Port
This script shows how to invert the input signal on multiple pins
- [invertPinPort()](https://docs.sparkfun.com/qwiic_gpio_py/classqwiic__gpio_1_1_qwiic_g_p_i_o.html#a9540c7dbd1b6b10191cf3f7aed9c91b1)


