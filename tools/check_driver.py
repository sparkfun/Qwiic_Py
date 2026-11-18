#!/usr/bin/env python3
"""Check drivers against the Qwiic_Py v3 conventions (see CONTRIBUTING.md).

Usage:
    check_driver.py [--no-mpy] [driver ...]

Checks every driver when none are named. Exits 1 if any check fails.
"""

import argparse
import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile

from qwiic_repo import load_drivers, read_text

CLASS_NAME = re.compile(r"^_?[A-Z][A-Za-z0-9]*$")
FUNCTION_NAME = re.compile(r"^_{0,2}[a-z][a-z0-9_]*$")
ARGUMENT_NAME = re.compile(r"^_?[a-z][a-z0-9_]*$")
EXAMPLE_NAME = re.compile(r"^(?P<driver>[a-z0-9_]+)_ex(?P<num>\d+[a-z]?)_[a-z0-9_]+\.py$")

# Modules a portable driver must not import
BANNED_IMPORTS = {"time", "utime", "os", "typing", "enum", "dataclasses", "subprocess", "smbus", "smbus2", "__future__"}

# 2.x qwiic_i2c names that no longer exist, and the removed connected property
OLD_API = re.compile(
    r"\b(getI2CDriver|isDeviceConnected|readByte|readWord|readBlock|writeCommand|writeByte|writeWord|"
    r"writeBlock|writeReadBlock|isPlatform|isNativeBus)\b|\.ping\(|\.connected\b(?!\s*\()|\bi2cbus\b"
    # Removed before 3.0: use write_byte(address, None, value) and read_block(address, register_bytes, n)
    r"|_i2c\.write_command\(|\.write_read_block\("
    # Renamed before 3.0: the bus object is an I2CBus, not a driver
    r"|\b(get_i2c_driver|set_default_i2c_driver|I2CDriver|i2c_driver)\b"
)

REQUIRED_PYPROJECT = {
    ("project", "requires-python"): ">=3.8",
    ("project", "readme"): "README.md",
}

RETIRED_FILES = ("setup.py", "setup.cfg", "requirements.txt", "DESCRIPTION.rst", ".readthedocs.yml", "MANIFEST.in")


class Report(object):
    def __init__(self):
        self.errors = []

    def error(self, path, line, message):
        self.errors.append("%s:%s: %s" % (os.path.relpath(path), line, message))


def _normalized(name):
    return name.replace("_", "").lower()


def check_source(report, driver, path, is_example):
    text = read_text(path)
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        report.error(path, e.lineno, "syntax error: %s" % e.msg)
        return

    for number, line in enumerate(text.splitlines(), 1):
        code = line.split("#", 1)[0]
        match = OLD_API.search(code)
        if match:
            report.error(path, number, "old API name %r: see MIGRATION.md for the v3 name" % match.group(0))

    portable = "micropython" in driver.platforms or "circuitpython" in driver.platforms
    is_core = not driver.is_device

    for node in ast.walk(tree):
        line = getattr(node, "lineno", 0)
        if isinstance(node, ast.Name) and node.id == "property":
            report.error(path, line, "property() is not allowed: use plain methods")
        elif isinstance(node, ast.ExceptHandler) and node.type is None:
            report.error(path, line, "bare except: catch a specific exception")
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom):
                if node.level and not driver.packages:
                    report.error(path, line, "relative import in a single-module driver")
                names = [node.module or ""]
            else:
                names = [alias.name for alias in node.names]
            for name in names:
                root = name.split(".")[0]
                if root in ("time", "utime") and not is_core and portable:
                    report.error(path, line, "import %s: use the qwiic_i2c timing helpers" % root)
                elif root == "__future__":
                    report.error(path, line, "from __future__ is not allowed")
                elif root in BANNED_IMPORTS and portable and not is_example and not is_core:
                    report.error(path, line, "import %s: not in the portable subset" % root)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print" and not is_example:
            report.error(path, line, "print() in a driver: return values or raise instead")

    if is_example:
        return

    # Public constants (module or class level, assigned a literal) are UPPER_CASE
    scopes = [tree.body] + [n.body for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    for body in scopes:
        for item in body:
            if isinstance(item, ast.Assign) and isinstance(item.value, (ast.Constant, ast.BinOp, ast.UnaryOp)):
                for target in item.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("_") and not target.id.isupper() and target.id != target.id.lower():
                        report.error(path, item.lineno, "constant %r is not UPPER_CASE" % target.id)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if not CLASS_NAME.match(node.name):
                report.error(path, node.lineno, "class name %r is not PascalCase" % node.name)
            seen = {}
            methods = set()
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.add(item.name)
            for item in node.body:
                names = []
                if isinstance(item, ast.FunctionDef):
                    names.append(item.name)
                elif isinstance(item, ast.Assign) and isinstance(item.value, ast.Name) and item.value.id in methods:
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            report.error(path, item.lineno, "%s = %s is an alias: one name per method" % (target.id, item.value.id))
                for name in names:
                    if name.startswith("__") and name.endswith("__"):
                        continue
                    key = _normalized(name)
                    if key in seen and seen[key] != name:
                        report.error(path, item.lineno, "%r duplicates %r" % (name, seen[key]))
                    seen[key] = name
        if isinstance(node, ast.FunctionDef):
            if not (node.name.startswith("__") and node.name.endswith("__")) and not FUNCTION_NAME.match(node.name):
                report.error(path, node.lineno, "function name %r is not snake_case" % node.name)
            arguments = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
            for extra in (node.args.vararg, node.args.kwarg):
                if extra:
                    arguments.append(extra)
            for argument in arguments:
                if argument.arg not in ("self", "cls") and not ARGUMENT_NAME.match(argument.arg):
                    report.error(path, node.lineno, "argument %r of %s is not snake_case" % (argument.arg, node.name))


def check_layout(report, driver):
    for name in RETIRED_FILES:
        if os.path.exists(os.path.join(driver.path, name)):
            report.error(os.path.join(driver.path, name), 0, "retired file: remove it")
    for name in ("README.md", "LICENSE"):
        if not os.path.exists(os.path.join(driver.path, name)):
            report.error(os.path.join(driver.path, name), 0, "missing")

    # MIT unless the driver's LICENSE says otherwise (ublox_gps is GPL-3.0-or-later)
    license_id = driver.pyproject.get("project", {}).get("license")
    license_path = os.path.join(driver.path, "LICENSE")
    license_text = read_text(license_path) if os.path.exists(license_path) else ""
    expected_license = "GPL-3.0-or-later" if "GNU General Public License" in license_text else "MIT"
    if license_id != expected_license:
        report.error(os.path.join(driver.path, "pyproject.toml"), 0, "project.license should be %r to match LICENSE (is %r)" % (expected_license, license_id))

    for (section, key), expected in REQUIRED_PYPROJECT.items():
        value = driver.pyproject.get(section, {}).get(key)
        if value != expected:
            report.error(os.path.join(driver.path, "pyproject.toml"), 0, "%s.%s should be %r (is %r)" % (section, key, expected, value))

    if not driver.py_modules and not driver.packages:
        report.error(os.path.join(driver.path, "pyproject.toml"), 0, "no py-modules or packages in [tool.setuptools]")
    for package in driver.packages:
        if not driver.package_data.get(package) and "micropython" in driver.platforms:
            report.error(os.path.join(driver.path, package), 0, "package without data files: flatten it into a single module")

    for path in driver.version_files():
        if not os.path.exists(path):
            continue  # reported below as missing
        version = driver.module_version(path)
        if version != driver.version:
            report.error(path, 0, "__version__ is %r but pyproject.toml says %r" % (version, driver.version))

    for _, rel in driver.source_files():
        if not os.path.exists(os.path.join(driver.path, rel)):
            report.error(os.path.join(driver.path, rel), 0, "listed in pyproject.toml but missing")

    if driver.is_device:
        examples = driver.example_files()
        if not examples:
            report.error(os.path.join(driver.path, "examples"), 0, "no examples")
        for name in examples:
            match = EXAMPLE_NAME.match(name)
            if not match or match.group("driver") != driver.name:
                report.error(os.path.join(driver.path, "examples", name), 0, "example name should be %s_ex<N>_<description>.py" % driver.name)


def check_mpy(report, driver, mpy_cross):
    with tempfile.TemporaryDirectory() as out:
        for rel in driver.python_files():
            path = os.path.join(driver.path, rel)
            result = subprocess.run(
                mpy_cross + ["-o", os.path.join(out, "x.mpy"), path],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
            )
            if result.returncode != 0:
                report.error(path, 0, "mpy-cross failed: %s" % result.stdout.strip().splitlines()[-1:])


def find_mpy_cross():
    exe = shutil.which("mpy-cross")
    if exe:
        return [exe]
    try:
        import mpy_cross  # noqa: F401
        return [sys.executable, "-m", "mpy_cross"]
    except ImportError:
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--no-mpy", action="store_true", help="skip the mpy-cross compile check")
    parser.add_argument("drivers", nargs="*")
    args = parser.parse_args()

    mpy_cross = None if args.no_mpy else find_mpy_cross()
    report = Report()
    drivers = load_drivers(args.drivers or None)
    for driver in drivers:
        check_layout(report, driver)
        for rel in driver.python_files():
            check_source(report, driver, os.path.join(driver.path, rel), is_example=False)
        for name in driver.example_files():
            check_source(report, driver, os.path.join(driver.path, "examples", name), is_example=True)
        if mpy_cross and ("micropython" in driver.platforms or "circuitpython" in driver.platforms):
            check_mpy(report, driver, mpy_cross)

    stale = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "gen_package_json.py"), "--check"] + [d.name for d in drivers],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
    )
    if stale.returncode != 0:
        report.errors.append(stale.stdout.strip())

    for error in report.errors:
        print(error)
    print("%d driver(s) checked, %d problem(s)" % (len(drivers), len(report.errors)))
    sys.exit(1 if report.errors else 0)


if __name__ == "__main__":
    main()
