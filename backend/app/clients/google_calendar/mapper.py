from datetime import datetime
from zoneinfo import ZoneInfo

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

        if all_day:

            start_dt = datetime.fromisoformat(start).replace(
                tzinfo=ZoneInfo("Asia/Manila")
            )

            end_dt = datetime.fromisoformat(end).replace(
                tzinfo=ZoneInfo("Asia/Manila")
            )

        else:

            start_dt = datetime.fromisoformat(start)

            end_dt = datetime.fromisoformat(end)


        return CalendarEvent(
            id=event["id"],
            title=event.get("summary", "(No Title)"),
            start=start_dt,
            end=end_dt,
            all_day=all_day,
        )