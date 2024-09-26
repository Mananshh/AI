import speech_recognition as sr
import pyaudio
import pyttsx3
import cv2


def speak(audio):
        print(audio)
        engine = pyttsx3.init('sapi5') 
        voices= engine.getProperty('voices') 
        engine.setProperty('voice', voices[0].id)
        engine.say(audio)
        engine.runAndWait()


def input_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Speak now...")
        recognizer.pause_threshold = 1.0
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the audio")
        return 404
    except sr.RequestError:
        speak("Unable to understand")
        return 404

while True:
    try:
        query = input_audio()
        if "testing" in query:
             speak("Test completed.")

    except Exception as e:
         speak(e)
         break
