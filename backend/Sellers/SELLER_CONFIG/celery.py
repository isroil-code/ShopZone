import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SELLER_CONFIG.settings")

app = Celery("SELLER_CONFIG")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
