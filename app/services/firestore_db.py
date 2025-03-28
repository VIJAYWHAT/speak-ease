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


def add_user(email, password, name, phone, age, gender, native_language, learn_languages, learning_reason, location, role, availability_from, availability_to, available_days):
    users_ref = db.collection('users')
    users_ref.add({
        'email': email,
        'password': password,  # Consider hashing for security
        'name': name,
        'phone': phone,
        'age': age,
        'gender': gender,
        'native_language': native_language,
        'learn_languages': learn_languages,  # Stored as an array
        'learning_reason': learning_reason,  # Stored as an array
        'location': location,
        'role': role,
        'availability_from': availability_from,
        'availability_to': availability_to,
        'available_days': available_days  # Stored as an array
    })

def authenticate_user(contact, password):
    users_ref = db.collection('users')
    users = users_ref.stream()  # Get all documents in users collection

    for user in users:
        user_data = user.to_dict()
        
        if (user_data.get('email') == contact or user_data.get('phone') == contact) and user_data.get('password') == password:
            return user_data 

    return None # No matching user found
