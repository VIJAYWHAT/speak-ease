from flask import Flask, redirect, render_template, request, jsonify, url_for
import firebase_admin
from firebase_admin import credentials, auth
from services import firestore_db
from flask_cors import CORS

cred = credentials.Certificate("app/speak-ease-key.json")

try:
    firebase_admin.initialize_app(cred)
except ValueError:
    print("Firebase already initialized")

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

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

        firestore_db.add_user(email, password)
        
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/signup2')
def signup2():
    return render_template('signup2.html')

@app.route('/logout')
def logout():
    return redirect(url_for('landing'))


if __name__ == '__main__':
    app.run(debug=True)
