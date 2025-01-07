import os
import firebase_admin
from flask import session
from firebase_admin import credentials, firestore

if os.getenv("RENDER"):
    cred = credentials.Certificate("/etc/secrets/speak-ease-key.json")
else:
    cred = credentials.Certificate("app/speak-ease-key.json") 


if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
def get_qoutes():
    doc_ref = db.collection('speakease').document('landing')
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        return data.get('qoutes', 'Guest')
    return 'Guest'


def add_user(user_data):
    users_ref = db.collection('users')
    users_ref.add(user_data)
    session['username'] = user_data['name']
    print("User added successfully!")

def authenticate_user(contact, password):
    users_ref = db.collection('users')
    users = users_ref.stream()  # Get all documents in users collection

    for user in users:
        user_data = user.to_dict()
        
        if (user_data.get('email') == contact or user_data.get('phone') == contact) and user_data.get('password') == password:
            return user_data 

    return None # No matching user found
