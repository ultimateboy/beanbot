from celery import Celery
from beanbot import main
from beanbot import celeryconfig

celery = Celery('tasks')
celery.config_from_object(celeryconfig)

@celery.task
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
