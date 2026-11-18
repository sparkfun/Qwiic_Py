# qwiic_i2c_micropython.py
#
# MicroPython backend for qwiic_i2c.
#
# Copyright (c) 2019-2026 SparkFun Electronics
# SPDX-License-Identifier: MIT

"""!
qwiic_i2c_micropython
=====================
MicroPython backend for qwiic_i2c, using machine.I2C or machine.SoftI2C.
"""

# Same as qwiic_i2c.__version__; circup reads each module's own version
__version__ = "3.0.0"

import sys
from qwiic_i2c import I2CBus, register_bytes


def _default_bus(sda, scl, freq):
    from machine import I2C, Pin

    port = sys.platform
    if port == "rp2":
        if sda is not None and scl is not None:
            bus_id = (scl // 2) % 2
            if (sda // 2) % 2 != bus_id:
                raise ValueError("SDA and SCL pins must be on the same I2C bus")
            return I2C(bus_id, scl=Pin(scl), sda=Pin(sda), freq=freq)
        # The port's default (400 kHz) is too fast for some devices, such as
        # the ATtiny-based Qwiic Soil Moisture Sensor
        return I2C(freq=freq)
    if "esp32" in port:
        if sda is not None and scl is not None:
            return I2C(scl=Pin(scl), sda=Pin(sda), freq=freq)
        return I2C(freq=freq)
    if "xbee" in port:
        return I2C(1, freq=freq)
    if "mimxrt" in port:
        # The port's default (400 kHz) is too fast for some devices
        return I2C(0, freq=freq)
    raise ValueError(
        "qwiic_i2c: no default I2C bus for MicroPython port '%s'. "
        "Pass a machine.I2C object to get_i2c_bus() instead." % port
    )


class MicroPythonI2C(I2CBus):
    """!
    I2C backend for MicroPython.
    """

    name = "MicroPython"

    def __init__(self, sda=None, scl=None, freq=100000, native_bus=None):
        """!
        @param sda: SDA pin number, to create a bus on specific pins
        @param scl: SCL pin number, to create a bus on specific pins
        @param freq: Bus frequency in Hz
        @param native_bus: An existing machine.I2C or machine.SoftI2C object to use instead
        """
        if native_bus is None:
            native_bus = _default_bus(sda, scl, freq)
        I2CBus.__init__(self, native_bus)

    @classmethod
    def is_platform(cls):
        return sys.implementation.name == "micropython"

    @classmethod
    def is_native_bus(cls, obj):
        for method in ("scan", "readfrom", "writeto", "readfrom_mem", "writeto_mem"):
            if not hasattr(obj, method):
                return False
        return True

    def read_block(self, address, register, num_bytes):
        if register is None:
            return self.native_bus.readfrom(address, num_bytes)
        if isinstance(register, int):
            return self.native_bus.readfrom_mem(address, register, num_bytes)
        # Wider register: write it without a STOP, then read (repeated start)
        self.native_bus.writeto(address, register_bytes(register), False)
        return self.native_bus.readfrom(address, num_bytes)

    def write_block(self, address, register, data):
        if isinstance(register, int):
            self.native_bus.writeto_mem(address, register, bytes(data))
        else:
            self.native_bus.writeto(address, register_bytes(register) + bytes(data))

    def is_device_connected(self, address):
        try:
            self.native_bus.writeto(address, b"")
            return True
        except OSError:
            return False

    def scan(self):
        return self.native_bus.scan()
