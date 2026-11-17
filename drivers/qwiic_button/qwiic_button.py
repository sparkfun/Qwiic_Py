#-----------------------------------------------------------------------------
# qwiic_button.py
#
# Python library for the SparkFun qwiic button.
#   https://www.sparkfun.com/products/15932
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, January 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2020 SparkFun Electronics
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

"""!
qwiic_button
============
Python module for the Qwiic Button.

This python package is a port of the exisiting [SparkFun Qwiic Button Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_Button_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun Qwiic Ecosystem](https://www.sparkfun.com/qwiic).
"""
#-----------------------------------------------------------------------------------

import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class definition
# as class variables, making them available without having to create a class instance.
# This allows higher level logic to rapidly create an index of qwiic devices at runtime.

# This is the name of the device
_DEFAULT_NAME = "Qwiic Button"

# Some devices have  multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the 
# device.
_QWIIC_BUTTON_DEFAULT_ADDRESS = 0x6F
_FULL_ADDRESS_LIST = list(range(0x08, 0x77+1))  # Full address list (excluding reserved addresses)
_FULL_ADDRESS_LIST.remove(_QWIIC_BUTTON_DEFAULT_ADDRESS >> 1)   # Remove default address from list
_AVAILABLE_I2C_ADDRESS = [_QWIIC_BUTTON_DEFAULT_ADDRESS]    # Initialize with default address
_AVAILABLE_I2C_ADDRESS.extend(_FULL_ADDRESS_LIST) # Add full range of I2C addresses

# Define the class that encapsulates the device being created. All information associated 
# with this device is encapsulated by this class. The device class should be the only value
# exported from this module.

class QwiicButton(object):
    """!
    "
    QwiicButton

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.

    @return **Object** The GPIO device object.
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Device ID for all Qwiic Buttons
    DEV_ID = 0x5D

    # Registers
    ID = 0x00
    FIRMWARE_MINOR = 0x01
    FIRMWARE_MAJOR = 0x02
    BUTTON_STATUS = 0x03
    INTERRUPT_CONFIG = 0x04
    BUTTON_DEBOUNCE_TIME = 0x05
    PRESSED_QUEUE_STATUS = 0x07
    PRESSED_QUEUE_FRONT = 0x08
    PRESSED_QUEUE_BACK = 0x0C
    CLICKED_QUEUE_STATUS = 0x10
    CLICKED_QUEUE_FRONT = 0x11
    CLICKED_QUEUE_BACK = 0x15
    LED_BRIGHTNESS = 0x19
    LED_PULSE_GRANULARITY = 0x1A
    LED_PULSE_CYCLE_TIME = 0x1B
    LED_PULSE_OFF_TIME = 0x1D
    I2C_ADDRESS = 0x1F

    # Status Flags
    event_available = 0
    has_been_clicked = 0
    is_pressed = 0

    # Interrupt Configuration Flags
    clicked_enable = 0
    pressed_enable = 0

    # Pressed Queue Status Flags
    pressed_pop_request = 0
    pressed_is_empty = 0
    pressed_is_full = 0

    # Clicked Queue Status Flags
    clicked_pop_request = 0
    clicked_is_empty = 0
    clicked_is_full = 0

    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
        else: 
            self._i2c = i2c_driver

    # -----------------------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?
    def is_connected(self):
        """!
        Determine if a Qwiic Button device is connected to the system.

        @return **bool** True if the device is connected, otherwise False.
        """
        return self._i2c.isDeviceConnected(self.address)
    
    # ------------------------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """!
        Initialize the operation of the Qwiic Button
            Run is_connected() and check the ID in the ID register

        @return **bool** Returns true if the intialization was successful, otherwise False.
        """
        if self.is_connected() == True:
            id = self._i2c.readByte(self.address, self.ID)
            
            if id == self.DEV_ID:
                return True
        
        return False
    
    # ------------------------------------------------
    # get_firmware_version()
    #
    # Returns the firmware version of the attached devie as a 16-bit integer.
    # The leftmost (high) byte is the major revision number, 
    # and the rightmost (low) byte is the minor revision number.
    def get_firmware_version(self):
        """!
        Read the register and get the major and minor firmware version number.

        @return **int** 16 bytes version number
        """
        version = self._i2c.readByte(self.address, self.FIRMWARE_MAJOR) << 8
        version |= self._i2c.readByte(self.address, self.FIRMWARE_MINOR)
        return version

    # -------------------------------------------------
    # set_I2C_address(new_address)
    #
    # Configures the attached device to attach to the I2C bus using the specified address
    def set_I2C_address(self, new_address):
        """!
        Change the I2C address of the Qwiic Button

        @param new_address: the new I2C address to set the Qwiic Button to
                The function itself checks if the entered parameter is a valid I2C address

        @return **bool** True if the change was successful, false otherwise.
        """
        # First, check if the specified address is valid
        if new_address < 0x08 or new_address > 0x77:
            return False
        
        # Write new address to the I2C address register of the Qwiic Button
        self._i2c.writeByte(self.address, self.I2C_ADDRESS, new_address)

        self.address = new_address
    
    # ---------------------------------------------------
    # get_I2C_address()
    #
    # Returns the I2C address of the device
    def get_I2C_address(self):
        """!
        Returns the current I2C address of the Qwiic Button

        @return **int** current I2C address
        """
        return self.address

    # ---------------------------------------------------
    # is_button_pressed()
    #
    # Returns 1 if the button/switch is pressed, 0 otherwise
    def is_button_pressed(self):
        """!
        Returns the value of the is_pressed status bit of the BUTTON_STATUS register

        @return **bool** is_pressed bit
        """
        # Read the button status register
        button_status = self._i2c.readByte(self.address, self.BUTTON_STATUS)
        # Convert to binary and clear all bits but is_pressed
        self.is_pressed = int(button_status) & ~(0xFB)
        # Shift is_pressed to the zero bit
        self.is_pressed = self.is_pressed >> 2
        # Return is_pressed as a bool
        return bool(self.is_pressed)
    
    # ----------------------------------------------------
    # has_button_been_clicked()
    #
    # Returns 1 if the button/switch is clicked, and 0 otherwise
    def has_button_been_clicked(self):
        """!
        Returns the value of the has_been_clicked status bit of the BUTTON_STATUS register

        @return **bool** has_been_clicked bit
        """
        # Read the button status register
        button_status = self._i2c.readByte(self.address, self.BUTTON_STATUS)
        # Convert to binary and clear all bits but has_been_clicked
        self.has_been_clicked = int(button_status) & ~(0xFD)
        # Shift has_been_clicked to the zero bit
        self.has_been_clicked = self.has_been_clicked >> 1
        # Return has_been_clicked as a bool
        return bool(self.has_been_clicked)
    
    # ------------------------------------------------------
    # get_debounce_time()
    #
    # Returns the time that the button waits for the mechanical
    # contacts to settle in milliseconds.
    def get_debounce_time(self):
        """!
        Returns the value in the BUTTON_DEBOUNCE_TIME register

        @return **int** debounce time in milliseconds
        """
        time_list = self._i2c.readBlock(self.address, self.BUTTON_DEBOUNCE_TIME, 2)
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2)
        return time
        
    # -------------------------------------------------------
    # set_debounce_time(time)
    #
    # Sets the time that the button waits for the mechanical 
    # contacts to settle in milliseconds.
    def set_debounce_time(self, time):
        """!
        Write two bytes into the BUTTON_DEBOUNCE_TIME register

        @param time: the time in milliseconds to set debounce time to
                The max debounce time is 0xFFFF milliseconds, but the function checks if
                the entered parameter is valid

        @return **void** Nothing
        """
        # First check that time is not too big
        if time > 0xFFFF:
            time = 0xFFFF
        time1 = time & ~(0xFF00)
        time2 = time & ~(0x00FF)
        time2 = time2 >> 8
        time_list = [time1, time2]
        # Then write two bytes
        self._i2c.writeWord(self.address, self.BUTTON_DEBOUNCE_TIME, time)
        
    # -------------------------------------------------------
    # enable_pressed_interrupt()
    #
    # The interrupt will be configured to trigger when the button
    # is pressed. If enableClickedInterrupt() has also been called,
    # then the interrupt will trigger on either a push or a click.
    def enable_pressed_interrupt(self):
        """!
        Set pressed_enable bit of the INTERRUPT_CONFIG register to a 1

        @return **Void** Nothing
        """
        # First, read the INTERRUPT_CONFIG register
        interrupt_config = self._i2c.readByte(self.address, self.INTERRUPT_CONFIG)
        self.pressed_enable = 1
        # Set the pressed_enable bit
        interrupt_config = interrupt_config | (self.pressed_enable << 1)
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, interrupt_config)
    
    # -------------------------------------------------------
    # disable_pressed_interrupt()
    # 
    # Interrupt will no longer be configured to trigger when the
    # button is pressed. If enable_clicked_interrupt() has also been called, 
    # then the interrupt will still trigger on the button click.
    def disable_pressed_interrupt(self):
        """!
        Clear the pressed_enable bit of the INTERRUPT_CONFIG register

        @return **Void** Nothing
        """
        # First, read the INTERRUPT_CONFIG register
        interrupt_config = self._i2c.readByte(self.address, self.INTERRUPT_CONFIG)
        self.pressed_enable = 0
        # Clear the pressed_enable bit
        interrupt_config = interrupt_config & ~(1 << 1)
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, interrupt_config)

    # -------------------------------------------------------
    # enable_clicked_interrupt()
    #
    # The interrupt will be configured to trigger when the button
    # is clicked. If enable_pressed_interrupt() has also been called, 
    # then the interrupt will trigger on either a push or a click.
    def enable_clicked_interrupt(self):
        """!
        Set the clicked_enable bit of the INTERRUPT_CONFIG register

        @return **Void** Nothing
        """
        # First, read the INTERRUPT_CONFIG register
        interrupt_config = self._i2c.readByte(self.address, self.INTERRUPT_CONFIG)
        self.clicked_enable = 1
        # Set the clicked_enable bit
        interrupt_config = interrupt_config | self.clicked_enable
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, interrupt_config)

    # -------------------------------------------------------
    # disable_clicked_interrupt()
    #
    # The interrupt will no longer be configured to trigger when
    # the button is clicked. If enable_pressed_interrupt() has also
    # been called, then the interrupt will still trigger on the 
    # button press.
    def disable_clicked_interrupt(self):
        """!
        Clear the clicked_enable bit of the INTERRUPT_CONFIG register

        @return **Void** Nothing
        """
        # First, read the INTERRUPT_CONFIG register
        interrupt_config = self._i2c.readByte(self.address, self.INTERRUPT_CONFIG)
        self.clicked_enable = 0
        # Clear the clicked_enable bit
        interrupt_config = interrupt_config & (self.clicked_enable)
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, interrupt_config)
    
    # -------------------------------------------------------
    # available()
    #
    # Returns the eventAvailble bit. This bit is set to 1 if a
    # button click or press event occurred.
    def available(self):
        """!
        Return the event_available bit of the BUTTON_STATUS register

        @return event_available bit
            :rtye: bool
        """
        # First, read BUTTON_STATUS register
        button_status = self._i2c.readByte(self.address, self.BUTTON_STATUS)
        # Convert to binary and clear all bits but the event_available bit
        self.event_available = int(button_status) & ~(0xFE)
        # Return event_available bit as a bool
        return bool(self.event_available)
    
    # -------------------------------------------------------
    # clear_event_bits()
    # 
    # Sets all button status bits (is_pressed, has_been_clicked, 
    # and event_available) to zero.
    def clear_event_bits(self):
        """!
        Clear the is_pressed, has_been_clicked, and event_available
            bits of the BUTTON_STATUS register

        @return **Void** Nothing
        """
        # First, read BUTTON_STATUS register
        button_status = self._i2c.readByte(self.address, self.BUTTON_STATUS)
        # Convert to binary and clear the last three bits
        button_status = int(button_status) & ~(0x7)
        # Write to BUTTON_STATUS register
        self._i2c.writeByte(self.address, self.BUTTON_STATUS, button_status)
        
    # -------------------------------------------------------
    # reset_interrupt_config()
    #
    # Resets the interrupt configuration back to defaults.
    def reset_interrupt_config(self):
        """!
        Enable pressed and clicked interrupts and clear the
            event_available bit of BUTTON_STATUS register

        @return **Void** Nothing
        """
        self.pressed_enable = 1
        self.clicked_enable = 1
        # write 0b11 to the INTERRUPT_CONFIG register
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, 0b11)
        self.event_available = 0
        # Clear has_been_clicked, is_pressed too
        # TODO: not sure if this is right
        self.has_been_clicked = 0
        self.is_pressed = 0
        # Clear the BUTTON_STATUS register by writing a 0
        self._i2c.writeByte(self.address, self.BUTTON_STATUS, 0x00)
    
    # -------------------------------------------------------
    # is_pressed_queue_full()
    #
    # Returns true if queue of button press time stamps is full,
    # and false otherwise.
    def is_pressed_queue_full(self):
        """!
        Returns the is_full bit of the PRESSED_QUEUE_STATUS register

        @return **bool** pressed_is_full
        """
        # First, read the PRESSED_QUEUE_STATUS register
        pressed_queue_stat = self._i2c.readByte(self.address, self.PRESSED_QUEUE_STATUS)
        # Convert to binary and clear all bits but isFull
        self.pressed_is_full = int(pressed_queue_stat) & ~(0xFB)
        self.pressed_is_full = self.pressed_is_full >> 2
        # Return pressed_is_full as a bool
        return bool(self.pressed_is_full)
    
    # -------------------------------------------------------
    # is_pressed_queue_empty()
    #
    # Returns true if the queue of button press time stamps is
    # empty, and false otherwise.
    def is_pressed_queue_empty(self):
        """!
        Returns the is_empty bit of the PRESSED_QUEUE_STATUS register

        @return **bool** pressed_is_empty
        """
        # First, read the PRESSED_QUEUE_STATUS register
        pressed_queue_stat = self._i2c.readByte(self.address, self.PRESSED_QUEUE_STATUS)
        # Convert to binary and clear all bits but is_empty
        self.pressed_is_empty = int(pressed_queue_stat) & ~(0xFD)
        # Shift pressed_is_empty to the zero bit
        self.pressed_is_empty = self.pressed_is_empty >> 1
        # Return pressed_is_empty as a bool
        return bool(self.pressed_is_empty)

    # ------------------------------------------------------
    # time_since_last_press()
    #
    # Returns how many milliseconds it has been since the last
    # button press. Since this returns a 32-bit int, it will 
    # roll over about every 50 days.
    def time_since_last_press(self):
        """!
        Returns the four bytes of PRESSED_QUEUE_FRONT.
            Time in milliseconds.

        @return **int** PRESSED_QUEUE_FRONT
        """
        time_list = self._i2c.readBlock(self.address, self.PRESSED_QUEUE_FRONT, 4)
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2) + int(time_list[2]) * 16 ** (4) + int(time_list[3]) * 16 ** (6) 
        return time
        
    # -------------------------------------------------------
    # time_since_first_press()
    #
    # Returns how many milliseconds it has been since the first 
    # button press. Since this returns a 32-bit int, it will 
    # roll over about every 50 days.
    def time_since_first_press(self):
        """!
        Returns the four bytes of PRESSED_QUEUE_BACK.
            Time in milliseconds

        @return **int** PRESSED_QUEUE_BACK
        """
        time_list = self._i2c.readBlock(self.address, self.PRESSED_QUEUE_BACK, 4)
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2) + int(time_list[2]) * 16 ** (4) + int(time_list[3]) * 16 ** (6)
        return time
        
    # -------------------------------------------------------
    # pop_pressed_queue()
    #
    # Returns the oldest value in the queue (milliseconds since 
    # first button press), and then removes it.
    def pop_pressed_queue(self):
        """!
        Returns contents of PRESSED_QUEUE_BACK register and 
            writes a 1 to popRequest bit of PRESSED_QUEUE_STATUS
            register.

        @return **int** PRESSED_QUEUE_BACK
        """
        # Get the time in milliseconds since the button was first pressed
        temp_data = self.time_since_first_press()
        # Read PRESSED_QUEUE_STATUS register
        pressed_queue_stat = self._i2c.readByte(self.address, self.PRESSED_QUEUE_STATUS)
        self.pressed_pop_request = 1
        # Set pop_request bit to 1
        pressed_queue_stat = pressed_queue_stat | (self.pressed_pop_request)
        self._i2c.writeByte(self.address, self.PRESSED_QUEUE_STATUS, pressed_queue_stat)
        return temp_data
    
    # ---------------------------------------------------------
    # is_clicked_queue_full()
    #
    # Returns true if the queue of button click timestamps is full
    # and false otherwise.
    def is_clicked_queue_full(self):
        """!
        Reads the is_full bit of the CLICKED_QUEUE_STATUS register

        @return **bool** clicked_is_full
        """
        # First, read the CLICKED_QUEUE_STATUS register
        clicked_queue_stat = self._i2c.readByte(self.address, self.CLICKED_QUEUE_STATUS)
        # Convert to binary and clear all bits but clicked_is_full
        self.clicked_is_full = int(clicked_queue_stat) & ~(0xFB)
        self.clicked_is_full = self.clicked_is_full >> 2
        # Return clicked_is_full as a bool
        return bool(self.clicked_is_full)
    
    # ----------------------------------------------------------
    # is_clicked_queue_empty()
    #
    # Returns true if the queue click timestamps is empty and false
    # otherwise.
    def is_clicked_queue_empty(self):
        """!
        Reads the is_empty bit of the CLICKED_QUEUE_STATUS register

        @return **bool** clicked_is_empty
        """
        # First, read the CLICKED_QUEUE_STATUS register
        clicked_queue_stat = self._i2c.readByte(self.address, self.CLICKED_QUEUE_STATUS)
        # Convert to binary and clear all bits but clicked_is_empty
        self.clicked_is_empty = int(clicked_queue_stat) & ~(0xFD)
        # Shift clicked_is_empty to the zero bit
        self.clicked_is_empty = self.clicked_is_empty >> 1
        # Return clicked_is_empty as a bool
        return bool(self.clicked_is_empty)

    # ------------------------------------------------------------
    # time_since_last_click()
    #
    # Returns how many milliseconds it has been since the last button
    # click. Since this returns a 32-bit int, it will roll over about
    # every 50 days
    def time_since_last_click(self):
        """!
        Returns the four bytes of CLICKED_QUEUE_FRONT register.
            Time in milliseconds

        @return **int** CLICKED_QUEUE_FRONT
        """
        time_list = self._i2c.readBlock(self.address, self.CLICKED_QUEUE_FRONT, 4)
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2) + int(time_list[2]) * 16 ** (4) + int(time_list[3]) * 16 ** (6)
        return time
        
    # ------------------------------------------------------------
    # time_since_first_click()
    #
    # Returns how many milliseconds it has been since the first button
    # click. Since this returns a 32-bit int, it will roll over about 
    # every 50 days
    def time_since_first_click(self):
        """!
        Returns the four bytes of CLICKED_QUEUE_BACK register.
            Time in milliseconds

        @return **int** CLICKED_QUEUE_BACK
        """
        time_list = self._i2c.readBlock(self.address, self.CLICKED_QUEUE_BACK, 4)
        time = int(time_list[0]) + int(time_list[1]) * 16 ** (2) + int(time_list[2]) * 16 ** (4) + int(time_list[3]) * 16 ** (6)
        return time
        
    # -------------------------------------------------------------
    # pop_clicked_queue()
    #
    # Returns the oldest value in the queue (milliseconds since first
    # button click), and then removes it.
    def pop_clicked_queue(self):
        """!
        Returns contents of CLICKED_QUEUE_BACK register and 
            writes a 1 to popRequest bit of CLICKED_QUEUE_STATUS
            register.

        @return **int** CLICKED_QUEUE_BACK
        """
        # Get the time in milliseconds since the button was first clicked
        temp_data = self.time_since_first_click()
        # Read CLICKED_QUEUE_STATUS register
        clicked_queue_stat = self._i2c.readByte(self.address, self.CLICKED_QUEUE_STATUS)
        self.clicked_pop_request = 1
        # Set pop_request bit to 1
        clicked_queue_stat = clicked_queue_stat | (self.clicked_pop_request)
        self._i2c.writeByte(self.address, self.CLICKED_QUEUE_STATUS, clicked_queue_stat)
        return temp_data

    # -------------------------------------------------------------
    # LED_config(brightness, cycle_time, off_time, granularity)
    #
    # Configures the LED with the given max brightness, granularity
    # (1 is fine for most applications), cycle time, and off time.
    def LED_config(self, brightness, cycle_time, off_time, granularity = 1):
        """!
        Write brightness, cycle_time, off_time, and granularity
            parameters to their respective registers: LED_BRIGHTNESS,
            LED_PULSE_CYCLE_TIME, LED_PULSE_OFF_TIME, LED_PULSE_GRANULARITY

        @param brightness: between 0 (led off) and 255 (max brightness)
        @param cycle_time: total pulse cycle in in milliseconds
                Range 0 to 0xFFFF
        @param off_time: off time between pulses in milliseconds
                Range 0 to 0xFFFF
        @param granularity: the amount of steps it takes to get to led brightness
                If not provided, granularity defaults to 1

        @return **Void** Nothing
        """
        # Write brightness
        self._i2c.writeByte(self.address, self.LED_BRIGHTNESS, brightness)
        # Write cycle_time
        self._i2c.writeWord(self.address, self.LED_PULSE_CYCLE_TIME, cycle_time)
        # Write off_time
        self._i2c.writeWord(self.address, self.LED_PULSE_OFF_TIME, off_time)
        # Write granularity
        self._i2c.writeByte(self.address, self.LED_PULSE_GRANULARITY, granularity)
    
    # --------------------------------------------------------------
    # LED_off()
    #
    # Turn the onboard LED off
    def LED_off(self):
        """!
        Write zero's to all the LED registers: LED_BRIGHTNESS,
            LED_PULSE_CYCLE_TIME, LED_PULSE_OFF_TIME, and LED_PULSE_GRANULARITY
            defaults to zero.

        @return **void** Nothing
        """
        self.LED_config(0, 0, 0)
    
    # --------------------------------------------------------------
    # LED_on(brightness)
    #
    # Turns the onboard LED on with specified brightness. Set brightness
    # to an integer between 0 and 255, where 0 is off and 255 is max
    # brightness.
    def LED_on(self, brightness):
        """!
        Set LED on without pulse

        @param brightness: between 0 (led off) and 255 (max brightness)

        @return **Void** Nothing
        """
        self.LED_config(brightness, 0, 0)
