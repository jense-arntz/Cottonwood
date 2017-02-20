import serial, time

ser = serial.Serial('/dev/ttyUSB0', 19600, timeout=0)

COMMAND_SAMPLE = {0x18, 0x03, 0xFF}


def write_data(data):
	ser.write(COMMAND_SAMPLE)
	read_from_ftdi()


def read_from_ftdi():
	while True:
		line = ser.read(ser.inWaiting())
		if len(line) > 0:
			print 'line: {}'.format(line)
			if "8003" in line:
				print 'There it is'
				break
		time.sleep(.2)
