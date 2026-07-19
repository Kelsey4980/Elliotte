from datetime import time

from pydantic import BaseModel


class TimeSlot(BaseModel):

    start_time: time

    end_time: time