import tkinter as tk
import threading
import speech_recognition as sr
from gtts import gTTS
import sounddevice as sd
import soundfile as sf

def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save('output.mp3')
    data, samplerate = sf.read('output.mp3')
    sd.play(data, samplerate)
    sd.wait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source, phrase_time_limit=3)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"boss: {query}")
    except:
        return ""
    return query.lower()
