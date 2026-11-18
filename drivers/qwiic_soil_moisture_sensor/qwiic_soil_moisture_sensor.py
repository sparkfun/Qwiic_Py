"""!
qwiic_soil_moisture_sensor
============
Python module for the [SparkFun Qwiic Soil Moisture Sensor](https://www.sparkfun.com/products/17731)

This python package is a port of the existing [SparkFun Soil Moisture Sensor Arduino Examples](https://github.com/sparkfun/Zio-Qwiic-Soil-Moisture-Sensor/tree/master/Firmware/Qwiic%20Soil%20Moisture%20Sensor%20Examples)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

import qwiic_i2c

__version__ = "3.0.0"

#======================================================================
# Basic setup of I2C commands and available I2C Addresses
#
#
# The name of this device - note this is private
_DEFAULT_NAME = "Qwiic Soil Moisture Sensor"


# Command addresses
COMMAND_LED_OFF = 0x00
COMMAND_LED_ON = 0x01
COMMAND_CHANGE_ADDRESS = 0x03
COMMAND_GET_VALUE = 0x05
COMMAND_NOTHING_NEW = 0x99
SENSOR_STATUS = 0x3F
SOIL_MOISTURE_SENSOR_DEFAULT_ADDRESS = 0x28

###############################################################################
###############################################################################
# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_FULL_ADDRESS_LIST = list(range(0x08,0x40))				    	# Full I2C Address List (excluding resrved addresses)
_FULL_ADDRESS_LIST.remove(SOIL_MOISTURE_SENSOR_DEFAULT_ADDRESS) # Remove Default Address of Soil Moisture Sensor from list
_AVAILABLE_I2C_ADDRESS = [SOIL_MOISTURE_SENSOR_DEFAULT_ADDRESS]	# Initialize with Default Address of Soil Moisture Sensor
_AVAILABLE_I2C_ADDRESS.extend(_FULL_ADDRESS_LIST)				# Add Full Range of I2C Addresses



class QwiicSoilMoistureSensor(object):
    """!
    QwiicSoilMoistureSensor

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.

    @return **Object** The Soil Moisture Sensor device object.
    """
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Constructor
    def __init__(self, address=None, i2c_bus=None):

        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

        # Last moisture level read by read_moisture_level()
        self.level = 0

    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """!
        Determine if a Soil Moisture Sensor device is connected to the system.

        The sensor doesn't acknowledge the empty write that
        qwiic_i2c.is_device_connected() sends, so this reads the moisture
        level instead.

        @return **bool** True if the device is connected, otherwise False.
        """
        try:
            self._i2c.read_block(self.address, COMMAND_GET_VALUE, 2)
            return True
        except OSError:
            return False

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """!
        Initialize the operation of the Soil Moisture Sensor module

        @return **bool** Returns true of the initialization was successful, otherwise False.
        """
        
        # Set variables
        self.level = 0

        # Basically return True if we are connected...
        return self.is_connected()

    #****************************************************************************#
    #
    #   Sensor functions
    #
    # ****************************************************************************#
    # Updates the moisture level data
    def read_moisture_level(self):
        """!
        Reads the results from the sensor and stores them in self.level

        @return **int** The moisture level
        """
        
        data = self._i2c.read_block(self.address, COMMAND_GET_VALUE, 2)
        self.level = data[1] << 8 | data[0]
        return self.level
        
    #----------------------------------------------------
    # Checks to see if error bit is set
    def check_status_error(self):
        """!
        Returns  if the Error bit on the sensor is set.

        @return **integer** value of Error bit
        """
        # return the status bit
        value = self._i2c.read_byte(self.address, SENSOR_STATUS)

        return value & 1 << 0


    # --------------------------------------------------------------
    # led_off()
    #
    # Turn the onboard LED off
    def led_off(self):
        """!
        Turn off the onboard LED.

        @return **void** Nothing
        """
        self._i2c.write_byte(self.address, None, 0x00)
    
    # --------------------------------------------------------------
    # led_on
    #
    # Turns the onboard LED on
    def led_on(self):
        """!
        Turn on the onboard LED.

        @return **void** Nothing
        """
        self._i2c.write_byte(self.address, None, 0x01)


    # ----------------------------------------------
    # change_address(new_address)
    #
    # This function changes the I2C address of the Qwiic Soil Moisture Sensor. The address
    # is written to the memory location in EEPROM that determines its address.
    def change_address(self, new_address):
        """!
        Changes the I2C address of the Qwiic Soil Moisture Sensor reader

        @param new_address: the new address to set the Soil Moisture Sensor reader to
        
        @return **bool** True if the address was changed, False if the address is out of range
        """
        if new_address < 0x08 or new_address > 0x3F:
            return False
        
        self._i2c.write_byte(self.address, COMMAND_CHANGE_ADDRESS, new_address)
        
        self.address = new_address
        return True
