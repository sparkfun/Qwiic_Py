# Sparkfun VL53L5CX Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_vl53l5cx_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Vl53L5Cx Ex1 Distance Array
This example shows how to read all 64 distance readings at once.

The key methods showcased by this example are: 
- [set_resolution()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#adad58008079492b344dfb185356712a0)
- [start_ranging()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#a208a5daf1c6a3d9456cb4aabf8919048)
- [check_data_ready()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#adb068707740b83735e25f6e0011a43c8)
- [get_ranging_data()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#a8cd5bc1150b8fbf0b863d2da19cc3cdc)

The key methods 
## Qwiic Vl53L5Cx Ex3 Set Freq
This example shows how to increase output frequency.

 Default is 1Hz.
 Using 4x4, min frequency is 1Hz and max is 60Hz
 Using 8x8, min frequency is 1Hz and max is 15Hz

The key methods showcased by this example are: 
- [set_ranging_frequency_hz()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#a518cf2c80832cd963fe3a35b4d0c07e6)
- [get_ranging_frequency_hz()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#a2d433e02d043872b2803735d603a1797)

## Qwiic Vl53L5Cx Ex6 Settings
This example shows how to read all 64 distance readings at once.

The key methods showcased by this example are: 
- [set_ranging_mode()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#a67c9860665d68334811fbee4189ece02)
- [set_power_mode()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#a48ae06f9f71185aacaf3abaa81b01c08)
- [set_integration_time_ms()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#a0e9827a98d91dd901577d4a162d64805)
- [set_sharpener_percent()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#ab638b7b3733319cf5f5701bf4ed5c5a8)
- [set_target_order()](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#a363e3822659196dad9f819cd36a5e552)

## Qwiic Vl53L5Cx Ex8 Set Address
This example shows how to set a custom address for the VL53L5CX.

The key methods showcased by this example are: 
- [set_i2c_address](https://docs.sparkfun.com/qwiic_vl53l5cx_py/classqwiic__vl53l5cx_1_1qwiic__vl53l5cx_1_1_qwiic_v_l53_l5_c_x.html#a0d23ae9ca12396bb73223995ec02ccec)
