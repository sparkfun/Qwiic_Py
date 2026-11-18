#-----------------------------------------------------------------------
# Qwiic Mux - Simple Disable Channels Example
#-----------------------------------------------------------------------
#
# Written by  SparkFun Electronics, June 2019
# Author: Wes Furuya
#
# Compatibility: https://www.sparkfun.com/products/14685
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on Qwiic Mux, check out the product page
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
This example disables channels 0 and 4.
"""

import sys
import qwiic_tca9548a


print("\nSparkFun TCA9548A 8-Channel Mux Example 4\n")

# Initialize Constructor
my_tca = qwiic_tca9548a.QwiicTCA9548A()

if not my_tca.is_connected():
    print("The Qwiic TCA9548A 8-Channel Mux device isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(1)

# List Channel Configuration
print("Enabled channels:", my_tca.list_channels())

# Disable Channels 0 and 4
my_tca.disable_channels([0, 4])

# List Channel Configuration
print("Enabled channels:", my_tca.list_channels())
