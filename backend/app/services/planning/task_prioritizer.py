from datetime import date

from app.models.task import Task


class TaskPrioritizer:
    """
    Orders tasks by scheduling priority.
    """

    def sort_tasks(
        self,
        tasks: list[Task],
    ) -> list[Task]:

        today = date.today()

        return sorted(
            tasks,
            key=lambda task: (
                task.due_date is None,
                (
                    task.due_date
                    if task.due_date
                    else date.max
                ),
                self._size_rank(task.size),
            ),
        )

    def _size_rank(
        self,
        size: str | None,
    ) -> int:

        ranking = {
            "Large": 0,
            "Medium": 1,
            "Small": 2,
        }

        return ranking.get(size, 3)