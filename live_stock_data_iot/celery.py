import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_stock_data_iot.settings')

app = Celery('live_stock_data_iot')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-weekly-summary': {
        'task': 'dashboard.tasks.send_weekly_summary',
        'schedule': crontab(minute=0, hour=9, day_of_week=0),  # This runs at 9 AM every Sunday
    },
}
