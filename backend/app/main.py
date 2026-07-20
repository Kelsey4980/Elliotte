from calendar import calendar
from pprint import pprint
from datetime import datetime, timedelta


from app.clients import notion
from app.clients.notion.client import NotionClient
from app.clients.notion.mapper import NotionMapper

from app.services import task_service
from app.services.task_service import TaskService

from app.services.planning import scheduler
from app.services.planning.scheduler import Scheduler

from app.services.planning.planner import Planner

from app.clients.google_calendar.client import GoogleCalendarClient
from app.clients.google_calendar.mapper import GoogleCalendarMapper
from app.models.calendar_event import CalendarEvent

from app.services.calendar.time_slot_service import TimeSlotService
from app.models.user_preferences import UserPreferences

def main():

    print("=" * 40)
    print("🤖 Elliotte")
    print("=" * 40)

    # ----------------------------
    # Fetch tasks from Notion
    # ----------------------------

    notion = NotionClient()

    pages = notion.get_pages(page_size=20)

    tasks = [
        NotionMapper.to_task(page)
        for page in pages
    ]

    print(f"Successfully retrieved {len(tasks)} tasks.\n")

    # ----------------------------
    # Process tasks
    # ----------------------------

    task_service = TaskService(tasks)

    pending_tasks = task_service.get_pending()

    print(f"Pending Tasks: {len(pending_tasks)}\n")

    # ----------------------------
    # Create schedule
    # ----------------------------

    # scheduler = Scheduler()

    # blocks = scheduler.create_blocks(
    #     pending_tasks,
    #     start=datetime.now()
    # )

    # ----------------------------
    # Display schedule
    # ----------------------------

    # print("📅 Weekly Plan\n")

    # for block in weekly_plan.blocks:

    #     print(
    #         f"{block.start:%A}"
    #     )

    #     print(
    #         f"{block.start:%I:%M %p}"
    #         f" - "
    #         f"{block.end:%I:%M %p}"
    #     )

    #     print(
    #         f"{block.title}\n"
    #     )

    # ----------------------------
    # Connect to Google Calendar
    # ----------------------------

    calendar = GoogleCalendarClient()

    events = calendar.get_events()

    # print("\n📅 Busy Events\n")

    # for event in events:

    #     print(
    #         f"{event.start:%I:%M %p}"
    #         f" -> "
    #         f"{event.end:%I:%M %p}"
    #         f" | "
    #         f"{event.title}"
    #     )
    
    # ----------------------------
    # Time Slots
    # ----------------------------

    preferences = UserPreferences(
        work_start=8,
        work_end=18,
    )

    service = TimeSlotService(preferences=preferences)

    availability = service.generate_time_slots(events)

    print(availability.total_free_hours)

    print("\n📅 Free Time Slots\n")

    for slot in availability.slots:
        print(
            f"[{slot.start:%A}] "
            f"{slot.start:%I:%M %p}"
            f" -> "
            f"{slot.end:%I:%M %p}"
            f" ({slot.duration_hours:.1f} hrs)"
        )

    # slots = service.generate_time_slots(events)

    # print("\n📅 Free Time Slots\n")

    # for slot in slots:

    #     print(
    #         f"[{slot.start:%A}] "
    #         f"{slot.start:%I:%M %p}"
    #         f" -> "
    #         f"{slot.end:%I:%M %p}"
    #         f" ({slot.duration_hours:.1f} hrs)"
    #     )
    
    # ----------------------------
    # Grouped Events
    # ----------------------------

    grouped = service.group_events_by_day(events)

    print("\nGrouped Events\n")

    for day, day_events in grouped.items():

        print(day)

        for event in day_events:

            print(
                f"   {event.start:%H:%M}"
                f" - "
                f"{event.end:%H:%M}"
                f" | "
                f"{event.title}"
            )
    
    # ----------------------------
    # Planner
    # ----------------------------

    planner = Planner()

    plan = planner.create_weekly_plan(
        pending_tasks,
        availability,
    )

    print("\n📅 Elliotte's Weekly Plan\n")

    for block in plan.blocks:

        print(
            f"[{block.start:%A}] "
            f"{block.start:%I:%M %p}"
            f" - "
            f"{block.end:%I:%M %p}"
        )

        print(f"   {block.title}\n")


if __name__ == "__main__":
    main()