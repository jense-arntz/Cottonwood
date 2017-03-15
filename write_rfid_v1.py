#!/usr/bin/python

import sysv_ipc, logging, serial, time
import binascii
import logging
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
INVENTORY = [0x31, 0x03, 0x01]

# Write to Tag

"""
Values
"""
ser = None
BUFF_SIZE = 1024


while ser is None:
	try:
		ser = serial.Serial('/dev/ttyUSB0', 9600)
		logging.info('Cotton Device Found\n')
	except Exception as e:
		ser = None
		print 'Serial Creation Error: {}'.format(e)
		logging.info('Serial Creation Error: {}\n'.format(e))



"""
Creating Message Queue
"""
while mq is None:
	try:
		mq = sysv_ipc.MessageQueue(Cotton_KEY)
		logging.info("Founded mq")
	except Exception as e:
		logging.info("no Founded mq: {}".format(e))
		pass


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
	try:
		ser.write(bytearray(FIRMWARE_ID))
		data = read_ser()
		print 'Firmware Data: {}'.format(data.encode('hex'))
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
	logging.info('Antenna Power\n')
	try:
		ser.write(bytearray(ANTENNA_POWER_ON))
		data = read_ser()
		print 'Received Data: {}'.format(data.encode('hex'))
		logging.info('Antenna_Power: {}'.format(data.encode('hex')))
		RES_ID = data[0].encode('hex')
		RES_len = int(data[1].encode('hex'), 16)

		Rfu = data[2:].encode('hex')
		print 'Rfu: {}'.format(Rfu)
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


def epc_tag_identification():
	command = [0xA0, 0x03, 0x82, 0x00, 0xDB]
	try:
		ser.write(bytearray(ANTENNA_POWER_ON))
		data = read_ser()
		print 'Received Data: {}'.format(data.encode('hex'))

	except Exception as e:
		print 'epc tag identification: {}'.format(e)


def read_barcode():
	"""
	Read data from barcode daemon.
	:return:
	"""
	logging.info('start receive message....')
	(message, priority) = mq.receive()
	msg = message.decode("utf-8")
	msg = msg.replace('\x00', '')
	logging.info('Received Data: {}'.format(msg))
	return msg


def main():
	"""
	Main Function
	:return:
	"""

	# while True:
	# 	try:
	# 		Found_EPC = None
	# 		count = 0
	# 		flag = True
	#
	# 		data = read_barcode()
	#
	# 		while Found_EPC is None:
	# 			if count > 50:
	# 				flag = False
	# 				break
	# 	except Exception as e:
	# 		logging.info('main error: {}'.format(e))
	# 		continue

	epc_tag_identification()

def check_sum(cmd):
	crc = 0xFF
	sum = 0
	for c in cmd:
		sum += ord(hex(c))
	print sum

	# print hex(sum)

if __name__ =='__main__':

	main()


