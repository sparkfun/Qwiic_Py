#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex4_HeartBeat_Plotter.py
#
# Simple example for the qwiic MAX3010x device
# Shows the user's heart beat on a graphical plotter
# Using Matplotlib
# To learn more about plotting data in python check out this tutorial:
# https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/
# The example code below was built using the code from the previously mentioned tutorial.
# Thanks Shawn Hymel!
#
# Instructions:
#   1) Install MatplotLib (see below)
#   2) Connect sensor to system via qwiic cable
#   3) Attach sensor to your finger with a rubber band (see below)
#   4) Run this python example
#   5) Checkout the blips!
#   6) Feel the pulse on your neck and watch it mimic the blips
#
#   It is best to attach the sensor to your finger using a rubber band or other tightening
#   device. Humans are generally bad at applying constant pressure to a thing. When you
#   press your finger against the sensor it varies enough to cause the blood in your
#   finger to flow differently which causes the sensor readings to go wonky.
#
# MatplotLib install
# Install Dependencies
# Like any good Linux project, we need to install a number of dependencies and libraries 
# in order to get matplotlib to run properly. Make sure you have an Internet connection 
# and in a terminal, enter the following commands. You may need to wait several minutes 
# while the various packages are downloaded and installed.
#
# sudo apt-get update
# sudo apt-get install libatlas3-base libffi-dev at-spi2-core python3-gi-cairo
# sudo pip3 install cairocffi
# sudo pip3 install matplotlib
#
#------------------------------------------------------------------------
#
# Written by Pete Lewis
# SparkFun Electronics, May 2020
#
# Based on code from the SparkFun MAX3010x Sensor Arduino Library
# https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library
# By: Nathan Seidle @ SparkFun Electronics, October 2nd, 2016
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
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
# Example 4
#

import qwiic_max3010x
import time
import sys

sensor = qwiic_max3010x.QwiicMax3010x()

#Plotter Stuff
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xlen= 100 #sample number, increments and is used for labeling x axis in plot
xs = list(range(0,xlen))
ys = [0]*xlen
line, = ax.plot(xs, ys)
plt.title('Heartbeat over time')
plt.ylabel('IR Value')

# This function is called periodically from FuncAnimation
def animate(i, ys):
	# Read IR from MAX3010x
	ir = sensor.getIR()
	
	ys.append(ir)
	ys = ys[-xlen:]
	line.set_ydata(ys)
	ax.set_ylim([min(ys),max(ys)])
	
	return line,


def runExample():

	print("\nSparkFun MAX3010x Photodetector - Example 4\n")

	if sensor.begin() == False:
		print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("The Qwiic MAX3010x is connected.")

  	# Setup to sensor
	ledBrightness = 0x1F # Options: 0=Off to 255=50mA
	sampleAverage = 8 # Options: 1, 2, 4, 8, 16, 32
	ledMode = 3 # Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
	sampleRate = 100 # Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
	pulseWidth = 411 # Options: 69, 118, 215, 411
	adcRange = 4096 # Options: 2048, 4096, 8192, 16384

	if sensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange) == False:
		print("Device setup failure. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Setup complete.")
	# Set up plot to call animate() function periodically
	ani = animation.FuncAnimation(fig, animate, fargs=(ys,), interval=10, blit=True)
	plt.show()


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 4")
		sys.exit(0)


