from collections import defaultdict
from datetime import datetime

from app.models.calendar_event import CalendarEvent
from app.models.time_slot import TimeSlot
from app.models.user_preferences import UserPreferences


class TimeSlotService:

    def __init__(
        self,
        preferences: UserPreferences | None = None,
    ):

        self.preferences = (
            preferences
            if preferences
            else UserPreferences()
        )

    def generate_time_slots(
        self,
        events: list[CalendarEvent],
    ) -> list[TimeSlot]:

        grouped = self.group_events_by_day(events)

        slots = []

        for day_events in grouped.values():

            slots.extend(
                self.generate_daily_slots(day_events)
            )

        return slots

    def group_events_by_day(
        self,
        events: list[CalendarEvent],
    ) -> dict:

        grouped = defaultdict(list)

        for event in events:

            grouped[event.start.date()].append(event)

        return grouped

    def generate_daily_slots(
        self,
        events: list[CalendarEvent],
    ) -> list[TimeSlot]:

        slots = []

        if not events:
            return slots

        events.sort(key=lambda event: event.start)

        current_day = events[0].start.date()

        tz = events[0].start.tzinfo

        day_start = datetime(
            current_day.year,
            current_day.month,
            current_day.day,
            self.preferences.work_start,
            tzinfo=tz,
        )

        day_end = datetime(
            current_day.year,
            current_day.month,
            current_day.day,
            self.preferences.work_end,
            tzinfo=tz,
        )

        current = day_start

        for event in events:

            if event.start > current:

                slots.append(
                    TimeSlot(
                        start=current,
                        end=event.start,
                    )
                )

            current = max(current, event.end)

        if current < day_end:

            slots.append(
                TimeSlot(
                    start=current,
                    end=day_end,
                )
            )

        return slots