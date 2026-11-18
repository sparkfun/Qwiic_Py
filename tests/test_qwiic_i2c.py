"""Unit tests for qwiic_i2c, using fake native bus objects (no hardware).

Run with: python -m unittest discover -s tests
"""

import os
import sys
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "qwiic_i2c"))

import qwiic_i2c  # noqa: E402
import qwiic_i2c_circuitpython  # noqa: E402
import qwiic_i2c_linux  # noqa: E402
import qwiic_i2c_micropython  # noqa: E402


class FakeDevice(object):
    """Register map of one device, with an auto-incrementing register pointer."""

    def __init__(self, size=256):
        self.registers = bytearray(size)
        self.pointer = 0

    def write(self, data):
        data = bytes(data)
        if data:
            self.pointer = data[0]
            for i, value in enumerate(data[1:]):
                self.registers[(self.pointer + i) % len(self.registers)] = value

    def read(self, count):
        out = bytes(self.registers[(self.pointer + i) % len(self.registers)] for i in range(count))
        self.pointer = (self.pointer + count) % len(self.registers)
        return out


class FakeMachineI2C(object):
    """Mimics MicroPython's machine.I2C."""

    def __init__(self, devices):
        self.devices = devices

    def _dev(self, address):
        if address not in self.devices:
            raise OSError(19)
        return self.devices[address]

    def scan(self):
        return sorted(self.devices)

    def writeto(self, address, data, stop=True):
        self._dev(address).write(data)

    def readfrom(self, address, count):
        return self._dev(address).read(count)

    def readfrom_mem(self, address, register, count):
        dev = self._dev(address)
        dev.pointer = register
        return dev.read(count)

    def writeto_mem(self, address, register, data):
        self._dev(address).write(bytes([register]) + bytes(data))


class FakeBusioI2C(FakeMachineI2C):
    """Mimics CircuitPython's busio.I2C."""

    def __init__(self, devices):
        FakeMachineI2C.__init__(self, devices)
        self.locked = False

    def try_lock(self):
        if self.locked:
            return False
        self.locked = True
        return True

    def unlock(self):
        self.locked = False

    def readfrom_into(self, address, buffer):
        buffer[:] = self._dev(address).read(len(buffer))

    def writeto_then_readfrom(self, address, out_buffer, in_buffer):
        self._dev(address).write(out_buffer)
        in_buffer[:] = self._dev(address).read(len(in_buffer))


class FakeSMBus(object):
    """Mimics smbus2.SMBus."""

    def __init__(self, devices):
        self.devices = devices

    def _dev(self, address):
        if address not in self.devices:
            raise OSError(121, "Remote I/O error")
        return self.devices[address]

    def write_quick(self, address):
        self._dev(address)

    def read_byte(self, address):
        return self._dev(address).read(1)[0]

    def read_byte_data(self, address, register):
        dev = self._dev(address)
        dev.pointer = register
        return dev.read(1)[0]

    def read_word_data(self, address, register):
        dev = self._dev(address)
        dev.pointer = register
        data = dev.read(2)
        return data[0] | (data[1] << 8)

    def read_i2c_block_data(self, address, register, length):
        if length > 32:
            raise ValueError("SMBus blocks are limited to 32 bytes")
        dev = self._dev(address)
        dev.pointer = register
        return list(dev.read(length))

    def write_byte(self, address, value):
        self._dev(address).write([value])

    def write_byte_data(self, address, register, value):
        self._dev(address).write([register, value])

    def write_word_data(self, address, register, value):
        self._dev(address).write([register, value & 0xFF, value >> 8])

    def write_i2c_block_data(self, address, register, data):
        if len(data) > 32:
            raise ValueError("SMBus blocks are limited to 32 bytes")
        self._dev(address).write([register] + list(data))

    def i2c_rdwr(self, *messages):
        for message in messages:
            dev = self._dev(message.addr)
            if message.flags & 1:  # I2C_M_RD
                message.buf[:] = dev.read(message.len)
            else:
                dev.write(bytes(message.buf[: message.len]))


class FakeMsg(object):
    def __init__(self, addr, flags, data):
        self.addr = addr
        self.flags = flags
        self.buf = bytearray(data)
        self.len = len(self.buf)

    def __iter__(self):
        return iter(self.buf)


class FakeI2CMsg(object):
    @staticmethod
    def read(address, length):
        return FakeMsg(address, 1, bytes(length))

    @staticmethod
    def write(address, data):
        return FakeMsg(address, 0, bytes(data))


class FakeSmbus2Module(object):
    i2c_msg = FakeI2CMsg


ADDRESS = 0x42


class BackendContract(object):
    """Behaviour every backend must share."""

    def make(self, devices):
        raise NotImplementedError

    def setUp(self):
        self.device = FakeDevice()
        self.driver = self.make({ADDRESS: self.device})

    def test_byte_round_trip(self):
        self.driver.write_byte(ADDRESS, 0x10, 0xAB)
        self.assertEqual(self.driver.read_byte(ADDRESS, 0x10), 0xAB)

    def test_word_is_little_endian(self):
        self.driver.write_word(ADDRESS, 0x20, 0x1234)
        self.assertEqual(self.device.registers[0x20], 0x34)
        self.assertEqual(self.device.registers[0x21], 0x12)
        self.assertEqual(self.driver.read_word(ADDRESS, 0x20), 0x1234)

    def test_block_round_trip(self):
        self.driver.write_block(ADDRESS, 0x30, [1, 2, 3, 4])
        self.assertEqual(list(self.driver.read_block(ADDRESS, 0x30, 4)), [1, 2, 3, 4])

    def test_long_block_write(self):
        data = list(range(91))
        self.driver.write_block(ADDRESS, 0x00, bytes(data))
        self.assertEqual(list(self.device.registers[:91]), data)

    def test_register_as_bytes(self):
        # A register given as bytes is sent first, then read after a repeated start
        self.device.registers[0x05] = 0xEA
        self.device.registers[0x06] = 0xCC
        self.assertEqual(list(self.driver.read_block(ADDRESS, [0x05], 2)), [0xEA, 0xCC])
        self.assertEqual(list(self.driver.read_block(ADDRESS, b"\x05", 2)), [0xEA, 0xCC])
        self.driver.write_block(ADDRESS, [0x40], [7, 8])
        self.assertEqual(list(self.device.registers[0x40:0x42]), [7, 8])

    def test_write_byte_without_register_and_raw_read(self):
        # write_byte(address, None, value) sends just the byte (a command)
        self.device.registers[0x07] = 0x5A
        self.driver.write_byte(ADDRESS, None, 0x07)
        self.assertEqual(self.driver.read_byte(ADDRESS), 0x5A)

    def test_word_byteorder(self):
        self.driver.write_word(ADDRESS, 0x50, 0x1234, byteorder="big")
        self.assertEqual(list(self.device.registers[0x50:0x52]), [0x12, 0x34])
        self.assertEqual(self.driver.read_word(ADDRESS, 0x50, byteorder="big"), 0x1234)
        self.assertEqual(self.driver.read_word(ADDRESS, 0x50), 0x3412)

    def test_only_two_transfers_per_backend(self):
        # The conveniences live in the base class, not in each backend
        for name in ("read_byte", "write_byte", "read_word", "write_word"):
            self.assertNotIn(name, type(self.driver).__dict__, name)
        for name in ("read_block", "write_block"):
            self.assertIn(name, type(self.driver).__dict__, name)

    def test_is_device_connected(self):
        self.assertTrue(self.driver.is_device_connected(ADDRESS))
        self.assertFalse(self.driver.is_device_connected(0x10))

    def test_scan(self):
        self.assertEqual(list(self.driver.scan()), [ADDRESS])

    def test_timing_helpers(self):
        start = self.driver.ticks_ms()
        self.driver.delay_ms(5)
        self.driver.delay_us(10)
        self.assertGreaterEqual(self.driver.ticks_diff(self.driver.ticks_ms(), start), 4)

    def test_no_duplicate_names(self):
        names = [n for n in dir(self.driver) if not n.startswith("_")]
        normalized = [n.replace("_", "").lower() for n in names]
        self.assertEqual(len(normalized), len(set(normalized)), names)


class MicroPythonTest(BackendContract, unittest.TestCase):
    def make(self, devices):
        return qwiic_i2c_micropython.MicroPythonI2C(native_bus=FakeMachineI2C(devices))

    def test_native_bus_detection(self):
        self.assertTrue(qwiic_i2c_micropython.MicroPythonI2C.is_native_bus(FakeMachineI2C({})))
        self.assertFalse(qwiic_i2c_micropython.MicroPythonI2C.is_native_bus(object()))


class MicroPythonDefaultBusTest(unittest.TestCase):
    # _default_bus() on each port, with fake sys and machine modules

    def default_bus(self, platform, machine_name="", sda=None, scl=None, freq=100000):
        calls = []

        class FakeI2C:
            def __init__(self, *args, **kwargs):
                calls.append((args, kwargs))

        fake_machine = types.ModuleType("machine")
        fake_machine.I2C = FakeI2C
        fake_machine.Pin = lambda n: n
        fake_sys = types.SimpleNamespace(
            platform=platform,
            implementation=types.SimpleNamespace(name="micropython", _machine=machine_name))
        real_sys = qwiic_i2c_micropython.sys
        sys.modules["machine"] = fake_machine
        qwiic_i2c_micropython.sys = fake_sys
        try:
            qwiic_i2c_micropython._default_bus(sda, scl, freq)
        finally:
            qwiic_i2c_micropython.sys = real_sys
            sys.modules.pop("machine", None)
        return calls

    def test_rp2_default_runs_at_100khz(self):
        self.assertEqual(self.default_bus("rp2"), [((), {"freq": 100000})])

    def test_esp32_default_runs_at_100khz(self):
        self.assertEqual(self.default_bus("esp32", "ESP32C3 module with ESP32C3"), [((), {"freq": 100000})])

    def test_esp32_with_pins(self):
        self.assertEqual(self.default_bus("esp32", sda=21, scl=22),
                         [((), {"scl": 22, "sda": 21, "freq": 100000})])


class CircuitPythonTest(BackendContract, unittest.TestCase):
    def make(self, devices):
        self.bus = FakeBusioI2C(devices)
        return qwiic_i2c_circuitpython.CircuitPythonI2C(native_bus=self.bus)

    def test_bus_unlocked_after_error(self):
        with self.assertRaises(OSError):
            self.driver.read_byte(0x10, 0x00)
        self.assertFalse(self.bus.locked)

    def test_native_bus_detection(self):
        self.assertTrue(qwiic_i2c_circuitpython.CircuitPythonI2C.is_native_bus(self.bus))
        self.assertFalse(qwiic_i2c_circuitpython.CircuitPythonI2C.is_native_bus(FakeMachineI2C({})))


class LinuxTest(BackendContract, unittest.TestCase):
    def make(self, devices):
        sys.modules["smbus2"] = FakeSmbus2Module()
        return qwiic_i2c_linux.LinuxI2C(native_bus=FakeSMBus(devices))

    def tearDown(self):
        sys.modules.pop("smbus2", None)

    def test_raw_word_read(self):
        self.device.registers[0] = 0x34
        self.device.registers[1] = 0x12
        self.device.pointer = 0
        self.assertEqual(self.driver.read_word(ADDRESS), 0x1234)

    def test_long_block_read(self):
        self.device.registers[:40] = bytes(range(40))
        self.assertEqual(list(self.driver.read_block(ADDRESS, 0x00, 40)), list(range(40)))

    def test_native_bus_detection(self):
        self.assertTrue(qwiic_i2c_linux.LinuxI2C.is_native_bus(FakeSMBus({})))

    def test_jetson_probes_with_a_read(self):
        # Jetson boards time out on write_quick, so is_device_connected() reads
        class QuickWriteTimesOut(FakeSMBus):
            def write_quick(self, address):
                raise TimeoutError(110, "Connection timed out")

        original = qwiic_i2c_linux._board_name
        try:
            for board, found in (("NVIDIA Jetson Nano Developer Kit", True),
                                 ("NVIDIA Jetson Xavier NX Developer Kit", True),
                                 ("NVIDIA Jetson Orin Nano Developer Kit", True),
                                 ("Raspberry Pi 5 Model B Rev 1.0", False)):
                qwiic_i2c_linux._board_name = lambda board=board: board
                bus = qwiic_i2c_linux.LinuxI2C(native_bus=QuickWriteTimesOut({ADDRESS: FakeDevice()}))
                self.assertEqual(bus.is_device_connected(ADDRESS), found, board)
        finally:
            qwiic_i2c_linux._board_name = original


class GetI2CBusTest(unittest.TestCase):
    def setUp(self):
        qwiic_i2c._default_bus = None
        self.devices = {ADDRESS: FakeDevice()}

    def tearDown(self):
        qwiic_i2c._default_bus = None

    def test_existing_driver_is_returned_unchanged(self):
        sys.modules["smbus2"] = FakeSmbus2Module()
        try:
            driver = qwiic_i2c_linux.LinuxI2C(native_bus=FakeSMBus(self.devices))
        finally:
            sys.modules.pop("smbus2", None)
        self.assertIs(qwiic_i2c.get_i2c_bus(driver), driver)

    def test_native_bus_is_wrapped(self):
        if not qwiic_i2c_linux.LinuxI2C.is_platform():
            self.skipTest("needs Linux")
        bus = FakeSMBus(self.devices)
        driver = qwiic_i2c.get_i2c_bus(bus)
        self.assertIsInstance(driver, qwiic_i2c_linux.LinuxI2C)
        self.assertIs(driver.native_bus, bus)
        self.assertTrue(driver.is_device_connected(ADDRESS))
        self.assertTrue(qwiic_i2c.is_device_connected(ADDRESS, bus))

    def test_set_default_i2c_bus(self):
        sys.modules["smbus2"] = FakeSmbus2Module()
        try:
            first = qwiic_i2c_linux.LinuxI2C(native_bus=FakeSMBus(self.devices))
            second = qwiic_i2c_linux.LinuxI2C(native_bus=FakeSMBus({}))
        finally:
            sys.modules.pop("smbus2", None)
        self.assertIs(qwiic_i2c.set_default_i2c_bus(first), first)
        self.assertIs(qwiic_i2c.get_i2c_bus(), first)
        self.assertIs(qwiic_i2c.get_i2c_bus(None), first)
        self.assertTrue(qwiic_i2c.is_device_connected(ADDRESS))
        # An explicit bus is still used as given, and doesn't change the default
        self.assertIs(qwiic_i2c.get_i2c_bus(second), second)
        self.assertIs(qwiic_i2c.get_i2c_bus(), first)
        # A device driver created without a bus gets the default
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "drivers", "qwiic_tmp102"))
        import qwiic_tmp102
        self.assertIs(qwiic_tmp102.QwiicTMP102()._i2c, first)
        self.assertIs(qwiic_tmp102.QwiicTMP102(second)._i2c, second)
        # None resets to the platform default, created on next use
        self.assertIsNone(qwiic_i2c.set_default_i2c_bus(None))
        self.assertIsNone(qwiic_i2c._default_bus)

    def test_set_default_wraps_native_bus(self):
        if not qwiic_i2c_linux.LinuxI2C.is_platform():
            self.skipTest("needs Linux")
        bus = FakeSMBus(self.devices)
        driver = qwiic_i2c.set_default_i2c_bus(bus)
        self.assertIsInstance(driver, qwiic_i2c_linux.LinuxI2C)
        self.assertIs(driver.native_bus, bus)
        self.assertIs(qwiic_i2c.get_i2c_bus(), driver)

    def test_module_timing_helpers(self):
        start = qwiic_i2c.ticks_ms()
        qwiic_i2c.delay_ms(2)
        self.assertGreaterEqual(qwiic_i2c.ticks_diff(qwiic_i2c.ticks_ms(), start), 1)

    def test_device_args(self):
        bus = object()
        self.assertEqual(qwiic_i2c.device_args(None, None), (None, None))
        self.assertEqual(qwiic_i2c.device_args(0x76, None), (0x76, None))
        self.assertEqual(qwiic_i2c.device_args(0x76, bus), (0x76, bus))
        self.assertEqual(qwiic_i2c.device_args(bus, None), (None, bus))
        self.assertEqual(qwiic_i2c.device_args(bus, 0x76), (0x76, bus))
        with self.assertRaises(TypeError):
            qwiic_i2c.device_args(bus, object())

    def test_register_bytes(self):
        self.assertEqual(qwiic_i2c.register_bytes(None), b"")
        self.assertEqual(qwiic_i2c.register_bytes(0x10), b"\x10")
        self.assertEqual(qwiic_i2c.register_bytes([0x01, 0x0F]), b"\x01\x0f")

    def test_no_2x_names(self):
        for name in ("getI2CDriver", "isDeviceConnected", "ping"):
            self.assertFalse(hasattr(qwiic_i2c, name), name)
        for name in ("write_command", "write_read_block"):
            self.assertFalse(hasattr(qwiic_i2c.I2CBus, name), name)


if __name__ == "__main__":
    unittest.main()
