// Reviews Module
import { db, auth } from './firebase-config.js';
import { 
  collection, doc, addDoc, getDocs, updateDoc, query, where, orderBy, serverTimestamp 
} from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';

const reviewsRef = collection(db, 'reviews');

// Add review
export async function addReview(productId, rating, comment) {
  const user = auth.currentUser;
  if (!user) return { success: false, error: 'Silakan login untuk memberi review.' };
  
  try {
    // Check if user already reviewed this product
    const existing = query(reviewsRef, 
      where('userId', '==', user.uid), 
      where('productId', '==', productId)
    );
    const existingSnap = await getDocs(existing);
    if (!existingSnap.empty) {
      return { success: false, error: 'Anda sudah memberikan review untuk produk ini.' };
    }
    
    await addDoc(reviewsRef, {
      userId: user.uid,
      userName: user.displayName || 'Anonymous',
      productId: productId,
      rating: rating,
      comment: comment,
      createdAt: serverTimestamp()
    });
    
    // Update product average rating
    const allReviews = await getProductReviews(productId);
    const avgRating = allReviews.reduce((sum, r) => sum + r.rating, 0) / allReviews.length;
    await updateDoc(doc(db, 'products', productId), {
      rating: Math.round(avgRating * 10) / 10,
      reviewCount: allReviews.length
    });
    
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Get reviews for a product
export async function getProductReviews(productId) {
  try {
    const q = query(reviewsRef, where('productId', '==', productId), orderBy('createdAt', 'desc'));
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    console.error('Error getting reviews:', error);
    return [];
  }
}

// Render star rating HTML
export function renderStars(rating, interactive = false) {
  let html = '<div class="star-rating">';
  for (let i = 1; i <= 5; i++) {
    if (interactive) {
      html += `<span class="star ${i <= rating ? 'active' : ''}" data-rating="${i}" style="cursor:pointer">★</span>`;
    } else {
      html += `<span class="star ${i <= rating ? 'active' : ''}">★</span>`;
    }
  }
  html += '</div>';
  return html;
}
