# micropython distribution of Qwiic_Py package
limited support for the Qwiic_Py modules on micropython platforms

you may use pre-compiled ```*.mpy``` files to add Qwiic drivers / support to your micropython board. using the pre-compiled files saves RAM on systems with limited resources such as microcontrollers. ```*.mpy``` is a micropython specific format and will not work with regular Python.

**supported boards**
* [SparkFun Pro Micro - RP2040](https://www.sparkfun.com/products/17717)

## quick start

**installing prerequisites**
the ```/dist``` directory contains pre-compiled bytecode files. to use a driver your target board must have some prerequisite files onboard in a particular file structure:

target file | source | purpose
-----------|--------|--------
```__future__.mpy``` | ```dist/micropython/src/__future__.mpy``` | provides limited ```__future__``` module functionality
```enum.mpy``` | ```dist/micropython/src/enum.mpy``` | provides limited ```enum``` module functionality
```board.mpy``` | ```dist/micropython/src/boards/${BOARDNAME}/board.mpy``` | provides board pin definitions of the Qwiic connector + i2c port
```qwiic_i2c/__init__.mpy``` | ```dist/qwiic_i2c/__init__.mpy``` | module definition for ```import qwiic_i2c```
```qwiic_i2c/i2c_driver.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/i2c_driver.mpy``` | defines an interface which driver modules utilize
```qwiic_i2c/micropython_rp2040_i2c.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/micropython_rp2040_i2c.mpy``` | this is the i2c driver that actually applies to the RP2040
```qwiic_i2c/circuitpy_i2c.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/circuitpy_i2c.mpy``` | needed b/c it is imported by ```__init__.mpy```
```qwiic_i2c/linux_i2c.mpy``` | ```dist/qwiic_i2c/qwiic_i2c/linux_i2c.mpy``` | needed b/c it is imported by ```__init__.mpy```

**we will use *[rshell](https://github.com/dhylands/rshell)* to copy the files onto the board** (though you can use whatever methods you like)

here's a cheat sheet for [```rshell```](https://github.com/dhylands/rshell) commands to copy the prereq files over.

**note:** use the ```pico``` branch of rshell because:
* it auto-connects to the pico board
* it appears to solve some [issues](https://github.com/dhylands/rshell/issues/144)

to do so you may need to use git. clone [rshell](https://github.com/dhylands/rshell) and switch to the ```pico``` branch. then run the main script like this:

```./rshell/rshell/main.py -a```
(the ```-a``` flag is very important)

**note:** the on-board directories are referred to by the board name. this will change depending on which board you are using. we use ```${BOARDNAME}``` to indicate a variable that contains the board name, such as ```BOARDNAME=rp2040_promicro```

### initial setup (repeat when core drivers are updated)

**first**

copy the appropriate ```board.py``` or ```board.mpy``` file exists on the board. you can use the precompiled bytecode to save memory or you can use the ```.py``` file in case you want to easily edit the file on-board.

this configures the ```${BOARDNAME}``` as well as the default I2C bus settings for Qwiic (such as which pins and peripheral module to use)

board files for supported boards are located within the ```micropython/src/boards``` directory. custom or 3rd party boards may require a specialized board file that you provide.

**then**

use the following commands (with appropriate variable substitutions) to upload the core drivers

```
cd Qwiic_Py
./${PATH_TO_RSHELL}/r.py -a
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

**shortcut:** 

using rshell's scripting feature (```-f FILENAME```) we can automate these steps. use the script that matches your desired boardname:
```./${PATH_TO_RSHELL}/rshell/main.py -a -f micropython/tools/qwiic-mpy/push-drivers/${BOARDNAME}.rshell```

### using a driver

the drivers (located in ```Qwiic_Py/qwiic/drivers```) are interfaces to particular sensors, actuators, and other peripheral devices that depend solely on the ```qwiic_i2c``` interface. once the prerequisites are available on your target board you can copy the bytecode driver for the device you want to control. it should exist at the root of the target's filesystem so that other code (e.g. examples) can import it as expected. 

here's an example of how to add a driver to your board, using the ```qwiic_adxl313``` module.

**rshell**
```
cp micropython/dist/qwiic/drivers/qwiic_adxl313/qwiic_adxl313.mpy /${BOARDNAME}/qwiic_adxl313.mpy
```

you can now:
**repl**
```
>>> import qwiic_adxl313
```

### using examples

the examples import any necessary drivers which you should have already added by following the instructions above

**rshell**
```
cp micropython/dist/qwiic/drivers/qwiic_adxl313/examples/ex1_qwiic_adxl313_basic_readings.mpy /${BOARDNAME}/ex1_qwiic_adxl313_basic_readings.mpy
```

you can now:
**repl**
```
>>> import ex1_qwiic_adxl313_basic_readings
>>> ex1_qwiic_adxl313_basic_readings.runExample()
```

## generating precompiled .mpy files

this package includes pre-compiled files for convenience. making changes requires re-compiling the files using mpy-cross. the ```tools/qwiic-mpy/mpygen.py``` script is included to easily regenerate modified files.

for complete usage details use the help menu

```tools/qwiic-mpy/mpygen.py --help```

## supported platforms
**note:** currently only the RP2040 is supported. the distributed ```.mpy``` bytecode files have been built with flags that are specific to the RP2040. other platforms are not expected to work
(however the system is relatively flexible and adding support for other platforms in the future is a possibility)

## issues

driver | level | description
-------|-------|------------
titan gps | error | the ```pynmea2``` module does not have a upy port
micro oled | error | usage of the ```__file__``` keyword to find binary fonts fails and requires driver modification
proximity | error | ```OSError 5``` occurs on reads
tca9548a | error | the tca9548a does not comply with the driver as most other drivers are expected to work. because it is a single-register device it does not take an offset (commandCode) value for reads/writes. it is likely that a change to the api will be required to handle such cases. there is also an inconsistency with the tca9548a driver importing ```qwiic``` instead of ```qwiic_TCA9548A``` thus imparting a dependency on the full package

