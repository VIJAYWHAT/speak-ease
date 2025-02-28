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

        await setDoc(doc(db, "users", user.uid), {
            uid: user.uid,
            email: user.email,
            name: user.displayName,
            profilePic: user.photoURL, 
            createdAt: serverTimestamp()
        }, { merge: true });

        console.log("User signed in and saved:", user);
        
        // Redirect to home after sign-in
        window.location.href = "/home";
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
        } else {
            window.location.href = "/login"; // Redirect to login if not signed in
        }
    });
};
