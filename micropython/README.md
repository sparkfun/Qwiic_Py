# micropython distribution of Qwiic_Py package
this directory contains limited support for the Qwiic_Py modules on micropython platforms

## supported platforms
**note:** currently only the RP2040 is supported. the distributed ```.mpy``` bytecode files have been built with flags that are specific to the RP2040. other platforms are not expected to work
(however the system is relatively flexible and adding support for other platforms in the future is a possibility)

## quick start

**installing prerequisites**
the ```/dist``` directory contains pre-compiled bytecode files. to use a driver your target board must have some prerequisite files onboard in a particular file structure:

taget file | source | purpose
-----------|--------|--------
```__future__.mpy``` | ```dist/micropython/src/__future__.mpy``` | provides limited ```__future__``` module functionality
```enum.mpy``` | ```dist/micropython/src/enum.mpy``` | provides limited ```enum``` module functionality
```board.mpy``` | ```dist/micropython/src/boards/${BOARDNAME}/board.mpy``` | provides board pin definitions of the Qwiic connector + i2c port
```qwiic_i2c/__init__.mpy``` | ```dist/micropython/src/qwiic_i2c/__init__.mpy``` | module definition for ```import qwiic_i2c```
```qwiic_i2c/i2c_driver.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/i2c_driver.mpy``` | defines an interface which driver modules utilize
```qwiic_i2c/micropython_rp2040_i2c.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/micropython_rp2040_i2c.mpy``` | this is the i2c driver that actually applies to the RP2040
```qwiic_i2c/circuitpy_i2c.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/circuitpy_i2c.mpy``` | needed b/c it is imported by ```__init__.mpy```
```qwiic_i2c/linux_i2c.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/linux_i2c.mpy``` | needed b/c it is imported by ```__init__.mpy```


here's a cheat sheet for [```rshell```](https://github.com/dhylands/rshell) commands to copy the prereq files over.

**note:** use the ```pico``` branch of rshell because:
* it auto-connects to the pico board
* it appears to solve some [issues](https://github.com/dhylands/rshell/issues/144)

to do so you may need to use git. clone [rshell](https://github.com/dhylands/rshell) and switch to the ```pico``` branch. then run the main script like this:

```./rshell/rshell/main.py -a```
(the ```-a``` flag is very important)

**note:** the board directories are referred to the board name. this will change depending on which board you are using. we use ```${BOARDNAME}``` to indicate a variable that contains the board name, such as ```BOARDNAME=PiMicro```

```
cd Qwiic_Py
./${PATH_TO_RSHELL}/rshell/main.py -a
rm -rf /${BOARDNAME}/qwiic_i2c
rm -f /${BOARDNAME}/__future__.mpy
rm -f /${BOARDNAME}/enum.mpy
mkdir /${BOARDNAME}/qwiic_i2c
cp micropython/dist/micropython/src/__future__.mpy /${BOARDNAME}/__future__.mpy
cp micropython/dist/micropython/src/boards/${BOARDNAME}/board.mpy /${BOARDNAME}/board.mpy
cp micropython/dist/qwiic_i2c/qwiic_i2c/__init__.mpy /${BOARDNAME}/qwiic_i2c/__init__.mpy
cp micropython/dist/qwiic_i2c/qwiic_i2c/i2c_driver.mpy /${BOARDNAME}/qwiic_i2c/i2c_driver.mpy
cp micropython/dist/qwiic_i2c/qwiic_i2c/micropython_rp2040_i2c.mpy /${BOARDNAME}/qwiic_i2c/micropython_rp2040_i2c.mpy
cp micropython/dist/qwiic_i2c/qwiic_i2c/linux_i2c.mpy /${BOARDNAME}/qwiic_i2c/linux_i2c.mpy
cp micropython/dist/qwiic_i2c/qwiic_i2c/circuitpy_i2c.mpy /${BOARDNAME}/qwiic_i2c/circuitpy_i2c.mpy
## 
```

**shortcut:** using rshell's scripting feature (```-f FILENAME```) we can automate these steps. use the script that matches your desired boardname:
```./${PATH_TO_RSHELL}/rshell/main.py -a -f micropython/tools/qwiic-mpy/push-drivers/${BOARDNAME}.rshell```

**using a driver**

the drivers (located in ```Qwiic_Py/qwiic/drivers```) are interfaces to particular sensors, actuators, and other peripheral devices that depend solely on the ```qwiic_i2c``` interface. once the prerequisites are available on your target board you can copy the bytecode driver for the device you want to control. it should exist at the root of the target's filesystem so that other code (e.g. examples) can import it as expected. 

here's an example of how to add a driver to your board, using the ```qwiic_adxl313``` module.
```
cp micropython/dist/qwiic/drivers/qwiic_adxl313/qwiic_adxl313.mpy /${BOARDNAME}/qwiic_adxl313.mpy
```

you can now:
```
>>> import qwiic_adxl313
```

**using examples**

```
cp micropython/dist/qwiic/drivers/qwiic_adxl313/examples/ex1_qwiic_adxl313_basic_readings.mpy /${BOARDNAME}/ex1_qwiic_adxl313_basic_readings.mpy
```

you can now:
```
>>> import ex1_qwiic_adxl313_basic_readings
>>> ex1_qwiic_adxl313_basic_readings.runExample()
```

```
from machine import I2C
from machine import Pin
scl = Pin(17)
sda = Pin(16)
id = 0
i2c = I2C(freq=400000, id=id, scl=scl, sda=sda)
```

## issues
there can be some trouble uploading certain binary files over rshell. these issues subsequently cascade into the ```qwiic_i2c``` module. as a temporary workaround a modified version of ```qwiic_i2c/__init__.py``` is used which only imports the RP2040 driver
