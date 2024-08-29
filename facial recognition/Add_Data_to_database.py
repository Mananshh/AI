import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(r"C:\Users\Storm\After Hours(Python)\facial recognition\facerecognition-17636-firebase-adminsdk-zraqk-5a3e032310.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' :"https://facerecognition-17636-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    
    "Manansh":
        {
            "name" : "Manansh",
            "position" : "Creator",
            "logins" : 0
        },
    
    "Elon":
        {
            "name" : "Elon",
            "position" : "inspiration",
            "logins" : 0
        }


}

for key , values in data.items():
    ref.child(key).set(values)