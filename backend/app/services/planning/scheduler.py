from datetime import timedelta

from app.models.schedule_block import ScheduleBlock
from app.models.task import Task
from app.models.time_slot import TimeSlot
from app.models.weekly_availability import WeeklyAvailability
from app.services.planning.task_estimator import TaskEstimator


class Scheduler:
    """
    Schedules tasks into available time slots.
    """

    def __init__(self):

        self.estimator = TaskEstimator()

    def schedule(
        self,
        tasks: list[Task],
        availability: WeeklyAvailability,
    ) -> list[ScheduleBlock]:

        blocks: list[ScheduleBlock] = []

        #
        # Copy slots because we'll modify them.
        #
        slots = availability.slots.copy()

        for task in tasks:

            duration = timedelta(
                hours=self.estimator.estimate_hours(task)
            )

            for slot in slots:

                available = slot.end - slot.start

                if available >= duration:

                    block = ScheduleBlock(
                        title=task.title,
                        start=slot.start,
                        end=slot.start + duration,
                        task=task,
                    )

                    blocks.append(block)

                    #
                    # Shrink the remaining slot.
                    #
                    slot.start = block.end

                    break

        return blocks