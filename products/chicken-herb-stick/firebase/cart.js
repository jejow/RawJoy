// Cart Module
import { db, auth } from './firebase-config.js';
import { 
  doc, getDoc, setDoc, updateDoc, deleteDoc, serverTimestamp 
} from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';

// Get cart for current user
export async function getCart() {
  const user = auth.currentUser;
  if (!user) return { items: [], total: 0 };
  
  try {
    const cartDoc = await getDoc(doc(db, 'cart', user.uid));
    if (cartDoc.exists()) {
      const data = cartDoc.data();
      const total = data.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
      return { items: data.items || [], total };
    }
    return { items: [], total: 0 };
  } catch (error) {
    console.error('Error getting cart:', error);
    return { items: [], total: 0 };
  }
}

// Add item to cart
export async function addToCart(product, quantity = 1, variant = null) {
  const user = auth.currentUser;
  if (!user) return { success: false, error: 'Silakan login terlebih dahulu.' };
  
  try {
    const cartRef = doc(db, 'cart', user.uid);
    const cartDoc = await getDoc(cartRef);
    let items = [];
    
    if (cartDoc.exists()) {
      items = cartDoc.data().items || [];
    }
    
    // Check if product already in cart
    const existingIndex = items.findIndex(
      item => item.productId === product.id && item.variant === variant
    );
    
    if (existingIndex >= 0) {
      items[existingIndex].quantity += quantity;
    } else {
      items.push({
        productId: product.id,
        name: product.name,
        price: variant ? product.variants.find(v => v.name === variant)?.price || product.price : product.price,
        quantity: quantity,
        image: product.mainImage || product.images?.[0] || '',
        variant: variant,
        slug: product.slug
      });
    }
    
    await setDoc(cartRef, { items, updatedAt: serverTimestamp() });
    return { success: true, itemCount: items.reduce((sum, i) => sum + i.quantity, 0) };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Update cart item quantity
export async function updateCartItem(productId, quantity, variant = null) {
  const user = auth.currentUser;
  if (!user) return { success: false };
  
  try {
    const cartRef = doc(db, 'cart', user.uid);
    const cartDoc = await getDoc(cartRef);
    if (!cartDoc.exists()) return { success: false };
    
    let items = cartDoc.data().items || [];
    const index = items.findIndex(
      item => item.productId === productId && item.variant === variant
    );
    
    if (index >= 0) {
      if (quantity <= 0) {
        items.splice(index, 1);
      } else {
        items[index].quantity = quantity;
      }
    }
    
    await setDoc(cartRef, { items, updatedAt: serverTimestamp() });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Remove item from cart
export async function removeFromCart(productId, variant = null) {
  return updateCartItem(productId, 0, variant);
}

// Clear cart
export async function clearCart() {
  const user = auth.currentUser;
  if (!user) return { success: false };
  
  try {
    await deleteDoc(doc(db, 'cart', user.uid));
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Get cart item count
export async function getCartCount() {
  const cart = await getCart();
  return cart.items.reduce((sum, item) => sum + item.quantity, 0);
}
