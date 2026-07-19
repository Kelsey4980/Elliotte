from datetime import datetime

from app.models.calendar_event import CalendarEvent


class GoogleCalendarMapper:
    """
    Converts Google Calendar API responses into Elliotte models.
    """

    @staticmethod
    def to_calendar_event(event: dict) -> CalendarEvent:

        # Google returns either:
        # start.dateTime
        # or
        # start.date

        start = event["start"].get(
            "dateTime",
            event["start"].get("date")
        )

        end = event["end"].get(
            "dateTime",
            event["end"].get("date")
        )

        all_day = "date" in event["start"]

        return CalendarEvent(
            id=event["id"],
            title=event.get("summary", "(No Title)"),
            start=datetime.fromisoformat(start),
            end=datetime.fromisoformat(end),
            all_day=all_day,
        )