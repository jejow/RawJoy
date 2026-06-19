// Products Module
import { db } from './firebase-config.js';
import { 
  collection, doc, getDoc, getDocs, query, where, orderBy, limit, startAfter,
  addDoc, updateDoc, deleteDoc, serverTimestamp 
} from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';

const productsRef = collection(db, 'products');
const categoriesRef = collection(db, 'categories');

// Get all products
export async function getAllProducts(options = {}) {
  try {
    let q = productsRef;
    const constraints = [];
    
    if (options.category) {
      constraints.push(where('category', '==', options.category));
    }
    if (options.sortBy === 'price-asc') {
      constraints.push(orderBy('price', 'asc'));
    } else if (options.sortBy === 'price-desc') {
      constraints.push(orderBy('price', 'desc'));
    } else if (options.sortBy === 'name') {
      constraints.push(orderBy('name', 'asc'));
    } else {
      constraints.push(orderBy('createdAt', 'desc'));
    }
    
    if (options.limit) {
      constraints.push(limit(options.limit));
    }
    
    q = query(productsRef, ...constraints);
    const snapshot = await getDocs(q);
    
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    console.error('Error getting products:', error);
    return [];
  }
}

// Get single product by slug
export async function getProductBySlug(slug) {
  try {
    const q = query(productsRef, where('slug', '==', slug));
    const snapshot = await getDocs(q);
    if (!snapshot.empty) {
      const doc = snapshot.docs[0];
      return { id: doc.id, ...doc.data() };
    }
    return null;
  } catch (error) {
    console.error('Error getting product:', error);
    return null;
  }
}

// Get product by ID
export async function getProductById(id) {
  try {
    const docSnap = await getDoc(doc(db, 'products', id));
    if (docSnap.exists()) {
      return { id: docSnap.id, ...docSnap.data() };
    }
    return null;
  } catch (error) {
    console.error('Error getting product:', error);
    return null;
  }
}

// Search products
export async function searchProducts(searchTerm) {
  try {
    const snapshot = await getDocs(productsRef);
    const term = searchTerm.toLowerCase();
    return snapshot.docs
      .map(doc => ({ id: doc.id, ...doc.data() }))
      .filter(p => 
        p.name.toLowerCase().includes(term) || 
        p.description.toLowerCase().includes(term) ||
        p.category.toLowerCase().includes(term)
      );
  } catch (error) {
    console.error('Error searching:', error);
    return [];
  }
}

// Get all categories
export async function getCategories() {
  try {
    const snapshot = await getDocs(categoriesRef);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    console.error('Error getting categories:', error);
    return [];
  }
}

// Admin: Add product
export async function addProduct(productData) {
  try {
    const docRef = await addDoc(productsRef, {
      ...productData,
      createdAt: serverTimestamp(),
      rating: 0,
      reviewCount: 0
    });
    return { success: true, id: docRef.id };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Admin: Update product
export async function updateProduct(id, data) {
  try {
    await updateDoc(doc(db, 'products', id), { ...data, updatedAt: serverTimestamp() });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Admin: Delete product
export async function deleteProduct(id) {
  try {
    await deleteDoc(doc(db, 'products', id));
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
