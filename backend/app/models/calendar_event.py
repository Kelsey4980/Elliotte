
from datetime import datetime

from pydantic import BaseModel


class CalendarEvent(BaseModel):

    id: str

    title: str

    start: datetime

    end: datetime

    all_day: bool = False