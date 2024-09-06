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
                    print('Unknown user detected')

                    # print(f"Good morning ")
                    # initialize()
            elif matches[matchIndex]:
                print("Known user detected")
                studentInfo = db.reference(f'Students/{matchIndex}').get()
                name = studentInfo['name']
                print("name ", name, "matchindex ", matchIndex)
                #    studentInfo1 =  db.reference(f'Students/{matchIndex-1}').get()
                
                # wishme(studentInfo['name'])
                #    else:
                #         print("LKJFLSDKJLSDKJFLKSDJasdfasdfasdfasdf")  
        return True              

face_check()