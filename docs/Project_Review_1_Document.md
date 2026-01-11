# Speak Ease – Final Year Project (1st Review Document)

**Team:** Tech Spartans  
**Document Type:** First Review Submission  
**Academic Year:** 2024–2025

---

## 1. Project Title

**Speak Ease** – A Collaborative Language Learning Platform with Progress Tracking, Lessons, Quizzes, and Live Support

_(Alternative short title: Speak Ease – Language Learning & Progress Tracking Platform)_

---

## 2. What Problem You’re Solving

- **Fragmented learning:** Many learners use multiple apps or materials without a single place to track what they’re learning (e.g. English, Hindi, Spanish, Tamil, French) and how far they’ve progressed.
- **Lack of structure:** There is no unified flow from “choose language” → “take lessons” → “test with quiz” → “see progress” in one platform.
- **Limited live/community support:** Learners often lack easy access to scheduled video classes, tutor chat, and forums in one place.
- **No personalized dashboard:** Users don’t get a single dashboard that shows their chosen languages, progress per course, upcoming classes, and quick access to AI help and chat.

Speak Ease addresses these by providing:

- **One platform** for signing up, choosing languages and reasons for learning, and getting a personalized home.
- **Structured courses** with lessons (with presentation/video links) and in-lesson quizzes.
- **Progress tracking** per course and an overall profile view.
- **Live elements:** upcoming video classes (with tutor and link), chat (tutor/forum), and an AI assistant (e.g. IBM Granite) for extra practice.

---

## 3. Why This Problem Matters

- **Education and employability:** Strong language skills (especially English and regional languages) improve academic and job opportunities; a structured, trackable platform makes learning more effective.
- **Accessibility:** A free, web-based platform with optional live classes and AI support can reach learners who cannot afford expensive courses or coaching.
- **Consistency and motivation:** Progress tracking and visible completion (e.g. % per course) help users stay consistent and motivated.
- **Scalability:** Digital lessons, quizzes, and scheduled video classes can scale to many users without proportionally increasing cost.
- **Real-world relevance:** Supporting both “Student” and “Tutor” roles, availability, and forums aligns the project with real tutoring and community-based learning.

---

## 4. Who Will Use It

| User Type              | How They Use Speak Ease                                                                                                                                     |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Language learners**  | Sign up, choose languages (e.g. English, Hindi, Tamil), take lessons, attempt quizzes, view progress, join video classes, use chat/forums and AI assistant. |
| **Students**           | Same as above; can set role as “Student,” specify availability and days for live sessions.                                                                  |
| **Tutors**             | Can register as “Tutor,” set availability and days; (future: conduct/manage video classes and respond in chat).                                             |
| **Educators / admins** | (Future) Manage courses, lessons, quizzes, and video class schedule in the backend/Firestore.                                                               |

**Primary users:** Students and adult learners who want to learn one or more languages in a structured way with progress tracking and optional live support.

---

## 5. Technology Stack

| Layer                     | Technology                                                                                      |
| ------------------------- | ----------------------------------------------------------------------------------------------- |
| **Backend**               | Python 3, Flask 3.0                                                                             |
| **Frontend**              | HTML5, CSS3, JavaScript (vanilla), Jinja2 templates                                             |
| **Database**              | Firebase Firestore (NoSQL)                                                                      |
| **Auth**                  | Custom auth (email/phone + password) with session; Firebase Admin SDK for backend access        |
| **APIs / SDKs**           | Firebase Admin SDK (Python), Firestore client                                                   |
| **Deployment**            | Gunicorn, Render (with env-based config for production)                                         |
| **Version control**       | Git / GitHub                                                                                    |
| **External integrations** | IBM Granite Playground (AI assistant iframe), YouTube/Canva links for lessons and video classes |

**Supporting tools:** Flask-CORS, python-dotenv, requests; Firebase Console for Firestore and (optional) Authentication.

---

## 6. Key Features (Summary)

- **Landing page** with call-to-action (Get Started / Login).
- **User registration (2-step):** Signup → User details (name, phone, age, gender, native language, languages to learn, reason, location, role, availability, days).
- **Login** with email or phone and password.
- **Home dashboard:** Welcome by name, course cards with progress %, links to lessons, upcoming video classes modal, quiz button, AI assistant modal, chat link, profile dropdown, logout.
- **Lessons:** Course-wise lessons from Firestore, prev/next navigation, presentation/video links, in-lesson quiz.
- **Quiz:** Day-quiz from Firestore (question + options + correct answer), result feedback.
- **Profile:** User info, overall progress %, course-wise progress list.
- **Chat:** Tutor/forum list, message UI, video call button (UI); currently simple auto-reply (e.g. “hi” → “Hello! How are you?”).
- **Video classes:** List of upcoming classes (title, description, tutor, link) from Firestore `videoclass` collection.

---

## 7. Add-ons That Strengthen the Document

### 7.1 System Architecture (High-Level)

- **Client:** Browser (HTML/CSS/JS + Jinja2).
- **Server:** Flask app (routes for pages, auth, lessons, quiz, session, logout).
- **Data:** Firestore collections – `users`, `courses`, `courses/{id}/lessons`, `quiz`, `videoclass`, `speakease` (e.g. landing content).
- **Auth:** Session-based after custom email/phone + password check using Firestore `users`.

### 7.2 Future Scope (Good for Review)

- **Progress persistence:** Save quiz results and lesson completion to Firestore and update `users.progress` and possibly lesson-level completion.
- **Real chat:** Backend or Firebase-based chat so tutors/forums send real messages (and optional real-time with Firestore listeners).
- **Firebase Authentication:** Migrate to Firebase Auth (email/Google) for security and scalability.
- **Firestore rules:** Replace current “deny all” with proper read/write rules for `users`, `courses`, `quiz`, `videoclass`.
- **Tutor dashboard:** For role “Tutor,” allow creating/editing video class slots and viewing assigned learners.
- **Notifications:** Email or in-app reminders for upcoming video classes.
- **Mobile responsiveness:** Ensure all pages (landing, home, lesson, chat, profile) work well on phones and tablets.

### 7.3 Deliverables You Can Mention

- Deployed working application (e.g. Render).
- GitHub repository with README and setup instructions.
- Firestore data model (users, courses, lessons, quiz, videoclass).
- Document (this file) for first review.

---

## 8. References / Links (Optional to Add)

- Live app: [Speak Ease on Render](https://speak-ease.onrender.com/)
- Repository: (Add your GitHub repo link)
- Firebase: https://firebase.google.com/
- Flask: https://flask.palletsprojects.com/

---

_This document is intended for the first review of the final year project. Update the “Academic Year,” “Team,” and “References” as per your college format._
