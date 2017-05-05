#!/usr/bin/python

import logging, serial, time
import binascii
import threading

Cotton_KEY = 1234
mq = None

logging.basicConfig(filename='/var/log/rfid_card.log', level=logging.INFO)

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
START_INVENTORY = [0x31, 0x03, 0x01]
NEXT_INVENTORY = [0x31, 0x03, 0x02]
# Write to Tag

"""
Values
"""
ser = None
BUFF_SIZE = 1024
BUF_LEN = 24

while ser is None:
	try:
		ser = serial.Serial('/dev/ttyUSB0', 9600)
		logging.info('Cotton Device Found\n')
	except Exception as e:
		ser = None
		print 'Serial Creation Error: {}'.format(e)
		logging.info('Serial Creation Error: {}\n'.format(e))


def read_ser():
	"""
	Read serial data from cottonwood.
	:return:
	"""
	tdata = ser.read()           # Wait forever for anything
	time.sleep(1)              # Sleep (or inWaiting() doesn't give the correct value)
	data_left = ser.inWaiting()  # Get the number of characters ready to be read
	tdata += ser.read(data_left)
	return tdata


def Firmware():
	"""
	Return Firmware ID
	:return:
	"""
	print 'Reading Firmware ID\n'
	try:
		ser.write(bytearray(FIRMWARE_ID))
		data = read_ser()
		RES_ID = data[0].encode('hex')
		RES_len = int(data[1].encode('hex'), 16)
		firmware_version = data[2:]
		print 'firmware version: {}\n'.format(firmware_version.encode('hex'))
		logging.info('firmware version: {}\n'.format(firmware_version.encode('hex')))
		return True

	except Exception as e:
		print 'Firmware Error: {}\n'.format(e)
		return False


def Antenna_Power():
	"""
	Enable Antenna Power On.
	:return:
	"""
	logging.info('Antenna Power\n')
	print 'Setting Antenna Power\n'
	try:
		ser.write(bytearray(ANTENNA_POWER_ON))
		data = read_ser()
		RES_ID = data[0].encode('hex')
		RES_len = int(data[1].encode('hex'), 16)
		Rfu = data[2:].encode('hex')
		print 'Rfu: {}\n'.format(Rfu)
		logging.info('Rfu: {}'.format(Rfu))

		if Rfu == '00':
			print 'Success'
			logging.info("Antenna Power Read Success\n\n")
			return True

		print 'Antenna Power failed\n\n'
		logging.info('Antenna Power failed\n\n')
		return False

	except Exception as e:
		print 'Antenna Power Error: {}\n'.format(e)
		logging.info('Antenna Power Error: {}\n'.format(e))
		return False


def Start_Inventory():
	"""
	Inventory
	:return:
	"""
	logging.info('Inventory')
	try:
		ser.write(bytearray(START_INVENTORY))
		data = read_ser()
		logging.info('Inventory: {}'.format(data.encode('hex')))
		RES_ID = data[0].encode('hex')
		RES_len = int(data[1].encode('hex'), 16)
		Found_Tag_Num = int(data[2].encode('hex'), 16)
		EPC_Len = int(data[3].encode('hex'), 16) - 2  # 2 bytes is reserved bytes.
		EPC = data[4:5].encode('hex')
		rfu = data[6:].encode('hex')

		# print 'Inventory: {}'.format(data.encode('hex'))
		print 'Found_Tag_Num: {}'.format(Found_Tag_Num)
		print 'EPC: {}\n'.format(EPC)
		print 'EPC ID: {}\n'.format(rfu)

		return (Found_Tag_Num, rfu)
	except Exception as e:
		print 'Inventory Error: {}\n'.format(e)
		logging.info('Inventory Error: {}\n'.format(e))
		return False


def Next_Inventory():
	"""
	Inventory
	:return:
	"""
	logging.info('Inventory')
	try:
		ser.write(bytearray(NEXT_INVENTORY))
		data = read_ser()
		RES_ID = data[0].encode('hex')
		RES_len = int(data[1].encode('hex'), 16)
		Found_Tag_Num = data[2].encode('hex')
		EPC_Len = int(data[3].encode('hex'), 16) - 2  # 2 bytes is reserved bytes.
		EPC = data[4:5].encode('hex')
		rfu = data[6:].encode('hex')

		print 'Inventory: {}'.format(data.encode('hex'))
		print 'Found_Tag_Num: {}'.format(Found_Tag_Num)
		print 'EPC: {}\n'.format(EPC)
		print 'EPC ID: {}\n'.format(rfu)

		return (Found_Tag_Num, rfu)
	except Exception as e:
		print 'Inventory Error: {}\n'.format(e)
		logging.info('Inventory Error: {}\n'.format(e))
		return False


def split_data(num, data):
	Founded = []
	for i in range(num):
		Founded.append(data[i*BUF_LEN: BUF_LEN])

	return Founded


def main():
	"""
	Main Function
	:return:
	"""

	while True:
		try:
			Found_EPC = Start_Inventory()

			if Found_EPC:
				Founded = split_data(Found_EPC[0], Found_EPC[1])
				logging.info('FOUNDED: {}'.format(Founded))
				print 'Founded: {}'.format(Founded)
		except Exception as e:
			logging.info('main error: {}'.format(e))
			continue

if __name__ =='__main__':

	if not Firmware():
		print 'failed to read Firmware'
		logging.info('failed to read Firmware')

	if not Antenna_Power():
		print 'failed to set Antenna Power On'
		logging.info('failed to set Antenna Power On')

	main()