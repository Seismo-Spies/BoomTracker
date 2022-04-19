import time
import os
import RPi.GPIO as GPIO

pin = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)
while True:
#	print('test')
	input = GPIO.input(pin)
	if (input == True):
		exec(open("test.py").read())
	time.sleep(1)
