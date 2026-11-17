#-------------------------------------------------------------------------------
# qwiic_huskylens.py
#
# Python library for the DF Robot HuskyLens, available here:
# https://www.dfrobot.com/product-1922.html
#
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, February 2025
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2023 SparkFun Electronics
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
#===============================================================================

"""
qwiic_huskylens
============
Python module for the DFRobot HuskyLens for use with Sparkfun Qwiic
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c

_DEFAULT_NAME = "Qwiic HuskyLens"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x32]

class QwiicHuskyLens(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # See the huskylens User Guide here: https://wiki.microblocks.fun/en/extension_libraries/huskylens
    # From the user guide: 
    # HuskyLens has two object types: Blocks and Arrows.

    # Faces, colors, objects, and tags are Block type.
    # Lines are Arrow type.

    # HuskyLens can learn to recognize Objects and assigns an ID number to each learned Object. The ID numbers are consecutive.

    # Here is a sequence that needs to be followed in order to obtain any detected object information from the HuskyLens:
    # 1. Train HuskyLens using any supported algorithm.
    # 2. Set Communications mode
    # 3. Select Algorithm desired
    # 4. Make a request for Blocks or Arrows
    # 5. Analyze returned data and take action

    # Commands
    kCommandRequest = 0x20 # Request all blocks and arrows from the HUSKYLENS
    kCommandRequestBlocks = 0x21 # Request all blocks from the HUSKYLENS
    kCommandRequestArrows = 0x22 # Request all arrows from the HUSKYLENS
    kCommandRequestLearned = 0x23 # Request all learned blocks/arrows from the HUSKYLENS
    kCommandRequestBlocksLearned = 0x24 # Request all learned blocks from the HUSKYLENS
    kCommandRequestArrowsLearned = 0x25 # Request all learned arrows from the HUSKYLENS
    kCommandRequestById = 0x26 # Request block or arrow by ID from the HUSKYLENS
    kCommandRequestBlocksById = 0x27 # Request block by ID from the HUSKYLENS
    kCommandRequestArrowsById = 0x28 # Request arrow by ID from the HUSKYLENS
    kCommandReturnInfo = 0x29 # Return the number of blocks and arrows from the HUSKYLENS
    kCommandReturnBlock = 0x2A # Return the block information from the HUSKYLENS
    kCommandReturnArrow = 0x2B # Return the arrow information from the HUSKYLENS
    kCommandRequestKnock = 0x2C # Used to check if the HUSKYLENS is connected
    kCommandRequestAlgorithm = 0x2D # Change the algorithm of the HUSKYLENS
    kCommandReturnOk = 0x2E # Return result of request_algorithm or request_knock
    kCommandRequestCustomNames = 0x2F # Set a custom name for a learned object from the HUSKYLENS
    kCommandRequestPhoto = 0x30 # Save a photo on the HUSKYLENS SD Card
    kCommandRequestSendKnowledges = 0x32 # Save the current algorithms model to the SD Card
    kCommandRequestReceiveKnowledges = 0x33 # Load a model file from the SD Card to the current algorithm
    kCommandRequestCustomText = 0x34 # Place a string of text on the HUSKYLENS UI
    kCommandRequestClearText = 0x35 # Clear and delete all custom UI texts from the screen
    kCommandRequestLearn = 0x36 # Learn the current recognized object on screen with a chosen ID
    kCommandRequestForget = 0x37 # Forget learned objects for the current running algorithm
    kCommandRequestSaveScreenshot = 0x39 # Save a screenshot of the current UI to the HUSKYLENS SD Card
    kCommandRequestIsPro = 0x3B # Check what model your HUSKYLENS is
    kCommandReturnIsPro = 0x3B # Return the model of the HUSKYLENS
    kCommandRequestFirmwareVersion = 0x3C # Request the firmware version of the HUSKYLENS
    kCommandReturnBusy = 0x3D # Return busy if multiple commands are sent without waiting for OK
    kCommandReturnNeedPro = 0x3E # Return need pro if a pro only command is sent to the HUSKYLENS

    # Algorithms 
    # Note, algorithms are 16-bit values, but existing commands only use the low byte and have 0 for the high byte
    kAlgorithmFaceRecognition = 0x00
    kAlgorithmObjectTracking = 0x01
    kAlgorithmObjectRecognition = 0x02
    kAlgorithmLineTracking = 0x03
    kAlgorithmColorRecognition = 0x04
    kAlgorithmTagRecognition = 0x05
    kAlgorithmObjectClassification = 0x06

    def __init__(self, address=None, i2c_driver=None):
        """!
        Constructor

        @param int address: The I2C address to use for the device
            If not provided, the default address is used
        @param I2CDriver i2c_driver: An existing i2c driver object
            If not provided, a driver object is created
        @param int nLearned: The number of objects already learned.
            The HuskyLens will assign IDs to learned objects starting from nLearned + 1.
            It is assumed by the protocol that the IDs are consecutive.
        """

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver
        
        self.blocks = [] # The blocks (objects, faces, etc.) detected by the HuskyLens
        self.arrows = [] # The arrows (lines) detected by the HuskyLens
        self.nLearned = 0 # The number of objects/IDs already learned
        self.idToName = {} # A dictionary of IDs to names for learned objects

    def _checksum(self, pkt):
        """!
        Calculate the checksum for a packet to be sent to the HuskyLens

        @param list pkt: The I2C address to use for the device
            If not provided, the default address is used
        """
        # The checksum is the low-byte of the sum of all bytes in the packet, including the header and address
        return sum(pkt) & 0xFF

    def _send_command(self, command, data=None):
        """!
        Send a command to the HuskyLens

        @param int command: The command to send
        @param list data: The data to send with the command (optional)
        """

        dlen = 0
        if data is not None:
            dlen = len(data)
        
        # All packets have the same header and address, then variable data-length, command, data, and checksum
        pkt = [0x55, 0xAA, 0x11, dlen, command]
        
        if data is not None:
            pkt.extend(data)
        
        pkt.append(self._checksum(pkt))

        # Send the packet (Since huskylens has no notion of writing to specific registers, 
        # we just treat pkt[0] as the register so we can use write_block to write out the whole packet)
        self._i2c.write_block(self.address, pkt[0], pkt[1:])
    
    class _Response:
        def __init__(self, pkt):
            self.header = pkt[0]
            self.header2 = pkt[1]
            self.address = pkt[2]
            self.dlen = pkt[3]
            self.command = pkt[4]
            self.data = pkt[5:-1]
            self.checksum = pkt[-1]
            self.valid = self.checksum == sum(pkt[:-1]) & 0xFF

    def _get_response(self):
        """!
        Get a response from the HuskyLens

        @param int command: The command to send
        @return _Response: The response from the HuskyLens
        """
        # Sometimes we receive some invalid bytes before the address so we want to read until we get the first header byte
        readBytes = [0]
        while readBytes[0] != 0x55:
            readBytes[0] = self._i2c.read_byte(self.address)

        # First read the header, address, data length and command bytes
        # so we know how much data we expect.
        readBytes.extend(list(self._i2c.read_block(self.address, None, 4)))

        # Read the rest of the data
        leftToRead = readBytes[3] + 1 # Data length + 1 byte for checksum
        readBytes.extend(list(self._i2c.read_block(self.address, None, leftToRead)))

        return self._Response(readBytes)

    def request_knock(self):
        """!
        Request a knock from the HuskyLens

        @return **bool** `True` if successful, otherwise `False`
        """
        # Send the request
        self._send_command(self.kCommandRequestKnock)

        # Get the response
        response = self._get_response()
        return response.valid and response.command == self.kCommandReturnOk

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        if not self._i2c.isDeviceConnected(self.address):
            return False
    
        if not self.request_knock():
            return False
        
        return True

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False
        
        # Initialize blocks, arrows and most importantly number of already learned ids with an initial request
        return self.request()

    # TODO: We might want to move these out of the class or make them functions returning dicts
    class _ReturnInfo():
        def __init__(self, resp):
            self.nBlocksAndArrows = resp.data[0] + (resp.data[1] << 8)
            self.nIDs = resp.data[2] + (resp.data[3] << 8)
            self.frameNumber = resp.data[4] + (resp.data[5] << 8)
    
    class Block():
        def __init__(self, resp):
            self.xCenter = resp.data[0] + (resp.data[1] << 8)
            self.yCenter = resp.data[2] + (resp.data[3] << 8)
            self.width = resp.data[4] + (resp.data[5] << 8)
            self.height = resp.data[6] + (resp.data[7] << 8)
            self.id = resp.data[8] + (resp.data[9] << 8)
    
    class Arrow():
        def __init__(self, resp):
            self.xOrigin = resp.data[0] + (resp.data[1] << 8)
            self.yOrigin = resp.data[2] + (resp.data[3] << 8)
            self.xTarget = resp.data[4] + (resp.data[5] << 8)
            self.yTarget = resp.data[6] + (resp.data[7] << 8)
            self.id = resp.data[8] + (resp.data[9] << 8)

    def _handle_response_blocks(self, response):
        """!
        Handle a response that contains block information (return info and blocks)

        @param _Response response: The response from the HuskyLens
        """
        if not response.valid or response.command != self.kCommandReturnInfo:
            return False
        
        returnInfo = self._ReturnInfo(response)

        # Get the blocks
        self.blocks = [None] * returnInfo.nBlocksAndArrows
        self.nLearned = returnInfo.nIDs

        for i in range(returnInfo.nBlocksAndArrows):
            response = self._get_response()
            if not response.valid or response.command != self.kCommandReturnBlock:
                return False

            self.blocks[i] = self.Block(response)

        return True
    
    def _handle_response_arrows(self, response):
        """!
        Handle a response that contains arrow information (return info and arrows)

        @param _Response response: The response from the HuskyLens
        """
        if not response.valid or response.command != self.kCommandReturnInfo:
            return False
        
        returnInfo = self._ReturnInfo(response)

        # Get the arrows
        self.arrows = [None] * returnInfo.nBlocksAndArrows
        self.nLearned = returnInfo.nIDs

        for i in range(returnInfo.nBlocksAndArrows):
            response = self._get_response()
            if not response.valid or response.command != self.kCommandReturnArrow:
                return False

            self.arrows[i] = self.Arrow(response)
        
        return True
    
    def _handle_response_mixed(self, response):
        """!
        Handle a response that contains both block and arrow information (return info, blocks, and arrows)
        
        @param _Response response: The response from the HuskyLens
        """
        if not response.valid or response.command != self.kCommandReturnInfo:
            return False
        
        returnInfo = self._ReturnInfo(response)

        # Get the blocks and arrows
        self.blocks = []
        self.arrows = []
        self.nLearned = returnInfo.nIDs

        for i in range(returnInfo.nBlocksAndArrows):
            response = self._get_response()
            if not response.valid:
                return False

            if response.command == self.kCommandReturnBlock:
                self.blocks.append(self.Block(response))
            elif response.command == self.kCommandReturnArrow:
                self.arrows.append(self.Arrow(response))
            else:
                return False
        
        return True

    def request(self):
        """!
        Request all blocks and arrows from the HuskyLens

        Will fill self.blocks and self.arrows with the returned information

        @return **bool** `True` if successful, otherwise `False`
        """
        # Send the request
        self._send_command(self.kCommandRequest)

        # Get the response
        return self._handle_response_mixed(self._get_response())
    
    def wait_for_objects_of_interest(self):
        """!
        Wait for the HuskyLens to detect objects of interest (blocks) based on the current algorithm
        """
        while True:
            self.request_blocks()
            if len(self.blocks) > 0:
                break
    
    def wait_for_lines_of_interest(self):
        """!
        Wait for the HuskyLens to detect lines of interest (arrows) based on the current algorithm
        """
        while True:
            self.request_arrows()
            if len(self.arrows) > 0:
                break

    def get_objects_of_interest(self):
        """!
        Get the objects of interest (blocks) detected by the HuskyLens based on the current algorithm

        Returned objects have the following properties:
        - id: The ID of the object
        - xCenter: The x-coordinate of the center of the object
        - yCenter: The y-coordinate of the center of the object
        - width: The width of the object
        - height: The height of the object

        @return **list** A list of Block objects
        """
        self.request_blocks()
        return self.blocks

    def get_lines_of_interest(self):
        """!
        Get the lines of interest (arrows) detected by the HuskyLens based on the current algorithm

        Returned objects have the following properties:
        - id: The ID of the object
        - xOrigin: The x-coordinate of the origin of the line
        - yOrigin: The y-coordinate of the origin of the line
        - xTarget: The x-coordinate of the target of the line
        - yTarget: The y-coordinate of the target of the line

        @return **list** A list of Arrow objects
        """
        self.request_arrows()
        return self.arrows

    def request_blocks(self):
        """!
        Request all blocks from the HuskyLens

        Will fill self.blocks with the returned information

        @return **bool** `True` if successful, otherwise `False`
        """
        # Send the request
        self._send_command(self.kCommandRequestBlocks)

        # Get the response
        return self._handle_response_blocks(self._get_response())

    def request_arrows(self):
        """!
        Request all arrows from the HuskyLens

        Will fill self.arrows with the returned information

        @return **bool** `True` if successful, otherwise `False`
        """
        # Send the request
        self._send_command(self.kCommandRequestArrows)

        # Get the response
        return self._handle_response_arrows(self._get_response())

    def request_learned(self):
        """!
        Request all learned blocks and arrows from the HuskyLens
        """
        # Send the request
        self._send_command(self.kCommandRequestLearned)
        
        # Get the response
        return self._handle_response_mixed(self._get_response())

    def request_blocks_learned(self):
        """!
        Request all learned blocks from the HuskyLens
        """
        # Send the request
        self._send_command(self.kCommandRequestBlocksLearned)
        
        # Get the response
        return self._handle_response_blocks(self._get_response())

    def request_arrows_learned(self):
        """!
        Request all learned arrows from the HuskyLens
        """
        # Send the request
        self._send_command(self.kCommandRequestArrowsLearned)
        
        # Get the response
        return self._handle_response_arrows(self._get_response())

    def request_by_id(self, id):
        """!
        Request all blocks or arrows by a given ID from the HuskyLens

        This will fill self.blocks or self.arrows with the returned information

        @param int id: The ID to request
        """
        # Send the request
        self._send_command(self.kCommandRequestById, [id & 0xFF, id >> 8])

        # Get the response
        self._handle_response_mixed(self._get_response())

    def request_blocks_by_id(self, id):
        """!
        Request all blocks by a given ID from the HuskyLens

        This will fill self.blocks with the returned information

        @param int id: The ID to request
        """
        # Send the request
        self._send_command(self.kCommandRequestBlocksById, [id & 0xFF, id >> 8])

        # Get the response
        self._handle_response_blocks(self._get_response())

    def request_arrows_by_id(self, id):
        """!
        Request all arrows by a given ID from the HuskyLens

        This will fill self.arrows with the returned information

        @param int id: The ID to request
        """
        # Send the request
        self._send_command(self.kCommandRequestArrowsById, [id & 0xFF, id >> 8])

        # Get the response
        self._handle_response_arrows(self._get_response())

    def request_algorithm(self, algorithm):
        """!
        Change the algorithm of the HuskyLens and return the result.

        @param int algorithm: The algorithm to set. See the kAlgorithm constants.

        @return **bool** `True` if successful, otherwise `False`.
        """
        if algorithm not in [self.kAlgorithmFaceRecognition, 
                            self.kAlgorithmObjectTracking, 
                            self.kAlgorithmObjectRecognition, 
                            self.kAlgorithmLineTracking, 
                            self.kAlgorithmColorRecognition, 
                            self.kAlgorithmTagRecognition, 
                            self.kAlgorithmObjectClassification]:
            return False

        # Send the request
        self._send_command(self.kCommandRequestAlgorithm, [algorithm & 0xFF, algorithm >> 8])

        # Get the response
        response = self._get_response()
        return response.valid and response.command == self.kCommandReturnOk

    def set_algorithm(self, algorithm):
        """!
        Change the algorithm of the HuskyLens

        @param int algorithm: The algorithm to set. See the kAlgorithm constants.

        @return **bool** `True` if successful, otherwise `False`.
        """
        return self.request_algorithm(algorithm)

    def request_custom_names(self, id, name):
        """!
        Set a custom name for a learned object from the HuskyLens

        @param int id: The ID of the object
        @param str name: The name to set
        """
        data = [id, len(name) + 1]
        data.extend([ord(c) for c in name])
        data.append(0)
        self._send_command(self.kCommandRequestCustomNames, data)
        self.idToName[id] = name
    
    def get_name_for_id(self, id):
        """!
        Get the name of a learned object by its ID.

        Note: This will does not query the device and is based on internal program state, so it will not persist across program runs.

        @param int id: The ID of the object
        @return **str** The name of the object, or `None` if not found
        """
        # We store the names in a dictionary, so we can look them up by ID
        # The device doesn't return this in any way so we have to keep track of it ourselves
        # The device will show the names on screen however
        if id not in self.idToName:
            return None
        
        return self.idToName[id]

    def name_last(self, name):
        """!
        Set a custom name for the last learned object from the HuskyLens

        @param str name: The name to set
        """
        self.request_custom_names(self.nLearned, name)

    def request_photo(self):
        """!
        Save a photo on the HuskyLens SD Card
        """
        self._send_command(self.kCommandRequestPhoto)

    def request_send_knowledges(self, fileNum):
        """!
        Save the current algorithms model to the SD Card

        @param int fileNum: The file number to save
        """
        self._send_command(self.kCommandRequestSendKnowledges, [fileNum & 0xFF, fileNum >> 8])

    def request_receive_knowledges(self, fileNum):
        """!
        Load a model file from the SD Card to the current algorithm

        @param int fileNum: The file number to load
        """
        self._send_command(self.kCommandRequestReceiveKnowledges, [fileNum & 0xFF, fileNum >> 8])

    def request_custom_text(self, text, x=0, y=0):
        """!
        Place a string of text on the HuskyLens UI

        @param str text: The text to display
        @param int x: The x-coordinate of the text
        @param int y: The y-coordinate of the text
        """
        if len(text) > 20:
            return False
        
        if x > 255:
            data = [len(text), 0xFF, x % 255, y]
        else:
            data = [len(text), 0, x, y]

        data.extend([ord(c) for c in text])
        self._send_command(self.kCommandRequestCustomText, data)

        return True

    def write_to_screen(self, text, x=0, y=0):
        """!
        Place a string of text on the HuskyLens UI

        @param str text: The text to display
        @param int x: The x-coordinate of the text
        @param int y: The y-coordinate of the text
        """
        self.request_custom_text(text, x, y)

    def request_clear_text(self):
        """!
        Clear and delete all custom UI texts from the screen
        """
        self._send_command(self.kCommandRequestClearText)
    
    def clear_screen(self):
        """!
        Clear and delete all custom UI texts from the screen
        """
        self.request_clear_text()
    
    def request_learn(self, id):
        """!
        Learn a current recognized object on screen based on its ID

        @param int id: The ID to assign to the object
        """
        self._send_command(self.kCommandRequestLearn, [id & 0xFF, id >> 8])
        
    def learn_new(self):
        """!
        Learn the current recognized object on screen. It will be assigned an ID starting from nLearned + 1.
        """
        self.nLearned += 1
        self.request_learn(self.nLearned)
    
    def learn_same(self):
        """!
        Learn the current recognized object on screen with the same ID as the last learn call.
        """
        self.request_learn(self.nLearned)

    def request_forget(self):
        """!
        Forget learned objects for the current running algorithm
        """
        self.nLearned = 0
        self.idToName = {}
        self._send_command(self.kCommandRequestForget)
    
    def forget(self):
        """!
        Forget all learned objects for the current running algorithm
        """
        self.request_forget()
    
    def request_save_screenshot(self):
        """!
        Save a screenshot of the current UI to the HuskyLens SD Card
        """
        self._send_command(self.kCommandRequestSaveScreenshot)

    def request_is_pro(self):
        """!
        Check what model your HuskyLens is

        @return **bool** `True` if the HuskyLens is a pro model, otherwise `False`
        """
        self._send_command(self.kCommandRequestIsPro)

        response = self._get_response()
        if not response.valid or response.command != self.kCommandReturnIsPro:
            return False
        
        return response.data[0] == 1
    
    # def request_firmware_version(self):
    #     """!
    #     Request the firmware version of the HuskyLens. Not specified where this goes...
    #     """
    #     self._send_command(self.kCommandRequestFirmwareVersion)

        # The ICD is blank for the response to this or where this goes...
        # response = self._get_response()
        # if not response.valid:
        #     return None
        
        # return ".".join([str(c) for c in response.data])