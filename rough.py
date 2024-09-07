import cv2
import os
import face_recognition as frm
import pickle
import numpy as np
import cvzone
import firebase_admin
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
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# from langchain_community.llms import Ollama
def generate_audio(message: str,voice : str = "en-US-Wavenet-D"):
    url: str = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={{{message}}}"

    headers = {'User-Agent':'Mozilla/5.0(Maciontosh;intel Mac OS X 10_15_7)AppleWebKit/537.36(KHTML,like Gecoko)Chrome/119.0.0.0 Safari/537.36'}
    
    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except:
        return None
    
def cooler_print(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)  # Adjust the sleep duration for the animation speed
    print()


def Co_speak(message: str, voice: str = "en-US-Wavenet-D", folder: str = "", extension: str = ".mp3") -> Union[None,str]:
    try:
        result_content = generate_audio(message,voice)
        file_path = os.path.join(folder,f"{voice}{extension}")
        with open(file_path,"wb") as file:
            file.write(result_content)
        playsound(file_path)
        os.remove(file_path)
        return None
    except Exception as e:
        print(e)


def speak(text):
    t1 = threading.Thread(target=Co_speak,args=(text,))
    t2 = threading.Thread(target=cooler_print,args=(text,))
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
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the audio")
        return 404
    except sr.RequestError:
        speak("Unable to understand")
        return 404

# while True:
#     try:
#         query = input_audio()
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

cred = credentials.Certificate(r"C:\Users\Storm\After Hours(Python)\facial recognition\serviceAccountKey.json")
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

bkground = cv2.imread(r'C:\Users\Storm\After Hours(Python)\FaceRec\Resources\Background.png')

fmodepath = r'C:\Users\Storm\After Hours(Python)\FaceRec\Resources\Modes'
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
file = open(r'C:\Users\Storm\After Hours(Python)\facial recognition\EncodeFile.p' , 'rb')
encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds

# modeType = 0
# counter = 0
# id = 0

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
                    speak('Unknown user detected')

                    # speak(f"Good morning ")
                    # initialize()
            elif matches[matchIndex]:
                speak("Known user detected")
                studentInfo = db.reference(f'Students/{matchIndex}').get()
                #    studentInfo1 =  db.reference(f'Students/{matchIndex-1}').get()
                # name = studentInfo['name']
                # wishme(name)
                print(matchIndex)
                print(studentInfo)
                print(studentInfo['name'])
                return True
                #    else:
                #         print("LKJFLSDKJLSDKJFLKSDJasdfasdfasdfasdf")  
        break     

if face_check():
     while True:
        inp = input("Enter ")
        if inp == "E":
            print("TT")
            break