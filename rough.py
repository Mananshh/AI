import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage

cred = credentials.Certificate(r"C:\Users\Storm\After Hours(Python)\facial recognition\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' :"https://facerecognition-17636-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognition-17636.appspot.com"
})

studentInfo = db.reference(f'Students').get()
print(studentInfo[''])