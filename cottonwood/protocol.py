import logging
# logging.basicConfig(filename='/var/log/rfid_card.log', level=logging.INFO)

SEND_TYPE = 0xA0
RECV_TYPE = 0xE0
RECV_ERR = 0xE4


def check_sum(cmd):
	"""
	Calculate check sum.
	:param cmd:
	:return:
	"""
	sum = 0
	for buf in cmd:
		sum += buf
		if sum > 256:
			sum = sum % 256
	print sum

	sum = 255 - sum + 1

	print('check sum: {}'.format(hex(sum)))
	logging.info('check sum: {}'.format(hex(sum)))
	return sum


def convert_int(data):
	"""
	Convert String to Int
	:param data:
	:return:
	"""
	array = []
	for i in data:
		array.append(int(i))

	while len(array) < 12:
		array.insert(0, 0x00)

	return array


def protocol_packet(TYPE, CMD, DATA=[]):
	"""
	:param TYPE:
	:param CMD:
	:param DATA:
	:return:
	"""
	LEN = len(DATA) + 2
	payload = [TYPE, LEN, CMD] + DATA
	crc = check_sum(bytearray(payload))
	payload.append(crc)
	print 'payload: {}'.format(payload)
	return payload


def epc_tag_identy():
	return protocol_packet(SEND_TYPE, 0x82, DATA=[0x00])


def epc_tag_read():
	return protocol_packet(SEND_TYPE, 0x80, DATA=[0x06, 0x80, 0x00, 0x01, 0x02, 0x01])


def epc_tag_write_multi(badge):
	data = [0x00, 0x01, 0x01, 0x02, 0x06]
	data += convert_int(badge)
	return protocol_packet(SEND_TYPE, 0x81, DATA=data)