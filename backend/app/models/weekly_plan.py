from pydantic import BaseModel

from app.models.schedule_block import ScheduleBlock


class WeeklyPlan(BaseModel):
    blocks: list[ScheduleBlock] = []