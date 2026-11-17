# Sparkfun SCD4X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_scd4x_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Scd4X Ex1 Basic
This example prints the current CO2 level, relative humidity, and temperature in C.

The key methods showcased by this example are: 
- [read_measurement](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#affe3309dbe3da48d095edaa53a597ce9)
- [get_co2()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a97472da6c394561f24493550dc7cc8ba)
- [get_temperature()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a3e8ce1dbe5e629b64db82973d5707388)
- [get_humidity()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#abfa5cefdda548361967bcc4f74064e56)

## Qwiic Scd4X Ex2 Low Power
This example uses low-power measurements and 
 prints the current CO2 level, relative humidity, and temperature in C.

The key methods showcased by this example are: 
- [start_low_power_periodic_measurement()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a36784dce77ed07222fe0ef47cf6f9cbe)

## Qwiic Scd4X Ex3 Disable Auto Calibration
This example disables automatic calibration and 
 prints the current CO2 level, relative humidity, and temperature in C.

The key methods showcased by this example are: 
- [begin()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#ad182acc748274f81ff90d1a1663a31d1)

## Qwiic Scd4X Ex4 Skip Stop Periodic
This example skips the stop_periodic_measurement() call in begin() and 
 prints the current CO2 level, relative humidity, and temperature in C.

The key methods showcased by this example are: 
- [stop_periodic_measurement()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a5039de760a61e7292e9cd6dfcb6c73a9)

## Qwiic Scd4X Ex6 Signal Compensation
This example shows how to set the three signal compensation settings: 
 temperature offset, sensor altitude, and ambient pressure.

The key methods showcased by this example are: 
- [set_temperature_offset()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a636e06cc55a0abaf6999e19550f952f8)
- [set_sensor_altitude()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#aa50cf29659bbb7b8a3b17b1aca33d07f)
- [set_ambient_pressure()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#aeb20c3d3b5bccd7194935414bdcb6847)
- [get_serial_number()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a184a764f64b8da330bc5501246d32174)

## Qwiic Scd4X Ex7 Test And Reset
This example shows how to perform a self test and factory reset on the SCD4x sensor.

The key methods showcased by this example are: 
- [perform_self_test()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a22aacfc3b049bd5b85d8c96f60c50cee)
- [perform_factory_reset()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a0b0954bebeb0eee8d9a8cfb65a93d055)

## Qwiic Scd4X Ex8 Scd41 Single Shot
This example shows how to perform single-shot data acquisition on the SCD41 sensor.

The key methods showcased by this example are: 
- [measure_single_shot_rht_only()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a97bb442769a1b92d52266feff99e0912)

## Qwiic Scd4X Ex9 Sensor Type
This example determines and prints the device type then exits

The key methods showcased by this example are: 
- [get_feature_set_version()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a306a83ce051f77b0dda495947afcdd1d)
- [get_sensor_type()](https://docs.sparkfun.com/qwiic_scd4x_py/classqwiic__scd4x_1_1_qwiic_s_c_d4x.html#a4af997d91fe4d6d5f9e53259c6b51f19)


