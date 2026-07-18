from pprint import pprint

from app.clients.notion.client import NotionClient
from app.clients import notion


def main():
    print("=" * 40)
    print("🤖 Elliotte")
    print("=" * 40)

    notion = NotionClient()

    
    # results = notion.client.search()

    pages = notion.get_pages()

    print(f"Successfully retrieved {len(pages)} pages!\n")

    for page in pages[:5]:
        print("=" * 60)

        print("ID:", page["id"])

        properties = page["properties"]

        print("Properties:")

        for name, value in properties.items():
            print(f"  • {name}: {value['type']}")


if __name__ == "__main__":
    main()