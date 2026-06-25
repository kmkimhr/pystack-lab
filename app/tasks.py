import time

from app.worker import celery_app


@celery_app.task(bind=True)
def process_item(self, item_id: int) -> dict:
    time.sleep(20)  # 무거운 작업 시뮬레이션
    return {"item_id": item_id, "status": "processed"}