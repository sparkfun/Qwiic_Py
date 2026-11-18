# qwiic_i2c_circuitpython.py
#
# CircuitPython backend for qwiic_i2c.
#
# Copyright (c) 2019-2026 SparkFun Electronics
# SPDX-License-Identifier: MIT

"""!
qwiic_i2c_circuitpython
=======================
CircuitPython backend for qwiic_i2c, using busio.I2C.
"""

# Same as qwiic_i2c.__version__; circup reads each module's own version
__version__ = "3.0.0"

import sys
from qwiic_i2c import I2CBus, register_bytes

# How many times to try to lock the bus before giving up
_LOCK_ATTEMPTS = 1000


def _default_bus(sda, scl, freq):
    import board
    import busio

    if sda is not None and scl is not None:
        return busio.I2C(scl, sda, frequency=freq)
    if hasattr(board, "STEMMA_I2C"):
        return board.STEMMA_I2C()
    return busio.I2C(board.SCL, board.SDA, frequency=freq)


class CircuitPythonI2C(I2CBus):
    """!
    I2C backend for CircuitPython.
    """

    name = "CircuitPython"

    def __init__(self, sda=None, scl=None, freq=100000, native_bus=None):
        """!
        @param sda: SDA pin (board.* object), to create a bus on specific pins
        @param scl: SCL pin (board.* object), to create a bus on specific pins
        @param freq: Bus frequency in Hz
        @param native_bus: An existing busio.I2C (or compatible) object to use instead
        """
        if native_bus is None:
            native_bus = _default_bus(sda, scl, freq)
        I2CBus.__init__(self, native_bus)

    @classmethod
    def is_platform(cls):
        return sys.implementation.name == "circuitpython"

    @classmethod
    def is_native_bus(cls, obj):
        for method in ("try_lock", "unlock", "scan", "writeto", "readfrom_into", "writeto_then_readfrom"):
            if not hasattr(obj, method):
                return False
        return True

    def _lock(self):
        for _ in range(_LOCK_ATTEMPTS):
            if self.native_bus.try_lock():
                return
        raise OSError("qwiic_i2c: unable to lock the I2C bus")

    def _write(self, address, data):
        self._lock()
        try:
            self.native_bus.writeto(address, data)
        finally:
            self.native_bus.unlock()

    def read_block(self, address, register, num_bytes):
        buffer = bytearray(num_bytes)
        self._lock()
        try:
            if register is None:
                self.native_bus.readfrom_into(address, buffer)
            else:
                self.native_bus.writeto_then_readfrom(address, register_bytes(register), buffer)
        finally:
            self.native_bus.unlock()
        return list(buffer)

    def write_block(self, address, register, data):
        self._write(address, register_bytes(register) + bytes(data))

    def is_device_connected(self, address):
        self._lock()
        try:
            try:
                self.native_bus.writeto(address, b"")
                return True
            except OSError:
                pass
            # Some ports can't send a zero-length write; try a 1-byte read
            try:
                self.native_bus.readfrom_into(address, bytearray(1))
                return True
            except OSError:
                return False
        finally:
            self.native_bus.unlock()

    def scan(self):
        self._lock()
        try:
            return self.native_bus.scan()
        finally:
            self.native_bus.unlock()
