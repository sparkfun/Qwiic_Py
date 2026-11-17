#-----------------------------------------------------------------------------
# qwiic_kx13x.py
#
# Python library for the SparkFun qwiic KX13X sensor.
#
# This sensor is available on the SparkFun Environmental Combo Breakout board.
#   https://www.sparkfun.com/products/14348
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
#
# This python library supports the SparkFun Electroncis qwiic
# qwiic sensor/board ecosystem
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
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
# This is mostly a port of existing Arduino functionaly, so pylint is sad.
# The goal is to keep the public interface pthonic, but internal is internal
#
# pylint: disable=line-too-long, bad-whitespace, invalid-name, too-many-public-methods
#

"""!
qwiic_kx13x
============
Python module for the qwiic kx132/4 accelerometers.
This python package is a port of the existing [SparkFun KX13X Arduino Library](https://github.com/sparkfun/SparkFun_KX13X_Arduino_Library)
This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

#-----------------------------------------------------------------------------
import qwiic_i2c
from time import sleep

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at
# runtine
#
# The name of this device
_DEFAULT_NAME = "Qwiic KX13X"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x1F, 0x1E]

# Default Setting Values

# Part ID identifying KX132 and KX134 respectively
_WHO_AM_I = [0x3D, 0x46]

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class AccelerationData(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class QwiicKX13XCore(object):
    """!
    QwiicKX13XCore

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.

    @return **Object** The KX13X device object.
    """
    # Constructor
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    TOTAL_ACCEL_DATA_16BIT = 6
    TOTAL_ACCEL_DATA_8BIT  = 3
    MAX_BUFFER_LENGTH      = 32

    XLSB = 0
    XMSB = 1
    YLSB = 2
    YMSB = 3
    ZLSB = 4
    ZMSB = 5

    DEFAULT_SETTINGS     =  0xC0
    INT_SETTINGS         =  0xE0
    SOFT_INT_SETTINGS    =  0xE1
    BUFFER_SETTINGS      =  0xE2
    TILT_SETTINGS        =  0xE3

    COTR_DEF_STATE       =  0x55
    COTR_POS_STATE       =  0xAA

    BUFFER_16BIT_SAMPLES =  0x01
    BUFFER_8BIT_SAMPLES  =  0x00
    BUFFER_MODE_FIFO     =  0x00
    BUFFER_MODE_STREAM   =  0x01
    BUFFER_MODE_TRIGGER  =  0x02


    # Register names for the KX13X

    KX13X_MAN_ID           = 0x00
    KX13X_PART_ID          = 0x01
    KX13X_XADP_L           = 0x02
    KX13X_XADP_H           = 0x03
    KX13X_YADP_L           = 0x04
    KX13X_YADP_H           = 0x05
    KX13X_ZADP_L           = 0x06
    KX13X_ZADP_H           = 0x07
    KX13X_XOUT_L           = 0x08
    KX13X_XOUT_H           = 0x09
    KX13X_YOUT_L           = 0x0A
    KX13X_YOUT_H           = 0x0B
    KX13X_ZOUT_L           = 0x0C
    KX13X_ZOUT_H           = 0x0D
    # 0x0E - 0x11 Reserved
    KX13X_COTR             = 0x12
    KX13X_WHO_AM_I         = 0x13
    KXI3X_TSCP             = 0x14
    KX13X_TSPP             = 0x15
    KX13X_INS1             = 0x16
    KX13X_INS2             = 0x17
    KX13X_INS3             = 0x18
    KX13X_STATUS_REG       = 0x19
    KX13X_INT_REL          = 0x1A
    KX13X_CNTL1            = 0x1B
    KX13X_CNTL2            = 0x1C
    KX13X_CNTL3            = 0x1D
    KX13X_CNTL4            = 0x1E
    KX13X_CNTL5            = 0x1F
    KX13X_CNTL6            = 0x20
    KX13X_ODCNTL           = 0x21
    KX13X_INC1             = 0x22
    KX13X_INC2             = 0x23
    KX13X_INC3             = 0x24
    KX13X_INC4             = 0x25
    KX13X_INC5             = 0x26
    KX13X_INC6             = 0x27
    # 0x28 Reserved
    KX13X_TILT_TIMER       = 0x29
    KX13X_TDTRC            = 0x2A
    KX13X_TDTC             = 0x2B
    KX13X_TTH              = 0x2C
    KX13X_TTL              = 0x2D
    KX13X_FTD              = 0x2E
    KX13X_STD              = 0x2F
    KX13X_TLT              = 0x30
    KX13X_TWS              = 0x31
    KX13X_FFTH             = 0x32
    KX13X_FFC              = 0x33
    KX13X_FFCNTL           = 0x34
    # 0x35 - 0x36 Reserved
    KX13X_TILT_ANGLE_LL    = 0x37
    KX13X_TILT_ANGLE_HL    = 0x38
    KX13X_HYST_SET         = 0x39
    KX13X_LP_CNTL1         = 0x3A
    KX13X_LP_CNTL2         = 0x3B
    # 0x3C - 0x48 Reserved
    KX13X_WUFTH            = 0x49
    KX13X_BTSWUFTH         = 0x4A
    KX13X_BTSTH            = 0x4B
    KX13X_BTSC             = 0x4C
    KX13X_WUFC             = 0x4D
    # 0x4E - 0x5C Reserved
    KX13X_SELF_TEST        = 0x5D
    KX13X_BUF_CNTL1        = 0x5E
    KX13X_BUF_CNTL2        = 0x5F
    KX13X_BUF_STATUS_1     = 0x60
    KX13X_BUF_STATUS_2     = 0x61
    KX13X_BUF_CLEAR        = 0x62
    KX13X_BUF_READ         = 0x63
    KX13X_ADP_CNTL1        = 0x64
    KX13X_ADP_CNTL2        = 0x65
    KX13X_ADP_CNTL3        = 0x66
    KX13X_ADP_CNTL4        = 0x67
    KX13X_ADP_CNTL5        = 0x68
    KX13X_ADP_CNTL6        = 0x69
    KX13X_ADP_CNTL7        = 0x6A
    KX13X_ADP_CNTL8        = 0x6B
    KX13X_ADP_CNTL9        = 0x6C
    KX13X_ADP_CNTL10       = 0x6D
    KX13X_ADP_CNTL11       = 0x6E
    KX13X_ADP_CNTL12       = 0x6F
    KX13X_ADP_CNTL13       = 0x70
    KX13X_ADP_CNTL14       = 0x71
    KX13X_ADP_CNTL15       = 0x72
    KX13X_ADP_CNTL16       = 0x73
    KX13X_ADP_CNTL17       = 0x74
    KX13X_ADP_CNTL18       = 0x75
    KX13X_ADP_CNTL19       = 0x76
    # Reserved 0x77 - 0x7F

    KX13X_SUCCESS       = 0x00
    KX13X_GENERAL_ERROR = 0x01
    KX13X_I2C_ERROR     = 0x02

    # HARDWARE_INTERRUPTS
    HI_TILT_POSITION  = 0x01
    HI_WAKE_UP        = 0x02
    HI_TAP_DOUBLE_TAP = 0x04
    HI_BACK_TO_SLEEP  = 0x08
    HI_DATA_READY     = 0x10
    HI_WATERMARK      = 0x20
    HI_BUFFER_FULL    = 0x40
    HI_FREEFALL       = 0x80



    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self.address = self.available_addresses[0] if address is None else address

        # load the I2C driver if one isn't provided

        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver
        
        self.raw_output_data = AccelerationData(0,0,0)

    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """!
        Determine if a KX13X device is conntected to the system..

        @return **bool** True if the device is connected, otherwise False.
        """
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def beginCore(self):
        """!
        Initialize the operation of the KX13X module

        @return **bool** Returns true of the initializtion was successful, otherwise False.
        """
        # are we who we need to be?
        chipID = self._i2c.readByte(self.address, self.KX13X_WHO_AM_I)
        if chipID not in _WHO_AM_I:
            print("Invalid Chip ID: 0x" % chipID)

        return chipID

    def initialize(self, settings = DEFAULT_SETTINGS):
        """!
        Initialize configures the accelerometer's registers into a number of
            different modes: asyncronous, hardware trigger, software trigger,
            and buffer.

        @param settings: A class constant indicating which setting to
                configure: DEFAULT_SETTINGS, INT_SETTINGS, SOFT_INT_SETTINGS,
                BUFFER_SETTINGS.

        @return No return value.
        """
        self.enable_accel(False)

        if settings == self.DEFAULT_SETTINGS:
            self._i2c.writeByte(self.address, self.KX13X_CNTL1, self.DEFAULT_SETTINGS)
        elif settings == self.INT_SETTINGS:
            self.set_interrupt_pin(True, 1)
            self.route_hardware_interrupt(self.HI_DATA_READY)
            self._i2c.writeByte(self.address, self.KX13X_CNTL1, self.INT_SETTINGS)
        elif settings == self.SOFT_INT_SETTINGS:
            self._i2c.writeByte(self.address, self.KX13X_CNTL1, self.INT_SETTINGS)
        elif settings == self.BUFFER_SETTINGS:
            self.set_interrupt_pin(True, 1)
            self.route_hardware_interrupt(self.HI_BUFFER_FULL)
            self.set_buffer_operation(self.BUFFER_MODE_FIFO, self.BUFFER_16BIT_SAMPLES)
            self._i2c.writeByte(self.address, self.KX13X_CNTL1, self.INT_SETTINGS)
        # Space fore more default settings

    def run_command_test(self):
        """!
        This function runs the self test built into the accelerometer.

        @return **bool** Returns true upon successful test, and false otherwise.
        """
        reg_val = self._i2c.readByte(self.address, self.KX13X_CNTL2)
        reg_val &= 0xBF
        reg_val |= (1 << 6)
        self._i2c.writeByte(self.address, self.KX13X_CNTL2 , reg_val)

        reg_val = self._i2c.readByte(self.address, self.KX13X_COTR)
        if reg_val == self.COTR_POS_STATE:
            return True
        else:
            return False


    def enable_accel(self, enable=True):
        """!
        This functions controls the accelerometers power on and off state.

        @param enable: True or false indicating power on or off
            respectively.

        @return **bool** Returns false when an incorrect argumen has been passed.
        """
        if enable != True and enable != False:
            return False

        reg_val = self._i2c.readByte(self.address, self.KX13X_CNTL1)
        reg_val &= 0x7F
        reg_val |= (enable << 7)
        self._i2c.writeByte(self.address, self.KX13X_CNTL1 , reg_val)

    def accel_control(self, enable=True):
        """!
        Same as above enable_accel(), but with a different name to preserve backwards compatibility
        """
        self.enable_accel(enable)

    def get_accel_state(self):
        """!
        Retrieves the state of the accelerometer: on or off.

        @return **int** Returns bit indicating the accelerometers power state.
        """
        reg_val = self._i2c.readByte(self.address, self.KX13X_CNTL1)
        return (reg_val & 0x80) >> 7

    def set_range(self, kx13x_range):
        """!
        Sets the range reported by the accelerometer. For the KX132, the
            range is from 2G - 16G and for the KX134 it's 8G - 32G.

        @param kx13x_range: Eight constants (four per version) represent values from zero to
            four indicating the range to be set:
                KX132_RANGE2G,
                KX132_RANGE4G,
                KX132_RANGE8G,
                KX132_RANGE16G
                KX134_RANGE8G,
                KX134_RANGE16G,
                KX134_RANGE32G,
                KX134_RANGE64G.

        @return **bool** Returns false if an incorrect argument is given.
        """

        if kx13x_range < 0 or kx13x_range > 3:
            return False

        reg_val = self._i2c.readByte(self.address, self.KX13X_CNTL1)
        reg_val &= 0xE7
        reg_val |= (kx13x_range << 3)
        self._i2c.writeByte(self.address, self.KX13X_CNTL1 , reg_val)


    def set_output_data_rate(self, rate):
        """!
        Sets the rate at which the accelerometer outputs data.

        @param rate: A value from zero to fifteen indicating which rate to
            set.

        @return **bool** Returns false if an an incorrect argument is given.
        """
        if rate < 0 or rate > 15:
            return False

        accel_state = self.get_accel_state()
        self.enable_accel(False)

        reg_val = self._i2c.readByte(self.address, self.KX13X_ODCNTL)
        reg_val &= 0x40
        reg_val |= rate
        self._i2c.writeByte(self.address, self.KX13X_ODCNTL , reg_val)
        self.enable_accel(accel_state)


    def get_output_data_rate(self):
        """!
        Gets the accelerometers output data rate.

        @return **float** Accelerometer's data rate in hertz.
        """

        reg_val = self._i2c.readByte(self.address, self.KX13X_ODCNTL)
        reg_val &= 0x40
        return (0.78 * (2 * reg_val))

    output_data_rate = property(get_output_data_rate, set_output_data_rate)

    def set_interrupt_pin(self, enable, polarity = 0, pulse_width = 0,
                          latch_control = False):
        """!
        Sets all of whether the data ready bit is reported to the hardware
            interrupt pin, the polarity of the signal (HIGH or LOW), the width
            of the pulse, and how the interrupt is cleared.

        @param enable: Sets hardware interrupt to "on" or "off".
        @param polarity: Sets the active state of the hardware pin - HIGH
            or LOW.
        @param pulse_width: Sets the width of the interrupt pulse.
        @param latch_control: Sets how the interrupt pin is cleared.

        @return **bool** Returns false if an an incorrect argument is given.
        """
        if enable != True and enable != False:
            return False
        if polarity != 1 and polarity != 0:
            return False
        if pulse_width != 1 and pulse_width != 0:
            return False
        if latch_control < 0 or latch_control > 4:
            return False

        accel_state = self.get_accel_state()
        self.enable_accel(False)

        combined_arguments = (pulse_width << 6) | (enable << 5) | (polarity << 4) | (latch_control << 3)

        reg_val = self._i2c.readByte(self.address, self.KX13X_INC1)
        reg_val &= 0x07
        reg_val |= combined_arguments
        self._i2c.writeByte(self.address, self.KX13X_INC1 , reg_val)

    def route_hardware_interrupt(self, rdr, pin = 1):
        """!
        Determines which interrupt is reported: freefall, buffer full,
            watermark, data ready, back to sleep, tap/double tap, wakeup or
            tilt. Also which hardware pin its reported on: one or two.

        @param rdr: The interrupt to be reported.
        @param pin: The hardware pin on which the interrupt is reported.

        @return **bool** Returns true after configuring the register and false if an an
            incorrect argument is given.
        """
        if rdr < 0 or rdr > 128:
            return False
        if pin != 1 and pin != 2:
            return False

        accel_state = self.get_accel_state()
        self.enable_accel(False)

        if pin == 1:
            self._i2c.writeByte(self.address, self.KX13X_INC4 , rdr)
            self.enable_accel(accel_state)
            return True
        else:
            self._i2c.writeByte(self.address, self.KX13X_INC6 , rdr)
            self.enable_accel(accel_state)
            return True
    
    def enable_phys_interrupt(self, enable = True, pin = 1):
        """!
        Enables interrupts to be routed to the interrupt pins.

        @param enable: Whether to enable or disable the physical interrupt pin
        @param pin: The interrupt pin to enable or disable

        @return **bool** Returns true after configuring the register and false if an an
            incorrect argument is given.
        """
        if pin > 2 or pin <= 0:
            return False
        
        # Same bit for both pins
        kIenReadyBitMask = 0b1 << 5
            
        if pin == 1:
            reg_val = self._i2c.readByte(self.address, self.KX13X_INC1)
            
            reg_val &= ~kIenReadyBitMask
            if (enable):
                reg_val |= kIenReadyBitMask

            self._i2c.writeByte(self.address, self.KX13X_INC1, reg_val)
    
        if pin == 2:
            reg_val = self._i2c.readByte(self.address, self.KX13X_INC5)
            
            reg_val &= ~kIenReadyBitMask
            if (enable):
                reg_val |= kIenReadyBitMask

            self._i2c.writeByte(self.address, self.KX13X_INC5, reg_val)
        
        return True


    def clear_interrupt(self):
        """!
        Clears the interrupt.

        @return No return value.
        """
        self._i2c.readByte(self.address, self.KX13X_INT_REL)

    def data_ready(self):
        """!
        Reads the register indicating whether data is ready to be read.

        @return **bool** Returns true if data is ready to be read and false
            otherwise.
        """
        reg_val = self._i2c.readByte(self.address, self.KX13X_INS2)
        if reg_val & 0x10:
            return True
        else:
            return False
    
    def data_trigger(self):
        """!
        Same as above data_ready(), but with a different name to preserve backwards compatibility
        """
        return self.data_ready()

    def set_buffer_threshold(self, threshold):
        """!
        Sets how many samples are stored in the buffer.

        @param threshold: The number of samples to be stored.

        @return **bool** Returns false if an incorrect argument is given.
        """
        if threshold < 2 or threshold > 171:
            return False

        resolution = self._i2c.readByte(self.address, self.KX13X_BUF_CNTL2)
        resolution &= 0x40
        resolution = resolution >> 6

        if threshold > 86 and resolution == 1: # At 16bit resolution - max samples: 86
            threshold == 86

        self._i2c.writeByte(self.address, self.KX13X_BUF_CNTL1, threshold)

    def set_buffer_operation_and_resolution(self, operation_mode, resolution=True):
        """!
        Sets the mode and resolution of the samples stored in the buffer.

        @param operation_mode: Sets the mode:
                                   BUFFER_MODE_FIFO
                                   BUFFER_MODE_STREAM
                                   BUFFER_MODE_TRIGGER
        @param resolution: Sets the resolution of the samples, 8 or 16 bit. (True = 16 bit, False = 8 bit)

        @return **bool** Returns false if an incorrect argument is given.

            NOTE: This combines the functionality of the setBufferResolution and setBufferOperationMode methods from the arduino library
        """
        if resolution < 0 or resolution > 1:
            return False
        if operation_mode < 0 or operation_mode > 2:
            return False

        combined_arguments = (resolution << 6) | operation_mode

        reg_val = self._i2c.readByte(self.address, self.KX13X_BUF_CNTL2)
        reg_val &= 0xBC
        reg_val |= combined_arguments
        self._i2c.writeByte(self.address, self.KX13X_BUF_CNTL2 , reg_val)
    
    def set_buffer_operation(self, operation_mode, resolution):
        """!
        Same as above set_buffer_operation_and_resolution(), but with a different name to preserve backwards compatibility
        """
        self.set_buffer_operation_and_resolution(operation_mode, resolution)

    def enable_buffer_and_interrupt(self, enable = True, enable_interrupt = True):
        """!
        Enables the buffer and whether the buffer triggers an interrupt
            when full.

        @param enable: Enables the buffer.
        @param enable: Enables the buffer's interrupt.

        @return **bool** Returns false if an incorrect argument is given.

            NOTE: This combines the functionality of the enableSampleBuffer and enableBufferInt methods from the arduino library
        """
        if enable != True and enable != False:
            return False
        if enable_interrupt != True and enable_interrupt != False:
            return False

        combined_arguments = (enable << 7) | (enable_interrupt << 5)

        reg_val = self._i2c.readByte(self.address, self.KX13X_BUF_CNTL2)
        reg_val &= 0x5F
        reg_val |= combined_arguments
        self._i2c.writeByte(self.address, self.KX13X_BUF_CNTL2 , reg_val)

    def get_raw_accel_data(self):
        """!
        Retrieves the raw register values representing accelerometer data.

            Note: this method does not check if the registers contain valid data.
            The user needs to do that externally by calling dataReady
            or using the INT pins to indicate that data is ready.
        """

        accel_data = self._i2c.readBlock(self.address, self.KX13X_XOUT_L, self.TOTAL_ACCEL_DATA_16BIT)
        
        ux = (accel_data[self.XMSB] << 8) | accel_data[self.XLSB]
        uy = (accel_data[self.YMSB] << 8) | accel_data[self.YLSB]
        uz = (accel_data[self.ZMSB] << 8) | accel_data[self.ZLSB]

        # Convert to signed 16-bit ints
        if ux > 32767:
            ux -= 65536
        if uy > 32767:
            uy -= 65536
        if uz > 32767:
            uz -= 65536

        self.raw_output_data.x = ux
        self.raw_output_data.y = uy
        self.raw_output_data.z = uz

    def get_raw_accel_buffer_data(self, sixteenBit = -1):
        """!
        Retrieves the raw buffer values representing accelerometer data.

            If sixteenBit is -1 (the default), the code reads the Buffer Control Register 2 bres
            bit to determine if the buffer data is 8-bit or 16-bit. You can speed up the code
            by setting sixteenBit to: 0 for 8-bit data; 1 for 16-bit data.

            Note: theis method does not check if the buffer contains valid data.
            The user needs to do that externally by calling getSampleLevel
            or using the INT pins to indicate that data is ready.

        @return **bool** Returns false if an incorrect argument is given.
        """
        if sixteenBit > 1 or sixteenBit < -1:
            return False
        
        if sixteenBit == -1:
            # Need to manually check the resolution
            reg_val = self._i2c.readByte(self.address, self.KX13X_BUF_CNTL2)

            kBresMask = 1 << 6
            if reg_val & kBresMask:
                sixteenBit = 1
            else:
                sixteenBit = 0

        if sixteenBit == 1:
            # 16 bit data
            accel_data = self._i2c.readBlock(self.address, self.KX13X_BUF_READ, self.TOTAL_ACCEL_DATA_16BIT)
            
            ux = (accel_data[self.XMSB] << 8) | accel_data[self.XLSB]
            uy = (accel_data[self.YMSB] << 8) | accel_data[self.YLSB]
            uz = (accel_data[self.ZMSB] << 8) | accel_data[self.ZLSB]

        if sixteenBit == 0:
            # 8 bit data
            accel_data = self._i2c.readBlock(self.address, self.KX13X_BUF_READ, self.TOTAL_ACCEL_DATA_8BIT)
            
            ux = (accel_data[0] << 8)
            uy = (accel_data[1] << 8)
            uz = (accel_data[2] << 8)
        
        # Convert to signed 16-bit ints
        if ux > 32767:
            ux -= 65536
        if uy > 32767:
            uy -= 65536
        if uz > 32767:
            uz -= 65536

        self.raw_output_data.x = ux
        self.raw_output_data.y = uy
        self.raw_output_data.z = uz

        return True


    def software_reset(self):
        """!
        Resets the accelerometer

            Kionix Technical Reference Manual says:
            "To change the value of the SRST bit, the PC1 bit in CNTL1 register must first be set to 0."

            Kionix TN027 "Power On Procedure" says to:
            Write 0x00 to register 0x7F
            Write 0x00 to CNTL2
            Write 0x80 (SRST) to CNTL2

            Kionix Technical Reference Manual says:
            "For I2C Communication: Setting SRST = 1 will NOT result in an ACK, since the part immediately
            enters the RAM reboot routine. NACK may be used to confirm this command."
            However, we've not seen the NACK when writing the SRST bit. That write always seems to be ACK'd as normal.
            But, the _next_ I2C transaction _does_ get NACK'd...
            The solution seems to be to keep trying to read CNTL2 and wait for the SRST bit to be cleared.

        @return True if the reset was successful, False otherwise.
        """
        
        self.enable_accel(False)

        self._i2c.writeByte(self.address, 0x7F, 0x00)
        self._i2c.writeByte(self.address, self.KX13X_CNTL2, 0x00)
        self._i2c.writeByte(self.address, self.KX13X_CNTL2, 0x80)

        # Wait for the SRST bit to be cleared. Reset takes about 2ms. Timeout if we still see the SRST bit set after 10ms.
        sleep(0.003)
        reset_read_tries = 0
        while reset_read_tries < 10:
            if self._i2c.readByte(self.address, self.KX13X_CNTL2) & 0x80 == 0:
                return True

            reset_read_tries += 1
            sleep(0.001)
        
        return False
    
    def enable_data_engine(self, enable=True):
        """!
        Enables the data ready bit.

        @param enable: True to enable the data engine, False to disable it.
        """

        kDataReadyBitMask = 0b1 << 5
        reg_val = self._i2c.readByte(self.address, self.KX13X_CNTL1)
        
        reg_val &= ~kDataReadyBitMask
        if (enable):
            reg_val |= kDataReadyBitMask

        self._i2c.writeByte(self.address, self.KX13X_CNTL1, reg_val)
    
    def enable_tap_engine(self,enable=True):
        """!
        Enables the tap and double tap features of the accelerometers

        @param enable: True to enable the tap engine, False to disable it.
        """

        kTapEngineBitMask = 0b1 << 2
        reg_val = self._i2c.readByte(self.address, self.KX13X_CNTL1)
        
        reg_val &= ~kTapEngineBitMask
        if (enable):
            reg_val |= kTapEngineBitMask

        self._i2c.writeByte(self.address, self.KX13X_CNTL1, reg_val)
    
    def enable_direct_tap_interrupt(self, enable=True):
        """!
        Enables reporting on the direction of the latest generated tap.

        @param enable: True to enable the direct tap interrupt, False to disable it.
        """

        kDirectTapInterruptBitMask = 0b1 << 0
        reg_val = self._i2c.readByte(self.address, self.KX13X_TDTRC)
        
        reg_val &= ~kDirectTapInterruptBitMask
        if (enable):
            reg_val |= kDirectTapInterruptBitMask

        self._i2c.writeByte(self.address, self.KX13X_TDTRC, reg_val)


    def tap_detected(self):
        """!
        Checks the tap interrupt bit indicating that a tap has
            been detected.

        @return True if a tap has been detected, False otherwise.
        """

        kTapDetectedShift = 2
        kTapDetectedMask = 0b11 << 2
        reg_val = self._i2c.readByte(self.address, self.KX13X_INS2)
        
        tap_result = (reg_val & kTapDetectedMask) >> kTapDetectedShift

        kSingleTapStatusResult = 0x01
        return tap_result == kSingleTapStatusResult

    def get_direction(self):
        """!
        If the tap direction bit is enabled, this register will report
            the direction of the detected tap.
        """

        return self._i2c.readByte(self.address, self.KX13X_INS1)
    
    def unknown_tap(self):
        """!
        if the accelerometer is unsure whether it has in fact
            detected a tap, it will report an "unknown" state. in that
            case this function will return true. good for error checking.
        """
            
        kTapDetectedShift = 2
        kTapDetectedMask = 0b11 << 2
        reg_val = self._i2c.readByte(self.address, self.KX13X_INS2)
        
        tap_result = (reg_val & kTapDetectedMask) >> kTapDetectedShift

        kUnknownTapStatusResult = 0x03
        return tap_result == kUnknownTapStatusResult
    
    def double_tap_detected(self):
        """!
        Checks the double tap interrupt bit indicating that
            a double tap has been detected.
        """

        kTapDetectedShift = 2
        kTapDetectedMask = 0b11 << 2
        reg_val = self._i2c.readByte(self.address, self.KX13X_INS2)
        
        tap_result = (reg_val & kTapDetectedMask) >> kTapDetectedShift

        kDoubleTapStatusResult = 0x02
        return tap_result == kDoubleTapStatusResult

    def get_sample_level(self):
        """!
        Gets the number of samples in the Buffer.

        @return Returns integer number of samples in the buffer
        """

        reg_val = self._i2c.read_block(self.address, self.KX13X_BUF_STATUS_1, 2)

        # See page 44 of reference manual, sample level is 10 bits with the two most significant bits in the second byte
        return ( (reg_val[1] & 0x03) << 8) | reg_val[0]
            
class QwiicKX132(QwiicKX13XCore):

    KX132_WHO_AM_I = 0x3D
    KX132_RANGE2G  = 0x00
    KX132_RANGE4G  = 0x01
    KX132_RANGE8G  = 0x02
    KX132_RANGE16G = 0x03
    CONV_2G =  .00006103518784142582
    CONV_4G =  .0001220703756828516
    CONV_8G =  .0002441407513657033
    CONV_16G = .0004882811975463118

    def __init__(self, address = None, i2c_driver = None):
        super().__init__(address, i2c_driver)
        self.kx132_accel = AccelerationData(0,0,0)

    def begin(self):
        """!
        Checks that communication can be made with the QwiicKX132 by checking
            the WHO_AM_I register.

        @return **bool** Returns true if WHO_AM_I value is the correct one and
            false otherwise.
        """
        chipID = self.beginCore()
        if chipID == self.KX132_WHO_AM_I:
            return True
        else:
            return False

    def get_accel_data(self):
        """!
        Retrieves acceleration data and converts it, and stores it
        """
        self.get_raw_accel_data()
        self.conv_accel_data()

    def conv_accel_data(self):
            """!
            Converts raw acceleration data according to the range setting and
                stores it
            """
            accel_range = self._i2c.readByte(self.address, self.KX13X_CNTL1)
            accel_range &= 0x18
            accel_range = accel_range >> 3

            if accel_range == self.KX132_RANGE2G:
                self.kx132_accel.x = round(self.raw_output_data.x * self.CONV_2G, 6)
                self.kx132_accel.y = round(self.raw_output_data.y * self.CONV_2G, 6)
                self.kx132_accel.z = round(self.raw_output_data.z * self.CONV_2G, 6)
            elif accel_range == self.KX132_RANGE4G:
                self.kx132_accel.x = round(self.raw_output_data.x * self.CONV_4G, 6)
                self.kx132_accel.y = round(self.raw_output_data.y * self.CONV_4G, 6)
                self.kx132_accel.z = round(self.raw_output_data.z * self.CONV_4G, 6)
            elif accel_range == self.KX132_RANGE8G:
                self.kx132_accel.x = round(self.raw_output_data.x * self.CONV_8G, 6)
                self.kx132_accel.y = round(self.raw_output_data.y * self.CONV_8G, 6)
                self.kx132_accel.z = round(self.raw_output_data.z * self.CONV_8G, 6)
            elif accel_range == self.KX132_RANGE16G:
                self.kx132_accel.x = round(self.raw_output_data.x * self.CONV_16G, 6)
                self.kx132_accel.y = round(self.raw_output_data.y * self.CONV_16G, 6)
                self.kx132_accel.z = round(self.raw_output_data.z * self.CONV_16G, 6)


class QwiicKX134(QwiicKX13XCore):

    KX134_WHO_AM_I = 0x46
    KX134_RANGE8G  = 0x00
    KX134_RANGE16G = 0x01
    KX134_RANGE32G = 0x02
    KX134_RANGE64G = 0x03

    CONV_8G =  .000244140751365703299
    CONV_16G = .000488281197546311838
    CONV_32G = .000976523950926236762
    CONV_64G = .001953125095370342112

    def __init__(self, address = None, i2c_driver = None):
        super().__init__(address, i2c_driver)
        self.kx134_accel = AccelerationData(0,0,0)

    def begin(self):
        """!
        Checks that communication can be made with the QwiicKX134 by checking
            the WHO_AM_I register.

        @return **bool** Returns true if WHO_AM_I value is the correct one and
            false otherwise.
        """
        chipID = self.beginCore()
        if chipID == self.KX134_WHO_AM_I:
            return True
        else:
            return False

    def get_accel_data(self):
        """!
        Retrieves acceleration data and converts it, and stores it
        """
        self.get_raw_accel_data()
        self.conv_accel_data()

    def conv_accel_data(self):
        """!
        Converts raw acceleration data according to the range setting and
            stores it
        """
        accel_range = self._i2c.readByte(self.address, self.KX13X_CNTL1)
        accel_range &= 0x18
        accel_range = accel_range >> 3

        if accel_range == self.KX134_RANGE8G:
            self.kx134_accel.x = round(self.raw_output_data.x * self.CONV_8G, 6)
            self.kx134_accel.y = round(self.raw_output_data.y * self.CONV_8G, 6)
            self.kx134_accel.z = round(self.raw_output_data.z * self.CONV_8G, 6)
        elif accel_range == self.KX134_RANGE16G:
            self.kx134_accel.x = round(self.raw_output_data.x * self.CONV_16G, 6)
            self.kx134_accel.y = round(self.raw_output_data.y * self.CONV_16G, 6)
            self.kx134_accel.z = round(self.raw_output_data.z * self.CONV_16G, 6)
        elif accel_range == self.KX134_RANGE32G:
            self.kx134_accel.x = round(self.raw_output_data.x * self.CONV_32G, 6)
            self.kx134_accel.y = round(self.raw_output_data.y * self.CONV_32G, 6)
            self.kx134_accel.z = round(self.raw_output_data.z * self.CONV_32G, 6)
        elif accel_range == self.KX134_RANGE64G:
            self.kx134_accel.x = round(self.raw_output_data.x * self.CONV_64G, 6)
            self.kx134_accel.y = round(self.raw_output_data.y * self.CONV_64G, 6)
            self.kx134_accel.z = round(self.raw_output_data.z * self.CONV_64G, 6)

