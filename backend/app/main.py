from pprint import pprint

from app.clients.notion.client import NotionClient
from app.clients import notion
from app.clients.notion.mapper import NotionMapper


def main():
    print("=" * 40)
    print("🤖 Elliotte")
    print("=" * 40)

    notion = NotionClient()

    
    # results = notion.client.search()

    pages = notion.get_pages(page_size=5)

    print(f"Successfully retrieved {len(pages)} pages!\n")

    tasks = [NotionMapper.to_task(page) for page in pages]

    print(f"Successfully retrieved {len(tasks)} tasks\n")

    for task in tasks:
        print(task)

    # for page in pages:
    #     print("=" * 60)

    #     print("ID:", page["id"])

    #     properties = page["properties"]

    #     print("Properties:")

    #     for name, value in properties.items():
    #         print(f"  • {name}: {value['type']}")


if __name__ == "__main__":
    main()