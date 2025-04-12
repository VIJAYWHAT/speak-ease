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
    users_ref = db.collection("users").where("email", "==", user_data["email"]).stream()
    user_doc_id = None

   
    for user in users_ref:
        user_doc_id = user.id  # Get Firestore document ID
        break

    if user_doc_id:
        # Update existing user document
        db.collection("users").document(user_doc_id).update(user_data)
        print(f"Updated existing user: {user_data['email']}")
    else:
        # Create new user document
        new_doc_ref = db.collection("users").document()
        user_data["uid"] = new_doc_ref.id
        new_doc_ref.set(user_data) 
        print(f"Added new user: {user_data['email']} with UID: {new_doc_ref.id}")


    session['username'] = user_data.get('name', 'User')


def authenticate_user(contact, password):
    users_ref = db.collection('users')
    users = users_ref.stream()  # Get all documents in users collection

    for user in users:
        user_data = user.to_dict()
        
        # Check if email or phone matches and password matches
        if (user_data.get('email') == contact or user_data.get('phone') == contact) and user_data.get('password') == password:
            return user_data 

    return None
