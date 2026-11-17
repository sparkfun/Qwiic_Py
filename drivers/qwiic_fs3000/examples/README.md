# Sparkfun FS3000 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_fs3000_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Fs3000 Ex1 Basic
Read values of air velocity from the FS3000 sensor, print them to terminal.
   Prints raw data, m/s and mph.
   Note, the response time on the sensor is 125ms.

The key methods showcased by this example are:
- [set_range()](https://docs.sparkfun.com/qwiic_fs3000_py/classqwiic__fs3000_1_1_qwiic_f_s3000.html#a55e14e5f8a49547b3586305649805fbb)
- [read_raw()](https://docs.sparkfun.com/qwiic_fs3000_py/classqwiic__fs3000_1_1_qwiic_f_s3000.html#a37e48e5e89238b7eb714eb387c64dc64)
- [read_meters_per_second()](https://docs.sparkfun.com/qwiic_fs3000_py/classqwiic__fs3000_1_1_qwiic_f_s3000.html#a75fded05b28441fff37264fc3af637b6)
- [read_miles_per_hour()](https://docs.sparkfun.com/qwiic_fs3000_py/classqwiic__fs3000_1_1_qwiic_f_s3000.html#ace67b03c85a75a609621596d492498b4)

