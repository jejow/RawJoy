// Authentication UI Handler (Dynamic Modals & Header Controls)

import { DB } from './db-bridge.js';

// Helper to determine relative path prefix to the project root
function getDepthPrefix() {
  const pathParts = window.location.pathname.split('/').filter(Boolean);
  
  const rootIndicators = ['products', 'collections', 'pages', 'blogs', 'policies', 'cart', 'search', 'contact', 'css', 'js', 'images', 'firebase', 'data', 'api'];
  let rootIndex = -1;
  for (let i = 0; i < pathParts.length; i++) {
    if (rootIndicators.indexOf(pathParts[i].toLowerCase()) !== -1) {
      rootIndex = i;
      break;
    }
  }
  
  let depth = 0;
  if (rootIndex !== -1) {
    let remaining = pathParts.slice(rootIndex);
    if (remaining.length > 0) {
      let last = remaining[remaining.length - 1];
      if (last.includes('.')) {
        remaining.pop();
      }
    }
    depth = remaining.length;
  } else {
    let index = pathParts.findIndex(p => p.toLowerCase() === 'rawjoy' || p.toLowerCase() === 'op' || p.toLowerCase() === 'homepage');
    if (index !== -1) {
      let remaining = pathParts.slice(index + 1);
      if (remaining.length > 0) {
        let last = remaining[remaining.length - 1];
        if (last.includes('.')) {
          remaining.pop();
        }
      }
      depth = remaining.length;
    } else {
      let remaining = [...pathParts];
      if (remaining.length > 0) {
        let last = remaining[remaining.length - 1];
        if (last.includes('.')) {
          remaining.pop();
        }
      }
      depth = remaining.length;
    }
  }
  return depth > 0 ? '../'.repeat(depth) : './';
}

// Append CSS link dynamically if not already loaded
if (!document.querySelector('link[href*="db-ui.css"]')) {
  const cssLink = document.createElement('link');
  cssLink.rel = 'stylesheet';
  const prefix = getDepthPrefix();
  cssLink.href = `${prefix}css/db-ui.css`;
  document.head.appendChild(cssLink);
}

// Global modal state
let currentMode = 'login'; // 'login' or 'register'

// Create modal DOM structure dynamically
function createModal() {
  if (document.getElementById('auth-modal')) return;

  const modalDiv = document.createElement('div');
  modalDiv.id = 'auth-modal';
  modalDiv.className = 'db-modal';
  modalDiv.innerHTML = `
    <div class="db-modal-content">
      <button class="db-modal-close" id="auth-modal-close">&times;</button>
      
      <div class="auth-tabs">
        <button type="button" class="auth-tab active" id="tab-login">Masuk</button>
        <button type="button" class="auth-tab" id="tab-register">Daftar</button>
      </div>

      <h3 class="db-modal-title" id="auth-modal-title">Masuk ke RawJoy</h3>
      
      <form id="auth-form">
        <!-- Register fields (hidden by default) -->
        <div class="db-form-group" id="reg-name-group" style="display: none;">
          <label for="auth-name">Nama Lengkap</label>
          <input type="text" id="auth-name" class="db-form-input" placeholder="Masukkan nama Anda">
        </div>
        
        <div class="db-form-group" id="reg-phone-group" style="display: none;">
          <label for="auth-phone">Nomor Telepon</label>
          <input type="tel" id="auth-phone" class="db-form-input" placeholder="08xxxxxxxxxx">
        </div>

        <!-- Shared fields -->
        <div class="db-form-group">
          <label for="auth-email">Alamat Email</label>
          <input type="email" id="auth-email" class="db-form-input" required placeholder="name@example.com">
        </div>
        
        <div class="db-form-group">
          <label for="auth-password">Password</label>
          <input type="password" id="auth-password" class="db-form-input" required placeholder="••••••••">
        </div>

        <div class="db-error-msg" id="auth-error" style="display: none;"></div>

        <button type="submit" class="db-btn" id="auth-submit-btn" style="margin-top: 15px;">Masuk</button>
      </form>

      <div class="db-form-footer">
        <span id="auth-footer-text">Belum punya akun?</span>
        <a href="#" class="db-form-link" id="auth-toggle-mode">Daftar Sekarang</a>
      </div>
    </div>
  `;

  document.body.appendChild(modalDiv);

  // Bind close buttons
  document.getElementById('auth-modal-close').addEventListener('click', hideAuthModal);
  modalDiv.addEventListener('click', (e) => {
    if (e.target === modalDiv) hideAuthModal();
  });

  // Bind tabs
  document.getElementById('tab-login').addEventListener('click', () => switchMode('login'));
  document.getElementById('tab-register').addEventListener('click', () => switchMode('register'));

  // Bind toggle mode link
  document.getElementById('auth-toggle-mode').addEventListener('click', (e) => {
    e.preventDefault();
    toggleMode();
  });

  // Bind form submission
  document.getElementById('auth-form').addEventListener('submit', handleFormSubmit);
}

// Switch explicitly to Login or Register mode
function switchMode(mode) {
  if (currentMode === mode) return;
  currentMode = mode;
  
  const title = document.getElementById('auth-modal-title');
  const nameGroup = document.getElementById('reg-name-group');
  const phoneGroup = document.getElementById('reg-phone-group');
  const submitBtn = document.getElementById('auth-submit-btn');
  const footerText = document.getElementById('auth-footer-text');
  const toggleLink = document.getElementById('auth-toggle-mode');
  const errorMsg = document.getElementById('auth-error');
  
  const tabLogin = document.getElementById('tab-login');
  const tabRegister = document.getElementById('tab-register');

  errorMsg.style.display = 'none';

  if (currentMode === 'register') {
    tabLogin.classList.remove('active');
    tabRegister.classList.add('active');
    
    title.textContent = 'Daftar Akun RawJoy';
    nameGroup.style.display = 'block';
    phoneGroup.style.display = 'block';
    document.getElementById('auth-name').required = true;
    submitBtn.textContent = 'Daftar';
    footerText.textContent = 'Sudah punya akun?';
    toggleLink.textContent = 'Masuk';
  } else {
    tabLogin.classList.add('active');
    tabRegister.classList.remove('active');

    title.textContent = 'Masuk ke RawJoy';
    nameGroup.style.display = 'none';
    phoneGroup.style.display = 'none';
    document.getElementById('auth-name').required = false;
    submitBtn.textContent = 'Masuk';
    footerText.textContent = 'Belum punya akun?';
    toggleLink.textContent = 'Daftar Sekarang';
  }
}

// Toggle between modes (helper for bottom text link)
function toggleMode() {
  const nextMode = currentMode === 'login' ? 'register' : 'login';
  switchMode(nextMode);
}

// Show the authentication modal
export function showAuthModal() {
  createModal();
  const modal = document.getElementById('auth-modal');
  modal.classList.add('active');
}

// Hide the authentication modal
export function hideAuthModal() {
  const modal = document.getElementById('auth-modal');
  if (modal) {
    modal.classList.remove('active');
    // Clear inputs
    document.getElementById('auth-form').reset();
    document.getElementById('auth-error').style.display = 'none';
  }
}

// Handle Form Submit
async function handleFormSubmit(e) {
  e.preventDefault();
  
  const email = document.getElementById('auth-email').value;
  const password = document.getElementById('auth-password').value;
  const errorMsg = document.getElementById('auth-error');
  const submitBtn = document.getElementById('auth-submit-btn');

  errorMsg.style.display = 'none';
  submitBtn.disabled = true;
  submitBtn.textContent = 'Memproses...';

  try {
    if (currentMode === 'login') {
      const res = await DB.auth.login(email, password);
      if (res.success) {
        hideAuthModal();
        updateHeaderAccount();
        // Refresh page or trigger callback if defined
        window.location.reload();
      } else {
        errorMsg.textContent = res.error || 'Login gagal.';
        errorMsg.style.display = 'block';
      }
    } else {
      const name = document.getElementById('auth-name').value;
      const phone = document.getElementById('auth-phone').value;
      const res = await DB.auth.register(email, password, name, phone);
      if (res.success) {
        hideAuthModal();
        updateHeaderAccount();
        window.location.reload();
      } else {
        errorMsg.textContent = res.error || 'Pendaftaran gagal.';
        errorMsg.style.display = 'block';
      }
    }
  } catch (err) {
    errorMsg.textContent = 'Terjadi kesalahan sistem.';
    errorMsg.style.display = 'block';
    console.error(err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = currentMode === 'login' ? 'Masuk' : 'Daftar';
  }
}

// Update the header/account UI depending on auth status
export function updateHeaderAccount() {
  const user = DB.auth.getCurrentUser();
  const accountBtns = document.querySelectorAll('.header-account-btn, .account-trigger');

  accountBtns.forEach(btn => {
    // Unbind existing listeners to avoid multiple fires
    const newBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn, btn);
    
    if (user) {
      // Logged in: redirect to account page
      newBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const prefix = getDepthPrefix();
        window.location.href = `${prefix}pages/account/index.html`;
      });
      // Optionally update tooltip/label
      newBtn.setAttribute('title', `Akun Saya (${user.displayName || user.email})`);
    } else {
      // Logged out: open modal
      newBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        showAuthModal();
      });
      newBtn.setAttribute('title', 'Masuk / Daftar');
    }
  });
}

// Auto init on page load - use a safe, non-redirecting approach and intercept links
function initAuthUI() {
  // Use onAuthChange which handles async Firebase auth state properly
  // This prevents the "redirect to homepage" bug where getCurrentUser() returns null
  // before Firebase has finished initializing
  DB.auth.onAuthChange((user) => {
    updateHeaderAccount();
  });

  // Intercept all login/register clicks globally
  document.addEventListener('click', (e) => {
    const anchor = e.target.closest('a');
    if (!anchor) return;
    
    const href = anchor.getAttribute('href') || '';
    const isLoginLink = href.includes('/account/login') || 
                        href.includes('pebble-rawjoy.myshopify.com/account/login') || 
                        href.includes('customer_authentication/redirect') || 
                        href.includes('/account?login');
    const isRegisterLink = href.includes('/account/register') || 
                           href.includes('pebble-rawjoy.myshopify.com/account/register');
    
    if (isLoginLink || isRegisterLink) {
      e.preventDefault();
      e.stopPropagation();
      
      const user = DB.auth.getCurrentUser();
      if (user) {
        const prefix = getDepthPrefix();
        window.location.href = `${prefix}pages/account/index.html`;
      } else {
        if (isRegisterLink) {
          showAuthModal();
          switchMode('register');
        } else {
          showAuthModal();
          switchMode('login');
        }
      }
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAuthUI);
} else {
  initAuthUI();
}

