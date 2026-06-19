// Authentication Module
import { auth, db } from './firebase-config.js';
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged,
  updateProfile 
} from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js';
import { 
  doc, setDoc, getDoc, updateDoc, serverTimestamp 
} from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';

// Register new user
export async function registerUser(email, password, name, phone = '') {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;
    
    // Update display name
    await updateProfile(user, { displayName: name });
    
    // Save user data to Firestore
    await setDoc(doc(db, 'users', user.uid), {
      name: name,
      email: email,
      phone: phone,
      address: '',
      role: 'user',
      createdAt: serverTimestamp()
    });
    
    return { success: true, user };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Login
export async function loginUser(email, password) {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    return { success: true, user: userCredential.user };
  } catch (error) {
    let message = 'Login gagal.';
    if (error.code === 'auth/user-not-found') message = 'Email tidak ditemukan.';
    if (error.code === 'auth/wrong-password') message = 'Password salah.';
    if (error.code === 'auth/invalid-email') message = 'Format email tidak valid.';
    return { success: false, error: message };
  }
}

// Logout
export async function logoutUser() {
  try {
    await signOut(auth);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Get current user
export function getCurrentUser() {
  return auth.currentUser;
}

// Listen to auth state changes
export function onAuthChange(callback) {
  return onAuthStateChanged(auth, callback);
}

// Get user profile from Firestore
export async function getUserProfile(uid) {
  try {
    const docRef = doc(db, 'users', uid);
    const docSnap = await getDoc(docRef);
    if (docSnap.exists()) {
      return { success: true, data: docSnap.data() };
    }
    return { success: false, error: 'Profile not found' };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Update user profile
export async function updateUserProfile(uid, data) {
  try {
    const docRef = doc(db, 'users', uid);
    await updateDoc(docRef, { ...data, updatedAt: serverTimestamp() });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Check if user is admin
export async function isAdmin(uid) {
  const profile = await getUserProfile(uid);
  return profile.success && profile.data.role === 'admin';
}
