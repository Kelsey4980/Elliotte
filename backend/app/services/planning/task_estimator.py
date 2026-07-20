from app.models.task import Task


class TaskEstimator:
    """
    Estimates how long a task should take based on its size.
    """

    DEFAULT_HOURS = 2.0

    SIZE_MAPPING = {
        "Small": 1.0,
        "Medium": 2.0,
        "Large": 4.0,
    }

    def estimate_hours(
        self,
        task: Task,
    ) -> float:

        if task.size is None:
            return self.DEFAULT_HOURS

        return self.SIZE_MAPPING.get(
            task.size,
            self.DEFAULT_HOURS,
        )