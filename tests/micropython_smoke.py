# Smoke test for every driver on MicroPython's Unix port (no hardware).
#
# Run from the repository root:
#     micropython tests/micropython_smoke.py
#
# Imports each driver class listed in qwiic/qwiic_registry.py, creates it with
# a fake qwiic_i2c bus and calls is_connected(). This runs the code under
# MicroPython's own compiler and runtime, so it catches syntax and library
# features CPython has but MicroPython doesn't.

import os
import sys

sys.path.append("qwiic_i2c")
sys.path.append("qwiic")
for name in sorted(os.listdir("drivers")):
    sys.path.append("drivers/" + name)

import qwiic_i2c  # noqa: E402
from qwiic_registry import DRIVERS  # noqa: E402


class FakeI2C(qwiic_i2c.I2CBus):
    """Every device is present and every register reads as zero.

    Only the two transfers are faked, so the drivers also go through the
    base class's read_byte/write_byte/read_word/write_word.
    """

    def read_block(self, address, register, num_bytes):
        return [0] * num_bytes

    def write_block(self, address, register, data):
        pass

    def is_device_connected(self, address):
        return True

    def scan(self):
        return []

    @staticmethod
    def delay_ms(ms):
        pass

    @staticmethod
    def delay_us(us):
        pass


failures = 0
for module_name, class_name, device_name, addresses in DRIVERS:
    try:
        module = __import__(module_name)
        cls = getattr(module, class_name)
        device = cls(i2c_bus=FakeI2C())
        device.is_connected()
        # The bus may come first
        bus = FakeI2C()
        assert cls(bus)._i2c is bus
        assert cls(bus, addresses[-1]).address == addresses[-1]
        print("ok   %s.%s" % (module_name, class_name))
    except Exception as e:  # report every failure, not just the first
        failures += 1
        print("FAIL %s.%s: %s: %s" % (module_name, class_name, type(e).__name__, e))
        sys.print_exception(e)

print("%d of %d driver classes failed" % (failures, len(DRIVERS)))
sys.exit(1 if failures else 0)
