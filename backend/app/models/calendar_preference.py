from pydantic import BaseModel

class CalendarPreference(BaseModel):

    calendar_id: str
    enabled: bool = True
    blocks_time: bool = True