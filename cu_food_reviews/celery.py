from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from . import settings

SECURE_SSL_REDIRECT = True


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cu_food_reviews.settings')

app = Celery('cu_food_reviews')

app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    broker_url = os.environ.get('CLOUDAMQP_URL', 'pyamqp://guest@localhost//'),
    broker_pool_limit = 2, # Will decrease connection usage
    result_backend = 'django-db',
    event_queue_expires = 60, # Will delete all celeryev. queues without consumers after 1 minute.
    worker_prefetch_multiplier = 1, # Disable prefetching, it's causes problems and doesn't help performance
    worker_concurrency = 5,

)

# crontab runs in UTC timezone by default.
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'cu_food_reviews.tasks.add',
        'schedule': timedelta(seconds=30),
        'args': (30,69)
    },
    'load_data_from_endpoint_task_every_day': {
        'task': 'cu_food_reviews.tasks.load_data_from_endpoint_task',
        'schedule': crontab(hour=6, minute=0), # 1:00 AM EST, daily
        'args': ()
    },
    'send_meal_item_alerts_daily': {
        'task': 'meal_item_alert.tasks.send_users_alert_email',
        'schedule': crontab(hour=11, minute=30), # 6:30 AM EST, daily.
        'args': ()
    },
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

