import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(r"C:\Users\Storm\After Hours(Python)\FINAL AI\facial recognition\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' :"https://facerec-810ae-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "0":
        {
            "name" : "Manansh",
            "position" : "Creator",
            "logins" : 0
        },

    "1":
        {
            "name": "Emily",
            "position": "Test subject",
            "logins" :0
        },


    "2":
        {
            "name" : "Elon",
            "position" : "Inspiration",
            "logins" : 0
        },
    
    

}

for key , values in data.items():
    ref.child(key).set(values)