# Sparkfun VL53L1X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_vl53l1x_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example1 Read Distance
This example prints the distance to an object. If you are getting weird
readings, be sure the vacuum tape has been removed from the sensor.

The key methods showcased by this example are: 
- [sensor_init()](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html#a6247a075a2485d26b5e92ee206bd0d80)
- [start_ranging()](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html#a9e1ca7a1d6d6eb629c5987f6a13cc2c5)
- [get_distance()](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html#a481bdfe2107fcaa449a0a38bc6ba7947)
- [stop_ranging()](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html#a014aacbfdc6ed8f61c495dcc151b5aad)

## Example2 Set Distance Mode
This example configures the sensor to short distance mode and then
prints the distance to an object. If you are getting weird readings,
be sure the vacuum tape has been removed from the sensor.

The key methods showcased by this example are: 
- [set_distance_mode()](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html#a1aac43e830b9df0c84d581c306de498c)

## Example3 Status And Rate
This example configures the sensor to short distance mode and then
prints the distance to an object. The output also includes a
running average of the last 10 readings along with some statistics,
like signal rate and frequency (of the measurements).

If you are getting weird readings, be sure the vacuum tape has been
removed from the sensor.

The key methods showcased by this example are: 
- [get_signal_rate()](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html#a549ebc6209239d6883ca15dea441acaf)
- [get_range_status()](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html#aea9be5b36fa5459542276c4cfbdd9306)

## Example4 Set Intermeasurement Period
This example configures the inter-measurement period of the sensor
and then prints the distance to an object. If you are getting weird
readings, be sure the vacuum tape has been removed from the sensor.

The key methods showcased by this example are: 
- [set_inter_measurement_in_ms()](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html#a757a1d8d2c5631c1a8aef49d694da912)
- [get_inter_measurement_in_ms()](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html#aa3188f1f9bb914a6675ff47b5b1f456c)
