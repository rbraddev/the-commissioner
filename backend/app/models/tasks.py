from typing import *

from pydantic import BaseModel


class TaskBase(BaseModel):
    task_id: str


class TaskData(BaseModel):
    name: str
    path: str
    status: str
    total: int
    complete: Optional[int]
    task_failed_msg: Optional[str]
    failed: Optional[int]
    run_time: Optional[float]


class TaskResults(BaseModel):
    host: Optional[dict]


class TaskFailed(BaseModel):
    host: Optional[dict]


class TaskStatus(TaskBase):
    task_data: TaskData
    results: Optional[list]
    failed: Optional[list]


class TaskSubmitted(TaskBase):
    task_name: str


class TaskSubmitDataNodeId(BaseModel):
    nodeids: List[int]


class TaskSubmitDataSite(BaseModel):
    site: str
