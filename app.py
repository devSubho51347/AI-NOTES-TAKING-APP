import os
import tempfile

import numpy as np
import streamlit as st
import speech_recognition as sr
import gtts
from playsound import playsound

rec = sr.Recognizer()

command_activator = "hello ram"

command_deactivator = "bye ram"


### Method to record the audio

def get_audio():
    with sr.Microphone() as source:
        print("get_audio activated")
        audio = rec.listen(source)
        return audio


### Method to transcribe audio to text

def audio_transcriber(audio):
    text = ""
    try:
        text = rec.recognize_google(audio)

    except sr.UnknownValueError:
        print("Unable to understand audio")

    except sr.RequestError:
        print("API busy, Please try after some time")

    return text


### Method to get audio feedback
def sound_feedback(text):
    try:
        tts = gtts.gTTS(text)
        # tempfile = "./temp.mp3"
        # temp_dir = tempfile.mkdtemp()
        variable = np.random.randint(1111, 1111111)
        file_name = 'recording.mp3'
        tempfile = f'./recording{variable}.mp3'
        # temp_path = os.path.join(temp_dir, file_name)
        tts.save(tempfile)
        playsound(tempfile)
        print("hello")
        os.remove(tempfile)

    except AssertionError:
        print("unable to play audio")


#
# st.title("SMART TO DO APP")
#
# st.subheader("Hello my name is Gita and I am a smart AI assistant")
#
# st.write("To activate Gita, say hello gita")
#
# button_1 = st.button("Activate Voice Command")

while True:
    sound_feedback("My name is Ram. What can I do for you?")
    my_command = get_audio()
    voice_text = audio_transcriber(my_command)
    print(voice_text)

    if command_activator in voice_text.lower():
        sound_feedback("Voice Command Activated")
        sound_feedback("My name is Ram. What can I do for you?")
        note = get_audio()
        note = audio_transcriber(note)
        # sound_feedback(note)
        if note:
            sound_feedback(note)

    if command_deactivator in voice_text.lower():
        sound_feedback("Bye Bye")
        st.write("Stopped")
        break
