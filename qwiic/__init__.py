#-----------------------------------------------------------------------------
# __init__.py
#
#------------------------------------------------------------------------
#
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#-----------------------------------------------------------------------------
# Usage
#
# The package provides a wrapper/overview of classes that encapsulate a specific 
# object that represnets a qwiic enabled device.
#
# Use of the pacakge is as follows:
#
# Option 1 - import the package, create the specific class
#
#	import qwiic
#   myDevice = qwiic.MyDevice()
#
# Option 2 - Import the object from the package directly
#
#	from qwiic import MyDevice
#   myDevice = MyDevice()
#
# Option 3 - Create the device object using the devices Human Readable Name (listed on the board)
# ### Not Implemented ###
#
#	import qwiic
#	myDevice = qwiic.createDevice("My Device Name")
#
# Option 4 - Create the device object using the devices i2c ID
# ### Not Implemented ###
#
#   import qwiic
#	myDevice = qwiic.createDevicByID(idNumber)
#
#
#
#-----------------------------------------------------------------------------
# try:
# 	from __future__ import print_function
# except:
# 	pass
	
# from . import qwiic_i2c
# from .qwiicdevice import QwiicDevice
import sys
import os

#-----------------------------------------------------------------------------
# Objects exported from this package. 
#
# For each device added, add it's device object import below.
#
# example:
#
# from .exampledevice import ExampleDevice

# from .qwiic_bme280 			import QwiicBME280
# from .qwiic_ccs811 			import QwiicCCS811
# from .qwiic_micro_oled 		import QwiicMicroOLED
# from .qwiic_proximity  		import QwiicProximity
# from .qwiic_distance   		import QwiicDistance
# from .qwiic_twist			import QwiicTwist
# from .qwiic_human_presence	import QwiicHumanPresence
# from .qwiic_scmd			import QwiicSCMD

#-----------------------------------------------------------------------
# The I2C Device driver
_i2cDriver = None

def _getI2CDriver():

	global _i2cDriver

	if _i2cDriver != None:
		return _i2cDriver

	_i2cDriver = qwiic_i2c.getI2CDriver()

	if _i2cDriver == None:
		print("Unable to get the plaform I2C driver for QWIIC.", file=sys.stderr)

	return _i2cDriver

# -----------------------------------------------------------------------
# I2C Bus / Device methods
#-----------------------------------------------------------------------
# 
# Cache for QWIIC device classes - determined at runtime
#
# The qwiic device classe defs are stored in a dictionary indexed by I2C 
# addresse(s) for the specific device. 

__availableDevices = {}

#-----------------------------------------------------------------------
# Dynamic loading of the qwiic driver object/classes.
#
# We determine what drivers are available at runtime and set those 
# classes as attributes for the this package. 
#
# The pattern followed is:
#   - list the modules in the driver subdirectory.
#	- Derive a class name for these 
#		- take "one_two_three" and camel case it = "OneTwoThree"
#	- Load the module
#	- Get the class definition
#	- set the <name> attribue to the class definition (which is the constructor)
#

def __loadDriver(driver_dir, driver_class):

	# load the driver module
	drvModule = __import__('qwiic.drivers.'+driver_dir + '.' + driver_dir, fromlist=(driver_class))

	# get the class for the driver

	dvrClass = getattr(drvModule, driver_class)

	# Create a driver instance AND change the value for this attribute to
	# the class definition (away from this function)

	drvObj = dvrClass()

	setattr(sys.modules[__name__], driver_class, dvrClass)

	return drvObj


# define a lambda to lazy load the driver and associated class. 
#
# This is called so we can capture the current scope/context when we create the lambda. 
def __lambda_factory(driver_dir, driver_class):

	return lambda : __loadDriver(driver_dir, driver_class)
# 
def __setupDriverAttributes():

	# get the subdirectories of the driver folder

	dirDriver = __file__.rsplit(os.sep, 1)[0] + os.sep + 'drivers'
	theDrivers = os.listdir(dirDriver)

	if len(theDrivers) == 0:
		print("No qwiic drivers found. Is the package installed properly")
		return

	for driver_dir in theDrivers:

		# camel case name 
		dvrClass = ''.join(x.capitalize() for x in driver_dir.split('_'))

		# Define a lambda function so we can lazy load the drivers as needed

		dvrFunc = __lambda_factory(driver_dir, dvrClass)

		# set attribute on this package for driver classname to 
		# the lambda function. This way, the driver isn't loaded until
		# needed. 
		setattr(sys.modules[__name__], dvrClass, dvrFunc)

		# Used to keep a running list of devices -- used in later functions
		__availableDevices[dvrClass] = ''
#

# setup the driver load functions

__setupDriverAttributes()
#-----------------------------------------------------------------------
# _getAvailableDevices()
#
# Return a dictionary that defines the available qwiic devices in the 
# package. The key is the I2C address. 
#
# Devices with multiple possible addresses have mulitple entries.
#
#

def _getAvailableDevices():

	global __availableDevices

	# do we already have these 
	if len(__availableDevices) > 0:  
		return __availableDevices

	# Time to build the dictionary. Go through and find all subclasses
	# of the QwiicDevice class. From this list, loop through and add 
	# the class to the dict - address is the key.

	subClasses = QwiicDevice.__subclasses__()

	for deviceClass in subClasses:

		# loop over the device addresses - add name/address 
		for addr in deviceClass.available_addresses:

			__availableDevices[addr] = deviceClass


	return __availableDevices
#-----------------------------------------------------------------------
# scan()
#
# Scans the I2C bus and returns a list of addresses that have a devices connected
#
def scan():
	""" Returns a list of addresses for the devices connected to the I2C bus."""

	i2cDriver = _getI2CDriver()

	if i2cDriver == None:
		return []
	
	return i2cDriver.scan()


#-----------------------------------------------------------------------
# list_devices()
#
#	Return a list of tubles that define the qwiic devices connected to the 
#   I2C bus.
#
def list_devices():
	""" Returns a list of known qwiic devices connected to the I2C bus.

		The return values are tuples which contain (device address, device name)
	"""

	# Scan the bus
	foundDevices = scan()
	if len(foundDevices) == 0:
		return []

	# What QWIIC devices do we know about -- what's defined in the package
	qwiicDefs = _getAvailableDevices()
	if len(qwiicDefs) == 0:
		return []

	foundQwiic = []
	# match scan, with definition
	for currAddress in foundDevices:

		if currAddress in qwiicDefs.keys():

			foundQwiic.append((currAddress, qwiicDefs[currAddress].device_name, qwiicDefs[currAddress].__name__))


	return foundQwiic


#-------------------
# get_devices()
#
# 	Returns a list of objects that define the qwiic devices attached to the 
#   I2C bus.
#
def get_devices():
	""" Returns a list of qwiic device objects for the qwiic devices connected to the 
		I2C bus.
	"""

	# Scan the bus
	foundDevices = scan()
	if len(foundDevices) == 0:
		return []

	# What QWIIC devices do we know about -- what's defined in the package
	qwiicDefs = _getAvailableDevices()
	if len(qwiicDefs) == 0:
		return []

	foundQwiic = []
	# match scan, with definition
	for currAddress in foundDevices:

		if currAddress in qwiicDefs.keys():
			# Create an object and append to our found list
			# note: class defs are stored in the defs dictionary..
			foundQwiic.append(qwiicDefs[currAddress]())


	return foundQwiic

#-------------------
# create_device()
#
# 	Given the Address, Name or Clasname of a qwiic device, create the 
#	assocaited device object and return it to the caller.
#
#   The intent is for the user to call list_devices(), find a device they like AND 
# 	use this method to create the device
#
def create_device(device=None):

	if device == None:
		print("No device provided.", file=sys.stderr)
		return None

	connDevices = list_devices()

	for currDev in connDevices:
		# the entries in the connDevices list are tuples, with the following values
		#   (I2C address, Device Name, Class Name)
		#
		# If the provided value is in the current device tuple, we're done
		if device in currDev:
			# we need the class definition 
			qwiicDefs = _getAvailableDevices()

			# Index using the I2C address (entry 0 of currDev)
			return qwiicDefs[currDev[0]]()

	# if we are here, we have an issue 
	print("Unabled to create requested device - is the device connected?", file=sys.stderr)

	return None


