"""
Celery configuration for api project.

Start worker: celery -A config worker -l info
Start beat:   celery -A config beat -l info
"""

import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Beat schedule: Run batch processing every 2 hours
app.conf.beat_schedule = {
    'process-batch-every-2-hours': {
        'task': 'records.tasks.process_batch',
        'schedule': crontab(minute=0, hour='*/2'),  # Every 2 hours
    },
}

app.conf.timezone = 'UTC'
