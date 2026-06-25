from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=f"redis://{settings.redis_host}:{settings.redis_port}/0",
    backend=f"redis://{settings.redis_host}:{settings.redis_port}/1",
    include=["app.tasks"],
)

celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"