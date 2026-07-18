import os

from dotenv import load_dotenv
from notion_client import Client


class NotionClient:
    """
    Client for communicating with the Notion API.
    """

    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("NOTION_API_KEY")
        self.data_source_id = os.getenv("NOTION_DATA_SOURCE_ID")

        if not self.api_key:
            raise ValueError("NOTION_API_KEY is missing.")

        if not self.data_source_id:
            raise ValueError("NOTION_DATA_SOURCE_ID is missing.")

        self.client = Client(auth=self.api_key)

    def get_database(self):
        """
        Returns the entire database response.
        """
        return self.client.databases.retrieve(
            database_id=self.data_source_id
        )

    def get_pages(self, page_size=5, **kwargs):
        """
        Returns pages from the configured Notion data source.
        """
        response = self.client.data_sources.query(
            data_source_id=self.data_source_id,
            page_size=page_size,
            **kwargs
        )

        return response["results"]

    def query_database(self, **kwargs):
        """
        Allows custom filters/sorts when querying.
        """
        return self.client.databases.query(
            database_id=self.data_source_id,
            **kwargs
        )["results"]