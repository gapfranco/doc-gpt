import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aidoc.settings")

app = Celery("aidoc")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.accept_content = [
    "application/json",
    "application/x-python-serialize",
]

app.autodiscover_tasks()
