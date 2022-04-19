from MCP3008 import MCP3008
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
from matplotlib.animation import FuncAnimation
import csv
import urllib.request

# set up raspberri pi model, refer to as GPIO
import RPi.GPIO as GPIO

# set numbering system
GPIO.setmode(GPIO.BCM)

# set up ADC
adc = MCP3008()

# create an eventLog and time array
eventLog = [[]]  # = [ [x1, y1, z1], [x2, y2, z2] ]
timeArray = []
xLog = []
yLog = []
zLog = []

def animate(i):
    # read x, y and z from adc
    xAccel = adc.read(channel=2)
    yAccel = adc.read(channel=1)
    zAccel = adc.read(channel=0)

    # append x, y, and z to eventLog
    xLog.append(xAccel)
    yLog.append(yAccel)
    zLog.append(zAccel)
    #eventLog = np.append([xAccel, yAccel, zAccel], axis=0)

    # append time to array
    now = datetime.now()
    currentTime = now.strftime("%M:%S")
    timeArray.append(i)

    # Plot
    plt.cla()
    plt.plot(timeArray, xLog)
    plt.plot(timeArray, yLog)
    plt.plot(timeArray, zLog)

# ani = FuncAnimation(plt.gcf(), animate, interval=1)

def onlyRead(numPts):
	for i in range(numPts):
		# read x, y and z from adc
		xAccel = adc.read(channel=2)
		yAccel = adc.read(channel=1)
		zAccel = adc.read(channel=0)

		# append x, y, and z to eventLog
		xLog.append(xAccel)
		yLog.append(yAccel)
		zLog.append(zAccel)
		timeArray.append(i)
		#time.sleep(0.001)

	plt.plot(timeArray, xLog)
	plt.plot(timeArray, yLog)
	plt.plot(timeArray, zLog)

def exportToCSV():
	arr = np.column_stack((xLog, yLog, zLog))
	with open("newFile.csv","w") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(arr)

def clearCurrentLogs():
	xLog.clear()
	yLog.clear()
	zLog.clear()
	timeArray.clear()

def exportToThingSpeak():
	baseURL = 'http://api.thingspeak.com/update?key=9H44G9OF897TOOPJ'
	count = 0
	arr = np.column_stack((xLog, yLog, zLog))
	for row in arr:
    		# ------- Send Sensor Data to the Cloud -----------
    		f = urllib.request.urlopen(
    		    baseURL + '&field1=' + str(row[0]) + '&field2=' + str(row[1]) + '&field3=' + str(row[2]))
    		f.read()
    		f.close()
    		print('Iteration: ' + str(count))
    		count = count + 1
    		time.sleep(15)

clearCurrentLogs()
onlyRead(100)
exportToCSV()
exportToThingSpeak()

#print(len(xLog), len(yLog), len(zLog), len(timeArray))

#plt.tight_layout()
#plt.show()
