# qwiic_i2c_linux.py
#
# Linux (CPython) backend for qwiic_i2c.
#
# Copyright (c) 2019-2026 SparkFun Electronics
# SPDX-License-Identifier: MIT

"""!
qwiic_i2c_linux
===============
Linux backend for qwiic_i2c, using smbus2 on CPython.
"""

# Same as qwiic_i2c.__version__; circup reads each module's own version
__version__ = "3.0.0"

import sys
from qwiic_i2c import I2CBus, register_bytes

# Attempts for each read before the error is raised
_RETRY_COUNT = 3

# Largest block an SMBus block transfer can carry. Longer writes use i2c_rdwr.
_SMBUS_BLOCK_MAX = 32

# Default I2C bus number on each board, matched against /proc/device-tree/model
_BOARD_BUS_IDS = (
    ("Jetson Orin Nano", 7),
    ("Raspberry Pi", 1),
)
_DEFAULT_BUS_ID = 1


def _board_name():
    try:
        with open("/proc/device-tree/model") as f:
            return f.read()
    except OSError:
        return ""


def default_bus_id():
    """!
    @return **int** The Qwiic bus number for this board (1 on a Raspberry Pi,
        7 on a Jetson Orin Nano, otherwise 1)
    """
    board = _board_name()
    for name, bus_id in _BOARD_BUS_IDS:
        if name in board:
            return bus_id
    return _DEFAULT_BUS_ID


class LinuxI2C(I2CBus):
    """!
    I2C backend for CPython on Linux.
    """

    name = "Linux"

    def __init__(self, bus_id=None, native_bus=None):
        """!
        @param bus_id: I2C bus number (/dev/i2c-N). Detected from the board when None.
        @param native_bus: An existing smbus2.SMBus (or compatible) object to use instead
        """
        if native_bus is None:
            import smbus2

            if bus_id is None:
                bus_id = default_bus_id()
            native_bus = smbus2.SMBus(bus_id)
        I2CBus.__init__(self, native_bus)
        ## The bus number, or None when an existing bus object was given
        self.bus_id = bus_id
        # Jetson boards (Nano, Xavier NX, Orin Nano, ...) time out on the quick
        # write used to probe for a device, so probe with a one-byte read there
        # (Qwiic_I2C_Py#18, #30)
        self._probe_with_read = "Jetson" in _board_name()

    @classmethod
    def is_platform(cls):
        return sys.platform.startswith("linux") and sys.implementation.name not in ("micropython", "circuitpython")

    @classmethod
    def is_native_bus(cls, obj):
        for method in ("read_byte", "read_byte_data", "write_byte_data", "read_i2c_block_data", "write_i2c_block_data", "i2c_rdwr"):
            if not hasattr(obj, method):
                return False
        return True

    def _retry(self, function, *args):
        for attempt in range(_RETRY_COUNT):
            try:
                return function(*args)
            except OSError:
                if attempt == _RETRY_COUNT - 1:
                    raise

    def _read_raw(self, address, num_bytes):
        from smbus2 import i2c_msg

        message = i2c_msg.read(address, num_bytes)
        self.native_bus.i2c_rdwr(message)
        return list(message)

    def _write_read(self, address, write_data, num_bytes):
        from smbus2 import i2c_msg

        write = i2c_msg.write(address, list(write_data))
        read = i2c_msg.read(address, num_bytes)
        self.native_bus.i2c_rdwr(write, read)
        return list(read)

    def read_block(self, address, register, num_bytes):
        if register is None:
            return self._retry(self._read_raw, address, num_bytes)
        if isinstance(register, int):
            # SMBus transfers where they fit; same bytes on the wire as i2c_rdwr
            if num_bytes == 1:
                return [self._retry(self.native_bus.read_byte_data, address, register)]
            if num_bytes <= _SMBUS_BLOCK_MAX:
                return self._retry(self.native_bus.read_i2c_block_data, address, register, num_bytes)
        return self._retry(self._write_read, address, register_bytes(register), num_bytes)

    def write_block(self, address, register, data):
        data = list(data)
        if isinstance(register, int):
            if len(data) == 1:
                self.native_bus.write_byte_data(address, register, data[0] & 0xFF)
                return
            if not data:
                self.native_bus.write_byte(address, register)
                return
            if len(data) <= _SMBUS_BLOCK_MAX:
                self.native_bus.write_i2c_block_data(address, register, data)
                return
        elif register is None and len(data) == 1:
            self.native_bus.write_byte(address, data[0] & 0xFF)
            return
        from smbus2 import i2c_msg

        self.native_bus.i2c_rdwr(i2c_msg.write(address, list(register_bytes(register)) + data))

    def is_device_connected(self, address):
        try:
            if self._probe_with_read:
                self.native_bus.read_byte(address)
            else:
                self.native_bus.write_quick(address)
            return True
        except OSError:
            return False

    def scan(self):
        return [address for address in range(0x08, 0x78) if self.is_device_connected(address)]
