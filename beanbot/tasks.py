from celery import Celery
from beanbot import main
from beanbot import celeryconfig

celery = Celery('tasks')
celery.config_from_object(celeryconfig)

@celery.task
def watch_coffee():
    main()
