import usb.core
import usb.util

VENDOR_ID = 0x0922
PRODUCT_ID = 0x8004

# find the USB device
device = usb.core.find(idVendor=VENDOR_ID,
                       idProduct=PRODUCT_ID)

if device.is_kernel_driver_active(0) is True:
    device.detach_kernel_driver(0)

# use the first/default configuration
device.set_configuration()

# first endpoint
endpoint = device[0][(0,0)][0]

# read a data packet
attempts = 10
data = None
while data is None and attempts > 0:
    try:
        data = device.read(endpoint.bEndpointAddress,
                           endpoint.wMaxPacketSize)
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            attempts -= 1
            continue

DATA_MODE_GRAMS = 2
DATA_MODE_OUNCES = 11

raw_weight = data[4] + data[5] * 256

if data[2] == DATA_MODE_OUNCES:
    ounces = raw_weight * 0.1
    weight = "%s oz" % ounces
elif data[2] == DATA_MODE_GRAMS:
    grams = raw_weight
    weight = "%s g" % grams

print weight


