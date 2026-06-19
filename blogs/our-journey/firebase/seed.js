/**
 * Seed Firestore with product data extracted from HTML.
 * Run this ONCE after setting up Firebase project.
 * 
 * Usage:
 *   1. Update firebase-config.js with your project keys
 *   2. Open seed.html in browser
 *   3. Click "Seed Database" button
 */
import { db } from './firebase-config.js';
import { doc, setDoc, collection, getDocs } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';

export async function seedDatabase(seedData) {
  const results = { products: 0, categories: 0, errors: [] };
  
  // Seed categories
  for (const cat of seedData.categories) {
    try {
      await setDoc(doc(db, 'categories', cat.id), cat);
      results.categories++;
    } catch (e) {
      results.errors.push(`Category ${cat.name}: ${e.message}`);
    }
  }
  
  // Seed products
  for (const product of seedData.products) {
    try {
      await setDoc(doc(db, 'products', product.id), product);
      results.products++;
    } catch (e) {
      results.errors.push(`Product ${product.name}: ${e.message}`);
    }
  }
  
  // Create admin user doc (you need to register this email first via Auth)
  try {
    await setDoc(doc(db, 'users', 'admin'), {
      name: 'Jun',
      email: 'admin@rawjoy.com',
      role: 'admin',
      createdAt: new Date().toISOString()
    });
  } catch (e) {
    results.errors.push(`Admin user: ${e.message}`);
  }
  
  return results;
}

// Check if database is already seeded
export async function isDatabaseSeeded() {
  try {
    const snapshot = await getDocs(collection(db, 'products'));
    return snapshot.size > 0;
  } catch {
    return false;
  }
}
