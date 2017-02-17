import sys

fp = open('/dev/hidraw0', 'rb')

while True:
	buffer = fp.read(8)
	for c in buffer:
		if ord(c) > 0:
			print 'Output: {}\r'.format(ord(c))
			print 'Output: {}\r'.format(c)
	print('\n')