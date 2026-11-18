"""Smoke tests for every driver, against a fake I2C bus (no hardware).

For each driver this imports its modules, constructs every driver class with a
fake qwiic_i2c bus, and checks is_connected() and the shared class
attributes. It catches broken imports, renamed or missing methods and
constructor errors.

Run with: python -m unittest discover -s tests
"""

import importlib
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "qwiic_i2c"))
# Every driver directory, so drivers that use another driver (pi_servo_hat
# uses qwiic_pca9685) can import it
for _name in sorted(os.listdir(os.path.join(ROOT, "drivers"))):
    sys.path.append(os.path.join(ROOT, "drivers", _name))

import qwiic_i2c  # noqa: E402
from qwiic_repo import load_drivers  # noqa: E402


class FakeI2C(qwiic_i2c.I2CBus):
    """Every device is present and every register reads as zero."""

    name = "fake"

    def __init__(self):
        qwiic_i2c.I2CBus.__init__(self, None)
        self.writes = []

    def read_block(self, address, register, num_bytes):
        return [0] * num_bytes

    def write_block(self, address, register, data):
        self.writes.append((address, register, list(data)))

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


def driver_cases():
    # QWIIC_DRIVERS=a,b limits the test to those drivers
    only = [n for n in os.environ.get("QWIIC_DRIVERS", "").split(",") if n]
    for driver in load_drivers(only or None):
        if not driver.is_device:
            continue
        yield driver


class DriverSmokeTest(unittest.TestCase):
    def test_every_driver(self):
        for driver in driver_cases():
            with self.subTest(driver=driver.name):
                sys.path.insert(0, driver.path)
                try:
                    classes = driver.driver_classes()
                    if not classes and driver.platforms == ("cpython",):
                        # Linux-only drivers for serial/SPI devices have no I2C class
                        continue
                    self.assertTrue(classes, "no class defines available_addresses")
                    for module_name, class_name in classes:
                        module = importlib.import_module(module_name)
                        self.assertEqual(getattr(module, "__version__", driver.version), driver.version)
                        cls = getattr(module, class_name)
                        self.assertTrue(cls.available_addresses, class_name)
                        self.assertTrue(cls.device_name, class_name)
                        device = cls(i2c_bus=FakeI2C())
                        # Some drivers also check a chip ID, which reads as 0 here
                        self.assertIn(device.is_connected(), (True, False), class_name)
                        self.assertIn(device.address, cls.available_addresses)

                        # The bus may come first (QwiicBME280(bus), QwiicBME280(bus, 0x76))
                        bus = FakeI2C()
                        device = cls(bus)
                        self.assertIs(device._i2c, bus, class_name)
                        self.assertEqual(device.address, cls(i2c_bus=bus).address, class_name)
                        last = cls.available_addresses[-1]
                        device = cls(bus, last)
                        self.assertIs(device._i2c, bus, class_name)
                        self.assertEqual(device.address, last, class_name)
                finally:
                    sys.path.remove(driver.path)


if __name__ == "__main__":
    unittest.main()
