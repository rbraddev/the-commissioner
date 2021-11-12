from aioredis.client import Redis
from app.core.tasks.network_tasks import update_network_interfaces_task
from app.core.tasks.tracker import TaskTracker, create_tracker
from app.models.tasks import TaskSubmitData, TaskSubmitted, TaskStatus
from app.redis import get_redis_con
from fastapi import APIRouter, BackgroundTasks, Depends

router = APIRouter()


@router.get("/status/{taskid}", response_model=TaskStatus, status_code=200)
async def task_status(taskid: str, redis_con: Redis = Depends(get_redis_con)):
    tracker = TaskTracker(redis_con, task_id=taskid)
    task_data = await tracker.getall()
    task_data.update({"task_id": taskid})
    return task_data


@router.post(
    "/network/update_interfaces", response_model=TaskSubmitted, status_code=201
)
async def update_network_interfaces(
    task_data: TaskSubmitData,
    background_tasks: BackgroundTasks,
    redis_con: Redis = Depends(get_redis_con),
):
    tracker: TaskTracker = await create_tracker(
        redis_con,
        name="update interface details",
        task_path="/inventory/network/update_interfaces",
        task_data=task_data.dict(),
    )
    background_tasks.add_task(
        update_network_interfaces_task, nodeids=task_data.nodeids, tracker=tracker
    )
    return {"task_id": tracker.task_id, "task_name": "Update Network Interface Details"}
