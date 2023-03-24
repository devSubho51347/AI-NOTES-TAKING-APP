import uuid
from notion_client import Client
from pprint import pprint
import json

notion_token = "secret_BYY1aFjE9UaOWpfyMbW2HsWEalgNqP5TlmIY9VKmX8f"
notion_page_id = "af9e68b2ccd044659ba30df4c7f98345"
notion_database_id = "871759ce667647eabe59a61b2a47580d"


def write_dict_to_file_as_json(content, file_name):
    content_as_json_str = json.dumps(content)

    with open(file_name, 'w') as f:
        f.write(content_as_json_str)


def read_text(client, page_id):
    response = client.blocks.children.list(block_id=page_id)
    return response['results']


def safe_get(data, dot_chained_keys):
    '''
        {'a': {'b': [{'c': 1}]}}
        safe_get(data, 'a.b.0.c') -> 1
    '''
    keys = dot_chained_keys.split('.')
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data


## Method to write data to the notion table
def write_row(client, database_id, task, status, date):

    client.pages.create(
        **{
            "parent": {
                "database_id": database_id
            },
            'properties': {
                'Task': {'title': [{'text': {'content': task}}]},
                'status': {'rich_text': [{'text': {'content': status}}]},
                'Date': {'date': {'start': date}}
            }
        }
    )


def main():
    client = Client(auth=notion_token)

    db_info = client.databases.retrieve(database_id=notion_database_id)

    write_dict_to_file_as_json(db_info, 'db_info.json')

    db_rows = client.databases.query(database_id=notion_database_id)

    write_dict_to_file_as_json(db_rows, 'db_rows.json')

    simple_rows = []

    for row in db_rows['results']:
        status = safe_get(row, 'properties.status.title.0.plain_text')
        date = safe_get(row, 'properties.Date.date.start')
        task = safe_get(row, 'properties.Task.title.0.plain_text')

        simple_rows.append({
            'task': task,
            'date': date,
            'status': status
        })

    task = "Teach"
    status = "Pending"
    date = '2022-12-25'

    write_row(client, notion_database_id, task, status, date)
    print("Data has been appended to the notion page")

    write_dict_to_file_as_json(simple_rows, 'simple_rows.json')

    # Failed to create the write function, need to work on that only that is failed and all the othe functions are working pretty well


if __name__ == '__main__':
    main()

