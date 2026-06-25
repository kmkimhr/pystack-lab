import time

from celery.exceptions import MaxRetriesExceededError

from app.worker import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def process_item(self, item_id: int) -> dict:
    try:
        raise ValueError("강제 에러 발생")  # 실패 시뮬레이션
        return {"item_id": item_id, "status": "processed"}
    except Exception as exc:
        raise self.retry(exc=exc)