import os, sys
import serial
import time
# ser = serial.Serial('/dev/hidraw0', 19200, timeout=5)
#
# while True:
# 	line = ser.readline()
# 	if len(line) == 0:
# 		print("Timeout ! Exit. \n")
# 		sys.exit()
# 	print line
#

import sys

fp = open('/dev/hidraw0', 'rb')

while True:
	buffer = fp.read(8)
	for c in buffer:
		if ord(c) > 0:
			print ord(c)
	print "\n"
