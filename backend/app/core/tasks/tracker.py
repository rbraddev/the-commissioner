import functools
import logging
from ast import literal_eval
from dataclasses import dataclass, field
from itertools import chain
from typing import *
from uuid import uuid4

from aioredis.client import Redis
from app.core.host import Host
from app.core.tasks.errors import NoTaskFound, NoTaskName

log = logging.getLogger("uvicorn")


@dataclass
class TaskTracker:
    _con: Redis = field(repr=False)
    task_id: str = field(default=None)
    name: str = field(default=None)

    async def _init(self):
        if not self.task_id:
            self.task_id = str(uuid4())
            if not self.name:
                raise NoTaskName("Task requires a name")
            task_defaults = {
                "name": self.name,
                "status": "pending",
                "total": 0,
                "complete": 0,
            }
            await self._set(task_defaults)
        else:
            task_data: dict = await self.getall()
            if task_data:
                self.name = task_data.get("name")
            else:
                raise NoTaskFound("No tasks found with Task ID provided")

    async def add_failed(self, host: Host):
        await self._con.lpush(f"{self.task_id}:failed", str(host.failed_dict()))

    async def add_host_result(self, host: Host):
        await self._con.lpush(f"{self.task_id}:result", str(host.result_dict()))

    async def _get_failed(self):
        failed = await self._con.lrange(f"{self.task_id}:failed", "0", "-1")
        return failed

    async def _get_host_results(self):
        results = await self._con.lrange(f"{self.task_id}:result", "0", "-1")
        return results

    async def completed(self):
        await self._con.hincrby(self.task_id, "complete", "1")

    async def set_status(self, status: str):
        await self._set({"status": status})

    async def set_result(self, result: dict):
        await self._set({"result": str(result)})

    async def set_host_status(self, result: dict):
        await self._con.lpush(f"{self.task_id}:result", str(result))

    async def set_total(self, total: str):
        await self._set({"total": str(total)})

    async def _set(self, data: dict) -> None:
        await self._con.hset(self.task_id, mapping=data)

    async def getall(self):
        task_data = await self._con.hgetall(self.task_id)
        results = await self._get_host_results()
        failed = await self._get_failed()
        task_data.update({"failed_count": len(failed)})

        task_dict = {
            "task_data": task_data if task_data else {},
            "results": [literal_eval(item) for item in results] if results else {},
            "failed": [literal_eval(item) for item in failed] if failed else {},
        }

        return task_dict

    async def get(self, key: str) -> Union[str, dict]:
        value = await self._con.hget(self.task_id, key)
        return value


async def create_tracker(
    con: Redis, task_id: str = None, name: str = None
) -> TaskTracker:
    task = TaskTracker(con, task_id=task_id, name=name)
    await task._init()
    return task


def track(func):
    @functools.wraps(func)
    async def wrapper(host, **kwargs):
        tracker: TaskTracker = kwargs["tracker"]
        result = await func(host, **kwargs)
        await tracker.completed()
        return result

    return wrapper
