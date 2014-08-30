import usb.core
import usb.util
import time
import picamera
from wand.image import Image
import glob
import os
import RPi.GPIO as GPIO
from beanbot.chat import send_jabber_message

# prepare berryclip
LEDS = [4,17,22,10,9,11]
GPIO.setmode(GPIO.BCM)

try:
    from local_settings import *
except ImportError:
    raise Exception("You need a local_settings.py file!")

def read_scale_weight():
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

    # scale gives different raw_weight depending on oz/g mode.
    if data[2] == DATA_MODE_OUNCES:
        ounces = raw_weight * 0.1
        grams = ounces / 0.035274
    elif data[2] == DATA_MODE_GRAMS:
        grams = raw_weight
        ounces = grams * 0.035274

    return grams

def scale_led_meter(scale_weight = 0):
    """ Uses the Berryclip to create a meter showing the current weight. """
    # Determine percentage remaining.
    prct_left = (scale_weight / (FULL_WEIGHT - EMPTY_WEIGHT))
    # Determine how many lights to turn on.
    on = round(prct_left * len(LEDS))
    # If weight is greater than FULL_WEIGHT, will return greater
    # than number of LEDS we have. We won't let that happen.
    on = len(LEDS) if on > len(LEDS) else on

    off_list = [0] * int((len(LEDS) - on))
    on_list = [1] * int(on)
    led_list = off_list + on_list

    # Turn the LEDS on/off.
    set_leds(led_list)

def set_leds(led_list):
    """ Accepts a list of booleans to turn on/off the associated LEDs. """
    for x in range(len(led_list)):
        GPIO.setup(LEDS[x], GPIO.OUT)
        GPIO.output(LEDS[x], bool(led_list[x]))

def sound_buzz(t = .1):
    """ Buzz for t seconds. """
    GPIO.setup(8, GPIO.OUT)
    GPIO.output(8, True)
    time.sleep(t)
    GPIO.output(8, False)
    return True

def capture_animated_gif():
    cwd = os.getcwd()
    if not os.path.exists(cwd+"/images"):
        os.makedirs(cwd+"/images")

    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        start = time.time()
        # let the camera warm up.
        time.sleep(2)
        # capture 10 frames.
        camera.capture_sequence((
            'images/image%03d.png' % i
            for i in range(10)
            ), use_video_port=True, format='png')
        print('Captured 10 images at %.2ffps' % (10 / (time.time() - start)))
        camera.stop_preview()

    # generate animated gif from 10 captured frames.
    L = glob.glob(cwd+"/images/*.png")
    L.sort()
    series_to_animated_gif(L, cwd+"/images/animated.gif")

def series_to_animated_gif(L, filepath):
    imgs = Image(filename=L[0])
    for i in L[1:]:
        im2 = Image(filename=i)
        imgs.sequence.append(im2)
        for i in imgs.sequence:
            i.delay = 25
    imgs.save(filename=filepath)
    imgs.close()
    print('saved animated.gif')


def main():
    full_pot_buzzed = False
    jabbermessage = ''
    while True:
        # Get the current weight.
        scale_weight = read_scale_weight()

        scale_led_meter(scale_weight)

        if scale_weight <= EMPTY_WEIGHT:
            # Reset full pot buzz.
            full_pot_buzzed = False

            jabbermessage = "We're out of coffee :("

        elif scale_weight > EMPTY_WEIGHT and scale_weight < ALERT_WEIGHT:
            # capture_animated_gif()
            print 'would capture gif'

        elif scale_weight >= FULL_WEIGHT:
             if not full_pot_buzzed:
                 full_pot_buzzed = sound_buzz()
             jabbermessage = 'Fresh pot of coffee!'

        # Send a jabber message if we have one to send.
        if jabbermessage:
            print 'would post to jabber:' + jabbermessage
            # commented out until we can be less annoying :P
            # send_jabber_message(jabbermessage)

if __name__ == '__main__':
    main()
