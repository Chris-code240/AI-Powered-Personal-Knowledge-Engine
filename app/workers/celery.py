from celery import Celery
from ..config.config import load_settings

settings = load_settings()

app = Celery(
    'app',
    broker=settings["celery"]["broker_url"],
    backend=settings["celery"]["result_backend"]
)

app.conf.update(
    task_serializer=settings["celery"]["task_serializer"],
    result_expires=settings["celery"]["result_expires"],
    worker_concurrency=settings["celery"]["concurrency"],
    worker_prefetch_multiplier=settings["celery"]["prefetch_multiplier"],
    timezone='UTC',
    enable_utc=True
)

app.autodiscover_tasks(['app.workers.main'])