from typing import Any

from fastapi import APIRouter, HTTPException, status
from rq import Retry

from ..redis_cfg import redis_conn, redis_queue
from ..size import Size
from ..utils import ImageProcessor, ImageSchema, generate_task_id

router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
    responses={404: {'description': 'Not found'}},
)


@router.post('', status_code=status.HTTP_201_CREATED)
def add_task(image_data: ImageSchema) -> dict[str, Any]:
    task_id = generate_task_id()
    task = redis_queue.enqueue(
        ImageProcessor.process,
        job_id=task_id,
        retry=Retry(max=3),
        args=(task_id, image_data.data),
    )
    return {'id': task_id, 'status': task.get_status()}


@router.get('/{task_id}')
def get_task(task_id: str) -> dict[str, Any]:
    task = redis_queue.fetch_job(task_id)
    if task is None:
        raise HTTPException(
            detail='Task not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return {'id': task_id, 'status': task.get_status()}


@router.get('/{task_id}/image')
def get_image(
    task_id: str,
    size: Size = Size('original'),
) -> Any:
    task = redis_queue.fetch_job(task_id)
    if task is None:
        raise HTTPException(
            detail='Task not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if task.get_status() != 'finished':
        raise HTTPException(
            detail='Task not finished',
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    img_data = redis_conn.hgetall(task.id)[size.encode()].decode()

    return img_data
