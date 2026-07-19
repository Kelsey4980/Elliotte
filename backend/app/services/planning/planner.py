from datetime import datetime

from app.models.task import Task
from app.models.weekly_plan import WeeklyPlan
from app.services.planning.scheduler import Scheduler


class Planner:
    """
    Elliotte's planning engine.

    Coordinates the scheduling process.
    """

    def __init__(self):
        self.scheduler = Scheduler()

    def create_weekly_plan(
        self,
        tasks: list[Task],
        start: datetime,
    ) -> WeeklyPlan:

        blocks = self.scheduler.create_blocks(
            tasks,
            start=start,
        )

        return WeeklyPlan(
            blocks=blocks
        )