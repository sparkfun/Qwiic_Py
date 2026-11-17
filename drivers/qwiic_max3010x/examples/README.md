# Sparkfun MAX3010X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_max3010x_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Ex1 Basic Readings
Simple example for the qwiic MAX3010x device
 Outputs all Red/IR/Green values.

The key methods showcased by this exmple are: 
- [getIR()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#a74b40102bfeaf8f765d20f91b3deb37c)
- [getGreen()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#ad443418504fbc1fe17db8ca4dd2ff271)

## Ex2 Presence Sensing
Simple example for the qwiic MAX3010x device
 This takes an average reading at power up and if the reading changes more than 100,
 then print 'Something is there!'.

The key methods showcased by this exmple are: 
- [setPulseAmplitudeRed()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#aff2c4701cdc8565ea27cfb03a207cc78)
- [setPulseAmplitudeGreen()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#a8cce76d9c5e32566ccaa9900e54cb12b)
- [getIR()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#a74b40102bfeaf8f765d20f91b3deb37c)


## Ex3 Temperature Sense
Simple example for the qwiic MAX3010x device
 This demo outputs the onboard temperature sensor. 
 The temp sensor is accurate to +/-1 C but
 has an astonishing precision of 0.0625 C.
 
The key methods showcased by this exmple are: 
- [readTemperature()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#a453aaba7260dd7200b8c5e806d8cb724)
- [readTemperatureF()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#a4e2e7d76dbdb48b67b152712677fcc17)

## Ex4 Heartbeat Plotter
NOTE: This example is ONLY available for Linux/Raspberry Pi, NOT MicroPython and CircuitPython
 Shows the user's heart beat on a graphical plotter
 Using Matplotlib
 To learn more about plotting data in python check out this tutorial:
 https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/
 The example code below was built using the code from the previously mentioned tutorial.
 Thanks Shawn Hymel!

## Ex5 Heartrate
Simple example for the qwiic MAX3010x device
 This is a demo to show the reading of heart rate or beats per minute (BPM) using
 a Penpheral Beat Amplitude (PBA) algorithm.
 
The key methods showcased by this exmple are: 
- [setPulseAmplitudeRed()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#aff2c4701cdc8565ea27cfb03a207cc78)
- [setPulseAmplitudeGreen()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#a8cce76d9c5e32566ccaa9900e54cb12b)
- [checkForBeat()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#a38a991958e121a42210a0ad44c6d4bdb)


## Ex6 Fifo Readings
Simple example for the qwiic MAX3010x device
 Outputs all Red/IR/Green values at  about 5Hz by polling the FIFO
 Note, the Hz is slowed down by printing to the python terminal,
 It can be drmatically speed up if printing is omitted or intermittent
 
The key methods showcased by this exmple are: 
- [available()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#a8bbd8851f5095ad14de9dfbb8643ed3f)
- [getFIFORed()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#a1c8df66708cfdf2fd12e16440a8e6316)
- [getFIFOIR()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#ac6de275aa402ba5f73c963fed638919e)
- [getFIFOGreen()](https://docs.sparkfun.com/qwiic_max3010x_py/classqwiic__max3010x_1_1qwiic__max3010x_1_1_qwiic_max3010x.html#ae912c2ac08f07689e03405d1192a16b7)



