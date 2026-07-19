from pathlib import Path
from datetime import datetime
import secrets

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

    SCOPES = [
        "https://www.googleapis.com/auth/calendar"
    ]

    def __init__(self):

        self.credentials = None

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
        max_results: int = 20,
    ) -> list[CalendarEvent]:

        from datetime import datetime

        now = datetime.utcnow().isoformat() + "Z"

        response = (
            self.service.events()
            .list(
                calendarId="primary",
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