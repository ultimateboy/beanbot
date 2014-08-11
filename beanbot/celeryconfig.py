from datetime import timedelta

BROKER_URL = 'redis://localhost:6379/0'
#BROKER_URL = 'mongodb://localhost:27017/beanbot'

CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    'once-a-minute': {
        'task': 'beanbot.tasks.watch_coffee',
        'schedule': timedelta(minutes=1),
    },
}