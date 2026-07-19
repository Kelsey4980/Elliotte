from datetime import datetime

from pydantic import BaseModel


class TimeSlot(BaseModel):

    start: datetime

    end: datetime

    @property
    def duration_hours(self) -> float:
        return (self.end - self.start).total_seconds() / 3600