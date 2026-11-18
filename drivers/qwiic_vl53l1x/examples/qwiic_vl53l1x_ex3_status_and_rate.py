#-----------------------------------------------------------------------
# qwiic_vl53l1x_ex3_status_and_rate.py
#-----------------------------------------------------------------------
#
# Ported by  SparkFun Electronics, October 2019
# Author: Nathan Seidle
# Ported: Wes Furuya
# SparkFun Electronics
# 
# License: This code is public domain but you buy me a beer if you use
# this and we meet someday (Beerware license).
#
# Compatibility: https://www.sparkfun.com/products/14722
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on VL53L1x (ToF), check out the product page
# linked above.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:www.gnu.org/licenses/>.
#
#=======================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#=======================================================================

"""
	Reading distance from the laser based VL53L1X

	This example configures the sensor to short distance mode and then
	prints the distance to an object. The output also includes a
	running average of the last 10 readings along with some statistics,
	like signal rate and frequency (of the measurements).
	
	If you are getting weird readings, be sure the vacuum tape has been
	removed from the sensor.
"""

import sys
import qwiic_vl53l1x
import qwiic_i2c


def mean(numbers):
	return float(sum(numbers)) / max(len(numbers), 1)


def read_distance(tof):
	"""Take one measurement and return the distance in mm."""
	tof.start_ranging()						# Write configuration bytes to initiate measurement
	qwiic_i2c.delay_ms(5)
	distance = tof.get_distance()			# Get the result of the measurement from the sensor
	qwiic_i2c.delay_ms(5)
	tof.stop_ranging()
	return distance


def run_example():
	print("VL53L1X Qwiic Test\n")
	tof = qwiic_vl53l1x.QwiicVL53L1X()

	if not tof.begin():						# Checks the sensor and loads its default settings
		print("The Qwiic VL53L1X device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	print("Sensor online!\n")

	tof.set_distance_mode(1)	# Sets Distance Mode Short (Long- Change value to 2)

	distance = [] # Initialize list

	while True:
		start = qwiic_i2c.ticks_ms()
		distance.append(read_distance(tof))
		end = qwiic_i2c.ticks_ms()

		if len(distance) < 10:
			avgdistance = mean(distance)
		else:
			distance.remove(distance[0])
			avgdistance = mean(distance[len(distance)-10:len(distance)+1]) # Running average of last 10 measurements

		signalrate = tof.get_signal_rate()
		rangestatus = tof.get_range_status()
		elapsed_ms = qwiic_i2c.ticks_diff(end, start)

		print("Distance(mm): %s avgDistance(mm): %.2f Signal Rate: %s Range Status: %s Hz: %.5f" % (distance[len(distance)-1], avgdistance, signalrate, rangestatus, elapsed_ms / 1000.0))


if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as ex_err:
		print("\nEnding Example 3")
		sys.exit(0)
