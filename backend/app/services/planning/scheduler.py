from datetime import timedelta

from app.models.schedule_block import ScheduleBlock
from app.models.task import Task
from app.models.time_slot import TimeSlot
from app.models.user_preferences import UserPreferences
from app.models.weekly_availability import WeeklyAvailability
from app.services.planning.task_estimator import TaskEstimator

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

        min_work = timedelta(
            minutes=self.preferences.min_work_session_minutes
        )

        slots = availability.model_copy(deep=True).slots

        blocks: list[ScheduleBlock] = []
        unscheduled: list[Task] = []

        continuous_work = ZERO
        last_work_end = None

        # Iterate through tasks
        for task in tasks:

            # Get duration of task
            remaining = timedelta(
                hours=self.estimator.estimate_hours(task)
            )

            part = 1

            # Iterate through available slots
            for slot in slots:
                
                # Exit if task is complete
                if remaining <= ZERO:
                    break

                # Skip empty slots.
                if slot.end <= slot.start:
                    continue

                # TODO: figure this out
                # Natural break between slots.
                if (
                    last_work_end is not None
                    and slot.start - last_work_end >= break_length
                ):
                    continuous_work = ZERO

                # Need a scheduled break?
                if (
                    continuous_work >= max_session
                    and slot.end - slot.start >= break_length # + min_work
                ):

                    break_block = self.create_break(
                        slot,
                        break_length,
                    )

                    blocks.append(break_block)

                    slot.start = break_block.end

                    continuous_work = ZERO

                available = slot.end - slot.start

                # Exit if no more available slots
                if available <= ZERO:
                    continue

                # TODO: figure this out too
                # Only work until the session limit.
                session_remaining = max_session - continuous_work

                work = min(
                    available,
                    remaining,
                    session_remaining,
                )

                # Exit if no more work remaining
                if work <= ZERO:
                    continue

                # Append part # if task is split into multiple blocks
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

                slot.start = block.end

                last_work_end = block.end
                continuous_work += work
                remaining -= work

                part += 1

                print("block title = ", block.title)
                print("continuous work = ", continuous_work)
                print()

            if remaining > ZERO:
                unscheduled.append(task)

        return blocks, unscheduled

    def create_break(
        self,
        slot: TimeSlot,
        break_length: timedelta,
    ) -> ScheduleBlock:

        minutes = int(
            break_length.total_seconds() / 60
        )

        return ScheduleBlock(
            title=f"☕ Break ({minutes} min)",
            start=slot.start,
            end=slot.start + break_length,
            is_break=True,
        )