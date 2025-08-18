from celery import Celery
from app import APP_NAME

app = Celery(APP_NAME,
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1')

# Optional: Set timezone for tasks
app.conf.update(
    timezone='UTC',
    enable_utc=True,
)
app.autodiscover_tasks()