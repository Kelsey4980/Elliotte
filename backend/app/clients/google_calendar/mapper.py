from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.calendar_event import CalendarEvent

LOCAL_TZ = ZoneInfo("Asia/Singapore")

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
                tzinfo=LOCAL_TZ
            )

            end_dt = datetime.fromisoformat(end).replace(
                tzinfo=LOCAL_TZ
            )

        else:

            start_dt = (
                datetime.fromisoformat(start)
                .astimezone(LOCAL_TZ)
            )

            end_dt = (
                datetime.fromisoformat(end)
                .astimezone(LOCAL_TZ)
            )

        print(event["summary"])

        # print(event["start"])
        # print(event["end"])
        print("START_DT and TZINFO:")
        print(start_dt)
        print(start_dt.tzinfo)
        print()

        return CalendarEvent(
            id=event["id"],
            title=event.get("summary", "(No Title)"),
            start=start_dt,
            end=end_dt,
            all_day=all_day,
        )