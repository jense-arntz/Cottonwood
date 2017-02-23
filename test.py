import serial, time

FIRMWARE_ID = [0x10, 0x03, 0x00]
HARDWARE_ID = [0x10, 0x03, 0x01]

# Antenna Power
ANTENNA_POWER_OFF = [0x18, 0x03, 0x00]
ANTENNA_POWER_ON = [0x18, 0x03, 0xFF]

# Command Inventory
INVENTORY = [0x31, 0x03, 0x01]


BUFF_SIZE = 1024

ser = serial.Serial('/dev/ttyUSB0', 9600)

ser.write(bytearray([0x10, 0x03, 0x00]))

while True:
	data = ser.read(9999)
	if len(data) > 0:
		print 'data: {}'.format(data)