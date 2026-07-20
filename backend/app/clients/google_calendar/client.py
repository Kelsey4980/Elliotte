from pathlib import Path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.models.calendar_event import CalendarEvent
from app.clients.google_calendar.mapper import GoogleCalendarMapper


class GoogleCalendarClient:
    """
    Client for communicating with Google Calendar.
    """

    ELLIOTTE_CALENDAR_NAME = "Elliotte"

    SCOPES = [
        "https://www.googleapis.com/auth/calendar"
    ]

    def __init__(self):

        self.credentials = None
        self._elliotte_calendar = None

        # secrets = Path("secrets")
        # token_path = secrets / "token.json"
        # credentials_path = secrets / "credentials.json"

        BASE_DIR = Path(__file__).resolve().parents[3]

        SECRETS_DIR = BASE_DIR / "secrets"

        token_path = SECRETS_DIR / "token.json"
        credentials_path = SECRETS_DIR / "credentials.json"

        # Load saved login
        if token_path.exists():
            self.credentials = Credentials.from_authorized_user_file(
                token_path,
                self.SCOPES
            )

        # Login if needed
        if (
            not self.credentials
            or not self.credentials.valid
        ):

            if (
                self.credentials
                and self.credentials.expired
                and self.credentials.refresh_token
            ):

                self.credentials.refresh(Request())

            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path,
                    self.SCOPES
                )

                self.credentials = flow.run_local_server(
                    port=0
                )

            token_path.write_text(
                self.credentials.to_json()
            )

        self.service = build(
            "calendar",
            "v3",
            credentials=self.credentials
        )

    def get_events(
        self, 
        max_results: int = 20
    ) -> list[CalendarEvent]:

        events: list[CalendarEvent] = []

        elliotte = self.get_or_create_elliotte_calendar()

        for calendar in self.get_calendars():

            if calendar["id"] == elliotte["id"]:
                continue

            events.extend(
                self.get_events_from_calendar(
                    calendar_id=calendar["id"],
                    max_results=max_results,
                )
            )

        for event in events:
            print(
                event.title,
                event.start,
                event.start.tzinfo,
            )

        events.sort(key=lambda event: event.start)

        return events
    
    def get_events_from_calendar(
        self,
        calendar_id: str,
        max_results: int = 20,
    ) -> list[CalendarEvent]:

        now = datetime.utcnow().isoformat() + "Z"

        response = (
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return [
            GoogleCalendarMapper.to_calendar_event(event)
            for event in response["items"]
        ]

    def get_calendars(self):

        response = (
            self.service.calendarList()
            .list()
            .execute()
        )

        return response["items"]
    
    def get_elliotte_calendar(self):

        if self._elliotte_calendar is not None:
            return self._elliotte_calendar

        for calendar in self.get_calendars():

            if calendar["summary"] == self.ELLIOTTE_CALENDAR_NAME:

                self._elliotte_calendar = calendar
                return calendar

        return None
    
    def create_elliotte_calendar(self):

        body = {
            "summary": "Elliotte",
            "timeZone": "Asia/Manila",
        }

        return (
            self.service.calendars()
            .insert(body=body)
            .execute()
        )
    
    def get_or_create_elliotte_calendar(self):

        calendar = self.get_elliotte_calendar()

        if calendar is None:

            calendar = self.create_elliotte_calendar()

            self._elliotte_calendar = calendar

        return calendar