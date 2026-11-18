# Sparkfun HUSKYLENS Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

## Qwiic HuskyLens Ex1 Basic Readings
`qwiic_huskylens_ex1_basic_readings.py`

This example shows how to get data from the HuskyLens. Set the HuskyLens to any algorithm, point it at something it can recognize, and this example will print the details of what it sees.

The key methods showcased by this example are: 
- `get_objects_of_interest()`
- `get_lines_of_interest()`

## Qwiic HuskyLens Ex2 Learn
`qwiic_huskylens_ex2_learn.py`

This example shows how to learn new objects with the HuskyLens over I2C rather than using the buttons on the device. This gives some more flexibility in how objects are learned, such as being able to set the names and ID values.

The key methods showcased by this example are: 
- `set_algorithm()`
- `forget()`
- `wait_for_objects_of_interest()`
- `wait_for_lines_of_interest()`
- `learn_new()`
- `learn_same()`
- `name_last()`

## Qwiic HuskyLens Ex3 Write To Screen
`qwiic_huskylens_ex3_write_to_screen.py`

This example shows how to write text to the screen of the HuskyLens.

The key methods showcased by this example are: 
- `write_to_screen()`
- `clear_screen()`
