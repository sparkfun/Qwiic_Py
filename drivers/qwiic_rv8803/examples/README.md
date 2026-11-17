# Sparkfun RV8803 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_rv8803_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Rv8803 Ex1 Set Time
This example shows how to set the time on the RTC to a custom time.

The key methods showcased by this example are: 
- [set_time()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a8a90178f4d99406a43ab31c30196acfb)
- [update_time()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a1b71285144f74069382eb4227ec31a92)
- [string_date_usa()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a1a8167a26358490f19e7c0f2745aa979)
- [string_time()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a1a8167a26358490f19e7c0f2745aa979)

## Qwiic Rv8803 Ex2 Print Time
This example shows how to print the time on the RTC.

## Qwiic Rv8803 Ex3 Set Hundredths
This example shows how to set the hundredths register through the I2C interface.
 The hundredths register will be reset to 0 every time the EVI button is pressed.

The key methods showcased by this example are: 
- [set_evi_event_capture()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a71cf4e9b491541fc4768349c27841f7d)
- [set_evi_debounce_time()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a86866190ba6a9e3d18a89eaad1529c01)
- [get_interrupt_flag()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#ae392f371da2c8cc319a3cb1badf4d463)
- [set_hundredths_to_zero()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#aecea8d2698633ea1e4908277843db937)
- [clear_interrupt_flag()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a3d07d63054893ddda246522f0499a3a2)
- [get_hundredths()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#aba051f248b830ea3d70f4d007b560be7)

## Qwiic Rv8803 Ex4A Alarm Interrupt
This example shows how to set an alarm and make the RTC generate an interrupt when the clock time matches the alarm time.
 The INT pin will be high (~3.3V) until real time matches alarm time when it will go low (~0V).

The key methods showcased by this example are: 
- [disable_all_interrupts()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a71b2cb30eae38f6726d6ab44f839a526)
- [clear_all_interrupt_flags()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#aeeec8216ba4e6d5448cee464b30d843d)
- [set_items_to_match_for_alarm()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a5e395ae49076eaf4d93de90f6e9f6356)
- [set_alarm_minutes()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a1b25b746111d409976070c2c06d22108)
- [set_alarm_hours()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a818b13e1b091bfdb1cc877160fddc405)
- [set_alarm_weekday()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a3f1ee8e7e204caa4699dcfcc5c935d38)
- [enable_hardware_interrupt()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a4d12980c89fece83258b5c42d4f36391)

## Qwiic Rv8803 Ex4B Countdown Interrupt
This example shows how to generate a periodic interrupt signal, 
 as well as show you how to calculate the proper set up values for your necessary time.

The key methods showcased by this example are: 
- [set_countdown_timer_frequency()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a825f5a892174dd9e5deb65ef3754b150)
- [set_countdown_timer_clock_ticks()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#ad91191351105a98a120de818de44fd70)
- [set_countdown_timer_enable()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#aa1c25f15930731273a06da3ddd1faac1)

## Qwiic Rv8803 Ex4C Periodic Interrupt
This example shows how to generate a periodic 1s interrupt pulse

The key methods showcased by this example are: 
- [set_periodic_time_update_frequency()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a974b76899aeb21a4a6ebd78d59df006c)

## Qwiic Rv8803 Ex5 Timestamp
This example shows how to get the timestamp of an event generated on the EVI pin, by a button press on the RTC.

The key methods showcased by this example are: 
- [string_timestamp()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a8a6a0115b6979b126da3a0fe2c5d5d1f)


## Qwiic Rv8803 Ex6 Fine Tuning
This example shows how to calibrate the RTC's oscillator to have it keep even more accurate time

The key methods showcased by this example are: 
- [set_calibration_offset()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a79e8c692c9786d08e247a839bfaef8c0)
- [set_clock_out_timer_frequency()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#aa39d189631478b5ec95366dbb72177a2)

## Qwiic Rv8803 Ex7 Print Epoch
This example shows how to print the epoch time from the RTC.

The key methods showcased by this example are: 
- [get_epoch()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#ac883dd3e0f56e3c8ea62dd26440fffcc)

## Qwiic Rv8803 Ex8 Set Epoch
This example shows how to set the epoch time for the RTC.
- [set_time_zone_quarter_hours()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a662cdc9ff0facd485cfe60a6987523e6)
- [set_epoch()](https://docs.sparkfun.com/qwiic_rv-8803_py/classqwiic__rv8803_1_1_qwiic_r_v8803.html#a5409283be629acb71e5e13dc3b04f75c)
