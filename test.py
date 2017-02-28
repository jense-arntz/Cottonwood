import sysv_ipc

mq = None
Cotton_KEY = 1234

"""
Creating Message Queue
"""
while mq is None:
	try:
		mq = sysv_ipc.MessageQueue(Cotton_KEY)
		print("Founded mq")
	except Exception as e:
		print("no Founded mq: {}".format(e))
		pass


def read_barcode():
	"""
	Read data from barcode daemon.
	:return:
	"""
	print('start receive message....')
	(message, priority) = mq.receive()
	msg = message.decode("utf-8")
	msg = msg.replace('\x00', '')
	print('Received Data: {}'.format(msg))
	return msg

if __name__ == '__main__':
	while True:
		read_barcode()
