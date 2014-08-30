import RPi.GPIO as GPIO
import time

try:
    from local_settings import *
except ImportError:
    raise Exception("You need a local_settings.py file!")

# Prepare Berryclip.
GPIO.setmode(GPIO.BCM)
b = 8

def sound_buzz(t = .01):
    """ Buzz for t seconds. """
    GPIO.setup(b, GPIO.OUT)
    GPIO.output(b, True)
    time.sleep(t)
    GPIO.output(b, False)
