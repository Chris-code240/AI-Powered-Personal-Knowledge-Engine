from celery import Celery
# from app import APP_NAME

app = Celery("app",
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1')

# Optional settings
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
app.autodiscover_tasks(['app.workers.main'])