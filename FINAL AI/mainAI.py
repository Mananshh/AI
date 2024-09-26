import cv2
import os
import face_recognition as frm
import pickle
import numpy as np
import webbrowser
import firebase_admin
from groq import Groq
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage
import speech_recognition as sr
import sys
import threading
import cv2
import datetime
import time
import requests
from playsound import playsound
from typing import Union 
import sounddevice as sd
from webscout import LLAMA3 as brain
from rich import print
import json
import smtplib
import AppOpener
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# from langchain_community.llms import Ollama
def generate_audio(message: str, voice: str = "en-US-Standard-B"):
    url: str = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={{{message}}}"
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    
    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except:
        return None

# Function to print text with animation effect
def cooler_print(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)  # Adjust the sleep duration for the animation speed
    print()

# Function to play generated speech and delete the audio file
def Co_speak(message: str, voice: str = "en-US-Standard-B", folder: str = "", extension: str = ".mp3"):
    try:
        result_content = generate_audio(message, voice)
        file_path = os.path.join(folder, f"{voice}{extension}")
        with open(file_path, "wb") as file:
            file.write(result_content)
        playsound(file_path)
        os.remove(file_path)
    except Exception as e:
        print(e)

# Function to speak and print text simultaneously
def speak(text):
    # Create threads for both speaking and printing
    t1 = threading.Thread(target=Co_speak, args=(text,))
    t2 = threading.Thread(target=cooler_print, args=(text,))
    
    # Start both threads
    t1.start()
    t2.start()
    
  
    t1.join()
    t2.join()


def input_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        recognizer.energy_threshold = 450
        recognizer.pause_threshold = 1.0
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return str(text.lower())
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the audio")
        return 404
    except sr.RequestError:
        speak("Unable to understand")
        return 404

# while True:
#     try:
#         query = input_audio(
#         if "testing" in query:
#              speak("Test completed.")

#     except Exception as e:
#          speak(e)
#          break
# def initialize():
#     while True:
#             query  = input_audio()
#             if "testing" in query:
#                  speak("Test compelete")
#             break

cred = credentials.Certificate(r"C:\Users\Storm\After Hours(Python)\FINAL AI\facial recognition\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' :"https://facerec-810ae-default-rtdb.firebaseio.com/",
    'storageBucket': "gs://facerec-810ae.appspot.com"
})
'''
The following adds the webacam to the function
'''
cap = cv2.VideoCapture(0)
cap.set(3 ,640) 
cap.set(4,480)

bkground = cv2.imread(r"C:\Users\Storm\After Hours(Python)\FINAL AI\FaceRec\Resources\Background.png")

fmodepath = r'C:\Users\Storm\After Hours(Python)\FINAL AI\FaceRec\Resources\Modes'
modepath = os.listdir(fmodepath) #This returns 1,png 2.png and so on
image_in_mode = []
roll_nos = []

for path in modepath:
        image_in_mode.append(cv2.imread(os.path.join(fmodepath , path)))
        roll_nos.append(path.strip(".png"))
'''
Added all the images in the mode file to a list
'''

def wishme(name):
    hour = int(datetime.datetime.now().hour)
    if 0<= hour < 12:
         speak(f"Good Evening {name}")
    elif 12<= hour <= 15:
         speak("Good Afternoon {name}")
    else:
         speak("Good Evening {name}")


def find_encodings(imagelist):
    encodelist =[]
    for image in imagelist:
            image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB) #Converts to RGB as that is the only one accepted by face recognition
            encode = frm.face_encodings(image)
            encodelist.append(encode)
    return encodelist

encodingListKnown = find_encodings(image_in_mode)
file = open(r'C:\Users\Storm\After Hours(Python)\FINAL AI\FaceRec\EncodeFile.p' , 'rb')
encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds

def sendEmail(recipient, text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    '''
    Import Data,  contacts as csv file or something
    '''
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', recipient, text)
    server.close()

# modeType = 0
# counter = 0
# id = 0
def functions(query):
    if "open google" in query:
         speak("Opening Google")
         webbrowser.open("google.com")    
    elif "send email" in query:
        try:
            speak("What should I say?")
            text = input_audio()
            recipient = "sample@gmail.com"    
            sendEmail(recipient, text)
            speak("Email has been sent!")
        except Exception:
            speak("Error sending the email. Please try again")
    elif "open youtube" in query:
        speak("Opening Youtube")
        webbrowser.open("youtube.com")
    elif "the time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"According to the ITC, the time is {strTime}")
    elif "open discord" in query:
         speak("Opening Discord")
         AppOpener.open("discord")
    elif "open telegram" in query:
         AppOpener.open("telegram")

def face_check():
    while True:
        success, img = cap.read()

        imgS = cv2.resize(img,(0, 0), None , 0.25, 0.25)
        imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faceCurFrame = frm.face_locations(imgS)
        encodeCurrFrame = frm.face_encodings(imgS, faceCurFrame)


        # bkground[162: 162+480, 55 : 55+640] = img #Cooridinates found by self, attaches the webcam to the window
        # bkground[44:44 + 633, 808 : 808 + 414] = image_in_mode[modeType]
    #     cv2.imshow("Vision" , img)
            
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurFrame):
            matches = frm.compare_faces(encodeListKnown, encodeFace)
            Face_Distance = frm.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(Face_Distance)
            
            if  not matches[matchIndex]:
                    # studentInfo = db.reference(f'Students/{id}').get()
                    pass

                    # speak(f"Good morning ")
                    # initialize()
            elif matches[matchIndex]:
                speak("Known user detected")
                studentInfo = db.reference(f'Students/{matchIndex}').get()
                #    studentInfo1 =  db.reference(f'Students/{matchIndex-1}').get()
                print("USER INFO:", studentInfo)
                name = studentInfo['name']
                print(name)
                wishme(name)
                return True
            break
                #    else:
                #         print("LKJFLSDKJLSDKJFLKSDJasdfasdfasdfasdf")  
                     


def listen_for_clap(threshold=0.75, samplerate=44100):
    detected = False

    def audio_callback(indata, frames, time, status):
        nonlocal detected
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > threshold:
            detected = True
            print("Activating......")
            raise sd.CallbackStop() 


    with sd.InputStream(callback=audio_callback, channels=1, samplerate=samplerate):
        while not detected:
            sd.sleep(100)


def save_to_backup(new_data):
    with open(r'C:\Users\Storm\After Hours(Python)\FINAL AI\conversations.txt', 'w') as f:
        json.dump(new_data, f, indent=4)

# from webscout import PhindSearch as brain
# #Phind search will give more tech, coding realted doubts for you to answer, Llama gives answers to more practical questions
# from rich import print
# from webscout.AIutel import RawDog
# from mainAI import speak
# from mainAI import cooler_print

# rawdog = RawDog()
# intro_prompt = rawdog.intro_prompt

# ai = brain(
#     is_conversation=True,
#     max_tokens=800,
#     timeout=30,
#     intro=intro_prompt,
#     filepath=r"C:\Users\Storm\After Hours(Python)\conversations.txt",
#     update_file=True,
#     proxies={},
#     history_offset=10250,
#     act=None,
# )

# def testingAI(text):
#     response = ai.chat(text)
#     rawdog_feedback = rawdog.main(response)
#     if rawdog_feedback:
#         ai.chat(rawdog_feedback)
#     speak(response)
#     return response

from webscout import LLAMA3 as brain
from rich import print
import os

history_file = r"C:\Users\Storm\After Hours(Python)\FINAL AI\conversations.json"

def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return file.read()
    return ""

def save_history(query, response):
    with open(history_file, 'w') as file:
        file.write(f"query: {query}, \nresponse: {response}")


conversation_history = load_history()

# Initialize the AI
# ai = brain(
#     is_conversation=True,  # AI will remember conversations
#     max_tokens=800,
#     timeout=30,
#     intro=None,
#     filepath=None,  # Memory file not used as we handle it manually
#     update_file=False,  # No need to update the memory file
#     proxies={},
#     history_offset=10250,  # Use a high context window model
#     act=None,
#     model='Meta-Llama-3.1-70B-Instruct',
#     system_prompt="Funny ai, with humor and sarcasm in replies"
# )

# def loadresponse(text):
#     conversation_history = load_history()
#     conversation_history += f"\nUser: {text}"

#     full_prompt = conversation_history + "\nAI:"

#     # try:
#     response_chunks = []
#     for chunk in ai.chat(full_prompt):
#         if "text" in chunk:
#             response_chunks.append(chunk[text])
#         else:
#             print("Error: 'text' key missing in response chunk")
#             return "I'm sorry, I couldn't process that."

#     response_text = "".join(response_chunks)
#     conversation_history += f"\nAI: {response_text}"
#     save_to_backup(conversation_history)
#     return response_text
#     # except Exception as e:
#     #     print(f"Error during AI response: {e}")
#     #     return "There was an error processing the request."

import google.generativeai as genai
import os


# genai.configure(api_key="AIzaSyC-U39CuWf_G3F_9IswOLy3XcSFPPSOU_8")
# generation_config = {"temperature": 0.9, "top_p":1 , "top_k":1, "max_output_tokens":2048}

# model = genai.GenerativeModel("gemini-pro", generation_config= generation_config)


# def loadresponse(query):
#         # query = input_audio()
#     response = model.generate_content(query)

#     for chunk in response:
#             answer  = chunk.text
        
    # return answer

os.environ["GROQ_API_KEY"] = "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"
def custom_str(text, end=""):
    result = str(text) + end
    return result

def loadresponse(query):
    past_conversations = load_history()
    
    # Prepare context from previous conversations
    context = ""
    for conv in past_conversations: 
        context += f"User: {conv['user']}\nAI: {conv['ai']}\n"
    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": context,

                "role" : "system",
                "content": "You are a sassy AI with humor",

                "role": "user",
                "content": query
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )


    accumulated_text = ""

    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        accumulated_text += content

        if len(accumulated_text) > 1000000 or any(punct in accumulated_text for punct in [ '!', '?']):
            speak(accumulated_text)  
            accumulated_text = ""  

    # Process any remaining accumulated text
    if accumulated_text:
        save_history(query , accumulated_text)
        speak(accumulated_text)

identify = True
def mainfn():
    while identify:
        # query = input_audio()
        query = input("Enter: ")
        load_history()
        response = loadresponse(query)
        speak(response)
        save_history(query, response)
        break

if __name__ == "__main__":
    print("-----------------------------ON------------------------------------------")
    # listen_for_clap()
    cooler_print("Jarvis is on")
    cooler_print("Initializing face recognition")
    if face_check():
        identify = True
        try:
            while identify:
                mainfn()          
        except AttributeError:
            pass
        except KeyError:
            pass
        except ValueError:
            pass
        except Exception:
            pass
    else:
        pass  
