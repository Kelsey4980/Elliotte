from datetime import date

from app.models.task import Task


class TaskService:

    def __init__(self, tasks: list[Task]):
        self.tasks = tasks

    def get_all(self) -> list[Task]:
        return self.tasks

    def get_pending(self) -> list[Task]:
        return [
            task
            for task in self.tasks
            if (
                task.status != "Done"
                and task.task_type == "Task"
            )
        ]

    def get_completed(self) -> list[Task]:
        return [
            task
            for task in self.tasks
            if task.is_completed
        ]

    def sort_by_due_date(self) -> list[Task]:
        return sorted(
            self.tasks,
            key=lambda task: task.due_date or date.max
        )

    def sort_by_course(self) -> list[Task]:
        return sorted(
            self.tasks,
            key=lambda task: task.course or ""
        )