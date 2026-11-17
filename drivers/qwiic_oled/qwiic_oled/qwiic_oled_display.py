#-----------------------------------------------------------------------------
# qwiic_oled_display.py
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
#
#
# More information on qwiic is at https:= www.sparkfun.com/qwiic
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
# pylint: disable=line-too-long, bad-whitespace, invalid-name, too-many-lines
# pylint: disable=too-many-lines, too-many-arguments, too-many-instance-attributes
# pylint: disable=too-many-public-methods

"""
qwiic_oled_display
======================
Python module for the [Qwiic OLED Display](https://www.sparkfun.com/products/17153)

This python package is a port of the existing [SparkFun Micro OLED Arduino Library](https://github.com/sparkfun/SparkFun_Micro_OLED_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""

import math
import qwiic_i2c

from qwiic_oled import QwiicOledBase

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
#
# The name of this device - note this is private
_DEFAULT_NAME = "Qwiic OLED Display (128x32)"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.

_AVAILABLE_I2C_ADDRESS = [0x3C, 0x3D]
_LCDWIDTH            = 128
_LCDHEIGHT           = 32

class QwiicOledDisplay(QwiicOledBase):
    """
    QwiicOledDisplay

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The OLED Display device object.
        :rtype: Object
    """

    # Constructor
    device_name         =_DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self.address = address if address is not None else self.available_addresses[0]

        # Instantiate OLED Display Driver - Base Class
        super().__init__(address, _LCDWIDTH, _LCDHEIGHT, i2c_driver)