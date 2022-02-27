from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler.settings')

app = Celery('main')

app.conf.enable_utc=True
# app.conf.update(timezone='Asia/Kolkata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django apps.

# sauce codes: 245074

# Celery Beat tasks registration 
app.conf.beat_schedule = {
    'Send_mail_to_Client': {
        'task': 'app.tasks.send_mail_task',
        # 'schedule': crontab(0, 0, day_of_month=27), #this will make the task run every first day of the month
        'schedule': crontab(minute=12, hour=15), #this will make the task run every 18:35, wish me luck
        # 'schedule': 75.0, #for tesing, send the email every 75 seconds
    }
}

#it will search the app module for task.py, import it then run any function with @shared_task decorator
app.autodiscover_tasks(['app'])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



# sauce codes: 165684