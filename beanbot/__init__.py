import usb.core
import usb.util
from beanbot.chat import send_jabber_message

try:
    from local_settings import *
except ImportError:
    raise Exception("You need a local_settings.py file!")

def main():
    # find the USB device
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    try:
        if device.is_kernel_driver_active(0) is True:
            device.detach_kernel_driver(0)
    except:
        raise Exception("Scale not detected. Not plugged in or not powered on.")

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

    raw_weight = data[4] + data[5] * 256

    if data[2] == DATA_MODE_OUNCES:
        ounces = raw_weight * 0.1
        weight = "%s oz" % ounces
    elif data[2] == DATA_MODE_GRAMS:
        grams = raw_weight
        weight = "%s g" % grams

    print weight

    # send jabber message if out of coffee or there is a fresh pot.
    if raw_weight <= EMPTY_WEIGHT:
        messagebody = "We're out of coffee :("
    elif raw_weight >= FULL_WEIGHT:
        messagebody = 'Fresh pot of coffee!'

    send_jabber_message(messagebody)

if __name__ == '__main__':
    main()