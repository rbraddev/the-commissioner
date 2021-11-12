from typing import *

from sqlalchemy.sql.expression import table
from sqlmodel import Field, SQLModel


class LogBase(SQLModel):
    username: str
    time: str


class AuthLogs(LogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    success: bool


class TaskLogs(LogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    taskname: str
    task_path: str
