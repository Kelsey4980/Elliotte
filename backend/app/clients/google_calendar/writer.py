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

        created_event = (
            self.service.events()
            .insert(
                calendarId="primary",
                body=event,
            )
            .execute()
        )

        return created_event