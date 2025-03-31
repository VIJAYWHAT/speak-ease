import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyATlfn28N-zL2iW4v84zow3PRb-cPnQ3IM",
    authDomain: "speak-ease-a221a.firebaseapp.com",
    projectId: "speak-ease-a221a",
    storageBucket: "speak-ease-a221a.appspot.com",
    messagingSenderId: "814624711121",
    appId: "1:814624711121:web:9ef1d07a10e121888dc0f0",
    measurementId: "G-VRG9W5GSP9",
    clientId: "814624711121-mbr8lk6nrbhgjoemfp85ulldo8qg2f4p.apps.googleusercontent.com"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
const db = getFirestore(app);

// Google Sign-In Function
window.googleSignIn = async function () {
    try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;

        // Save user details in Firestorse
        await setDoc(doc(db, "users", user.uid), {
            uid: user.uid,
            email: user.email,
            name: user.displayName,
            profilePic: user.photoURL, 
            createdAt: serverTimestamp()
        }, { merge: true });

        console.log("User signed in:", user);

        // Send user email to backend to store in session
        const response = await fetch("/set_session", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: user.email,
                name: user.displayName
            }),
        });

        if (response.ok) {
            console.log("Session updated in Flask.");
            window.location.href = "/home";  // Redirect to home after login
        } else {
            console.error("Failed to update session.");
            alert("Login failed on server side.");
        }
    } catch (error) {
        console.error("Error signing in:", error);
        alert("Google Sign-In failed!");
    }
};


// Fetch user name after login
window.getUserName = async function () {
    onAuthStateChanged(auth, async (user) => {
        if (user) {
            const userRef = doc(db, "users", user.uid);
            const userSnap = await getDoc(userRef);

            if (userSnap.exists()) {
                document.getElementById("user-name").textContent = userSnap.data().name;
            } else {
                document.getElementById("user-name").textContent = "User";
            }
            console.log("User is logged in:", user);
            window.location.href = "/home";  // Ensure they go to home
        } else {
            // window.location.href = "/login";
            console.log("No user is signed in.");
        }
    });
};
