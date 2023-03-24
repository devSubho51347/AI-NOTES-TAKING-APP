from notion_client import Client
from pprint import pprint

notion_token = "secret_BYY1aFjE9UaOWpfyMbW2HsWEalgNqP5TlmIY9VKmX8f"
notion_page_id = "af9e68b2ccd044659ba30df4c7f98345"
notion_database_id = "871759ce667647eabe59a61b2a47580d"


def main():
    client = Client(auth=notion_token)

    page_response = client.pages.retrieve(notion_page_id)

    pprint(page_response, indent=2)


if __name__ == '__main__':
    main()
    print("Notion has been activated and all the solutions has been deactivated")
