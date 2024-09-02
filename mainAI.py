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
import pyaudio
import pyttsx3
import cv2
import datetime
import sounddevice as sd
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from langchain_community.llms import Ollama


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
        print("Speak now...")
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
    'databaseURL' :"https://facerecognition-17636-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognition-17636.appspot.com"
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
    elif 12<= hour <= 18:
         speak("Good Afternoon {name}")
    else:
         speak("Good Evening {name}")


llm = Ollama(model="phi")
def beginAI():
     while True:
        prompt = input_audio()
        response = llm.invoke(prompt)
        speak(response)


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
                
                wishme(studentInfo['name'])
                #    else:
                #         print("LKJFLSDKJLSDKJFLKSDJasdfasdfasdfasdf")  
        return True              
        break

face_check()
if face_check():
    face_check()
    beginAI()

