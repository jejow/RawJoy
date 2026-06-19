// Orders Module
import { db, auth } from './firebase-config.js';
import { 
  collection, doc, addDoc, getDoc, getDocs, updateDoc, query, where, orderBy, serverTimestamp 
} from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';
import { clearCart } from './cart.js';

const ordersRef = collection(db, 'orders');

// Create new order
export async function createOrder(orderData) {
  const user = auth.currentUser;
  if (!user) return { success: false, error: 'Silakan login.' };
  
  try {
    const order = {
      userId: user.uid,
      userName: user.displayName || 'User',
      userEmail: user.email,
      items: orderData.items,
      subtotal: orderData.subtotal,
      shipping: orderData.shipping || 0,
      total: orderData.total,
      shippingAddress: orderData.shippingAddress,
      paymentMethod: orderData.paymentMethod || 'COD',
      status: 'pending',
      notes: orderData.notes || '',
      createdAt: serverTimestamp()
    };
    
    const docRef = await addDoc(ordersRef, order);
    
    // Clear cart after order
    await clearCart();
    
    return { success: true, orderId: docRef.id };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Get user's orders
export async function getUserOrders() {
  const user = auth.currentUser;
  if (!user) return [];
  
  try {
    const q = query(ordersRef, where('userId', '==', user.uid), orderBy('createdAt', 'desc'));
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    console.error('Error getting orders:', error);
    return [];
  }
}

// Get order by ID
export async function getOrderById(orderId) {
  try {
    const docSnap = await getDoc(doc(db, 'orders', orderId));
    if (docSnap.exists()) {
      return { id: docSnap.id, ...docSnap.data() };
    }
    return null;
  } catch (error) {
    console.error('Error getting order:', error);
    return null;
  }
}

// Admin: Get all orders
export async function getAllOrders(statusFilter = null) {
  try {
    let q;
    if (statusFilter) {
      q = query(ordersRef, where('status', '==', statusFilter), orderBy('createdAt', 'desc'));
    } else {
      q = query(ordersRef, orderBy('createdAt', 'desc'));
    }
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    console.error('Error getting orders:', error);
    return [];
  }
}

// Admin: Update order status
export async function updateOrderStatus(orderId, status) {
  try {
    await updateDoc(doc(db, 'orders', orderId), { 
      status, 
      updatedAt: serverTimestamp() 
    });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Order statuses
export const ORDER_STATUSES = {
  pending: { label: 'Pending', color: '#f59e0b' },
  processing: { label: 'Processing', color: '#3b82f6' },
  shipped: { label: 'Shipped', color: '#8b5cf6' },
  delivered: { label: 'Delivered', color: '#10b981' },
  cancelled: { label: 'Cancelled', color: '#ef4444' }
};
