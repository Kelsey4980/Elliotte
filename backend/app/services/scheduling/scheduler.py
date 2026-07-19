from collections import defaultdict
from datetime import date
from app.models.task import Task


class Scheduler:
    """
    Creates a simple weekly plan.
    """

    def create_plan(
        self,
        tasks: list[Task]
    ) -> dict[date, list[Task]]:

        schedule = defaultdict(list)

        for task in sorted(
            tasks,
            key=lambda t: t.due_date or date.max
        ):
            schedule[task.due_date].append(task)

        return schedule