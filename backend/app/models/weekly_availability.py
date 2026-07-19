

from pydantic import BaseModel
from datetime import date
from app.models.time_slot import TimeSlot
from app.models.calendar_event import CalendarEvent

class WeeklyAvailability(BaseModel):
    slots: list[TimeSlot]

    grouped_events: dict[date, list[CalendarEvent]]

    start_date: date

    end_date: date

    total_free_hours: float

    total_slots: int

    @property
    def planning_days(self) -> int:
        return (
            self.end_date - self.start_date
        ).days + 1