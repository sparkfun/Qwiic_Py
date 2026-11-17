# Sparkfun RFID Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_rfid_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Rfid Ex1 Gettag
Basic example that reads tag and prints ID and the time requested
 when prompted by user.

The key methods showcased by this example are: 
- [get_tag()](https://docs.sparkfun.com/qwiic_rfid_py/classqwiic__rfid_1_1_qwiic_r_f_i_d.html#a858a28925b9447d09df686b9308b662f)
- [get_prec_req_time()](https://docs.sparkfun.com/qwiic_rfid_py/classqwiic__rfid_1_1_qwiic_r_f_i_d.html#ad4e902d0810f503d899f7c254d2217ed)

## Qwiic Rfid Ex2 Getalltags
Basic example that reads RFID tags and prints all the IDs and the 
 times requested in the buffer when prompted by user.
 
 The key methods showcased by this example are: 
- [get_all_tags()](https://docs.sparkfun.com/qwiic_rfid_py/classqwiic__rfid_1_1_qwiic_r_f_i_d.html#aec0e56d2085a0b8f8f563fb25321106a)
- [get_all_prec_times()](https://docs.sparkfun.com/qwiic_rfid_py/classqwiic__rfid_1_1_qwiic_r_f_i_d.html#a2c36244592a29e2ddae0177db8230fee)

## Qwiic Rfid Ex3 Changei2Caddress
Example that takes user input to change the I2C address of Qwiic RFID
 
 The key methods showcased by this example are: 
- [change_address()](https://docs.sparkfun.com/qwiic_rfid_py/classqwiic__rfid_1_1_qwiic_r_f_i_d.html#aa9764cbe6a69f7d9f08b504c178c05e5)