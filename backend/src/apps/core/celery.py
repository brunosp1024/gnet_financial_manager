import os
from celery import Celery

# Set the default Django settings module for the Celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.core.settings')

app = Celery('core')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()
