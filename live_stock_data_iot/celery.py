import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_stock_data_iot.settings')

app = Celery('live_stock_data_iot')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
