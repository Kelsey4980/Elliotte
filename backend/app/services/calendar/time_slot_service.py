from collections import defaultdict
from datetime import datetime
from datetime import date

from app.models.calendar_event import CalendarEvent
from app.models.time_slot import TimeSlot
from app.models.user_preferences import UserPreferences
from app.models.weekly_availability import WeeklyAvailability


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
    ) -> WeeklyAvailability:

        grouped = self.group_events_by_day(events)

        slots = []

        for day in sorted(grouped):

            day_events = grouped[day]

            slots.extend(
                self.generate_daily_slots(day_events)
            )

        return self.build_availability(slots, grouped)

    def group_events_by_day(
        self,
        events: list[CalendarEvent],
    ) -> dict[date, list[CalendarEvent]]:

        grouped = defaultdict(list)

        for event in events:

            grouped[event.start.date()].append(event)

        return dict(grouped)

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
    
    def build_availability(
        self,
        slots: list[TimeSlot],
        grouped: dict[date, list[CalendarEvent]],
    ) -> WeeklyAvailability:
        
        if slots:

            start_date = min(
                slot.start.date()
                for slot in slots
            )

            end_date = max(
                slot.end.date()
                for slot in slots
            )

        else:

            today = datetime.now().date()

            start_date = today
            end_date = today

        total_hours = sum(
            slot.duration_hours
            for slot in slots
        )

        return WeeklyAvailability(
            slots=slots,
            grouped_events=grouped,
            start_date=start_date,
            end_date=end_date,
            total_free_hours=total_hours,
            total_slots=len(slots),
        )