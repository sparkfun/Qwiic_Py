#!/usr/bin/env python3
"""Write a driver's pyproject.toml from the standard v3 template.

Usage:
    make_pyproject.py <driver> --dist-name sparkfun-qwiic-bme280 \\
        --description "SparkFun Qwiic BME280 ..." [--version 3.0.0] \\
        [--module qwiic_bme280 ...] [--package qwiic_oled --data 'fonts/*.bin'] \\
        [--dependency 'pyserial; sys_platform == "linux"' ...] \\
        [--platform cpython ...]

Keeps the driver's existing PyPI name: pass it with --dist-name (PyPI treats
- and _ the same, so the hyphenated form is the same project).
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from qwiic_repo import ALL_PLATFORMS, GITHUB_REPO, REPO_ROOT, normalize_dist_name, package_path  # noqa: E402

QWIIC_I2C_REQUIREMENT = "sparkfun-qwiic-i2c>=3.0,<4"

TEMPLATE = """[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "{dist_name}"
version = "{version}"
description = "{description}"
readme = "README.md"
license = "MIT"
requires-python = ">=3.8"
authors = [{{name = "SparkFun Electronics", email = "info@sparkfun.com"}}]
dependencies = [{dependencies}]
keywords = ["electronics", "maker", "qwiic"{keywords}]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: Implementation :: CPython",{micropython_classifier}
    "Topic :: System :: Hardware",
]

[project.urls]
Homepage = "https://www.sparkfun.com/qwiic"
Documentation = "https://docs.sparkfun.com/Qwiic_Py/{driver}/"
Source = "https://github.com/{repo}/tree/main/{rel_path}"
Issues = "https://github.com/{repo}/issues"

[tool.setuptools]
{setuptools}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("driver")
    parser.add_argument("--dist-name", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--version", default="3.0.0")
    parser.add_argument("--module", action="append", default=[], help="single-file module (repeatable)")
    parser.add_argument("--package", help="package directory, only for drivers with data files")
    parser.add_argument("--data", action="append", default=[], help="package data glob, relative to the package")
    parser.add_argument("--dependency", action="append", default=[], help="extra requirement (repeatable)")
    parser.add_argument("--no-qwiic-i2c", action="store_true", help="the driver doesn't use qwiic_i2c")
    parser.add_argument("--platform", action="append", choices=ALL_PLATFORMS, help="limit platforms (default: all)")
    parser.add_argument("--keyword", action="append", default=[])
    args = parser.parse_args()

    path = package_path(args.driver)
    if not os.path.isdir(path):
        sys.exit("no such driver: " + path)
    if not args.module and not args.package:
        args.module = [args.driver]

    requirements = ([] if args.no_qwiic_i2c else [QWIIC_I2C_REQUIREMENT]) + args.dependency
    platforms = args.platform or list(ALL_PLATFORMS)

    setuptools = []
    if args.module:
        setuptools.append("py-modules = [%s]" % ", ".join('"%s"' % m for m in args.module))
    if args.package:
        setuptools.append('packages = ["%s"]' % args.package)
        if args.data:
            setuptools.append("")
            setuptools.append("[tool.setuptools.package-data]")
            setuptools.append('%s = [%s]' % (args.package, ", ".join('"%s"' % d for d in args.data)))

    text = TEMPLATE.format(
        dist_name=normalize_dist_name(args.dist_name),
        version=args.version,
        description=args.description.replace('"', '\\"'),
        dependencies=", ".join('"%s"' % r.replace('"', "'") for r in requirements),
        keywords="".join(', "%s"' % k for k in args.keyword),
        micropython_classifier=(
            '\n    "Programming Language :: Python :: Implementation :: MicroPython",' if "micropython" in platforms else ""
        ),
        driver=args.driver,
        rel_path=os.path.relpath(path, REPO_ROOT).replace(os.sep, "/"),
        repo=GITHUB_REPO,
        setuptools="\n".join(setuptools),
    )
    if args.platform:
        text += '\n[tool.qwiic]\nplatforms = [%s]\n' % ", ".join('"%s"' % p for p in platforms)

    with open(os.path.join(path, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", os.path.relpath(os.path.join(path, "pyproject.toml")))


if __name__ == "__main__":
    main()
