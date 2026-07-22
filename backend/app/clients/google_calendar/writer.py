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
            "summary": block.title,

            "description": (
                "Created by Elliotte\n\n"
                f"Priority: {block.task.size}\n"
                f"Due: {block.task.due_date:%Y-%m-%d}"
            ),

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

        return created_event

    def create_schedule(
        self,
        blocks: list[ScheduleBlock],
    ) -> None:

        for block in blocks:
            print(f"✓ {block.title}")
            self.create_event(block)

    def clear_schedule(self):

        calendar = self.client.get_or_create_elliotte_calendar()

        response = (
            self.client.service.events()
            .list(
                calendarId=calendar["id"],
            )
            .execute()
        )

        for event in response.get("items", []):

            props = (
                event.get("extendedProperties", {})
                    .get("private", {})
            )

            if props.get("source") != "elliotte":
                continue
            
            self.client.service.events().delete(
                calendarId=calendar["id"],
                eventId=event["id"],
            ).execute()

    def sync(
        self,
        blocks: list[ScheduleBlock],
    ):
        
        print("\n📤 Syncing to Google Calendar...\n")

        self.clear_schedule()

        self.create_schedule(blocks)

        print(
            f"\nSuccessfully created "
            f"{len(blocks)} events."
        )