import os
import json
import firebase_admin
from flask_cors import CORS
from datetime import datetime
from services import firestore_db
from firebase_admin import credentials, auth,  firestore
from flask import Flask, redirect, render_template, request, jsonify, url_for, session

if os.getenv("RENDER"):
    cred = credentials.Certificate("/etc/secrets/speak-ease-key.json")
else:
    cred = credentials.Certificate("app/speak-ease-key.json") 


if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
app.secret_key = "secure_secret_key"
db = firestore.client()

@app.route('/')
def landing():
    if "email" in session:
        return redirect(url_for("home"))   
    else:
        qoutes = firestore_db.get_qoutes()
        return render_template('index.html', qoutes = qoutes)
   

@app.route('/dashboard')
def dashboard():
    return "Welcome to Dashboard!"

@app.route('/home')
def home():
    if "email" not in session:
        return redirect(url_for("login"))

    email = session['email'] 

    # Fetch user document from Firestore
    users_ref = db.collection("users").where("email", "==", email).stream()
    user_data = None

    for user in users_ref:
        user_data = user.to_dict()
        break 

    if not user_data:
        return "User data not found!"

    if "learn_languages" not in user_data or not user_data["learn_languages"]:
        return redirect(url_for("signup2"))

    course_ids = user_data.get("learn_languages", [])
    progress_data = user_data.get("progress", {})

    courses_data = []
    for course_id in course_ids:
        course_doc = db.collection("courses").document(course_id).get()
        if course_doc.exists:
            course_dict = course_doc.to_dict()
            courses_data.append({
                "id": course_id,
                "name": course_dict.get("name", "Unknown"),
                "progress": progress_data.get(course_id, "0"),
                "desc": course_dict.get("desc", "No description available")
            })

    # Fetch video classes details
    now = datetime.now()
    classes_ref = db.collection('videoclass')
    docs = classes_ref.stream()

    upcoming_classes = []
    for doc in docs:
        data = doc.to_dict()
        class_time = datetime.strptime(data['datetime'], "%d-%m-%Y %H:%M")
        if class_time > now:
            upcoming_classes.append({
                'title': data['title'],
                'desc': data['desc'],
                'link': data['link'],
                'tutor_name': data['tutor_name']
            })

    return render_template(
        'home.html',
        username=user_data['name'],
        email=email,
        uid=user_data['uid'],
        courses=courses_data,
        video_classes=upcoming_classes
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        contact = request.form.get('contact')
        password = request.form.get('password')

        user = firestore_db.authenticate_user(contact, password)

        if user:
            session['username'] = user['name']
            session['email'] = user['email']  
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

        # 🔹 Convert JSON string back to a Python list
        learn_languages = json.loads(request.form.get('learn_languages', '[]'))
        learning_reason = json.loads(request.form.get('learning_reason', '[]'))

        user_data = {
            "email": email,
            "password": password,  
            "name": request.form.get('name'),
            "phone": request.form.get('phone'),
            "age": request.form.get('age'),
            "gender": request.form.get('gender'),
            "native_language": request.form.get('native_language'),
            "learn_languages": learn_languages,  
            "learning_reason": learning_reason, 
            "location": request.form.get('location'),
            "role": request.form.get('role'),
            "availability_from": request.form.get('availability_from'),
            "availability_to": request.form.get('availability_to'),
            "available_days": request.form.getlist('available_days')
        }

        firestore_db.add_user(user_data)

        return redirect(url_for('home'))  # Redirect to home

    return render_template('signup2.html')



@app.route('/get_lessons')
def get_lessons():
    course_id = request.args.get('course_id')
    
    if not course_id:
        return jsonify({"error": "Course ID is required"}), 400

    # Fetch lessons from Firestore
    lessons_ref = db.collection("courses").document(course_id).collection("lessons").stream()

    lessons = []
    for lesson in lessons_ref:
        lesson_data = lesson.to_dict()
        lessons.append({
            "title": lesson_data.get("title", "No Title"),
            "content": lesson_data.get("content", "No Content")
        })

    return jsonify(lessons)


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/lesson_page')
def lesson_page():
    return render_template('lesson.html')

@app.route('/get_quiz', methods=['GET'])
def get_quiz():
    quiz_doc = db.collection("quiz").document("day-quiz").get()

    if not quiz_doc.exists:
        return jsonify({"error": "Quiz not found"}), 404

    quiz_data = quiz_doc.to_dict()

    return jsonify({
        "question": quiz_data.get("question", "No question available"),
        "options": [
            quiz_data.get("option1", ""),
            quiz_data.get("option2", ""),
            quiz_data.get("option3", ""),
            quiz_data.get("option4", "")
        ],
        "correct_answer": quiz_data.get("correct_answer", "")  # This will be (option1, option3)
    })

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route("/set_session", methods=["POST"])
def set_session():
    data = request.get_json()
    if "email" in data:
        session["email"] = data["email"]  # Store email in session
        session["name"] = data.get("name", "User")
        return jsonify({"message": "Session updated"}), 200
    return jsonify({"error": "Invalid data"}), 400

@app.route("/check_session")
def check_session():
    return jsonify(dict(session))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))


if __name__ == '__main__':
    app.run(debug=True)
