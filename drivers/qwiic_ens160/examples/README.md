# Sparkfun ENS160 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_ens160_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Ens160 Ex1 Basic
This example shows basic data retrieval from the SparkFun Indoor Air Quality Sensor - ENS160.

The key methods showcased by this example are: 
- [set_operating_mode()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#a3aae69c3519a68f347308d4514a2b2a7)
- [get_flags()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#ade5bb0be558e2c204eb988dc1edc9e5b)
- [check_data_status()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#a131e811cac196d9642006cf2d7a7586a)
- [get_aqi()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#acbb117dac87a40058e1a96a8762268b0)
- [get_tvoc()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#ab5df698fbfcbcdd748deeea875a2c9fb)
- [get_eco2()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#a79c612e0d24eb26e46ec0010d9d3ead3)

## Qwiic Ens160 Ex4 Bme280 Temp Rh Compensation
This example shows how to give the ENS160 Temperature and Relative Humidity
  Data for compensation with the BME280. Note that the values that are given for compensation are not
  populated in their registers until the Air Quality Sensor is set to "Standard" operation
  and when data is ready (i.e. the data ready bit is set). Also note that there will be some 
  rounding of the temperature and relative humidity values when they're given to the sensor
  and again when they're read back.
 
 SparkFun Environmental Combo Breakout: https://www.sparkfun.com/products/22858
 SparkFun Atmospheric Sensor Breakout: https://www.sparkfun.com/products/15440

The key methods showcased by this example are: 
- [set_temp_compensation_celsius()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#a0e1cb111f595afe99eb6ce027e7f0ae6)
- [set_rh_compensation()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#ae1604144bbbae30bdc85f8f7c883192c)
- [get_rh()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#a2891de82df6ff1b0ae112265e57fec04)
- [get_temp_celsius()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#a12b48dc635ead9a5d1eb305d98665d1b)

## Qwiic Ens160 Ex6 Burn In
This example demonstrates the warm up phase of the ENS160. After the "burn-in" phase 
  the readings from the ENS160 will be more accurate. Before any data is given, the  
  the sensor waits for the status flag to return "Initial Start Up" or "Normal Operation".
  This time take approximately three minutes.

## Qwiic Ens160 Ex7 Raw Resistance
This example retreieves the raw resistance of the plates. This would be used
  in the case that you want to process these values yourself.

The key methods showcased by this example are: 
- [get_raw_resistance()](https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#a664f4c1467dda038f4b854e8402b0ead)

