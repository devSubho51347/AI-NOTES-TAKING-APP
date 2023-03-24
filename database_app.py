import streamlit as st
import pandas as pd
import numpy as np
# from matplotlib import pyplot as plt
from notion_client import Client

st.title("Task Manager App")

notion_token = "secret_BYY1aFjE9UaOWpfyMbW2HsWEalgNqP5TlmIY9VKmX8f"
notion_page_id = "af9e68b2ccd044659ba30df4c7f98345"
notion_database_id = "871759ce667647eabe59a61b2a47580d"

simple_rows = {"Task": [], "Date": [], "Status": []}

client = Client(auth=notion_token)

db_rows = client.databases.query(database_id=notion_database_id)


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


def create_dataframe(data):
    df = pd.DataFrame(data)
    return df


for row in db_rows['results']:
    status = safe_get(row, 'properties.status.title.0.plain_text')
    date = safe_get(row, 'properties.Date.date.start')
    task = safe_get(row, 'properties.Task.title.0.plain_text')

    simple_rows["Task"].append(task)
    simple_rows["Date"].append(date)
    simple_rows["Status"].append(status)

print(simple_rows)

if len(simple_rows["Task"]) > 0:
    df = create_dataframe(simple_rows)
    st.dataframe(df)
