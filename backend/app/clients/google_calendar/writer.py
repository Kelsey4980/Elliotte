from app.models.schedule_block import ScheduleBlock
from app.clients.google_calendar.client import GoogleCalendarClient

class CalendarWriter:

    def __init__(self):
        self.client = GoogleCalendarClient()
        self.service = self.client.service

    def create_event(
        self,
        block: ScheduleBlock,
    ):

        event = {
            "summary": f"📚 {block.title}",

            "description": "Created by Elliotte",

            "extendedProperties": {
                "private": {
                    "source": "elliotte"
                }
            },

            "start": {
                "dateTime": block.start.isoformat(),
            },

            "end": {
                "dateTime": block.end.isoformat(),
            },
        }

        calendar = self.client.get_or_create_elliotte_calendar()

        calendar_id = calendar["id"]

        created_event = (
            self.service.events()
            .insert(
                calendarId=calendar_id,
                body=event,
            )
            .execute()
        )

        for calendar in self.client.get_calendars():

            print(calendar["summary"])

        return created_event