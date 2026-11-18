# Sparkfun ADS1015 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Ads1015 Ex1 Read Basic
`qwiic_ads1015_ex1_read_basic.py`

This example shows how to output ADC values on one single-ended channel (A3).
   *at default gain setting of 1 (and 3.3V VCC), 0-2V will read 0-2047.
   *anything greater than 2V will read 2047.

The key methods showcased by this example are: 
- `get_single_ended()`

## Qwiic Ads1015 Ex2 Change Gain
`qwiic_ads1015_ex2_change_gain.py`

This example shows how to output ADC values on one single-ended channel (A3) with a PGA GAIN of 1. 
   At this gain setting (and 3.3V VCC), 0-3.3V will read 0-1652.

   Other possible gain settings are as follows. 
   Note, changing the gain effects the range of the sensor (aka the max and min voltages it can read).
   Also note, to avoid damaging your ADC, never exceed VDD (3.3V for a qwiic system).

   CONFIG_PGA_TWO_THIRDS  +/- 6.144v
   CONFIG_PGA_1          +/- 4.096v (used in this example)
   CONFIG_PGA_2          +/- 2.048v
   CONFIG_PGA_4          +/- 1.024v
   CONFIG_PGA_8          +/- 0.512v
   CONFIG_PGA_16         +/- 0.256v

The key methods showcased by this example are: 
- `set_gain()`

## Qwiic Ads1015 Ex3 Address
`qwiic_ads1015_ex3_address.py`

This example shows how to output ADC values on one single-ended channel (A3) with a NON-default address.
   This is useful if you'd like to connect multiple ADS1015 boards on the same bus.
   Note, you must cut a trace on the product hardware and solder to "0x49" jumper for this code to work.

## Qwiic Ads1015 Ex4 Differential
`qwiic_ads1015_ex4_differential.py`

This example shows how to output ADC values on one differential input between A0 and A1.
   *at default gain setting of 1 (and 3.3V VCC), 0-2V will read 0-2047.
   *anything greater than 2V will read 2047.

The key methods showcased by this example are: 
- `get_differential()`

## Qwiic Ads1015 Ex6 Display Millivolts
`qwiic_ads1015_ex6_display_millivolts.py`

This example shows how to output ADC values on one single-ended channel (A3).
   It will also print out the voltage of the reading in mV.
   Note, the conversion multiplier needs to be corrected for gain settings,
   And this is done automatically in the library, using `get_multiplier()`,
   as shown below.
  
   *at gain setting of 1, like in this example (and 3.3V VCC), 0-3.3V will read 0-1652.

The key methods showcased by this example are: 
- `get_multiplier()`

## Qwiic Ads1015 Ex7 Multi Channel
`qwiic_ads1015_ex7_multi_channel.py`

This example shows how to output ADC values on multiple channels.
  
   It is based on the example provided by \@StefanThoresson in Issue 6:
   https://github.com/sparkfun/SparkFun_ADS1015_Arduino_Library/issues/6
   Thank you Stefan.
  
   We used this example to determine the delay values for `conversion_delay()`.

The key methods showcased by this example are: 
- `get_single_ended_millivolts()`
- `get_differential_millivolts()`


