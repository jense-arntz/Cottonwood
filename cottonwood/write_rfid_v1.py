#!/usr/bin/python

import sysv_ipc, logging, serial, time
import binascii
import logging, time
from protocol import *

logging.basicConfig(filename='/var/log/rfid_card.log', level=logging.INFO)

Cotton_KEY = 1234
mq = None
ser = None
BUFF_SIZE = 1024

while ser is None:
	try:
		try:
			ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.0001)
			print 'Serial Connected Successfully\n'
			logging.info('Serial Connected Successfully\n')
	except Exception as e:
		ser = None
		print 'Serial Creation Error: {}'.format(e)
		logging.info('Serial Creation Error: {}\n'.format(e))

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
	size = ser.inWaiting()
	if size:
		x = ser.read(size)
		time.sleep(1)
		x = binascii.hexlify(x)
		q = x.decode("ascii")  #converting scanned data
		print('rfidvalue: {}'.format(q[4:27])) #converting scanned data
		rfidvalue = q[4:27]
		return rfidvalue
	else:
		print 'scanning...'


def send_ser(command=None):
	try:
		ser.write(bytearray(command))
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

	while True:
		try:
			data = read_barcode()
			send_ser(epc_tag_write_multi(data))
		except Exception as e:
			logging.info('main error: {}'.format(e))
			continue


if __name__ =='__main__':
	# main()
	send_ser(epc_tag_identy())

