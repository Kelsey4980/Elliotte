from datetime import timedelta

from app.models.schedule_block import ScheduleBlock
from app.models.task import Task
from app.models.weekly_availability import WeeklyAvailability
from app.services.planning.task_estimator import TaskEstimator

ZERO = timedelta()

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
    ) -> tuple[list[ScheduleBlock], list[Task]]:

        blocks: list[ScheduleBlock] = []

        unscheduled = []

        #
        # Copy slots because we'll modify them.
        #
        slots = availability.model_copy(deep=True).slots

        for task in tasks:

            estimated = timedelta(
                hours=self.estimator.estimate_hours(task)
            )

            remaining = estimated

            part = 1

            for slot in slots:

                if remaining <= ZERO:
                    break

                available = slot.end - slot.start

                if available <= ZERO:
                    continue

                work = min(
                    available,
                    remaining,
                )

                title = task.title

                if part > 1:
                    title += f" (Part {part})"  

                block = ScheduleBlock(
                    title=title,
                    start=slot.start,
                    end=slot.start + work,
                    task=task,
                )

                blocks.append(block)

                #
                # Shrink the remaining slot.
                #
                slot.start = block.end
                part += 1
                remaining -= work

            if remaining > timedelta():
                unscheduled.append(task)    

        return blocks, unscheduled