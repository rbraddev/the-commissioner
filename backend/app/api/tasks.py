from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Request
from fastapi.concurrency import run_in_threadpool
from starlette.status import HTTP_403_FORBIDDEN

from app.core.security.utils import get_current_user
from app.core.tasks.network_tasks import (
    update_network_interfaces_task,
    deactivate_site_task,
    activate_site_task,
)
from app.core.tasks.tracker import TaskTracker, create_tracker

from app.models.tasks import (
    TaskSubmitDataNodeId,
    TaskSubmitDataSite,
    TaskSubmitted,
    TaskStatus,
)
from app.models.auth import User
from app.redis import get_redis_con
from app.settings import Settings, get_settings

settings: Settings = get_settings()
router = APIRouter()


@router.get("/status/{taskid}", response_model=TaskStatus, status_code=200)
async def task_status(
    taskid: str,
    redis_con: Redis = Depends(get_redis_con),
    user: User = Depends(get_current_user),
):
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
    task_data: TaskSubmitDataNodeId,
    background_tasks: BackgroundTasks,
    redis_con: Redis = Depends(get_redis_con),
    user: User = Depends(get_current_user),
):
    if user["access_lvl"] < 5:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    tracker: TaskTracker = await create_tracker(
        redis_con,
        name="update interface details",
        task_path="/tasks/network/update_interfaces",
        task_data=task_data.dict(),
        username=user["username"],
    )
    # background_tasks.add_task(
    #     update_network_interfaces_task, nodeids=task_data.nodeids, tracker=tracker
    # )
    await run_in_threadpool(
        update_network_interfaces_task(nodeids=task_data.nodeids, tracker=tracker)
    )

    return {"task_id": tracker.task_id, "task_name": "Update Network Interface Details"}


@router.post("/network/deactivate_site", response_model=TaskSubmitted, status_code=201)
async def deactivate_site(
    task_data: TaskSubmitDataSite,
    redis_con: Redis = Depends(get_redis_con),
    user: User = Depends(get_current_user),
):
    if user["access_lvl"] < 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if task_data.site not in settings.TASK_DEACTIVATE_SITES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to deactivate site: {task_data.site}",
        )

    tracker: TaskTracker = await create_tracker(
        redis_con,
        name="deactivate site",
        task_path="/tasks/network/deactivate_site",
        task_data=task_data.dict(),
        username=user["username"],
    )
    await deactivate_site_task(site=task_data.site, tracker=tracker)
    return {
        "task_id": tracker.task_id,
        "task_name": f"Deactivate Site {task_data.site}",
    }


@router.post("/network/activate_site", response_model=TaskSubmitted, status_code=201)
async def activate_site(
    task_data: TaskSubmitDataSite,
    redis_con: Redis = Depends(get_redis_con),
    user: User = Depends(get_current_user),
):
    if user["access_lvl"] < 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if task_data.site not in settings.TASK_DEACTIVATE_SITES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to activate site: {task_data.site}",
        )

    tracker: TaskTracker = await create_tracker(
        redis_con,
        name="deactivate site",
        task_path="/tasks/network/activate_site",
        task_data=task_data.dict(),
        username=user["username"],
    )
    await activate_site_task(site=task_data.site, tracker=tracker)
    return {"task_id": tracker.task_id, "task_name": f"Activate Site {task_data.site}"}
