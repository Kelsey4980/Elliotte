from datetime import time

from pydantic import BaseModel


class Availability(BaseModel):
    weekday: int

    start_time: time

    end_time: time