from typing import *

from pydantic import BaseModel


class TaskSubmitted(BaseModel):
    task_id: str
    task_name: str


class TaskSubmitData(BaseModel):
    nodeids: List[int]
