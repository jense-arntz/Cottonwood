import os, sys
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=5)

while True:
	line = ser.readline()
	if len(line) == 0:
		print("Timeout ! Exit. \n")
		sys.exit()
	print line