# Berryclip LED/Buzzer.
LEDS = [4,17,22,10,9,11]
BUZZER = 8

# Scale USB Vendor/Product IDs.
# Dymo M25
VENDOR_ID = 0x0922
PRODUCT_ID = 0x8004
DATA_MODE_GRAMS = 2
DATA_MODE_OUNCES = 11

#import settings from local_settings.py
try:
    from beanbot.local_settings import *
except ImportError:
    raise Exception("You need a local_settings.py file!")
