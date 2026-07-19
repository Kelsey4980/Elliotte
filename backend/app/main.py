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

    planner = Planner()

    weekly_plan = planner.create_weekly_plan(pending_tasks, start=datetime.now())

    # ----------------------------
    # Display schedule
    # ----------------------------

    print("📅 Weekly Plan\n")

    for block in weekly_plan.blocks:

        print(
            f"{block.start:%A}"
        )

        print(
            f"{block.start:%I:%M %p}"
            f" - "
            f"{block.end:%I:%M %p}"
        )

        print(
            f"{block.title}\n"
        )


if __name__ == "__main__":
    main()