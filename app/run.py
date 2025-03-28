from flask import Flask, redirect, render_template, request, jsonify, url_for, session
import firebase_admin
from firebase_admin import credentials, auth,  firestore
from services import firestore_db
from flask_cors import CORS


cred = credentials.Certificate("app/speak-ease-key.json")

try:
    firebase_admin.initialize_app(cred)
except ValueError:
    print("Firebase already initialized")

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
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')


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
        # Get stored email and password
        email = session.get('email')
        password = session.get('password')

        if not email or not password:
            return redirect(url_for('signup'))  # Redirect back if session expired

        # Get user details from the form
        name = request.form.get('name')
        phone = request.form.get('phone')
        age = request.form.get('age')
        gender = request.form.get('gender')
        native_language = request.form.get('native_language')
        learn_languages = request.form.getlist('learn_languages')  # Multi-selection
        learning_reason = request.form.getlist('learning_reason')  # Multi-selection
        location = request.form.get('location')
        role = request.form.get('role')
        availability_from = request.form.get('availability_from')
        availability_to = request.form.get('availability_to')
        available_days = request.form.getlist('available_days')  # Multi-selection

        # Save all data to Firestore
        firestore_db.add_user(email, password, name, phone, age, gender, native_language, learn_languages, learning_reason, location, role, availability_from, availability_to, available_days)

        return redirect(url_for('home'))  # Redirect to home or dashboard

    return render_template('signup2.html')


@app.route('/logout')
def logout():
    return redirect(url_for('landing'))


if __name__ == '__main__':
    app.run(debug=True)
