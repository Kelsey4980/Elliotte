from datetime import timedelta

from app.models.schedule_block import ScheduleBlock
from app.models.task import Task
from app.models.weekly_availability import WeeklyAvailability
from app.services.planning.task_estimator import TaskEstimator
from app.models.user_preferences import UserPreferences
from app.models.time_slot import TimeSlot

ZERO = timedelta()

class Scheduler:
    """
    Schedules tasks into available time slots.
    """

    def __init__(
        self,
        preferences: UserPreferences | None = None,
    ):

        self.estimator = TaskEstimator()

        self.preferences = (
            preferences
            if preferences
            else UserPreferences()
        )

    def schedule(
        self,
        tasks: list[Task],
        availability: WeeklyAvailability,
    ) -> tuple[list[ScheduleBlock], list[Task]]:
        
        max_session = timedelta(
            hours=self.preferences.max_session_hours
        )

        break_length = timedelta(
            minutes=self.preferences.break_minutes
        )

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
                    max_session,
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
                remaining -= work
                slot.start = block.end
                part += 1

                minimum_work = timedelta(minutes=15)

                if (
                    remaining > ZERO
                    and slot.end - slot.start >= break_length + minimum_work
                ):

                    break_block = self.create_break(slot, break_length)
                    blocks.append(break_block)
                    slot.start = break_block.end
            
            if remaining > ZERO:
                unscheduled.append(task)

        return blocks, unscheduled
    
    def create_break(
        self,
        slot: TimeSlot,
        break_length: timedelta,
    ) -> ScheduleBlock:
        return ScheduleBlock(
            title="☕ Break (15 min)",
            start=slot.start,
            end=slot.start + break_length,
            is_break=True,
        )