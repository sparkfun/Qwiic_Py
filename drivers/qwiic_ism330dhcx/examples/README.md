# Sparkfun ISM330DHCX Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_ism330dhcx_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Ism330Dhcx Ex1 Basic
This example shows the basic settings and functions for retrieving accelerometer and gyroscopic data.


The key methods showcased by this example are: 
- [set_device_config()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#a5ba69284667f06d4dbbd3d01c4a9fc8a)
- [set_block_data_update()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#a3d8f3ba0b87b7e0fb901661bbd4bba86)
- [set_accel_data_rate()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#a9c1abd32c9418cfa39917bc88fb03a73)
- [set_accel_full_scale()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#aa02b5fa37a3fe246adf291ae77fbb070)
- [set_gyro_data_rate()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#a7e2dbf1bc5850d2ab6dc8c47b2b2aedc)
- [set_gyro_full_scale()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#ac66397d03b0fdcdd8e670e0c9c40c59e)
- [set_accel_filter_lp2()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#a0ad9375359d5bd08e2ae7285a70f80e9)
- [set_accel_slope_filter()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#aaab379457281cd78f003037cd90702eb)
- [set_gyro_filter_lp1()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#a341196c206d587e1d4d9f0de099b7a41)
- [set_gyro_lp1_bandwidth()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#a27c3af2665b190bdcc1b3c6093ac5c03)
- [check_status()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#ab2a7206894cb656f338bfa5032b288ae)
- [get_accel()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#a968fbe707a59a03772067be5a07c6559)
- [get_gyro()](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html#a45ea85e6f3c2fa08904b8a50535bd13b)
