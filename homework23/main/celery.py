import os
from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "DjangoProject8.settings"
)

app = Celery("DjangoProject8")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
