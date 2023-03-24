import tempfile

import numpy as np
import speech_recognition as sr
import gtts
from playsound import playsound
import os
from pathlib import Path
# import vlc
from datetime import datetime

import uuid
from notion_client import Client
from pprint import pprint
import json

r = sr.Recognizer()

notion_token = "secret_BYY1aFjE9UaOWpfyMbW2HsWEalgNqP5TlmIY9VKmX8f"
notion_page_id = "af9e68b2ccd044659ba30df4c7f98345"
notion_database_id = "871759ce667647eabe59a61b2a47580d"

# client = NotionClient(token, database_id)

ACTIVATION_COMMAND = "hello ram"


def get_audio():
    with sr.Microphone() as source:
        print("Say something")
        audio = r.listen(source)
    return audio


def audio_to_text(audio):
    text = ""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError:
        print("could not request results from API")
    return text


def play_sound(text):
    try:
        tts = gtts.gTTS(text)
        tempfile = Path().cwd() / "audio.mp3"
        print(str(tempfile))
        tts.save(str(tempfile))
        playsound(str(tempfile))
        os.remove(tempfile)
        # print("file has been removed")

        # temp_dir = tempfile.mkdtemp()
        # variable = np.random.randint(1111, 1111111)
        # file_name = f'recording{variable}.m4a'
        # temp_path = os.path.join(temp_dir, file_name)
        # tts = gtts.gTTS(text)
        # tts.save(temp_path)
        # media = vlc.MediaPlayer(temp_path)
        # media.play()
    except AssertionError:
        print("could not play sound")


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

    return True


if __name__ == "__main__":

    while True:
        a = get_audio()
        command = audio_to_text(a)
        status = "Not Started"
        client = Client(auth=notion_token)

        if ACTIVATION_COMMAND in command.lower():
            print("activate")
            play_sound("What can I do for you?")

            note = get_audio()
            note = audio_to_text(note)

            if note:
                play_sound("You have added the task " + note)

                date = datetime.now().astimezone().isoformat()
                task = note

                is_added = write_row(client, notion_database_id, task, status, date)
                if is_added:
                    play_sound("Stored new item")



                # res = client.create_page(note, now, status="Active")
                # if res.status_code == 200:
                #     play_sound("Stored new item")
