"""!
qwiic_tmp102
============
Python module for the [SparkFun Qwiic TMP102 Sensor](https://www.sparkfun.com/products/16304)

This python package is a port of the existing [SparkFun Qwiic TMP102 Sensor Arduino Examples](https://github.com/sparkfun/SparkFun_TMP102_Arduino_Library/tree/master/examples)

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
_DEFAULT_NAME = "Qwiic TMP102 Sensor"

# Command addresses. These can be found on page 23 of the datasheet
TEMPERATURE_REGISTER = 0x00
CONFIG_REGISTER = 0x01
T_LOW_REGISTER = 0x02
T_HIGH_REGISTER = 0x03
TMP102_DEFAULT_ADDRESS = 0x48


TMP102_RESOLUTION = 0.0625                   # Resolution of the device, found on (page 1 of datasheet)

#Address can only be 0x48 (GND), 
#	0x49 (V+), 0x4A (SDA), and 0x4B (SCL)
_AVAILABLE_I2C_ADDRESS = [0x48, 0x49, 0x4A, 0x4B]

###############################################################################
###############################################################################
# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
class QwiicTMP102(object):
    """!
    QwiicTMP102

    @param address: The I2C address to use for the device.
                    If not provided, the default address is used.
    @param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.

    @return **Object** The TMP102 Sensor device object.
    """
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Constructor
    def __init__(self, address=None, i2c_bus=None):

        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address?
        self.address = self.available_addresses[0] if address is None else address

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)


    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """!
        Determine if a TMP102 device is connected to the system.

        @return **bool** True if the device is connected, otherwise False.
        """        
        return qwiic_i2c.is_device_connected(self.address)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """!
        Initialize the operation of the TMP102 module

        @return **bool** Returns true of the initialization was successful, otherwise False.
        """
        # Set variables
        self.temp_c = 0
        self.temp_f = 0
        
        # Basically return True if we are connected...
        return self.is_connected()

    #****************************************************************************#
    #
    #   Sensor functions
    #
    # ****************************************************************************#
    def get_address(self):
        """!
        Returns the device address

        @return **int** The device address.
        """
        return self.address

    def read_temp_c(self):
        """!
        Reads the results from the sensor

        @return **float** The temperature in Celsius.
        """
        data = self.read_block_pointer_reg(TEMPERATURE_REGISTER)
        
        if (data[0] == 0xFF and data[1] == 0xFF):
                return None
                
        if(data[1]&0x01):	# 13 bit mode
                base_read = ((data[0]) << 5) | (data[1] >> 3)
                if(base_read > 0xFFF):
                        base_read |= 0xE000
        else:
                #Combine bytes to create a signed int 
                base_read = ((data[0]) << 4) | (data[1] >> 4)

        	#Temperature data can be + or -, if it should be negative,
                #convert 12 bit to 16 bit and use the 2s compliment.
                if(base_read > 0x7FF):
                        base_read |= 0xF000

        self.temp_c = base_read * 0.0625
        return self.temp_c
        
    def read_temp_f(self):
        """!
        Reads the results from the sensor
        
        @return **float** The temperature in Fahrenheit.
        """

        self.temp_f = self.read_temp_c() * 9.0 / 5.0 + 32.0
        return self.temp_f
        
    def set_conversion_rate(self, rate):
        """!
        Set the conversion rate (0-3)

        @ param int rate: The rate to set the conversion to.
        0 - 0.25 Hz
        1 - 1 Hz
	    2 - 4 Hz (default)
        3 - 8 Hz
        """
        
        config_byte = self.read_block_pointer_reg(CONFIG_REGISTER)
        rate = rate&0x03
                
        # Load new conversion rate
        config_byte[1] &= 0x3F           # Clear CR0/1 (bit 6 and 7 of second byte)
        config_byte[1] |= rate<<6        # Shift in new conversion rate
      
        self._i2c.write_block(self.address, CONFIG_REGISTER, config_byte)
        
    def set_extended_mode(self, mode):
        """!
        Enable or disable extended mode
        0 - disabled (-55C to +128C)
        1 - enabled  (-55C to +150C)
        """
        config_byte = self.read_block_pointer_reg(CONFIG_REGISTER)
        
        # Load new value for extention mode
        config_byte[1] &= 0xEF		# Clear EM (bit 4 of second byte)
        config_byte[1] |= mode<<4	# Shift in new exentended mode bit
        
        self._i2c.write_block(self.address, CONFIG_REGISTER, config_byte)
    
    def sleep(self):
        """!
        Switch sensor to low power mode
        """
        sleep_value = self.read_block_pointer_reg(CONFIG_REGISTER)[0]
        sleep_value |= 0x01	# Set SD (bit 0 of first byte)
        self._i2c.write_byte(self.address, CONFIG_REGISTER, sleep_value)

    def wakeup(self):
        """!
        Wakeup and start running in normal power mode
        """
        wake_value = self.read_block_pointer_reg(CONFIG_REGISTER)[0]
        wake_value &= 0xFE	# Clear SD (bit 0 of first byte)
        self._i2c.write_byte(self.address, CONFIG_REGISTER, wake_value)

    def set_alert_polarity(self, polarity):
        """!
        Set the polarity of Alert
        0 - Active LOW
        1 - Active HIGH
        """
        config_byte = self.read_block_pointer_reg(CONFIG_REGISTER)[0]
        
        # Load new value for polarity
        config_byte &= 0xFB           # Clear POL (bit 2 of register_byte)
        config_byte |= polarity<<2    # Shift in new POL bit

        self._i2c.write_byte(self.address, CONFIG_REGISTER, config_byte)

    def alert(self):
        """!
        Returns state of Alert register

        @return **int** The state of the alert register.
        """
        alert = self.read_block_pointer_reg(CONFIG_REGISTER)[1]
        alert &= 0x20   #Clear everything but the alert bit (bit 5)
        return alert>>5
        
    def one_shot(self, set_one_shot = 0):
        """!
        Sets the SingleShot Register. Returns 1 after the conversion is complete

        @param set_one_shot: **int** 1 - Start a one-shot conversion
                                 0 - Return the one-shot (conversion ready) bit (default)

        @return **int** The state of the one shot register.
        """
        register_byte = self.read_block_pointer_reg(CONFIG_REGISTER)[0]
        if(set_one_shot == 1):
                register_byte |= (1<<7)
                self._i2c.write_byte(self.address, CONFIG_REGISTER, register_byte)
                return 0
        else:
                register_byte &= (1<<7)
                return (register_byte>>7)


    def set_low_temp_c(self, temperature):
        """!
        Sets T_LOW (degrees C) alert threshold

        @param temperature: **float** The temperature in Celsius to set the alert threshold to.
        """
        if(temperature > 150.0):
                temperature = 150.0
        if(temperature < -55.0):
                temperature = -55.0
                
        register_byte = self.read_block_pointer_reg(CONFIG_REGISTER)
        
        #Check if temperature should be 12 or 13 bits
        # 0 - temp data will be 12 bits
        # 1 - temp data will be 13 bits
        extended_mode = (register_byte[1]&0x10) >> 4	
                                                                
        #Convert analog temperature to digital value
        temperature = temperature/0.0625
        
        # Align data for the temperature registers (see pg. 19 of datasheet)
        if(extended_mode):	#13-bit mode
                register_byte[0] = int(temperature)>>5
                register_byte[1] = (int(temperature) & 0x1F)<<3 # lower 5 bits 
        else:
                register_byte[0] = int(temperature)>>4
                register_byte[1] = (int(temperature) & 0xF)<<4 # lower 4 bits
              
        self._i2c.write_block(self.address, T_LOW_REGISTER, register_byte)

    def set_high_temp_c(self, temperature):
        """!
        Sets T_HIGH (degrees C) alert threshold

        @param temperature: **float** The temperature in Celsius to set the alert threshold to.
        """

        if(temperature > 150.0):
                temperature = 150.0
        if(temperature < -55.0):
                temperature = -55.0
        register_byte = self.read_block_pointer_reg(CONFIG_REGISTER)
        
        #Check if temperature should be 12 or 13 bits
        # 0 - temp data will be 12 bits
        # 1 - temp data will be 13 bits
        extended_mode = (register_byte[1]&0x10) >> 4	
                                                                
        #Convert analog temperature to digital value
        temperature = temperature/0.0625
        
        # Align data for the temperature registers (see pg. 19 of datasheet)
        if(extended_mode):	#13-bit mode
                register_byte[0] = int(temperature)>>5 
                register_byte[1] = (int(temperature) & 0x1F)<<3 # lower 5 bits 
        else:
                register_byte[0] = int(temperature)>>4
                register_byte[1] = (int(temperature) & 0xF)<<4 # lower 4 bits
                
        self._i2c.write_block(self.address, T_HIGH_REGISTER, register_byte)

    def set_low_temp_f(self, temperature):
        """!
        Sets T_LOW (degrees F) alert threshold

        @param temperature: **float** The temperature in Fahrenheit to set the alert threshold to.
        """
        new_temp = (temperature - 32)*5/9    # Convert temperature to C
        self.set_low_temp_c(new_temp)           # Set T_LOW

        
    def set_high_temp_f(self, temperature):
        """!
        Sets T_HIGH (degrees F) alert threshold
        """
        new_temp = (temperature - 32)*5/9    # Convert temperature to C
        self.set_high_temp_c(new_temp)           # Set T_HIGH


    def read_low_temp_c(self):
        """!
        Gets T_LOW (degrees C) alert threshold

        @return **float** The low temp in Celsius.
        """
        config_byte = self.read_block_pointer_reg(CONFIG_REGISTER)

        # 0 - temp data will be 12 bits
        # 1 - temp data will be 13 bits
        extended_mode = (config_byte[1]&0x10)>>4	

        low_temp_byte = self.read_block_pointer_reg(T_LOW_REGISTER)

        if(low_temp_byte[0] == 0xFF and low_temp_byte[1] == 0xFF):
                return None

        if (extended_mode):
                digital_temp = ((low_temp_byte[0]) << 5) | (low_temp_byte[1] >> 3)
                if(digital_temp > 0xFFF):
                        digital_temp |= 0xE000
        else:
                digital_temp = ((low_temp_byte[0]) << 4) | (low_temp_byte[1] >> 4)
                if(digital_temp > 0x7FF):
                        digital_temp |= 0xF000
                        
        return digital_temp*0.0625    
        
                    
    def read_high_temp_c(self):
        """!
        Gets T_HIGH (degrees C) alert threshold

        @return **float** The high temp in Celsius.
        """
        config_byte = self.read_block_pointer_reg(CONFIG_REGISTER)

        # 0 - temp data will be 12 bits
        # 1 - temp data will be 13 bits
        extended_mode = (config_byte[1]&0x10)>>4	

        high_temp_byte = self.read_block_pointer_reg(T_HIGH_REGISTER)

        if(high_temp_byte[0] == 0xFF and high_temp_byte[1] == 0xFF):
                return None

        if (extended_mode):
                digital_temp = ((high_temp_byte[0]) << 5) | (high_temp_byte[1] >> 3)
                if(digital_temp > 0xFFF):
                        digital_temp |= 0xE000
        else:
                digital_temp = ((high_temp_byte[0]) << 4) | (high_temp_byte[1] >> 4)
                if(digital_temp > 0x7FF):
                        digital_temp |= 0xF000
                        
        return digital_temp*0.0625


    def read_low_temp_f(self):
        """!
        Reads T_LOW register in F

        @return **float** The low temp in Fahrenheit.
        """
        return self.read_low_temp_c()*9.0/5.0 + 32.0
        
    def read_high_temp_f(self):
        """!
        Reads T_HIGH register in F

        @return **float** The high temp in Fahrenheit.
        """
        
        return self.read_high_temp_c()*9.0/5.0 + 32.0


    def set_fault(self, fault_setting):
        """!
        Set the number of consecutive faults

        @param fault_setting: **int** The number of consecutive faults to trigger an alert.
        0 - 1 fault
        1 - 2 faults
        2 - 4 faults
        3 - 6 faults
        """
        fault_setting = fault_setting&3   #Make sure rate is not set higher than 3.

        config_byte = self.read_block_pointer_reg(CONFIG_REGISTER)[0]
                
        #Load new conversion rate
        config_byte &= 0xE7                   # Clear F0/1 (bit 3 and 4 of first byte)
        config_byte |= fault_setting<<3        # Shift new fault setting
        
        self._i2c.write_byte(self.address, CONFIG_REGISTER, config_byte)
        
    def set_alert_mode(self, mode):
        """!
        Set Alert type

        @param mode: **int** The mode to set the alert to.
        0 - Comparator Mode: Active from temp > T_HIGH until temp < T_LOW
        1 - Thermostat Mode: Active when temp > T_HIGH until any read operation occurs
        """
        config_byte = self.read_block_pointer_reg(CONFIG_REGISTER)[0]
        
        #Load new conversion rate
        config_byte &= 0xFD            # Clear old TM bit (bit 1 of first byte)
        config_byte |= mode<<1	        # Shift in new TM bit

        self._i2c.write_byte(self.address, CONFIG_REGISTER, config_byte)

    def read_block_pointer_reg(self, reg, num_bytes = 2):
        """!
        To read from the device, we first write the register we want to read then explicitly send a stop bit.
        Then, restart the connection to read the data from the device.

        See datasheet page. 13

        @param reg: **int** The register to read from.
        @param num_bytes: **int** The number of bytes to read.

        @return **list** A list of bytes from the device.
        """
        self._i2c.write_byte(self.address, None, reg)

        return list(self._i2c.read_block(self.address, reg, num_bytes))
