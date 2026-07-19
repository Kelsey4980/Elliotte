from pprint import pprint

from app.clients.notion.client import NotionClient
from app.clients import notion
from app.clients.notion.mapper import NotionMapper
from app.services.task_service import TaskService
from app.services import task_service
from app.services.scheduling import scheduler
from app.services.scheduling.scheduler import Scheduler




def main():
    print("=" * 40)
    print("🤖 Elliotte")
    print("=" * 40)

    notion = NotionClient()

    
    # results = notion.client.search()

    pages = notion.get_pages(page_size=20)

    print(f"Successfully retrieved {len(pages)} pages!\n")

    tasks = [NotionMapper.to_task(page) for page in pages]

    task_service = TaskService(tasks)

    # pending_tasks = task_service.get_pending()

    # print(f"Pending Tasks: {len(pending_tasks)}\n")

    # for task in task_service.sort_by_due_date():
    #     if not task.is_completed:
    #         print(
    #             f"{task.due_date} | "
    #             f"{task.course} | "
    #             f"{task.title} | "
    #             f"{task.size}"
    #         )


    scheduler = Scheduler()

    plan = scheduler.create_plan(
        task_service.get_pending()
    )

    print("\n📅 Weekly Plan\n")

    for day, tasks in plan.items():

        print(day)

        for task in tasks:
            print(
                f"   • {task.title}"
            )

        print()


if __name__ == "__main__":
    main()