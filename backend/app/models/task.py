from datetime import date
from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    """
    Represents a task inside Elliotte.

    """
    id: str

    title: str

    status: str

    due_date: Optional[date] = None

    course: Optional[str] = None

    task_type: Optional[str] = None

    size: Optional[str] = None

    is_completed: bool = False

    @property
    def estimated_hours(self) -> float:
        """
        Converts the task size into an estimated duration.
        """

        # TODO: Change size to reflect Notion state 
        mapping = {
            "XS": 0.5,
            "S": 1,
            "M": 2,
            "L": 4,
            "XL": 8,
        }

        return mapping.get(self.size, 1)


    # Previous Model (save for future reference)
    # id: str
    # title: str

    # status: str = "Todo"

    # priority: str = "Medium"

    # estimated_hours: Optional[float] = None

    # due_date: Optional[date] = None

    # category: Optional[str] = None

    # can_split: bool = True