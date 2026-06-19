// Firebase Configuration - RawJoy E-Commerce
const firebaseConfig = {
  apiKey: "AIzaSyCUp8hkGxCtAktLbqCsNYHgTGJnZ5d2cSE",
  authDomain: "rawjoy-1998f.firebaseapp.com",
  projectId: "rawjoy-1998f",
  storageBucket: "rawjoy-1998f.firebasestorage.app",
  messagingSenderId: "217902038682",
  appId: "1:217902038682:web:c243e1aa485e2ec29b6923",
  measurementId: "G-FB9LLGD96L"
};

// Initialize Firebase using CDN modules
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';
import { getAuth } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js';

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

export { app, db, auth, firebaseConfig };
