# micropython distribution of Qwiic_Py package
this directory contains limited support for the Qwiic_Py modules on micropython platforms

## supported platforms
*** note:** currently only the RP2040 is supported. the distributed ```.mpy``` bytecode files have been built with flags that are specific to the RP2040. other platforms are not expected to work
(however the system is relatively flexible and adding support for other platforms in the future is a possibility)

## quick start

**installing prerequisites**
the ```/dist``` directory contains pre-compiled bytecode files. to use a driver your target board must have some prerequisite files onboard in a particular file structure:

taget file | source | purpose
-----------|--------|--------
```__future__.mpy``` | ```dist/micropython/src/\_\_future\_\_.mpy``` | provides limited ```__future__``` module functionality
```qwiic_i2c/__init__.mpy | dist/micropython/src/qwiic_i2c/__init__.mpy | module definition for ```import qwiic_i2c```
```qwiic_i2c/i2c_driver.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/i2c_driver.mpy``` | defines an interface which driver modules utilize
```qwiic_i2c/micropython_rp2040_i2c.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/micropython_rp2040_i2c.mpy``` | this is the i2c driver that actually applies to the RP2040


here's a cheat sheet for [```rshell```](https://github.com/dhylands/rshell) commands to copy the prereq files over. execute these one at a time to avoid possible issues with ```rshell```.
```
cd Qwiic_Py/micropython
rshell -a
connect serial /dev/cu.usbmodem0000000000001 115200
mkdir /pyboard/qwiic_i2c
cp dist/micropython/src/__future__.mpy /pyboard/__future__.mpy
cp dist/micropython/src/qwiic_i2c/__init__.mpy /pyboard/qwiic_i2c/__init__.mpy
cp dist/qwiic_i2c/qwiic_i2c/i2c_driver.mpy /pyboard/qwiic_i2c/i2c_driver.mpy
cp dist/qwiic_i2c/qwiic_i2c/micropython_rp2040_i2c.mpy /pyboard/qwiic_i2c/micropython_rp2040_i2c.mpy
## 
```

**using a driver**
the drivers (located in ```Qwiic_Py/qwiic/drivers```) are interfaces to particular sensors, actuators, and other peripheral devices that depend solely on the ```qwiic_i2c``` interface. once the prerequisites are available on your target board you can copy the bytecode driver for the device you want to control. it should exist at the root of the target's filesystem so that other code (e.g. examples) can import it as expected. 

here's an example of how to add a driver to your board, using the ```qwiic_adxl313``` module.
```
cp dist/qwiic/drivers/qwiic_adxl313/qwiic_adxl313.mpy /pyboard/qwiic_adxl313.mpy
```

you can now:
```
>>> import qwiic_adxl313
```

**using examples**

```
cp dist/qwiic/drivers/qwiic_adxl313/examples/ex1_qwiic_adxl313_basic_readings.mpy /pyboard/ex1_qwiic_adxl313_basic_readings.mpy
```

you can now:
```
>>> import ex1_qwiic_adxl313_basic_readings
>>> ex1_qwiic_adxl313_basic_readings.runExample()
```

## issues
there can be some trouble uploading certain binary files over rshell. these issues subsequently cascade into the ```qwiic_i2c``` module. as a temporary workaround a modified version of ```qwiic_i2c/__init__.py``` is used which only imports the RP2040 driver
