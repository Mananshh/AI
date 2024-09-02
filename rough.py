import firebase_admin
from firebase_admin import credentials, firestore
import face_recognition
import cv2

# Initialize Firebase
cred = credentials.Certificate(r"C:\Users\Storm\After Hours(Python)\facial recognition\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' :"https://facerecognition-17636-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognition-17636.appspot.com"
})
db = firestore.client()

# Load known faces and user IDs from Firebase
def load_known_faces():
    users_ref = db.collection('users')
    docs = users_ref.stream()
    known_face_encodings = []
    known_user_ids = []

    for doc in docs:
        user_data = doc.to_dict()
        face_encoding = user_data.get('face_encoding')  # Assuming face encodings are stored in Firebase
        if face_encoding:
            known_face_encodings.append(face_encoding)
            known_user_ids.append(doc.id)

    return known_face_encodings, known_user_ids

known_face_encodings, known_user_ids = load_known_faces()

# Recognize faces in real-time
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            user_id = known_user_ids[first_match_index]

            # Retrieve user data from Firebase
            user_ref = db.collection('users').document(user_id)
            user_data = user_ref.get().to_dict()
            if user_data:
                name = user_data.get('name')

        print(f"Hello, {name}!")

    # cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()