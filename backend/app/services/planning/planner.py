from app.models.task import Task
from app.models.weekly_availability import WeeklyAvailability
from app.models.weekly_plan import WeeklyPlan
from app.services.planning.scheduler import Scheduler
from app.services.planning.task_prioritizer import TaskPrioritizer


class Planner:
    """
    Elliotte's planning engine.
    """

    def __init__(self):

        self.prioritizer = TaskPrioritizer()
        self.scheduler = Scheduler()

    def create_weekly_plan(
        self,
        tasks: list[Task],
        availability: WeeklyAvailability,
    ) -> WeeklyPlan:

        ordered_tasks = self.prioritizer.sort_tasks(
            tasks
        )

        blocks = self.scheduler.schedule(
            ordered_tasks,
            availability,
        )

        print("\nPriority Order\n")

        for task in ordered_tasks:

            print(
                task.due_date,
                task.size,
                task.title,
            )

        return WeeklyPlan(
            blocks=blocks
        )