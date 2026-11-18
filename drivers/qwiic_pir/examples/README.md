# Sparkfun Qwiic PIR Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Each example waits 30 seconds for the PIR to stabilize before it starts reading.

## Example 1: Raw Reading
`qwiic_pir_ex1_raw_reading.py`

This example prints whether the PIR currently sees an object, using the raw (not debounced) PIR output.

The key methods showcased by this example are: 
- `begin()`
- `raw_reading()`

## Example 2: Debounced Events
`qwiic_pir_ex2_debounced_events.py`

This example waits for a debounced detect or remove event, prints it, and then clears the event bits.

The key methods showcased by this example are: 
- `available()`
- `object_detected()`
- `object_removed()`
- `clear_event_bits()`

## Example 3: Queue Timestamps
`qwiic_pir_ex3_queue_timestamps.py`

This example reads the detect and remove queues and prints how long ago the first and last events happened.

The key methods showcased by this example are: 
- `is_detected_queue_empty()`, `time_since_last_detect()`, `time_since_first_detect()`
- `is_removed_queue_empty()`, `time_since_last_remove()`, `time_since_first_remove()`

## Example 4: Pop Queue
`qwiic_pir_ex4_pop_queue.py`

This example pops the oldest timestamp off the detect or remove queue when you type `d` or `r`.

The key methods showcased by this example are: 
- `pop_detected_queue()`
- `pop_removed_queue()`

## Example 5: Change I2C Address
`qwiic_pir_ex5_change_i2c_address.py`

This example asks for a new I2C address, changes the PIR to it, and checks that the PIR answers at the new address.

The key method showcased by this example is `set_i2c_address()`
