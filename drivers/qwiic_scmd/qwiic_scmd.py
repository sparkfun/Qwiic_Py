#-----------------------------------------------------------------------------
# qwiic_scmd.py
#
# Qwii interface for the Serial Control Motor Driver
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
#
#
# More information on qwiic is at https:# www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
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
# pylint: disable=line-too-long, bad-whitespace, invalid-name
# pylint: disable=too-many-public-methods, too-many-instance-attributes
#

"""!
qwiic_scmd
============
Python module for the serial control motor driver.

This python package is a port of the existing [SparkFun Serial Controlled Motor Driver Arduino Library](https://github.com/sparkfun/SparkFun_Serial_Controlled_Motor_Driver_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
#
# The name of this device - note this is private
_DEFAULT_NAME = "Qwiic Serial Control Motor Driver"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x5D, 0x58, 0x59, 0x5A, 0x5C]

# pylint: disable=too-few-public-methods
# Simple replication of the diagnostic class.
class SCMDDiagnostics(object):
    """!
    SCMDDiagnostics

        Object used for diagnostic reporting.

        :ivar numberOfSlaves:
        :ivar U_I2C_RD_ERR:
        :ivar U_I2C_WR_ERR:
        :ivar U_BUF_DUMPED:
        :ivar E_I2C_RD_ERR:
        :ivar E_I2C_WR_ERR:
        :ivar LOOP_TIME:
        :ivar SLV_POLL_CNT:
        :ivar MST_E_ERR:
        :ivar MST_E_STATUS:
        :ivar FSAFE_FAULTS:
        :ivar REG_OOR_CNT:
        :ivar REG_RO_WRITE_CNT:
    """

    def __init__(self):

        super(SCMDDiagnostics, self).__init__()

        # Attainable metrics from SCMD
        self.numberOfSlaves = 0
        self.U_I2C_RD_ERR = 0
        self.U_I2C_WR_ERR = 0
        self.U_BUF_DUMPED = 0
        self.E_I2C_RD_ERR = 0
        self.E_I2C_WR_ERR = 0
        self.LOOP_TIME = 0
        self.SLV_POLL_CNT = 0
        self.MST_E_ERR = 0
        self.MST_E_STATUS = 0
        self.FSAFE_FAULTS = 0
        self.REG_OOR_CNT = 0
        self.REG_RO_WRITE_CNT = 0

class QwiicScmd(object):
    """!
        QwiicScmd

        @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        @param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.

        @return **Object** The Serial Control Motor Driver device object.
        """

    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Define the flags for  the device

    # defaults ( Set config in PSoC, use for reference in Arduino )
    ID_WORD                    = 0xA9  # Device ID to be programmed into memory for reads
    START_SLAVE_ADDR           = 0x50  # Start address of slaves
    MAX_SLAVE_ADDR             = 0x5F  # Max address of slaves
    MASTER_LOCK_KEY            = 0x9B
    USER_LOCK_KEY              = 0x5C
    FIRMWARE_VERSION           = 0x07
    POLL_ADDRESS               = 0x4A  # Address of an unasigned, ready slave
    MAX_POLL_LIMIT             = 0xC8  # 200

    # SCMD_STATUS_1 bits
    SCMD_ENUMERATION_BIT       = 0x01
    SCMD_BUSY_BIT              = 0x02
    SCMD_REM_READ_BIT          = 0x04
    SCMD_REM_WRITE_BIT         = 0x08
    SCMD_HW_EN_BIT             = 0x10

    # SCMD_CONTROL_1 bits
    SCMD_FULL_RESET_BIT        = 0x01
    SCMD_RE_ENUMERATE_BIT      = 0x02

    # SCMD_FSAFE_CTRL bits and masks
    SCMD_FSAFE_DRIVE_KILL      = 0x01
    SCMD_FSAFE_RESTART_MASK    = 0x06
    SCMD_FSAFE_REBOOT          = 0x02
    SCMD_FSAFE_RE_ENUM         = 0x04
    SCMD_FSAFE_CYCLE_USER      = 0x08
    SCMD_FSAFE_CYCLE_EXP       = 0x10

    # SCMD_MST_E_IN_FN bits and masks
    SCMD_M_IN_RESTART_MASK    = 0x03
    SCMD_M_IN_REBOOT          = 0x01
    SCMD_M_IN_RE_ENUM         = 0x02
    SCMD_M_IN_CYCLE_USER      = 0x04
    SCMD_M_IN_CYCLE_EXP       = 0x08

    # Address map
    SCMD_FID                   = 0x00
    SCMD_ID                    = 0x01
    SCMD_SLAVE_ADDR            = 0x02
    SCMD_CONFIG_BITS           = 0x03
    SCMD_U_I2C_RD_ERR          = 0x04
    SCMD_U_I2C_WR_ERR          = 0x05
    SCMD_U_BUF_DUMPED          = 0x06
    SCMD_E_I2C_RD_ERR          = 0x07
    SCMD_E_I2C_WR_ERR          = 0x08
    SCMD_LOOP_TIME             = 0x09
    SCMD_SLV_POLL_CNT          = 0x0A
    SCMD_SLV_TOP_ADDR          = 0x0B
    SCMD_MST_E_ERR             = 0x0C
    SCMD_MST_E_STATUS          = 0x0D
    SCMD_FSAFE_FAULTS          = 0x0E
    SCMD_REG_OOR_CNT           = 0x0F
    SCMD_REG_RO_WRITE_CNT      = 0x10
    SCMD_GEN_TEST_WORD         = 0x11
    SCMD_MOTOR_A_INVERT        = 0x12
    SCMD_MOTOR_B_INVERT        = 0x13
    SCMD_BRIDGE                = 0x14
    SCMD_LOCAL_MASTER_LOCK     = 0x15
    SCMD_LOCAL_USER_LOCK       = 0x16
    SCMD_MST_E_IN_FN           = 0x17
    SCMD_U_PORT_CLKDIV_U       = 0x18
    SCMD_U_PORT_CLKDIV_L       = 0x19
    SCMD_U_PORT_CLKDIV_CTRL    = 0x1A
    SCMD_E_PORT_CLKDIV_U       = 0x1B
    SCMD_E_PORT_CLKDIV_L       = 0x1C
    SCMD_E_PORT_CLKDIV_CTRL    = 0x1D
    SCMD_U_BUS_UART_BAUD       = 0x1E
    SCMD_FSAFE_CTRL            = 0x1F
    SCMD_MA_DRIVE              = 0x20
    SCMD_MB_DRIVE              = 0x21
    SCMD_S1A_DRIVE             = 0x22
    SCMD_S1B_DRIVE             = 0x23
    SCMD_S2A_DRIVE             = 0x24
    SCMD_S2B_DRIVE             = 0x25
    SCMD_S3A_DRIVE             = 0x26
    SCMD_S3B_DRIVE             = 0x27
    SCMD_S4A_DRIVE             = 0x28
    SCMD_S4B_DRIVE             = 0x29
    SCMD_S5A_DRIVE             = 0x2A
    SCMD_S5B_DRIVE             = 0x2B
    SCMD_S6A_DRIVE             = 0x2C
    SCMD_S6B_DRIVE             = 0x2D
    SCMD_S7A_DRIVE             = 0x2E
    SCMD_S7B_DRIVE             = 0x2F
    SCMD_S8A_DRIVE             = 0x30
    SCMD_S8B_DRIVE             = 0x31
    SCMD_S9A_DRIVE             = 0x32
    SCMD_S9B_DRIVE             = 0x33
    SCMD_S10A_DRIVE            = 0x34
    SCMD_S10B_DRIVE            = 0x35
    SCMD_S11A_DRIVE            = 0x36
    SCMD_S11B_DRIVE            = 0x37
    SCMD_S12A_DRIVE            = 0x38
    SCMD_S12B_DRIVE            = 0x39
    SCMD_S13A_DRIVE            = 0x3A
    SCMD_S13B_DRIVE            = 0x3B
    SCMD_S14A_DRIVE            = 0x3C
    SCMD_S14B_DRIVE            = 0x3D
    SCMD_S15A_DRIVE            = 0x3E
    SCMD_S15B_DRIVE            = 0x3F
    SCMD_S16A_DRIVE            = 0x40
    SCMD_S16B_DRIVE            = 0x41

    SCMD_INV_2_9               = 0x50
    SCMD_INV_10_17             = 0x51
    SCMD_INV_18_25             = 0x52
    SCMD_INV_26_33             = 0x53
    SCMD_BRIDGE_SLV_L          = 0x54
    SCMD_BRIDGE_SLV_H          = 0x55

    # SCMD_PAGE_SELECT           = 0x6F
    SCMD_DRIVER_ENABLE         = 0x70
    SCMD_UPDATE_RATE           = 0x71
    SCMD_FORCE_UPDATE          = 0x72
    SCMD_E_BUS_SPEED           = 0x73
    SCMD_MASTER_LOCK           = 0x74
    SCMD_USER_LOCK             = 0x75
    SCMD_FSAFE_TIME            = 0x76
    SCMD_STATUS_1              = 0x77
    SCMD_CONTROL_1             = 0x78

    SCMD_REM_ADDR              = 0x79
    SCMD_REM_OFFSET            = 0x7A
    SCMD_REM_DATA_WR           = 0x7B
    SCMD_REM_DATA_RD           = 0x7C
    SCMD_REM_WRITE             = 0x7D
    SCMD_REM_READ              = 0x7E


    def __init__(self, address=None, i2c_driver=None):


        # Did the user specify an I2C address?
        self.address = address if address is not None else self.available_addresses[0]

        # load the I2C driver if one isn't provided

        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    #----------------------------------------------
    def is_connected(self):
        """!
            Determine if a SCMD device is conntected to the system..

            @return **bool** True if the device is connected, otherwise False.
            """
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):
        """!
            Initialize the operation of the SCMD module

            @return **bool** Returns true of the initializtion was successful, otherwise False.
            """
        # dummy read
        self._i2c.readByte(self.address, self.SCMD_ID)

        return self._i2c.readByte(self.address, self.SCMD_ID)


    # check if enumeration is complete
    def ready(self):
        """!
            Returns if the driver is ready

            @return **boolean** Ready status
            """
        statusByte = self._i2c.readByte(self.address, self.SCMD_STATUS_1)

        return statusByte & self.SCMD_ENUMERATION_BIT  and  statusByte != 0xFF  #wait for ready flag and not 0xFF

    def busy(self):
        """!
            Returns if the driver is busy

            @return **boolean** busy status
            """
        statusByte = self._i2c.readByte(self.address, self.SCMD_STATUS_1)

        return statusByte & (self.SCMD_BUSY_BIT | self.SCMD_REM_READ_BIT | self.SCMD_REM_WRITE_BIT) != 0

    # Enable and disable functions.  Call after begin to enable the h-bridges
    def enable(self):
        """!
            Enable driver functions

            @return  No return value

        
            """
        self._i2c.writeByte(self.address, self.SCMD_DRIVER_ENABLE, 0x01)

    def disable(self):
        """!
            Disable driver functions

            @return  No return value

        
            """
        self._i2c.writeByte(self.address, self.SCMD_DRIVER_ENABLE, 0x00)

    # this is a hack in the Arduino lib - the placeholder is for compatablity
    def reset(self):
        """!
        This is a hack in the Arduino lib - the placeholder is for compatablity
        """
        pass

    # ****************************************************************************#
    #
    #   Drive Section
    #
    # ****************************************************************************#

    # set_drive( ... )
    #
    #     Drive a motor at a level
    #
    #   uint8_t motorNum -- Motor number from 0 to 33
    #   uint8_t direction -- 0 or 1 for forward and backward
    #   int8_t level -- (-255) to 255 for drive strength
    def set_drive(self, motorNum, direction, level):
        """!
            Drive a motor at a level

            @param motoNum: Motor number from 0 to 33
            @param direction: 0 or 1 for forward and backward
            @param level: (-255) to 255 for drive strength

            @return  No return value

        
            """

        # Convert value to a 7-bit int and match the indexing for uint8_t values as needed in Arduino library
        level = int(round((level + 1 - direction)/2))

        driveValue = 0 # use to build value to actually write to register

        # Make sure the motor number is valid
        if motorNum < 34:
            driveValue = (level * direction) + (level * (direction - 1)) # set to 1/2 drive if direction = 1 or -1/2 drive if direction = 0 (level * direction)
            driveValue += 128
            self._i2c.writeByte(self.address, self.SCMD_MA_DRIVE + motorNum, driveValue)


    # inversion_mode( ... )
    #
    #     Configure a motor's direction inversion
    #
    #   motorNum -- Motor number from 0 to 33
    #   polarity -- 0 or 1 for default or inverted
    def inversion_mode(self, motorNum, polarity):
        """!
            Configure a motor's direction inversion

            @param motoNum: Motor number from 0 to 33
            @param polarity: 0 or 1 for default or inverted

            @return  No return value

        
            """

        regTemp = 0
        # Select target register
        if motorNum < 2:

            # master
            if motorNum == 0:
                self._i2c.writeByte(self.address, self.SCMD_MOTOR_A_INVERT, polarity & 0x01)
            if motorNum == 1:
                self._i2c.writeByte(self.address, self.SCMD_MOTOR_B_INVERT, polarity & 0x01)

        else:

            if motorNum < 10:
                # register: SCMD_INV_2_9
                regTemp = self.SCMD_INV_2_9
                motorNum -= 2

            elif motorNum < 18:
                # register: SCMD_INV_10_17
                regTemp = self.SCMD_INV_10_17
                motorNum -= 10

            elif motorNum < 26:
                # register: SCMD_INV_18_25
                regTemp = self.SCMD_INV_18_25
                motorNum -= 18

            elif motorNum < 34:
                # register: SCMD_INV_26_33
                regTemp = self.SCMD_INV_26_33
                motorNum -= 26

            else:
                # out of range
                return

            # convert motorNum to one-hot mask
            data = self._i2c.readByte(self.address, regTemp) & (~(1 << motorNum) & 0xFF)
            self._i2c.writeByte(self.address, regTemp, data | ((polarity & 0x01) << motorNum))


    # bridgingMode( ... )
    #
    #     Configure a driver's bridging state
    #
    #   driverNum -- Number of driver.  Master is 0, slave 1 is 1, etc.  0 to 16
    #   bridged -- 0 or 1 for forward and backward
    def bridging_mode(self, driverNum, bridged):
        """!
            Configure a driver's bridging state

            @param driverNum: Number of driver.  Master is 0, slave 1 is 1, etc.  0 to 16
            @param bridged: 0 or 1 for forward and backward

            @return  No return value

        
            """

        regTemp = 0
        # Select target register
        if driverNum < 1:
            # master
            self._i2c.writeByte(self.address, self.SCMD_BRIDGE, bridged & 0x01)

        else:

            if driverNum < 9:
                # register: SCMD_BRIDGE_SLV_L
                regTemp = self.SCMD_BRIDGE_SLV_L
                driverNum -= 1

            elif driverNum < 17:
                # register: SCMD_BRIDGE_SLV_H
                regTemp = self.SCMD_BRIDGE_SLV_H
                driverNum -= 9

            else:
                # out of range
                return
            # convert driverNum to one-hot mask
            data = self._i2c.readByte(regTemp) & (~(1 << driverNum ) & 0xFF)
            self._i2c.writeByte(self.address, regTemp, data | ((bridged & 0x01) << driverNum))

    # ****************************************************************************#
    #
    #   Diagnostics
    #
    # ****************************************************************************#

    # getDiagnostics( ... )
    #
    #    Get diagnostic information from the master
    #
    #   Object returned with properties that are the diagnostic info

    def get_diagnostics(self):
        """!
            Get diagnostic information from the masterd

            @return **Object - SCMDDiagnostics()** Object returned with properties that are the diagnostic info
            """

        myDiag = SCMDDiagnostics()

        myDiag.U_I2C_RD_ERR = self._i2c.readByte(self.address, self.SCMD_U_I2C_RD_ERR)
        myDiag.U_I2C_WR_ERR = self._i2c.readByte(self.address, self.SCMD_U_I2C_WR_ERR)
        myDiag.U_BUF_DUMPED = self._i2c.readByte(self.address, self.SCMD_U_BUF_DUMPED)
        myDiag.E_I2C_RD_ERR = self._i2c.readByte(self.address, self.SCMD_E_I2C_RD_ERR)
        myDiag.E_I2C_WR_ERR = self._i2c.readByte(self.address, self.SCMD_E_I2C_WR_ERR)
        myDiag.LOOP_TIME    = self._i2c.readByte(self.address, self.SCMD_LOOP_TIME)
        myDiag.SLV_POLL_CNT = self._i2c.readByte(self.address, self.SCMD_SLV_POLL_CNT)

        # Count slaves
        topAddr = self._i2c.readByte(self.address,  self.SCMD_SLV_TOP_ADDR)
        if topAddr >= self.START_SLAVE_ADDR and topAddr < (self.START_SLAVE_ADDR + 16):
            # in valid range
            myDiag.numberOfSlaves = topAddr - self.START_SLAVE_ADDR + 1

        myDiag.MST_E_ERR        = self._i2c.readByte(self.address, self.SCMD_MST_E_ERR)
        myDiag.MST_E_STATUS     = self._i2c.readByte(self.address, self.SCMD_MST_E_STATUS)
        myDiag.FSAFE_FAULTS     = self._i2c.readByte(self.address, self.SCMD_FSAFE_FAULTS)
        myDiag.REG_OOR_CNT      = self._i2c.readByte(self.address, self.SCMD_REG_OOR_CNT)
        myDiag.REG_RO_WRITE_CNT = self._i2c.readByte(self.address, self.SCMD_REG_RO_WRITE_CNT)

        return myDiag

    # get_remote_diagnostics( ... )
    #
    #     Get diagnostic information from a slave
    #
    #   uint8_t address -- Address of slave to read.  Can be 0x50 to 0x5F for slave 1 to 16.
    #   SCMDDiagnostics &diagObjectReference -- Object to contain returned data
    def get_remote_diagnostics(self, address):
        """!
            Get diagnostic information from a slave

            @param address: Address of slave to read.  Can be 0x50 to 0x5F for slave 1 to 16.

            @return **Object - SCMDDiagnostics()** Object returned with properties that are the diagnostic info
            """

        myDiag = SCMDDiagnostics()

        myDiag.numberOfSlaves   = 0
        myDiag.U_I2C_RD_ERR     = 0
        myDiag.U_I2C_WR_ERR     = 0
        myDiag.U_BUF_DUMPED     = 0
        myDiag.E_I2C_RD_ERR     = self.read_remote_register(address, self.SCMD_E_I2C_RD_ERR)
        myDiag.E_I2C_WR_ERR     = self.read_remote_register(address, self.SCMD_E_I2C_WR_ERR)
        myDiag.LOOP_TIME        = self.read_remote_register(address, self.SCMD_LOOP_TIME)
        myDiag.SLV_POLL_CNT     = 0
        myDiag.MST_E_ERR        = 0
        myDiag.MST_E_STATUS     = 0
        myDiag.FSAFE_FAULTS     = self.read_remote_register(address, self.SCMD_FSAFE_FAULTS)
        myDiag.REG_OOR_CNT      = self.read_remote_register(address, self.SCMD_REG_OOR_CNT)
        myDiag.REG_RO_WRITE_CNT = self.read_remote_register(address, self.SCMD_REG_RO_WRITE_CNT)

        return myDiag

    # reset_diagnostic_counts( ... )
    #
    #     Reset the master's diagnostic counters
    #
    def reset_diagnostic_counts(self):
        """!
            Reset the master's diagnostic counters

            @return  No return value

        
            """

        self._i2c.writeByte(self.address, self.SCMD_U_I2C_RD_ERR, 0)
        self._i2c.writeByte(self.address, self.SCMD_U_I2C_WR_ERR, 0)
        self._i2c.writeByte(self.address, self.SCMD_U_BUF_DUMPED, 0)
        self._i2c.writeByte(self.address, self.SCMD_E_I2C_RD_ERR, 0)
        self._i2c.writeByte(self.address, self.SCMD_E_I2C_WR_ERR, 0)
        # Clear uport time
        self._i2c.writeByte(self.address, self.SCMD_LOOP_TIME, 0)
        self._i2c.writeByte(self.address, self.SCMD_MST_E_ERR, 0)
        self._i2c.writeByte(self.address, self.SCMD_FSAFE_FAULTS, 0)
        self._i2c.writeByte(self.address, self.SCMD_REG_OOR_CNT, 0)
        self._i2c.writeByte(self.address, self.SCMD_REG_RO_WRITE_CNT, 0)

    # reset_remote_diagnostic_counts( ... )
    #
    #     Reset a slave's diagnostic counters
    #
    #   uint8_t address -- Address of slave to read.  Can be 0x50 to 0x5F for slave 1 to 16.
    def reset_remote_diagnostic_counts(self, address):
        """!
            Reset a slave's diagnostic counters

            @param address: Address of slave to read.  Can be 0x50 to 0x5F for slave 1 to 16.

            @return  No return value

        
            """

        self.write_remote_register(address, self.SCMD_U_I2C_RD_ERR, 0)
        self.write_remote_register(address, self.SCMD_U_I2C_WR_ERR, 0)
        self.write_remote_register(address, self.SCMD_U_BUF_DUMPED, 0)
        self.write_remote_register(address, self.SCMD_E_I2C_RD_ERR, 0)
        self.write_remote_register(address, self.SCMD_E_I2C_WR_ERR, 0)
        # Clear uport time
        self.write_remote_register(address, self.SCMD_LOOP_TIME, 0)
        self.write_remote_register(address, self.SCMD_ID, 0)
        self.write_remote_register(address, self.SCMD_FSAFE_FAULTS, 0)
        self.write_remote_register(address, self.SCMD_REG_OOR_CNT, 0)
        self.write_remote_register(address, self.SCMD_REG_RO_WRITE_CNT, 0)


    # read_remote_register( ... )
    #
    #     Read data from a slave.  Note that this waits 5ms for slave data to be aquired
    #   before making the final read.
    #
    #   address -- Address of slave to read.  Can be 0x50 to 0x5F for slave 1 to 16.
    #   offset -- Address of data to read.  Can be 0x00 to 0x7F
    def read_remote_register(self, address, offset):
        """!
            Read data from a slave.  Note that this waits 5ms for slave data to be aquired
            before making the final read.

            @param address: Address of slave to read.  Can be 0x50 to 0x5F for slave 1 to 16.
            @param offset: Address of data to read.  Can be 0x00 to 0x7F

            @return **integer** Register Value
            """

        self._i2c.writeByte(self.address, self.SCMD_REM_ADDR, address)
        self._i2c.writeByte(self.address, self.SCMD_REM_OFFSET, offset)
        self._i2c.writeByte(self.address, self.SCMD_REM_READ, 1)

        while self.busy():
            pass

        return self._i2c.readByte(self.address, self.SCMD_REM_DATA_RD)


    # write_remote_register( ... )
    #
    #     Write data from a slave
    #
    #   address -- Address of slave to read.  Can be 0x50 to 0x5F for slave 1 to 16.
    #   offset -- Address of data to write.  Can be 0x00 to 0x7F
    #   dataToWrite -- Data to write.

    def write_remote_register(self, address, offset, dataToWrite):
        """!
            Write data from a slave

            @param address: Address of slave to read.  Can be 0x50 to 0x5F for slave 1 to 16.
            @param offset: Address of data to read.  Can be 0x00 to 0x7F
            @param dataToWrite: The data to write

            @return  No return value

        
            """

        while self.busy():
            pass

        self._i2c.writeByte(self.address, self.SCMD_REM_ADDR, address)
        self._i2c.writeByte(self.address, self.SCMD_REM_OFFSET, offset)
        self._i2c.writeByte(self.address, self.SCMD_REM_DATA_WR, dataToWrite)
        self._i2c.writeByte(self.address, self.SCMD_REM_WRITE, 1)

        while self.busy():
            pass
