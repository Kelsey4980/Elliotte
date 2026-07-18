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

    completed: bool = False


    # Previous Model (save for future reference)
    # id: str
    # title: str

    # status: str = "Todo"

    # priority: str = "Medium"

    # estimated_hours: Optional[float] = None

    # due_date: Optional[date] = None

    # category: Optional[str] = None

    # can_split: bool = True