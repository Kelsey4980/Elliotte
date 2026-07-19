from datetime import datetime, timedelta

from app.models.schedule_block import ScheduleBlock
from app.models.task import Task


class Scheduler:
    """
    Creates a schedule from a list of tasks.
    """

    def create_blocks(
        self,
        tasks: list[Task],
        start: datetime,
    ) -> list[ScheduleBlock]:

        blocks: list[ScheduleBlock] = []

        current = start.replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0,
        )

        for task in tasks:

            duration = timedelta(hours=task.estimated_hours)

            block = ScheduleBlock(
                title=task.title,
                start=current,
                end=current + duration,
                task=task,
            )

            blocks.append(block)

            current += duration

        return blocks