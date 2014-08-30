import picamera
import glob
import os
import time

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
    #series_to_animated_gif(L, cwd+"/images/animated.gif")
    #series_to_animated_gif(L, cwd+"/images/animated.gif").delay()
