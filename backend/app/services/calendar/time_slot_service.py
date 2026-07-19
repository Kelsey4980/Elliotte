from datetime import datetime, timedelta

from app.models.calendar_event import CalendarEvent
from app.models.time_slot import TimeSlot


class TimeSlotService:

    WORK_START = 9
    WORK_END = 21

    def get_free_time(
        self,
        events: list[CalendarEvent],
    ) -> list[TimeSlot]:

        slots = []

        if not events:
            return slots

        current_day = events[0].start.date()

        tz = events[0].start.tzinfo

        day_start = datetime(
            year=current_day.year,
            month=current_day.month,
            day=current_day.day,
            hour=self.WORK_START,
            tzinfo=tz,
        )

        day_end = datetime(
            year=current_day.year,
            month=current_day.month,
            day=current_day.day,
            hour=self.WORK_END,
            tzinfo=tz,
        )

        current = day_start

        for event in events:

            if event.start > current:

                slots.append(
                    TimeSlot(
                        start=current,
                        end=event.start
                    )
                )

            current = max(current, event.end)

        if current < day_end:

            slots.append(
                TimeSlot(
                    start=current,
                    end=day_end
                )
            )

        return slots