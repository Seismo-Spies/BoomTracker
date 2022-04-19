import time
import os
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
pin = 37


def readPin():
	input = GPIO.input(pin)
	if (input == False):
		print('Bye!')
		exec(open("switchfile.py").read())
i = 0

while True:
	print(i)
	i += 1
	time.sleep(1)
	f = open("demoFile.txt", "a")
	f.write(str(i))
	f.close
	readPin()
