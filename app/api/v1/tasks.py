from celery.result import AsyncResult
from fastapi import APIRouter

from app.tasks import process_item

router = APIRouter()


@router.post("/tasks/process-item/{item_id}")
async def run_process_item(item_id: int):
    task = process_item.delay(item_id)
    return {"task_id": task.id}


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    } 