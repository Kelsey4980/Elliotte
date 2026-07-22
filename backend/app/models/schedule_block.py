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

    task: Task | None = None

    is_break: bool = False

    @property
    def duration_hours(self) -> float:

        return (
            self.end - self.start
        ).total_seconds() / 3600