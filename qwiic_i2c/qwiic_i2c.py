# qwiic_i2c.py
#
# Platform independent I2C bus layer for the SparkFun Qwiic Python drivers.
#
# Copyright (c) 2019-2026 SparkFun Electronics
# SPDX-License-Identifier: MIT

"""!
qwiic_i2c
=========
Platform independent I2C bus layer for the SparkFun Qwiic Python drivers.

Device drivers talk to the bus through an I2CBus object. One backend module
per platform implements it:

- qwiic_i2c_micropython: MicroPython (machine.I2C / machine.SoftI2C)
- qwiic_i2c_circuitpython: CircuitPython (busio.I2C)
- qwiic_i2c_linux: CPython on Linux (smbus2)

Every module is flat (no package, no relative imports), so qwiic_i2c also works
on platforms that load each file as an independent top-level module.

The I2CBus also provides timing helpers (delay_ms, delay_us, ticks_ms,
ticks_diff), so drivers never import the time module directly.

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

__version__ = "3.0.0"

try:
    import time as _time
except ImportError:
    # Some platforms have no time module. Their backend provides the timing
    # helpers instead.
    _time = None


def register_bytes(register):
    """!
    For backends: the bytes to send for a register argument.

    @param register: None, an 8-bit register (int), or a sequence of register bytes
    @return **bytes** b"" for None, one byte for an int, otherwise the bytes given
    """
    if register is None:
        return b""
    if isinstance(register, int):
        return bytes([register])
    return bytes(register)


class I2CBus(object):
    """!
    Base class for the platform I2C backends.

    A backend implements the bus methods below for one platform. The timing
    helpers have defaults that use the time module when it exists.
    """

    ## Human readable name of the backend
    name = "qwiic I2C base class"

    def __init__(self, native_bus=None):
        """!
        @param native_bus: The platform's native I2C bus object
        """
        ## The platform's native I2C bus object (machine.I2C, busio.I2C, smbus2.SMBus, ...)
        self.native_bus = native_bus

    @classmethod
    def is_platform(cls):
        """!
        @return **bool** True if this backend runs on the current platform
        """
        return False

    @classmethod
    def is_native_bus(cls, obj):
        """!
        @param obj: Any object
        @return **bool** True if obj is an I2C bus object of this platform that the
            backend can wrap (for example machine.I2C on MicroPython)
        """
        return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # ---------------------------------------------------------------------
    # Transfers. Every backend implements these two.
    #
    # register is None (no register), an int (an 8-bit register), or a
    # sequence of bytes (a wider register, sent first, most significant byte
    # first as the device expects).

    def read_block(self, address, register, num_bytes):
        """!
        Read bytes. With a register, the register is written first and the
        bytes are read after a repeated start.

        @param address: 7-bit device address
        @param register: None, an 8-bit register, or the bytes of a wider register
        @param num_bytes: Number of bytes to read
        @return **sequence of int** The bytes read (bytes or list)
        """
        raise NotImplementedError()

    def write_block(self, address, register, data):
        """!
        Write bytes, after the register if one is given.

        @param address: 7-bit device address
        @param register: None, an 8-bit register, or the bytes of a wider register
        @param data: Bytes to write (bytes, bytearray or list of int)
        """
        raise NotImplementedError()

    # ---------------------------------------------------------------------
    # Conveniences built on the two transfers, the same for every backend.

    def read_byte(self, address, register=None):
        """!
        Read one byte.

        @param address: 7-bit device address
        @param register: None, an 8-bit register, or the bytes of a wider register
        @return **int** The byte read
        """
        return self.read_block(address, register, 1)[0]

    def write_byte(self, address, register, value):
        """!
        Write one byte. With register None, this sends just the byte (a command).

        @param address: 7-bit device address
        @param register: None, an 8-bit register, or the bytes of a wider register
        @param value: Byte to write
        """
        self.write_block(address, register, [value & 0xFF])

    def read_word(self, address, register=None, byteorder="little"):
        """!
        Read a 16-bit word.

        @param address: 7-bit device address
        @param register: None, an 8-bit register, or the bytes of a wider register
        @param byteorder: "little" (low byte first) or "big" (high byte first)
        @return **int** The word read
        """
        data = self.read_block(address, register, 2)
        if byteorder == "big":
            return (data[0] << 8) | data[1]
        return data[0] | (data[1] << 8)

    def write_word(self, address, register, value, byteorder="little"):
        """!
        Write a 16-bit word.

        @param address: 7-bit device address
        @param register: None, an 8-bit register, or the bytes of a wider register
        @param value: Word to write
        @param byteorder: "little" (low byte first) or "big" (high byte first)
        """
        low, high = value & 0xFF, (value >> 8) & 0xFF
        self.write_block(address, register, [high, low] if byteorder == "big" else [low, high])

    # ---------------------------------------------------------------------
    # Device detection. Every backend implements these.

    def is_device_connected(self, address):
        """!
        @param address: 7-bit device address
        @return **bool** True if a device acknowledges the address
        """
        raise NotImplementedError()

    def scan(self):
        """!
        @return **list of int** Addresses of every device that answers on the bus
        """
        raise NotImplementedError()

    # ---------------------------------------------------------------------
    # Timing. Drivers use these instead of the time module, so a platform
    # without one only needs to override them in its backend.

    @staticmethod
    def delay_ms(ms):
        """!
        Block for at least ms milliseconds.

        @param ms: Milliseconds to wait
        """
        if _time is None:
            raise NotImplementedError("No time module: the backend must implement delay_ms")
        if hasattr(_time, "sleep_ms"):
            _time.sleep_ms(int(ms))
        else:
            _time.sleep(ms / 1000)

    @staticmethod
    def delay_us(us):
        """!
        Block for at least us microseconds. Resolution depends on the platform.

        @param us: Microseconds to wait
        """
        if _time is None:
            raise NotImplementedError("No time module: the backend must implement delay_us")
        if hasattr(_time, "sleep_us"):
            _time.sleep_us(int(us))
        else:
            _time.sleep(us / 1000000)

    @staticmethod
    def ticks_ms():
        """!
        @return **int** A millisecond counter for measuring intervals. It may
            wrap, so compare values with ticks_diff().
        """
        if _time is None:
            raise NotImplementedError("No time module: the backend must implement ticks_ms")
        if hasattr(_time, "ticks_ms"):
            return _time.ticks_ms()
        if hasattr(_time, "monotonic_ns"):
            return _time.monotonic_ns() // 1000000
        return int(_time.monotonic() * 1000)

    @staticmethod
    def ticks_diff(end, start):
        """!
        @param end: Later value from ticks_ms()
        @param start: Earlier value from ticks_ms()
        @return **int** end - start in milliseconds, correct across a counter wrap
        """
        if _time is not None and hasattr(_time, "ticks_diff"):
            return _time.ticks_diff(end, start)
        return end - start


# -------------------------------------------------------------------------
# Backend discovery. The backend modules are imported by name inside a
# function, so the import is static (bundlers can see it) but happens only
# when a bus is first needed.

_backend_classes = None
_default_bus = None


def _backends():
    global _backend_classes
    if _backend_classes is None:
        found = []
        try:
            import qwiic_i2c_micropython
            found.append(qwiic_i2c_micropython.MicroPythonI2C)
        except ImportError:
            pass
        try:
            import qwiic_i2c_circuitpython
            found.append(qwiic_i2c_circuitpython.CircuitPythonI2C)
        except ImportError:
            pass
        try:
            import qwiic_i2c_linux
            found.append(qwiic_i2c_linux.LinuxI2C)
        except ImportError:
            pass
        _backend_classes = found
    return _backend_classes


def _platform_backend():
    for backend in _backends():
        if backend.is_platform():
            return backend
    return None


def get_i2c_bus(*args, **kwargs):
    """!
    Get an I2C bus for the current platform.

    - No arguments, or None: the shared default bus, created on first use.
    - An existing I2CBus: returned unchanged.
    - A native bus object (machine.I2C, machine.SoftI2C, busio.I2C,
      smbus2.SMBus, ...): wrapped in the platform's backend.
    - Anything else: passed to the backend's constructor, for example
      get_i2c_bus(sda=4, scl=5, freq=400000) on MicroPython or
      get_i2c_bus(bus_id=7) on Linux.

    @return **I2CBus** The bus
    @exception RuntimeError: No backend supports this platform
    """
    global _default_bus

    if len(args) == 1 and not kwargs:
        if args[0] is None:
            args = ()
        elif isinstance(args[0], I2CBus):
            return args[0]

    no_params = not args and not kwargs
    if no_params and _default_bus is not None:
        return _default_bus

    backend = _platform_backend()
    if backend is None:
        raise RuntimeError("qwiic_i2c: no I2C backend supports this platform")

    if args and backend.is_native_bus(args[0]):
        bus = backend(*args[1:], native_bus=args[0], **kwargs)
    else:
        bus = backend(*args, **kwargs)

    if no_params:
        _default_bus = bus
    return bus


def set_default_i2c_bus(bus):
    """!
    Choose the bus that drivers use when they're given none, for example a
    SoftI2C port, or the right bus on a board where the automatic choice is
    wrong. Drivers already created keep the bus they have.

        qwiic_i2c.set_default_i2c_bus(machine.SoftI2C(scl=machine.Pin(5), sda=machine.Pin(4)))
        sensor = qwiic_bme280.QwiicBME280()     # uses that bus

    @param bus: A qwiic_i2c bus or a native bus object (machine.I2C,
        busio.I2C, smbus2.SMBus, ...), or None to go back to the platform
        default (created again on next use)
    @return **I2CBus** The new default bus, or None after a reset
    @exception RuntimeError: No backend supports this platform
    """
    global _default_bus
    if bus is None:
        _default_bus = None
        return None
    bus = get_i2c_bus(bus)
    _default_bus = bus
    return bus


def device_args(address, i2c_bus):
    """!
    Sort out a device driver's first two constructor arguments.

    Every driver takes (address=None, i2c_bus=None), and lets the bus come
    first instead, so all of these work:

        QwiicBME280()                    # default bus and address
        QwiicBME280(0x76)                # address
        QwiicBME280(machine.I2C(0))      # bus: machine.I2C, busio.I2C, smbus2.SMBus
                                         #      or a qwiic_i2c bus
        QwiicBME280(bus, 0x76)           # bus, then address
        QwiicBME280(0x76, i2c)           # address, then bus

    An address is always an int and a bus never is, so the two can't be confused.

    @param address: The driver's first argument
    @param i2c_bus: The driver's second argument
    @return **(address, i2c_bus)** The address (int or None) and the bus (or None)
    @exception TypeError: Two buses were given
    """
    if address is None or isinstance(address, int):
        return address, i2c_bus
    # The first argument is a bus, so the second (if any) is the address
    if i2c_bus is not None and not isinstance(i2c_bus, int):
        raise TypeError("qwiic: give one I2C bus and one int address, not two buses")
    return i2c_bus, address


def is_device_connected(address, *args, **kwargs):
    """!
    @param address: 7-bit device address
    @param args, kwargs: Passed to get_i2c_bus() to choose the bus
    @return **bool** True if a device acknowledges the address
    """
    return get_i2c_bus(*args, **kwargs).is_device_connected(address)


def _timing():
    return _platform_backend() or I2CBus


def delay_ms(ms):
    """!
    Block for at least ms milliseconds. For examples and scripts; drivers use
    the method on their bus object instead.
    """
    _timing().delay_ms(ms)


def delay_us(us):
    """!
    Block for at least us microseconds.
    """
    _timing().delay_us(us)


def ticks_ms():
    """!
    @return **int** A millisecond counter. Compare values with ticks_diff().
    """
    return _timing().ticks_ms()


def ticks_diff(end, start):
    """!
    @return **int** end - start in milliseconds, correct across a counter wrap
    """
    return _timing().ticks_diff(end, start)
