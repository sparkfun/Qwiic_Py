# Sparkfun TMP117 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_tmp117_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Tmp117 Ex1 Basic
This script configures the TMP117 temperature sensor and prints the
 temperature in degrees celsius and fahrenheit with a 500ms delay for
 easier readings.

The key methods showcased by this example are: 
- [data_ready()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#a08e2872e73521ce3d651849c4df11d1f)
- [read_temp_c()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#a7b34b49d15b795da1e5f0a12fa977d03)
- [read_temp_f()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#a07a93484e8cdc07518a98918983aa696)

## Qwiic Tmp117 Ex2 Alert Statuses
This script sets the TMP117 temperature sensor's high limit,
 low limit, and alert function mode. Once set, we read the 
 temperature in C and checks alert status. If we are outside
 of the boundary, we will output a message indicating
 that we are beyond the limit.

The key methods showcased by this example are: 
- [set_high_limit()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#ae711118a3c8150507799d2c9aa820590)
- [set_low_limit()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#a56ad4da956c8fae7d535351a5d19ed00)
- [get_alert_function_mode()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#aec3efc2e9db564fd13441cc50ee97f59)
- [get_high_low_alert()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#a5be302ec6237abaeefaca002f95d2ad0)

## Qwiic Tmp117 Ex3 Set Offset Temp
This script configures the TMP117 temperature sensor and allows the user to
 set the offset temperature for System Correction.

The key methods showcased by this example are: 
- [get_temperature_offset()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#af7c9572d7ac3428beb230a87f8425055)
- [set_temperature_offset()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#ace97f0d6c94c80952fabcff85b556916)

## Qwiic Tmp117 Ex4 Set Conv Mode
This script can get and set the conversion mode to
 Continuous Conversion, Shutdown, or One-Shot

The key methods showcased by this example are: 
- [set_continuous_conversion_mode()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#a125649adcdc429e6d95fb97d7cce15fa)
- [set_shutdown_mode()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#a12d7bffb0c9a3a704fed3c37a027e303)
- [set_one_shot_mode()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#ad516dd76974b23d260be239f4d256c84)

## Qwiic Tmp117 Ex5 Set Alert Limits
This script can set and get the Alert Function Mode, Low Temperature 
 Limit, and High Temperature Limit for the sensor. These limits can
 be set within +/- 256°C. When the temperature goes above/below the 
 specified temperature limits, it will cause the alert pins to go
 high. To access these registers, please reference Example 2: Alert Statuses.

The key methods showcased by this example are: 
- [set_low_limit()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#a56ad4da956c8fae7d535351a5d19ed00)
- [set_high_limit()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#ae711118a3c8150507799d2c9aa820590)
- [set_alert_function_mode()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#aec3efc2e9db564fd13441cc50ee97f59)

## Qwiic Tmp117 Ex6 Set Conv Cycle
This script can set and get the Conversion Times in Continuous Conversion mode
 for the Sensor. A chart for the averaging modes and the conversion times can
 be found in the table below or in the Datasheet on page 27 table 7.

The key methods showcased by this example are: 
- [set_conversion_average_mode()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#ad541fac2271595329b1c9842deb83701)
- [set_conversion_cycle_bit()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#a1542dfbf7b5d5a2f5af1960b865fbbf5)

## Qwiic Tmp117 Ex7 Set Address
This script allows the user to change the address of the device and to
 change the Wire port for I2C Communications. The address can be physically
 changed with an external jumper on the back of the sensor. 
 
 See the "Address Select" section in the hookup guide for more information:
 https://learn.sparkfun.com/tutorials/qwiic-tmp117-high-precision-digital-temperature-sensor-hookup-guide

The key methods showcased by this example are: 
- [get_address()](https://docs.sparkfun.com/qwiic_tmp117_py/classqwiic__tmp117_1_1_qwiic_t_m_p117.html#ae32e838b7f1254ee362c799a5d636250)
