#settings go here
BUZZER = 8
LEDS = [4,17,22,10,9,11]

#import settings from local_settings.py
try:
    from beanbot.local_settings import *
except ImportError:
    raise Exception("You need a local_settings.py file!")