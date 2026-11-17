# Sparkfun BMP581 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_bmp581_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Bmp581 Ex1 Basic
This example demonstrates how to read basic temperature and pressure values from the Qwiic BMP581

The key methods showcased by this example are: 
- [get_sensor_data()](https://docs.sparkfun.com/qwiic_bmp581_py/classqwiic__bmp581_1_1_qwiic_b_m_p581.html#aed22ff35c9df4da2d8bc29291a166de4)

## Qwiic Bmp581 Ex4 Filtering
This example demonstrates how to use filtering to smooth temperature and pressure measurements.

The key methods showcased by this example are: 
- [set_iir_config()](https://docs.sparkfun.com/qwiic_bmp581_py/classqwiic__bmp581_1_1_qwiic_b_m_p581.html#af4dfb8b76838e64978b79ed5db2ecddd)

## Qwiic Bmp581 Ex5 Oversampling
This example demonstrates how to use oversampling to increase resolution and decrease noise
 in temperature and pressure measurements.

The key methods showcased by this example are: 
- [set_osr_multipliers()](https://docs.sparkfun.com/qwiic_bmp581_py/classqwiic__bmp581_1_1_qwiic_b_m_p581.html#a2f2a330312815ba96e4d16bb8e4164d8)
- [set_odr_frequency()](https://docs.sparkfun.com/qwiic_bmp581_py/classqwiic__bmp581_1_1_qwiic_b_m_p581.html#a17f3e1e5858ad227544657c99d329df7)
- [get_osr_odr_eff()](https://docs.sparkfun.com/qwiic_bmp581_py/classqwiic__bmp581_1_1_qwiic_b_m_p581.html#ad539356773b977a0cbdf7420a18acc17)

## Qwiic Bmp581 Ex7 Nvm
This example demonstrates how to read basic temperature and pressure values from the Qwiic BMP581

The key methods showcased by this example are: 
- [nvm_write()](https://docs.sparkfun.com/qwiic_bmp581_py/classqwiic__bmp581_1_1_qwiic_b_m_p581.html#a5899549ac6931904e6b8335deda5e113)
- [nvm_read()](https://docs.sparkfun.com/qwiic_bmp581_py/classqwiic__bmp581_1_1_qwiic_b_m_p581.html#a4ae37bf216b35247b8241e7759ac9c58)

## Qwiic Bmp581 Ex8 Low Power
This example demonstrates how to read basic temperature and pressure values from the Qwiic BMP581

The key methods showcased by this example are: 
- [set_power_mode()](https://docs.sparkfun.com/qwiic_bmp581_py/classqwiic__bmp581_1_1_qwiic_b_m_p581.html#a8ecd3e9d87f62ff4cc948d5120a35309)

