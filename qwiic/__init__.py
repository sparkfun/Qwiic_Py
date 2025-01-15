#-----------------------------------------------------------------------------
# __init__.py
#
#------------------------------------------------------------------------
#
#
# Written by  SparkFun Electronics, May 2021
#
# This python library supports the SparkFun Electroncis qwiic
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2021 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#==================================================================================
#
# pylint: disable=old-style-class, missing-docstring, wrong-import-position
#
#-----------------------------------------------------------------------------
# Usage
#
# The package provides a wrapper/overview of classes that encapsulate a specific
# object that represnets a qwiic enabled device.
#
# Use of the pacakge is as follows:
#
# Option 1 - import the package, create the specific class
#
#   import qwiic
#   myDevice = qwiic.MyDevice()
#
# Option 2 - Create the device object using the device address, classname or
#            human readable name
#
#   import qwiic
#   myDevice = qwiic.create_device("My Device Name")
#
#
#
"""
qwiic
========

The SparkFun qwiic python package aggregates all python qwiic
drivers/modules to provide a single entity for qwiic within a
python environment. The qwiic package delivers the high-level
functionality needed to dynamically discover connected qwiic
devices and construct their associated driver object.

New to qwiic? Take a look at the entire
[SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""
#-----------------------------------------------------------------------------
from __future__ import print_function
import sys
import os

import qwiic_i2c

#-----------------------------------------------------------------------------
# Define a class to store content, etc using class scoped methods and variables
#
# Simple method to encapsulate information, and create a simple
# store that doesnt' required the use of 'global'

class _QwiicInternal:
    qwiic_devices = []
    available_devices = {}
    i2c_driver = None

    def __init__(self):
        pass

    @classmethod
    def add_qwiic_device(cls, new_device):
        cls.qwiic_devices.append(new_device)

    @classmethod
    def get_qwiic_devices(cls):
        return cls.qwiic_devices

    @classmethod
    def get_i2c_driver(cls):

        if cls.i2c_driver is None:

            cls.i2c_driver = qwiic_i2c.getI2CDriver()

            if cls.i2c_driver is None:
                print("Unable to get the plaform I2C driver for QWIIC.")

        return cls.i2c_driver

    #-----------------------------------------------------------------------
    # _getAvailableDevices()
    #
    # Return a dictionary that defines the available qwiic devices in the
    # package as a list. The key is the I2C address.
    #
    # Devices with multiple possible addresses have mulitple entries.
    @classmethod
    def get_available_devices(cls):

        # do we already have these
        if not cls.available_devices:

            # Loop through the device lists and add the class to the
            # dict - address is the key.

            for device_class in cls.qwiic_devices:

                # loop over the device addresses - add list of device name
                for addr in device_class.available_addresses:
                    cls.available_devices.setdefault(addr,[]).append(device_class)

        # return cls.available_devices

        # return cls.available_devices, sorted by the I2C addresses
        return dict(sorted(cls.available_devices.items()))



#----------------------------------------------------
# _load_driver_classes()
#
# Method to load the qwiic driver Classes AND expose them as
# attributes to this package.
#
# Use the driver sub directory of this package to determine the names
# and drivers of these pacakges .
#

def _load_driver_classes():

    driver_dir = __file__.rsplit(os.sep, 1)[0] +  os.sep + "drivers"
    driver_dir_linux = __file__.rsplit(os.sep, 1)[0] +  os.sep + "drivers_linux_only"

    try:
        driver_packages = os.listdir(driver_dir)
        driver_packages += os.listdir(driver_dir_linux)
    except IOError:
        print("The qwiic drivers are not installed - please check your installation")
        return

    for driver in driver_packages:
        # The driver objects are just the driver pacakge names in camelcase

        tmp_parts = driver.split('_')

        class_name = tmp_parts[0].title() + ''.join(x.title() for x in tmp_parts[1:])

        try:
            module = __import__(driver)

            # by default we look for a class name of QwiicName, where name is camel cased
            # Camel case is sometimes missed by the driver implementors, so we try to
            # catch this here.. Adds a little to startup, but it's a one time event.

            if not hasattr(module, class_name):
                moduleItems = dir(module)
                i =0
                lname = class_name.lower()
                for tmp in moduleItems:
                    if lname == tmp.lower():
                        break
                    i = i + 1

                if i >= len(moduleItems):
                    print("Invalid driver class name. Unable to locate %s" % class_name)
                    continue

                class_name = moduleItems[i]

            cls_driver = getattr(module, class_name)

            setattr(sys.modules[__name__], class_name, cls_driver)

            _QwiicInternal.add_qwiic_device(cls_driver)
        except Exception as err:
            print("Error loading module `%s`: %s" % (driver, err))
            continue



# load the driver modules...
_load_driver_classes()

#-----------------------------------------------------------------------
# I2C Bus / Device methods
#-----------------------------------------------------------------------
#
# Cache for QWIIC device classes - determined at runtime

#-----------------------------------------------------------------------
# scan()
#
# Scans the I2C bus and returns a list of addresses that have a devices connected
#
def scan():
    """
        Used to scan the I2C bus, returning a list of I2C address attached to the computer.

        :return: A list of I2C addresses. If no devices are attached, an empty list is returned.
        :rtype: list

        :example:

        >>> import qwiic
        >>> [2]: qwiic.scan()
        [61, 91, 96, 119]
    """

    i2c_driver = _QwiicInternal.get_i2c_driver()

    if i2c_driver is None:
        return []

    return i2c_driver.scan()


#-----------------------------------------------------------------------
# list_devices()
#
#   Return a list of tuples that define the qwiic devices connected to the I2C bus.
#
def list_devices():
    """
        Returns a list of known qwiic driver/packages for I2c address(es) of device(s) connected to the I2C bus.

        :return: A list of the qwiic devices associated with the I2C address(es) 
            scanned from the I2C bus. Each element of the list a tuple that 
            contains the following values (Device I2C Address, Device Name, 
            Device Driver Class Name)
            If no devices are attached, an empty list is returned.
        :rtype: list

        :example:

        >>> import qwiic
        >>> qwiic.list_devices()
        [(61, 'Qwiic Micro OLED', 'QwiicMicroOled'),
        (61, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'),
        (91, 'Qwiic PCA9685', 'QwiicPCA9685'),
        (91, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'),
        (91, 'Qwiic CCS811', 'QwiicCcs811'),
        (96, 'Qwiic PCA9685', 'QwiicPCA9685'),
        (96, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'),
        (96, 'Qwiic Proximity Sensor', 'QwiicProximity'),
        (119, 'Qwiic PCA9685', 'QwiicPCA9685'),
        (119, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'),
        (119, 'Qwiic Mux', 'QwiicTCA9548A'),
        (119, 'Qwiic BME280', 'QwiicBme280')]

    """

    # Scan the bus
    device_address = scan()
    if not device_address:
        return []


    # What QWIIC devices do we know about -- what's defined in the package
    qwiic_devs = _QwiicInternal.get_available_devices()
    if not qwiic_devs:
        return []

    found_qwiic = []
    # match scan, with definition
    for address in device_address:

        if address in qwiic_devs.keys():

            # make list of devices at address
            device_list = list(qwiic_devs[address])

            for dev in device_list:
                # make the return tuple
                found_qwiic.append((address, dev.device_name, \
                    dev.__name__))


    return found_qwiic

#-----------------------------------------------------------------------
# list_available_drivers()
#
#   Return a list of tuples that define the available qwiic drivers/packages.
#
def list_available_drivers(device_address=None):
    """
        Returns a list of known drivers/packages for qwiic devices.

        :param device_address: A list with an I2C address or addresses. If no value
            was given, the I2C bus will be scanned and the address(es) of the
            connected qwiic devices will be used.

        :return: A list of qwiic drivers/packages associated with the address(es) in the
            list. Each element of the list a tuple that contains the following values
            (Device I2C Address, Device Name, Device Driver Class Name)
        :rtype: list


        :example:

        >>> import qwiic
        >>> qwiic.list_available_drivers([32])
        [(32, 'Qwiic GPIO', 'QwiicGPIO'),
        (32, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'),
        (32, 'SparkFun Qwiic Joystick', 'QwiicJoystick')]
        >>> qwiic.list_available_drivers([61,91])
        [(61, 'Qwiic Micro OLED', 'QwiicMicroOled'),
        (61, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'),
        (91, 'Qwiic PCA9685', 'QwiicPCA9685'),
        (91, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'),
        (91, 'Qwiic CCS811', 'QwiicCcs811')]

    """

    if device_address is None:
        device_address = list(range(0x08,0x77+1))


    # What QWIIC devices do we know about -- what's defined in the package
    qwiic_devs = _QwiicInternal.get_available_devices()
    if not qwiic_devs:
        return []

    found_qwiic = []

    # Match scan, with definition
    for address in device_address:

        # Make list of devices at address
        if address in qwiic_devs.keys():
            device_list = list(qwiic_devs[address])

            # List all devices from address
            for dev in device_list:
                # make the return tuple
                found_qwiic.append((address, dev.device_name, \
                    dev.__name__))


    return found_qwiic

#-------------------
# get_devices()
#
#   Returns a list of objects that define the qwiic devices attached to the
#   I2C bus.
#
def get_devices():
    """
        Used to create device objects for all qwiic devices attached to the computer.

        :return: A list of qwiic device objects.
            If no qwiic devices are an empty list is returned.
        :rtype: list

        :example:

        >>> import qwiic

        >>> qwiic.get_devices()
        [<qwiic_micro_oled.qwiic_micro_oled.QwiicMicroOled at 0x76081ef0>,
        <qwiic_ccs811.QwiicCcs811 at 0x752b78b0>,
        <qwiic_proximity.QwiicProximity at 0x752b0e10>,
        <qwiic_bme280.QwiicBme280 at 0x752b0a30>]

    """

    # Scan the bus
    found_devices = scan()
    if not found_devices:
        return []

    # What QWIIC devices do we know about -- what's defined in the package
    qwiic_devs = _QwiicInternal.get_available_devices()
    if not qwiic_devs:
        return []


    found_qwiic = []
    # match scan, with definition
    for address in found_devices:

        if address in qwiic_devs.keys():

            # make list of devices at address
            device_list = list(qwiic_devs[address])

            for dev in device_list:
                # Create an object and append to our found list
                # note: class defs are stored in the defs dictionary..
                found_qwiic.append(dev(address))


    return found_qwiic

#-------------------
# create_device()
#
#   Given the Address, Name or Clasname of a qwiic device, create the
#   assocaited device object and return it to the caller.
#
#   The intent is for the user to call list_devices() (connected devices only),
#   find a device they like AND use this method to create the device at the
#   connected address
#
def create_device(device=None):
    """
        Used to create a device object for a specific qwiic device

        :param device: The I2C address (int), Name or Class name (str) of the device to created,
            or selection from listed connected devices (tuple).
            The device address should be an integer value, of the hex value. For
            an example, for an `0x60` (hex) address enter `qwiic.create_device(60)`.
        :return: A qwiic device object for the specified qwiic device, using the I2C address
            that the device is connected at.
            If the specified device isn't found, None is returned.
        :rtype: Object

        :example:

        >>> import qwiic
        >>> results = qwiic.list_devices()
        >>> print(results)
        [(16, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'), (16, 'Qwiic Titan GPS', 'QwiicTitanGps'), (41, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'), (60, 'Qwiic Micro OLED (64x48)', 'QwiicMicroOled'), (60, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'), (60, 'SSD1306 Display Driver', 'QwiicSSD1306Driver'), (60, 'Qwiic OLED Display (128x32)', 'QwiicOledDisplay'), (61, 'Qwiic Micro OLED (64x48)', 'QwiicMicroOled'), (61, 'Qwiic 4m Distance Sensor (ToF)', 'QwiicVL53L1X'), (61, 'SSD1306 Display Driver', 'QwiicSSD1306Driver'), (61, 'Qwiic OLED Display (128x32)', 'QwiicOledDisplay')]
        >>> mydevice1 = qwiic.create_device(results[47])
        >>> print(mydevice1)
        <qwiic_micro_oled.qwiic_micro_oled.QwiicMicroOled object at 0x743558f0>
        >>> mydevice2 = qwiic.create_device(41)
        >>> print(mydevice2)
        <qwiic_vl53l1x.QwiicVL53L1X object at 0x743e7bb0>
        >>> mydevice3 = qwiic.create_device("QwiicTitanGps")
        ============================================================================
        Message about Titan GPS package...
        ============================================================================
        >>> print(mydevice3)
        <qwiic_titan_gps.QwiicTitanGps object at 0x739c4430>

    """

    if device is None:
        print("No device provided.")
        return None

    conn_devices = list_devices()


    # The entries in the connDevices list are tuples, with the values:
    #   (I2C address, Device Name, Class Name)
    # For the provided value (device), if a match is found in the current
    # device tuple, a list is created from the tuple 
    if type(device) is tuple:
        dev_match = [curr_dev for curr_dev in conn_devices if device == curr_dev]
    else:
        dev_match = [curr_dev for curr_dev in conn_devices if device in curr_dev]


    # If there are no matching entries for the inputted device descriptor
    if len(dev_match) == 0:
        print("Error: No matching connected devices\n")

        return None

    # If there are mulitple entries for the inputted device descriptor
    elif len(dev_match) > 1:
        # Print out matched devices
        print("Error: Multiple matches found for input: \n")
        print(dev_match, "\n")

        return None

    # If there is a match
    else:
        # we need the class definition
        qwiic_defs = _QwiicInternal.get_available_devices()

        
        if type(device) is int:
            return qwiic_defs[device][0](int)
        else:
            # Match classes that are indexed at dev_address, to the dev_name
            for dev_class in qwiic_defs[dev_match[0][0]]:
                if dev_class.device_name == dev_match[0][1]:
                    # Create a device using cless at the connected address
                    return dev_class(dev_match[0][0])


    # if we are here, we have an issue
    print("Unabled to create requested device - is the device connected?")

    return None
