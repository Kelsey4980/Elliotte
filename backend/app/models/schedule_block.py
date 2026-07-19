from datetime import datetime

from pydantic import BaseModel

from app.models.task import Task


class ScheduleBlock(BaseModel):
    """
    Represents a scheduled block of work.
    """

    title: str

    start: datetime

    end: datetime

    task: Task