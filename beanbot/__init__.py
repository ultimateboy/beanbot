import time
import atexit
from beanbot.chat import *
from beanbot.scale import *
from beanbot.berryclip import *
from beanbot.picam import *
from beanbot.settings import *

def main():
    did_full_pot_buzz = False
    did_jabber_empty = False
    did_jabber_full = False
    did_animated_gif = False
    did_post_animated_gif = False

    weight_history = []

    while True:
        # Get the current weight.
        scale_weight = read_scale_weight()
        weight_history.append(scale_weight)

        # Only keep the last 20 in history.
        if len(weight_history) > 20:
            weight_history.pop(0)

        print str(scale_weight)

        led_scale_meter(scale_weight)

        # Empty or below.
        if scale_weight <= EMPTY_WEIGHT:
            # Send empty notification to jabber.
            if not did_jabber_empty:
                jabbermessage = "We're completely out of coffee :("
                send_jabber_message(jabber_client, jabbermessage)
                did_jabber_empty = True

        # Greater than empty, but less than the alert weight.
        elif scale_weight > EMPTY_WEIGHT and scale_weight < ALERT_WEIGHT:
            # Capture an animated gif to be sent later if pot not filled.
            if not did_animated_gif:
                print 'capturing gif'
                # Buzz to warn of gif capture.
                sound_buzzer()
                capture_animated_gif()
                did_animated_gif = int(time.time())

        # Between one quarter full and full.
        elif scale_weight > ((FULL_WEIGHT - EMPTY_WEIGHT) / 4) \
            and scale_weight < FULL_WEIGHT:
            print 'quarter full'

            # Reset full pot buzz and jabber notification.
            did_full_pot_buzz = False
            did_jabber_full = False

            # Reset jabber empty notification and animated gif.
            did_jabber_empty = False
            did_animated_gif = False
            did_post_animated_gif = False

        elif scale_weight >= FULL_WEIGHT:
             # Buzz quickly once to inform full pot is ready.
             if not did_full_pot_buzz:
                 sound_buzzer()
                 did_full_pot_buzz = True

             # Send fresh pot notification to jabber.
             if not did_jabber_full:
                 jabbermessage = 'Fresh pot of coffee!'
                 send_jabber_message(jabber_client, jabbermessage)
                 did_jabber_full = True

        # Shame whoever emptied the pot and did not fill it back up within
        # a reasonable amount of time.
        if (did_animated_gif \
            and did_animated_gif < (int(time.time() - POT_PREP_TIME))) \
            and not did_post_animated_gif:

            print 'would post gif'
            did_post_animated_gif = True

@atexit.register
def goodbye():
    # Turn LEDs off.
    set_leds([0] * len(LEDS))

if __name__ == '__main__':
    main()
