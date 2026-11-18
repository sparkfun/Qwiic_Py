# Sparkfun MAX1704X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Max1704X Ex1 Basic
`qwiic_max1704x_ex1_basic.py`

This example will print the gauge's voltage and state-of-charge (SOC) readings

The key methods showcased by this example are: 
- `quick_start()`
- `set_threshold()`
- `get_voltage()`
- `get_soc()`
- `get_alert()`

## Qwiic Max1704X Ex4 Kitchen Sink
`qwiic_max1704x_ex4_kitchen_sink.py`

This example is an "everything-but-the-kitchen-sink" test of the MAX17048.

The key methods showcased by this example are: 
- `reset()`
- `get_id()`
- `get_version()`
- `set_valrt_max_volts()`
- `set_valrt_min_volts()`
- `enable_soc_alert()`
- `get_hibrt_act_thr()`
- `get_change_rate()`
- `is_voltage_high()`
- `is_voltage_low()`
- `is_low()`
- `is_change()`
- `is_hibernating()`