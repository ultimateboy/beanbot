import usb.core
import usb.util
import xmpp

# todo: move to settings file.
jabberuser = ''
jabberpass = ''
jabbername = 'beanbot'
jabberroom = ''
jabberserver = ''
jabberport = 5222

# Weight in grams of empty/full pot of coffee.
emptyweight = 400 
fullweight = 500 

# Scale USB Vendor/Product IDs.
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

# send jabber message if out of coffee or there is a fresh pot.
if raw_weight <= emptyweight:
    messagebody = "We're out of coffee :("
elif raw_weight >= fullweight:
    messagebody = 'Fresh pot of coffee!'

client = xmpp.Client(jabberserver)
client.connect(server=(jabberserver, jabberport))
client.auth(jabberuser,jabberpass,jabbername)
client.sendInitPresence()
client.send(xmpp.Presence(to="%s/%s" % (jabberroom, jabbername)))
message = xmpp.protocol.Message(body=messagebody)
message.setTo(jabberroom)
message.setType('groupchat')
client.send(message)
