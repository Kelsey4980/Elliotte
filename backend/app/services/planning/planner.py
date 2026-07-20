from app.models.task import Task
from app.models.weekly_availability import WeeklyAvailability
from app.models.weekly_plan import WeeklyPlan
from app.services.planning.scheduler import Scheduler


class Planner:
    """
    Elliotte's planning engine.
    """

    def __init__(self):

        self.scheduler = Scheduler()

    def create_weekly_plan(
        self,
        tasks: list[Task],
        availability: WeeklyAvailability,
    ) -> WeeklyPlan:

        blocks = self.scheduler.schedule(
            tasks,
            availability,
        )

        return WeeklyPlan(
            blocks=blocks
        )