import time		#important libraries we need to communicate with board
import board
import busio
import adafruit_adxl34x
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import urllib.request
import RPi.GPIO as GPIO
from gpiozero import Button
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

timeArray, xLog, yLog, zLog, datetimeLog = [], [], [], [], []
sample_rate = 1000

def shutdown():
	clearCurrentLogs()
	os.system("sudo poweroff")

def ledOn(GPIOpin):
	GPIO.setup(GPIOpin, GPIO.OUT)
	GPIO.output(GPIOpin, GPIO.HIGH)

def ledOff(GPIOpin):
	GPIO.output(GPIOpin, GPIO.LOW)

def fTransform(amplitude1, amplitude2, amplitude3, samplingFrequency):
	# the log values is the amplitude
	# sample rate is the samplingFrequency

	#fft1(x)
	fourierTransform1 = np.fft.fft(amplitude1)/len(amplitude1)
	fourierTransform1 = fourierTransform1[range(int(len(amplitude1)/2))]

	tpCount1 = len(amplitude1)
	values1 = np.arange(int(tpCount1/2))
	timePeriod1 = tpCount1/samplingFrequency
	frequencies1 = values1/timePeriod1

	#fft2(y)
	fourierTransform2 = np.fft.fft(amplitude2)/len(amplitude2)
	fourierTransform2 = fourierTransform2[range(int(len(amplitude2)/2))]
	tpCount2 = len(amplitude2)
	values2 = np.arange(int(tpCount2/2))
	timePeriod2 = tpCount2/samplingFrequency
	frequencies2 = values2/timePeriod2

	#fft3(z)
	fourierTransform3 = np.fft.fft(amplitude3)/len(amplitude3)
	fourierTransform3 = fourierTransform3[range(int(len(amplitude3)/2))]
	tpCount3 = len(amplitude3)
	values3 = np.arange(int(tpCount3/2))
	timePeriod3 = tpCount3/samplingFrequency
	frequencies3 = values3/timePeriod3

	# Make matrix of fourier transform data
	ftMatrix = np.column_stack((frequencies1, abs(fourierTransform1), abs(fourierTransform2), abs(fourierTransform3)))

	# graph frequency domain
	plt.title('Fourier transform depicting the frequency components')
	plt.plot(frequencies1, abs(fourierTransform1), label='x')
	plt.plot(frequencies2, abs(fourierTransform2), label='y')
	plt.plot(frequencies3, abs(fourierTransform3), label='z')
	plt.xlabel('Frequency')
	plt.ylabel('Amplitude')
	plt.legend()
	#plt.show()

	return ftMatrix

def exportToCSV(matrix):
        arr = np.column_stack((datetimeLog, xLog, yLog, zLog))
        fileName = "TimeDomain." + str(datetimeLog[0]) + ".csv"
        with open(fileName,"w") as my_csv:
                csvWriter = csv.writer(my_csv,delimiter=',')
                csvWriter.writerows(arr)

        ftFileName = "FreqDomain." + str(datetimeLog[0]) + ".csv"
        with open(ftFileName,"w") as my_csv:
                csvWriter = csv.writer(my_csv,delimiter=',')
                csvWriter.writerows(matrix)

def exportToThingSpeak():
        baseURL = 'http://api.thingspeak.com/update?key=9H44G9OF897TOOPJ'
        count = 0
        arr = np.column_stack((datetimeLog, xLog, yLog, zLog))
        for row in arr:
                # ------- Send Sensor Data to the Cloud -----------
                f = urllib.request.urlopen(baseURL + '&field1=' + str(row[1]) + '&field2=' + str(row[2]) + '&field3=' + str(row[3]))
                f.read()
                f.close()
                print('Iteration: ' + str(count))
                count = count + 1
                time.sleep(15)

def onlyRead(numPts):
        for i in range(numPts):
                # read x, y and z from adxl
                xAccel = accelerometer.raw_x / 250
                yAccel = accelerometer.raw_y / 250
                zAccel = accelerometer.raw_z / 250
                now = datetime.now()
                dt_str = now.strftime("%d-%m-%Y.%H-%M-%S.%f")

                # append x, y, and z to eventLog
                xLog.append(xAccel)
                yLog.append(yAccel)
                zLog.append(zAccel)
                datetimeLog.append(dt_str)
                timeArray.append(i)
                time.sleep(1/sample_rate)

        # Delete the first row of data
        del xLog[0]
        del yLog[0]
        del zLog[0]
        del datetimeLog[0]
        del timeArray[0]

def clearCurrentLogs():
        xLog.clear()
        yLog.clear()
        zLog.clear()
        datetimeLog.clear()
        timeArray.clear()

def animate(i):
#read x, y and z from adxl
	xAccel = accelerometer.raw_x
	yAccel = accelerometer.raw_y
	zAccel = accelerometer.raw_z

        # append x, y, and z to eventLog
	xLog.append(xAccel)
	yLog.append(yAccel)
	zLog.append(zAccel)

	timeArray.append(i)

    # Plot
	plt.cla()
	plt.plot(timeArray, xLog, label='x')
	plt.plot(timeArray, yLog, label='y')
	plt.plot(timeArray, zLog, label='z')
	plt.legend()

########################## INITIALIZE VARIABLES AND PI ################################
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_motion_detection(threshold=6)
accelerometer.offset = 0, 0, 0
DATA_FORMAT = 0x00 # Sets to +/- 2gs

print("Hold accelerometer flat to set offsets to 0, 0, and -1g...")
time.sleep(1)
x = accelerometer.raw_x
y = accelerometer.raw_y
z = accelerometer.raw_z
print("Raw x: ", x)
print("Raw y: ", y)
print("Raw z: ", z)

accelerometer.offset = (
	round(-x / 8),
	round(-y / 8),
	round(-(z + 250) / 8)
)
print("Calibrated offsets: ", accelerometer.offset)

sum = 0

############################### Motion Detection ##############################
#while True:
#        print("motion detected: %s"%accelerometer.events['motion'])
#        time.sleep(.005)
#        if(accelerometer.events['motion']):
#                sum=sum+1
#                print(sum)
#                time.sleep(1)

############################## Print accel values #############################

#while True:
#	print(accelerometer.acceleration)
#	time.sleep(0.5)

################# COLLECT DATA #######################################
ani = FuncAnimation(plt.gcf(), animate, interval=1)
plt.tight_layout()
plt.show()

#onlyRead(100)

timeDomainPlot = plt.figure(1)
plt.plot(timeArray, xLog, label='x')
plt.plot(timeArray, yLog, label='y')
plt.plot(timeArray, zLog, label='z')
plt.xlabel("Time (ms)")
plt.legend()

clearCurrentLogs()
#exportToThingSpeak()
#fTransform(xLog, yLog, zLog, sample_rate)


#################### Main Loop ##################################
time.sleep(1)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)
while True:
	time.sleep(0.001)
	if GPIO.input(21): # 0 if OFF 1 if ON
		shutdown()
	if(accelerometer.events['motion']):
		print("motion detected: %s"%accelerometer.events['motion'])
		time.sleep(0.001)
		if(accelerometer.events['motion']):
			print('Motion Detected')
			leave = 0
			time.sleep(0.001)
			while (leave == 0):
				leave = 1
				sum = 0
				print('Reading Data')
				ledOn(18)
				#time.sleep(1)
				for i in range(100):
					onlyRead(2)
					time.sleep(0.001)
					if(accelerometer.events['motion']):
						sum = sum + 1
						#print(i)
				print('Done Reading')
				print(sum)
				ledOff(18)
				if (sum >= 30):
					leave = 0
					sum = 0
			ftOut = fTransform(xLog, yLog, zLog, sample_rate)
			print('Exporting', len(xLog), 'points')
			print('Will be complete in', 15*len(xLog)/60, 'minutes.')
			exportToCSV(ftOut)
			print('Done Exporting CSV')
			exportToThingSpeak()
			print('Done Exporting to Cloud')
			clearCurrentLogs()
