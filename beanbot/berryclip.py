import RPi.GPIO as GPIO
import time
from beanbot.settings import *

# Prepare Berryclip.
GPIO.setmode(GPIO.BCM)

def led_scale_meter(scale_weight = 0):
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

def sound_buzzer(t = .01):
    """ Buzz for t seconds. """
    GPIO.setup(BUZZER, GPIO.OUT)
    GPIO.output(BUZZER, True)
    time.sleep(t)
    GPIO.output(BUZZER, False)
