#-----------------------------------------------------------------------
# Pi Servo Hat - Example 1
#-----------------------------------------------------------------------
#
# Written by  SparkFun Electronics, June 2019
# Author: Wes Furuya
#
# Compatibility:
#     * Original: https://www.sparkfun.com/products/14328
#     * v2: https://www.sparkfun.com/products/15316
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on Pi Servo Hat, check out the product page
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
This example should be used with a 90 degree (range of rotation) servo
on channel 0 of the Pi Servo Hat.

The extended code (commented out), at the end of the example could be
used to test the full range of the servo motion. However, users should
be wary as they can damage their servo by giving it a position outside
the standard range of motion.
"""

import sys
import qwiic_i2c
import pi_servo_hat


def run_example():
    print("\nSparkFun Pi Servo HAT Example 1\n")

    # Initialize Constructor
    hat = pi_servo_hat.PiServoHAT()

    if not hat.is_connected():
        print("The Pi Servo HAT isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    hat.begin()

    # Restart Servo Hat (in case Hat is frozen/locked)
    hat.restart()

    # Test Run
    #########################################
    # Moves servo position to 0 degrees (1ms), Channel 0
    hat.move_servo_position(0, 0)

    # Pause 1 sec
    qwiic_i2c.delay_ms(1000)

    # Moves servo position to 90 degrees (2ms), Channel 0
    hat.move_servo_position(0, 90)

    # Pause 1 sec
    qwiic_i2c.delay_ms(1000)

    # Sweep
    #########################################
    while True:
        for i in range(0, 90):
            print(i)
            hat.move_servo_position(0, i)
            qwiic_i2c.delay_ms(1)
        for i in range(90, 0, -1):
            print(i)
            hat.move_servo_position(0, i)
            qwiic_i2c.delay_ms(1)

    #########################################
    # Code below may damage servo, use with caution
    # Test sweep for full range of servo (outside 0 to 90 degrees).
    # while True:
    #     for i in range(-23, 100):
    #         print(i)
    #         hat.move_servo_position(0, i)
    #         qwiic_i2c.delay_ms(1)
    #     for i in range(100, -23, -1):
    #         print(i)
    #         hat.move_servo_position(0, i)
    #         qwiic_i2c.delay_ms(1)


if __name__ == "__main__":
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit):
        print("\nEnding Example 1")
        sys.exit(0)
