#! /bin/bash

# The MIT License (MIT)
#
# Copyright (c) 2021 Scott Shawcroft for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# This script builds the bundle

set -e

# This script gets executed in "test" steps for non-release builds. See the "Build assets" step in release.yml for the build of actual release artifacts
# Gather the package submods that are supported in CircuitPython and create a comma-separated string to pass to circuitpython-build-bundles
# CIRCUP_DIRS="$(paste -sd ',' circuitpython_support.txt | sed 's/,/, /g')"
# echo "FOUND CIRCUP DIRS: ${CIRCUP_DIRS}"
circuitpython-build-bundles --filename_prefix qwiic-py --library_location qwiic/drivers --library_depth 1 --package_folder_prefix "Qwiic, qwiic, Pi"
