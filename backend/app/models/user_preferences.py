from pydantic import BaseModel

from app.models.calendar_preference import CalendarPreference


class UserPreferences(BaseModel):
    """
    Stores scheduling preferences for the user.
    """

    work_start: int = 9
    work_end: int = 21

    lunch_start: int = 12
    lunch_end: int = 13

    preferred_block_hours: float = 2.0
    minimum_block_minutes: int = 30

    break_after_hours: float = 2.0

    calendar_preferences: list[CalendarPreference]