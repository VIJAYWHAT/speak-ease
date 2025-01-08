from flask import Flask, redirect, render_template, request, jsonify, url_for, session
import firebase_admin
from firebase_admin import credentials, auth,  firestore
from services import firestore_db
from flask_cors import CORS
import os



if os.getenv("RENDER"):
    cred = credentials.Certificate("/etc/secrets/speak-ease-key.json")
else:
    cred = credentials.Certificate("app/speak-ease-key.json") 


if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
app.secret_key = "your_secret_key"

@app.route('/')
def landing():
    qoutes = firestore_db.get_qoutes()
    return render_template('index.html', qoutes = qoutes)

@app.route('/dashboard')
def dashboard():
    return "Welcome to Dashboard!"

@app.route('/home')
def home():
    username = session.get('username', 'Guest')
    return render_template('home.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        contact = request.form.get('contact')
        password = request.form.get('password')

        # Check Firestore for matching user
        user = firestore_db.authenticate_user(contact, password)

        if user:
            session['username'] = user['name']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")

    return render_template('login.html', error=None)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Store email & password in session for next page
        session['email'] = email
        session['password'] = password
        
        return redirect(url_for('signup2'))

    return render_template('signup.html')

@app.route('/signup2', methods=['GET', 'POST'])
def signup2():
    if request.method == 'POST':
        # Get stored email and password from session
        email = session.get('email')
        password = session.get('password')

        if not email or not password:
            return redirect(url_for('signup'))  # Redirect back if session expired

        # Collect user details from form
        user_data = {
            "email": email,
            "password": password,  
            "name": request.form.get('name'),
            "phone": request.form.get('phone'),
            "age": request.form.get('age'),
            "gender": request.form.get('gender'),
            "native_language": request.form.get('native_language'),
            "learn_languages": request.form.getlist('learn_languages'),  # Multi-selection
            "learning_reason": request.form.getlist('learning_reason'),  # Multi-selection
            "location": request.form.get('location'),
            "role": request.form.get('role'),
            "availability_from": request.form.get('availability_from'),
            "availability_to": request.form.get('availability_to'),
            "available_days": request.form.getlist('available_days')  # Multi-selection
        }

        # Save user data to Firestore
        firestore_db.add_user(user_data)

        return redirect(url_for('home'))  # Redirect to home

    return render_template('signup2.html')


@app.route('/logout')
def logout():
    return redirect(url_for('landing'))


if __name__ == '__main__':
    app.run(debug=True)
