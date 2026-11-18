#-----------------------------------------------------------------------------
# oled_fonts.py
#
# Utilities to manage the fonts for the OLED display
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https:= www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2021 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
	
#
# Fonts live in the "fonts" folder next to this module, one file per font,
# named <fontnumber>_<fontname>.bin. Only when font data is requested is the
# data loaded for that font.
#
# The os module isn't part of the portable subset (and isn't available on every
# platform), so the font folder is found from __file__ with plain string
# operations and the font files are listed in _FONT_NAMES below.

import math

# Font names, by font number. Font n is in the file "<n>_<name>.bin".
_FONT_NAMES = ["font5x7", "font8x16", "7segment", "fontlargenumber", "fontlargeletter31x48"]

# font cache - the most recently used font
_fontCacheIndex = -1
_fontCache = None

_fontDir = None


#-----------------------------------------
# Font Object - to manage a font

class OLEDFont():

	def __init__(self, font_file):
		self.width = 0
		self.height = 0
		self.start_char = 0
		self.total_char = 0
		self.map_width = 0

		# The font data is chunked - broken up into characters within a dictionary
		# Good for memory state (fragementation), but slightly slower.
		self._fontData = []

		self._load_font_file(font_file)

	def _load_font_file(self, font_file):

		# OSError if the file is missing: check that the fonts were installed
		fp = open(font_file, 'rb')

		try:
			# read the font header
			fHeader = fp.read(6)
			fHeader = bytearray(fHeader) ## for int conversion
			self.width 		= fHeader[0]
			self.height 	= fHeader[1]
			self.start_char = fHeader[2]
			self.total_char = fHeader[3]
			self.map_width 	= fHeader[4]*100 + fHeader[5] #two bytes values into integer 16

			# build the list to store the fonts - list uses less mem than a dict. 
			self._fontData = [0]* (self.height//8 * self.total_char)	
			# Break font into rows - not as effeicent, but great for memory.
			# note: the fonts span rows - and each row is 8 bits. So i font height > 8,
			#       the font spans multiple rows.
			#
			# Double note: If the font is a single row - we add a byte to the row buffer
			#			   Seems no margin was encoded on this font, and this bust be added

			rowsPerChar = int(math.ceil(self.height/8.))

			# do we add a pad byte?
			nPad = (rowsPerChar == 1)*1

			# buffer padding bytes
			bBuffer = bytearray(nPad)

			# read in font
			for iChar in range(self.total_char * rowsPerChar):
				self._fontData[iChar] = bytearray(fp.read(self.width))  + bBuffer
		finally:
			fp.close()


	# method to override [] access for this object. 
	#
	# key => character index into the data. 

	def __getitem__(self, key):

		# key -> the absolute index into the font data array - not pretty, but that's fonts

		if key < 0 or key >= len(self._fontData):
			raise IndexError("Index (%d) out of range[0,%d]." % (key, len(self._fontData)))

		return self._fontData[key]


def _check_if_exists(filename):
	"""!
	Checks if a file exists, without the os module.
	"""
	try:
		f = open(filename, 'rb')
	except OSError:
		return False
	f.close()
	return True

# handy util
def _get_font_dir():

	global _fontDir

	if _fontDir is not None:
		return _fontDir

	first_font = "0_" + _FONT_NAMES[0] + ".bin"

	# First check if font directory exists where it is installed when using a frozen SparkFun MicroPython package
	# It should exist in "_frozen_data" if the package is frozen
	if _check_if_exists("_frozen_data/fonts/" + first_font):
		_fontDir = "_frozen_data/fonts"
		return _fontDir

	# Otherwise the fonts are next to this module. "/" works as the separator
	# on every platform, Windows included.
	try:
		here = __file__.replace("\\", "/")
	except NameError:
		here = ""

	if "/" in here:
		_fontDir = here.rsplit("/", 1)[0] + "/fonts"
	else:
		_fontDir = "fonts"

	return _fontDir

def count():
	"""!
	@return **int** The number of fonts
	"""
	return len(_FONT_NAMES)

def font_names():
	"""!
	@return **list of str** The font names, by font number
	"""
	return _FONT_NAMES

def get_font(font_number):
	"""!
	Load a font (or return it from the cache).

	@param font_number: The font number
	@return **OLEDFont** The font
	@exception OSError: The font file is missing (check that the package was installed with its fonts)
	"""

	global _fontCache, _fontCacheIndex

	if font_number != _fontCacheIndex:

		fFont = _get_font_dir() + "/" + str(font_number) + '_' + _FONT_NAMES[font_number] + '.bin'

		_fontCache = OLEDFont(fFont)
		_fontCacheIndex = font_number

	return _fontCache
