import serial, time

"""
Command List
"""

# Firm-/Hardware ID
FIRMWARE_ID = [0x10, 0x03, 0x00]
HARDWARE_ID = [0x10, 0x03, 0x01]

# Antenna Power
ANTENNA_POWER_OFF = [0x18, 0x03, 0x00]
ANTENNA_POWER_ON = [0x18, 0x03, 0xFF]

# Command Inventory
INVENTORY = [0x31, 0x03, 0x01]

# Write to Tag

"""
Values
"""
ser = None
BUFF_SIZE = 1024


while ser is not None:
	try:
		ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)
	except Exception as e:
		print 'Serial Creation Error: {}'.format(e)


def Firmware():
	"""
	Return Firmware ID
	:return:
	"""
	try:
		ser.write(bytearray(FIRMWARE_ID))
		data = ser.read(1024)
		RES_ID = data[0].encode('hex')
		RES_len = int(data[1].encode('hex'), 16)

		print 'RES_ID: {}\n'.format(RES_ID)
		print 'RES_len: {}\n'.format(RES_len)
		firmware_version = data[2:]
		print 'firmware version: {}'.format(firmware_version.encode('hex'))
		return True

	except Exception as e:
		print 'Firmware Error: {}'.format(e)
		return False


def Antenna_Power():
	"""
	Enable Antenna Power On.
	:return:
	"""
	try:
		ser.write(bytearray(ANTENNA_POWER_ON))
		data = ser.read(1024)
		RES_ID = data[0].encode('hex')
		RES_len = int(data[1].encode('hex'), 16)

		print 'RES_ID: {}\n'.format(RES_ID.encode('hex'))
		print 'RES_len: {}\n'.format(RES_len)

		Rfu = data[2:]
		print 'Rfu: {}'.format(Rfu.encode('hex'))
		return True

	except Exception as e:
		print 'Antenna Power: {}'.format(e)
		return False


def Inventory():
	"""
	Inventory
	:return:
	"""
	try:
		ser.write(bytearray(INVENTORY))
		data = ser.read(1024)
		RES_ID = data[0].encode('hex')
		RES_len = int(data[1].encode('hex'), 16)

		print 'RES_ID: {}\n'.format(RES_ID.encode('hex'))
		print 'RES_len: {}\n'.format(RES_len)

		Found_Tag_Num = data[2].encode('hex')
		EPC_Len = int(data[3].encode('hex'), 16)
		EPC = data[4:5].encode('hex')
		rfu = data[6:].encode('hex')
		print 'Found_Tag_Num: {}\n'.format(Found_Tag_Num.encode('hex'))
		print 'EPC_len: {}\n'.format(EPC_Len)
		print 'EPC: {}\n'.format(EPC.encode('hex'))
		print 'EPC ID: {}\n'.format(rfu.encode('hex'))

		return EPC_Len, rfu
	except Exception as e:
		print 'Inventory Error: {}'.format(e)
		return False


def Select_Tag(EPC_len, EPC_ID):
	"""
	Write the Tag information to Tag.
	:return:
	"""
	try:
		tag_len = hex(EPC_len + 3)
		ser.write(bytearray([0x33, tag_len, hex(EPC_len), EPC_ID]))
		data = ser.read(1024)
		RES_ID = data[0].encode('hex')
		RES_len = int(data[1].encode('hex'), 16)

		print 'RES_ID: {}\n'.format(RES_ID.encode('hex'))
		print 'RES_len: {}\n'.format(RES_len)

		if data[2].encode('hex') == 0x00:
			print 'Found Tag\n'
			return True  # Found the tag

		if data[2].encode('hex') == 0x09:
			print 'No Found Tag.\n'
			return False  # Not Found

		return False

	except Exception as e:
		print 'Tag Error: {}'.format(e)
		return False


def Write_info_tag(data):
	"""
	Write the info to tag
	:param data:
	:return:
	"""
	pass


def read_from_ftdi():
	while True:
		line = ser.read(ser.inWaiting())
		if len(line) > 0:
			print 'line: {}'.format(line.decode("utf-8"))
			if "8003" in line:
				print 'There it is'
				break
		time.sleep(.2)


def main():
	"""
	Main Function
	:return:
	"""

	data = None

	if not Firmware():
		print 'failed to get firmware'

	if not Antenna_Power():
		print 'failed to set Antenna Power On'

	EPC_len, EPC_ID = Inventory()

	# if not Select_Tag(EPC_len, EPC_ID):
	# 	print('failed to select tag :{}'.format(EPC_ID))
	#
	# Write_info_tag(data)

if __name__ =='__main__':
	main()