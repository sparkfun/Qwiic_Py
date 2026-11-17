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
	
import sys
import os

import math

# Define storage for fonts

# map - map font index to font name
_fontIndexMap=[]

# font cache - maps name to font data
_fontCacheIndex = -1
_fontCache=None

_isInited = False



#-----------------------------------------
# Font Object - to manage a font

class OLEDFont():

	def __init__(self, fontFile):
		self.width = 0
		self.height = 0
		self.start_char = 0
		self.total_char = 0
		self.map_width = 0

		# The font data is chunked - broken up into characters within a dictionary
		# Good for memory state (fragementation), but slightly slower.
		self._fontData = []

		self._loadFontFile(fontFile)

	def _loadFontFile(self, fontFile):

		fp = None

		try:
			fp = open(fontFile, 'rb')

		except Exception as exError:
			print("Error opening font file: %s" % fontFile)

			raise exError

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

			try:

				self._fontData[iChar] = bytearray(fp.read(self.width))  + bBuffer

			except Exception as exError:
				print("Error reading font data. Character: %d, File:%s" % (iChar, _loadFontFile))

				fp.close()
				# cascade this up
				raise exError

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
	Checks if a file or directory exists. Works on MicroPython and CircuitPython
	which do not have os.path functions (as well as Linux which does).
	"""
	try:
		os.stat(filename)
		return True
	except:
		return False
		
# handy util
def _getFontDir():

	# First check if font directory exists where it is installed when using a frozen SparkFun MicroPython package
	# It should exist in "_frozen_data" if the package is frozen
	if _check_if_exists("_frozen_data" + os.sep + "fonts"):
		return "_frozen_data" + os.sep + "fonts"

	return __file__.rsplit(os.sep, 1)[0] +  os.sep + "fonts"

#-----------------------------------------
# General Structure
#
# Fonts are stored in the fonts subfolder of this package. Uses filenames
# to deliniate the fonts.
#
# Name Structure
#      <fontnumber>_<fontname>.bin
#
# This system lists the filenames and builds the index map
#
# Only when font data is requested is the data loaded for that font.
# 
# 
def _initFontSystem():

	global _isInited, _fontIndexMap

	if _isInited:
		return

	_isInited = True

	fDir = _getFontDir()

	try: 
		tmpFiles = os.listdir(fDir)
	except:
		print("OLED fonts do not exists - check your installation")
		return


	fontFiles = []

	for tFile in tmpFiles:
		if tFile.find('.bin') == -1:
			continue

		fontFiles.append(tFile)

	# get our font names 

	if len(fontFiles) == 0:
		print("OLED - no fonts found")
		return


	# build our font index

	_fontIndexMap = [''] * len(fontFiles)

	for fBase in fontFiles:

		iSep = fBase.find('_')
		if iSep == -1:
			print("Invalid Font File: %s " % fBase)
			continue
		nFont = int(fBase[0:iSep])

		# stash the name, strip off the number and the suffix
		_fontIndexMap[nFont] = fBase[iSep+1:-4]

def count():

	if not _isInited:
		_initFontSystem()

	return len(_fontIndexMap)

def font_names():

	if not _isInited:
		_initFontSystem()

	return _fontIndexMap

def get_font(iFont):

	global _fontCache, _fontCacheIndex

	if not _isInited:
		_initFontSystem()

	if iFont != _fontCacheIndex:

		fFont = _getFontDir() + os.sep + str(iFont) + '_' + _fontIndexMap[iFont] + '.bin'

		_fontCache = OLEDFont(fFont)
		_fontCacheIndex = iFont

	return _fontCache


