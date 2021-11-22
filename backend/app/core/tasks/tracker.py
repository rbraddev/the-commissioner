import functools
import logging
import asyncio
from time import perf_counter
from datetime import datetime
from ast import literal_eval
from dataclasses import dataclass, field
from itertools import chain
from typing import *
from uuid import uuid4

from aioredis.client import Redis
from sqlmodel import Session

from app.core.host import Host
from app.core.tasks.errors import NoTaskFound, NoTaskName
from app.db import get_engine
from app.models.logs import TaskLogs

log = logging.getLogger("uvicorn")


@dataclass
class TaskTracker:
    _con: Redis = field(repr=False)
    task_id: str = field(default=None)
    name: str = field(default=None)
    task_path: str = field(default=None)
    tasks_data: dict = field(default=None, repr=False)
    username: str = field(default=None, repr=False)

    async def _init(self):
        if not self.task_id:
            self.task_id = str(uuid4())
            if not self.name:
                raise NoTaskName("Task requires a name")
            task_defaults = {
                "name": self.name,
                "username": self.username,
                "path": self.task_path,
                "status": "pending",
                "total": 0,
                "complete": 0,
            }
            await self._set(task_defaults)
            self.log_task()
        else:
            task_data: dict = await self.getall()
            if task_data:
                self.name = task_data.get("name")
            else:
                raise NoTaskFound("No tasks found with Task ID provided")
    
    def log_task(self):
        with Session(get_engine()) as session:
            session.add(
                TaskLogs(
                    time=datetime.now(),
                    username=self.username,
                    taskname=self.name,
                    task_path=self.task_path
                    
                )
            )
            session.commit()

    async def add_failed(self, host: Host):
        await self._con.lpush(f"{self.task_id}:failed", str(host.failed_dict()))

    async def add_host_result(self, host: Host):
        await self._con.lpush(f"{self.task_id}:result", str(host.result_dict()))

    async def _get_failed(self):
        failed = await self._con.lrange(f"{self.task_id}:failed", "0", "-1")
        return failed

    async def task_failed(self, msg: str):
        await self._set({"task_failed_msg": msg})
        await self.set_status("failed")

    async def _get_host_results(self):
        results = await self._con.lrange(f"{self.task_id}:result", "0", "-1")
        return results

    async def completed(self):
        await self._con.hincrby(self.task_id, "complete", 1)

    async def set_status(self, status: str):
        await self._set({"status": status})

    async def set_result(self, result: dict):
        await self._set({"result": str(result)})

    async def set_host_status(self, result: dict):
        await self._con.lpush(f"{self.task_id}:result", str(result))

    async def set_total(self, total: int):
        await self._set({"total": total})

    async def set_starttime(self, s_time: float):
        await self._set({"start": s_time})

    async def set_endtime(self, e_time: float):
        await self._set({"end": e_time})

    async def valid_username(self, username: str) -> bool:
        task_username = await self._get("username")
        return task_username == username

    async def _get(self, key):
        result = await self._con.hget(self.task_id, key)
        return result

    async def _set(self, data: dict) -> None:
        await self._con.hset(self.task_id, mapping=data)

    async def run_time(self) -> float:
        if await self._get("end"):
            start = await self._get("start")
            end = await self._get("end")
            return float(f"{float(end) - float(start):.2f}")
        return 0.0

    async def getall(self):
        task_data = await self._con.hgetall(self.task_id)
        task_data.update({"task_failed_msg": await self._get("task_failed_msg")})
        results = await self._get_host_results()
        failed = await self._get_failed()
        task_data.update({"failed": len(failed)})
        task_data.update({"run_time": await self.run_time()})

        task_dict = {
            "task_id": self.task_id,
            "task_data": task_data if task_data else {},
            "results": [literal_eval(item) for item in results] if results else [],
            "failed": [literal_eval(item) for item in failed] if failed else [],
        }

        return task_dict

    async def get(self, key: str) -> Union[str, dict]:
        value = await self._con.hget(self.task_id, key)
        return value


async def create_tracker(
    con: Redis,
    task_id: str = None,
    name: str = None,
    task_path: str = None,
    task_data: dict = None,
    username: str = None,
) -> TaskTracker:
    task = TaskTracker(
        con,
        task_id=task_id,
        name=name,
        username=username,
        task_path=task_path,
        tasks_data=task_data,
    )
    await task._init()
    return task


def track_task(func):
    @functools.wraps(func)
    async def wrapper(**kwargs):
        tracker: TaskTracker = kwargs["tracker"]
        await start_task(tracker)
        try:
            result = await func(**kwargs)
        except Exception as exc:
            result = None
            await tracker.task_failed(str(exc))
        asyncio.create_task(track_complete(tracker))
        return result    

    return wrapper


async def track_complete(tracker: TaskTracker):
    while await tracker.get("status") != "complete":
        if int(await tracker.get("complete")) == int(await tracker.get("total")):
            await end_task(tracker) 

async def start_task(tracker: TaskTracker):
    await tracker.set_status("running")
    await tracker.set_starttime(perf_counter())


async def end_task(tracker: TaskTracker):
    await tracker.set_endtime(perf_counter())
    await tracker.set_status("complete")


def track(func):
    @functools.wraps(func)
    async def wrapper(**kwargs):
        tracker: TaskTracker = kwargs["tracker"]
        host: Host = kwargs["host"]
        try:
            result = await func(**kwargs)
            await tracker.add_host_result(host)
        except Exception as exc:
            result = None
            host.failed_msg = str(exc)
            await tracker.add_failed(kwargs["host"])
        await tracker.completed()
        return result

    return wrapper
