from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from starlette.status import HTTP_403_FORBIDDEN

from app.core.security.utils import get_current_user
from app.core.tasks.network_tasks import update_network_interfaces_task
from app.core.tasks.tracker import TaskTracker, create_tracker

from app.models.tasks import TaskSubmitData, TaskSubmitted, TaskStatus
from app.models.auth import User
from app.redis import get_redis_con

router = APIRouter()


@router.get("/status/{taskid}", response_model=TaskStatus, status_code=200)
async def task_status(taskid: str, redis_con: Redis = Depends(get_redis_con), user: User = Depends(get_current_user)):
    tracker = TaskTracker(redis_con, task_id=taskid)
    if await tracker.valid_username(user["username"]) or user["access_lvl"] == 10: 
        task_data = await tracker.getall()
        task_data.update({"task_id": taskid})
        return task_data
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)


@router.post(
    "/network/update_interfaces", response_model=TaskSubmitted, status_code=201
)
async def update_network_interfaces(
    task_data: TaskSubmitData,
    background_tasks: BackgroundTasks,
    redis_con: Redis = Depends(get_redis_con),
    user: User = Depends(get_current_user)
):
    if user["access_lvl"] < 5:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    tracker: TaskTracker = await create_tracker(
        redis_con,
        name="update interface details",
        task_path="/inventory/network/update_interfaces",
        task_data=task_data.dict(),
        username=user["username"]
    )
    background_tasks.add_task(
        update_network_interfaces_task, nodeids=task_data.nodeids, tracker=tracker
    )
    return {"task_id": tracker.task_id, "task_name": "Update Network Interface Details"}
