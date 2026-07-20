from app.models.schedule_block import ScheduleBlock
from app.models.task import Task
from pydantic import BaseModel


class WeeklyPlan(BaseModel):
    """
    Elliotte's generated weekly plan.
    """

    blocks: list[ScheduleBlock]

    unscheduled_tasks: list[Task] = []

    total_tasks: int = 0

    scheduled_tasks: int = 0

    scheduled_hours: float = 0