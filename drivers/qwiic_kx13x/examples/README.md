# Sparkfun KX13X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_kx13x_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Kx13X Ex1
Simple example for the Qwiic KX132/4 Accelerometer

The key methods showcased by this example are: 
- [software_reset()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a16a4cedff07e87cf12db5af9c44dbffc)
- [enable_accel()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#ac9d0fa05a1be1f21e6783c3f65eb71f4)
- [set_range()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a868630ae1b7001d11c55f20b535503b8)
- [enable_data_engine()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a71f267dfeb12ac3a9b617b6cf0561265)
- [enable_accel()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#ac9d0fa05a1be1f21e6783c3f65eb71f4)
- [data_ready()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a5deb5967c8598941d1c59bde224bbe41)
- [get_accel_data()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x134.html#a0b9a7adf9b0b08a49d94df176105b19a)

## Qwiic Kx13X Ex3
This example shows both how to setup the buffer but also how to route the buffer's
  interrupt to a physical interrupt pin.

The key methods showcased by this example are: 
- [enable_buffer_and_interrupt()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a1b3d8b6d2bb75e9001e0293cefa10bc2)
- [enable_phys_interrupt()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#af82d8d707e161c27ef43b02f912a49bc)
- [route_hardware_interrupt()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#ad721eece0ba48479e4d3e13a9ca92f8e)
- [set_buffer_operation_and_resolution()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a494d65f169313f87f99a613cfc0e423b)
- [get_sample_level()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a6072fc487cb73a8ca77a592e8b9097dc)
- [get_raw_accel_buffer_data()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#ab422a9616193c24c72dd6141e1d43d49)
- [conv_accel_data()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x134.html#a33896e31955a98e207a8aad03858935f)

## Qwiic Kx13X Ex4
Example for the Qwiic KX132/4 Accelerometer that shows the how to enable the tap interrupts.

The key methods showcased by this example are: 
- [enable_tap_engine()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a29c559f07627b5416bfb16af1cacd0e8)
- [tap_detected()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a465b78834be9af826f549ef5f679dfc6)
- [unknown_tap()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#afd18ce39a238afd075654ab8a98a2a1b)
- [double_tap_detected()](https://docs.sparkfun.com/qwiic_kx13x_py/classqwiic__kx13x_1_1_qwiic_k_x13_x_core.html#a3861df73b526c9cc39ee841e2d23c0ec)
