# Sparkfun RV8803 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Rv8803 Ex1 Set Time
`qwiic_rv8803_ex1_set_time.py`

This example shows how to set the time on the RTC to a custom time.

The key methods showcased by this example are: 
- `set_time()`
- `update_time()`
- `string_date_usa()`
- `string_time()`

## Qwiic Rv8803 Ex2 Print Time
`qwiic_rv8803_ex2_print_time.py`

This example shows how to print the time on the RTC.

## Qwiic Rv8803 Ex3 Set Hundredths
`qwiic_rv8803_ex3_set_hundredths.py`

This example shows how to set the hundredths register through the I2C interface.
 The hundredths register will be reset to 0 every time the EVI button is pressed.

The key methods showcased by this example are: 
- `set_evi_event_capture()`
- `set_evi_debounce_time()`
- `get_interrupt_flag()`
- `set_hundredths_to_zero()`
- `clear_interrupt_flag()`
- `get_hundredths()`

## Qwiic Rv8803 Ex4A Alarm Interrupt
`qwiic_rv8803_ex4a_alarm_interrupt.py`

This example shows how to set an alarm and make the RTC generate an interrupt when the clock time matches the alarm time.
 The INT pin will be high (~3.3V) until real time matches alarm time when it will go low (~0V).

The key methods showcased by this example are: 
- `disable_all_interrupts()`
- `clear_all_interrupt_flags()`
- `set_items_to_match_for_alarm()`
- `set_alarm_minutes()`
- `set_alarm_hours()`
- `set_alarm_weekday()`
- `enable_hardware_interrupt()`

## Qwiic Rv8803 Ex4B Countdown Interrupt
`qwiic_rv8803_ex4b_countdown_interrupt.py`

This example shows how to generate a periodic interrupt signal, 
 as well as show you how to calculate the proper set up values for your necessary time.

The key methods showcased by this example are: 
- `set_countdown_timer_frequency()`
- `set_countdown_timer_clock_ticks()`
- `set_countdown_timer_enable()`

## Qwiic Rv8803 Ex4C Periodic Interrupt
`qwiic_rv8803_ex4c_periodic_interrupt.py`

This example shows how to generate a periodic 1s interrupt pulse

The key methods showcased by this example are: 
- `set_periodic_time_update_frequency()`

## Qwiic Rv8803 Ex5 Timestamp
`qwiic_rv8803_ex5_timestamp.py`

This example shows how to get the timestamp of an event generated on the EVI pin, by a button press on the RTC.

The key methods showcased by this example are: 
- `string_timestamp()`


## Qwiic Rv8803 Ex6 Fine Tuning
`qwiic_rv8803_ex6_fine_tuning.py`

This example shows how to calibrate the RTC's oscillator to have it keep even more accurate time

The key methods showcased by this example are: 
- `set_calibration_offset()`
- `set_clock_out_timer_frequency()`

## Qwiic Rv8803 Ex7 Print Epoch
`qwiic_rv8803_ex7_print_epoch.py`

This example shows how to print the epoch time from the RTC.

The key methods showcased by this example are: 
- `get_epoch()`

## Qwiic Rv8803 Ex8 Set Epoch
`qwiic_rv8803_ex8_set_epoch.py`

This example shows how to set the epoch time for the RTC.
- `set_time_zone_quarter_hours()`
- `set_epoch()`
