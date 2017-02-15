import usb.core
import usb.util

IDVENDOR = 0x05e0
IDPRODUCT = 0x1200
# find our device
dev = usb.core.find(idVendor=0x05e0, idProduct=0x1200)

# was it found?
if dev is None:
	print 'Device not Found'
	raise ValueError('Device not found')

# set the active configuration. With no arguments, the first configuration will be the active one.
dev.set_configuration()
print 'Device Found.'


# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

ep = usb.util.find_descriptor(
	intf,
	# match the first OUT endpoint
	custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

assert ep is not None
ep.read()