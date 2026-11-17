# Sparkfun BUTTON Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_button_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Button Ex1 Buttonpress
Simple Example for the Qwiic Button. Checks whether the button is pressed and
 then prints its status.

The key methods showcased by this example are: 
    - [is_button_pressed()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#a4650881c1b1b92ae7f5136f85c8f7385)

## Qwiic Button Ex2 Ledon
Simple Example for the Qwiic Button. Turns on the button's built in LED 
 when pressed and prints status.

 The key methods showcased by this example are:
 - [LED_on()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#a782725413ccd408499c68e98a90de8da)
 - [LED_off()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#a336063d15fae188869bea17f28742950)

## Qwiic Button Ex3 Ledconfig
Simple Example for the Qwiic Button. Checks whether the button is pressed and
 and the LED pulses if it is.

 The key methods showcased by this example are:
 - [LED_config()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#abc191302e346c948db1afb240e4162db)

## Qwiic Button Ex4 Queueusage
Simple Example for the Qwiic Button. Shows how to use he FIFO Queue on the Qwiic Button.

 The key methods showcased by this example are:
 - [is_pressed_queue_empty()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#acbfa1c9c3a4e4d66db5bb7572899c346)
 - [time_since_last_press()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#a9b613cd3b2950e32e5fdd55cd05db41e)
 - [time_since_first_press()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#a3e03b887cc2689aadc7e7830f2f2b8ac)
 - [is_clicked_queue_empty()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#ad633b6b3f42fbd3c7a560e1e68e45848) 
 - [time_since_last_click()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#a35c95e275d2ec89a03a2fab95b63de58) 
 - [time_since_first_click()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#a34cf627be486f530c9e2a33b158990bc) 

## Qwiic Button Ex5 Popqueue
Simple Example for the Qwiic Button. Shows how to use he FIFO Queue on the Qwiic Button.

 The key methods showcased by this example are:
 - [pop_clicked_queue()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#a3e169dd9951d413a4c88e849fd22b67f)

## Qwiic Button Ex6 Changei2Caddress
Simple Example for the Qwiic Button. Shows how to change the I2C address of
 the Qwiic Button

 The key methods showcased by this example are:
 - [set_I2C_address()](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html#a0658dfd332b10404ad5d18e74de1b7aa)

## Qwiic Button Ex7 2Buttons
Simple Example for the Qwiic Button. Daisy chain together two Qwiic Buttons 
 with different I2C addresses. This example works for a Qwiic Button with the 
 default address of 0x6F and one with an address changed to 0x5B. To change 
 the address of a Qwiic Button, please visit example 6.
