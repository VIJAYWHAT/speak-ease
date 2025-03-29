# SpeakEase By Tech Spartans

[SpeakEase](https://speak-ease.onrender.com/) is a collaborative learning platform that helps users track and manage their language learning progress. It integrates Firebase Firestore for real-time data storage and Firebase Authentication for user management.

## Features
- User authentication (Email/Password, Google Sign-In)
- Firestore integration for storing user progress
- Real-time course tracking
- Deployed using Render with Gunicorn

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/VIJAYWHAT/speak-ease.git
cd speakease
```

### 2️⃣ Create a Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Firebase
1. Go to the **Firebase Console** → Create a new project.
2. Enable **Firestore** (in native mode) and **Firebase Authentication**.
3. Download the `serviceAccountKey.json` file.
4. Place it in the `app/` directory and rename it as `speak-ease-key.json`.

### 5️⃣ Set Up Environment Variables
Create a `.env` file in the project root:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

---

## 🏃 Running the Project Locally
```sh
flask run
```
The application should be available at: **http://127.0.0.1:5000**

If using **Gunicorn**:
```sh
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🔥 Firebase Firestore Structure
```
users (Collection)
 ├── {user_id} (Document)
 │   ├── email: "user@example.com"
 │   ├── name: "John Doe"
 │   ├── learn_languages: ["course_1", "course_2"]

courses (Collection)
 ├── {course_id} (Document)
 │   ├── name: "English"
 │   ├── progress: 10
 │   ├── desc: "Basic English course"
```

---

## 🔗 Deployment on Render

1. Create a **Render** account and a new **Web Service**.
2. Connect your **GitHub repository**.
3. Set up **environment variables** (`FLASK_ENV`, `SECRET_KEY`).
4. Install dependencies:
```sh
pip install gunicorn
```
5. Add a `Procfile` for deployment:
```
web: gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
6. Deploy 🚀

---

## 📌 Important Notes
- Make sure `speak-ease-key.json` is **not** committed to GitHub.
- If Firestore rules block access, update the security rules.
- Debugging? Use `print()` statements or enable Flask debug mode.

---

## 💡 Contributing
1. Fork the repo
2. Create a feature branch
3. Submit a PR!

---

## 📜 License
MIT License © 2025 SpeakEase
