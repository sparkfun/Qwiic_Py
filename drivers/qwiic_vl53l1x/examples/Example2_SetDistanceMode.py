#-----------------------------------------------------------------------
# VL53L1X - Example 2
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
	prints the distance to an object. If you are getting weird readings,
	be sure the vacuum tape has been removed from the sensor.
"""

import qwiic_vl53l1x
import time

print("VL53L1X Qwiic Test\n")
ToF = qwiic_vl53l1x.QwiicVL53L1X()

if (ToF.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor online!\n")

ToF.set_distance_mode(1)	# Sets Distance Mode Short (Long- Change value to 2)

while True:
	try:
		ToF.start_ranging()						 # Write configuration bytes to initiate measurement
		time.sleep(.005)
		distance = ToF.get_distance()	 # Get the result of the measurement from the sensor
		time.sleep(.005)
		ToF.stop_ranging()

		distanceInches = distance / 25.4
		distanceFeet = distanceInches / 12.0

		print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))

	except Exception as e:
		print(e)
