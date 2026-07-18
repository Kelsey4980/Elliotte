from datetime import date

from app.models.task import Task


class NotionMapper:
    """
    Converts raw Notion pages into Elliotte Task objects.
    """

    @staticmethod
    def to_task(page: dict) -> Task:
        properties = page["properties"]

        # Assessment (Title)
        title = ""
        if properties["Assessment"]["title"]:
            title = properties["Assessment"]["title"][0]["plain_text"]

        # Status
        status = ""
        if properties["Status"]["select"]:
            status = properties["Status"]["select"]["name"]

        # Due Date
        due_date = None
        if properties["Due Date"]["date"]:
            due_date = date.fromisoformat(
                properties["Due Date"]["date"]["start"]
            )

        # Course
        course = None
        if properties["Course"]["select"]:
            course = properties["Course"]["select"]["name"]

        # Type
        task_type = None
        if properties["Type"]["select"]:
            task_type = properties["Type"]["select"]["name"]

        # Size
        size = None
        if properties["Size"]["select"]:
            size = properties["Size"]["select"]["name"]

        # Completed checkbox
        completed = properties[" "]["checkbox"]

        return Task(
            id=page["id"],
            title=title,
            status=status,
            due_date=due_date,
            course=course,
            task_type=task_type,
            size=size,
            completed=completed,
        )