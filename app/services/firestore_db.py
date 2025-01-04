import firebase_admin
from firebase_admin import credentials, firestore, auth
from werkzeug.security import generate_password_hash

cred = credentials.Certificate("app/speak-ease-key.json")
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    print("Firebase already initialized")

db = firestore.client()

def get_qoutes():
    doc_ref = db.collection('speakease').document('landing')
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        return data.get('qoutes', 'Guest')
    return 'Guest'


def add_user(email, password):
    users_ref = db.collection('users')
    users_ref.add({
        'email': email,
        'password': password 
    })
