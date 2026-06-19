<?php
// Authentication API Controller

require_once __DIR__ . '/db.php';

$action = $_GET['action'] ?? '';

// Helper to decode JSON input payloads
function getRequestData() {
    $raw = file_get_contents('php://input');
    $decoded = json_decode($raw, true);
    return is_array($decoded) ? $decoded : $_POST;
}

switch ($action) {
    case 'register':
        registerUser($pdo);
        break;
        
    case 'login':
        loginUser($pdo);
        break;
        
    case 'logout':
        logoutUser();
        break;
        
    case 'get_profile':
        getUserProfile($pdo);
        break;
        
    case 'update_profile':
        updateUserProfile($pdo);
        break;
        
    case 'current_user':
        getCurrentUser();
        break;
        
    default:
        sendResponse(['success' => false, 'error' => 'Invalid auth action.'], 400);
}

/**
 * Register a new user
 */
function registerUser($pdo) {
    $data = getRequestData();
    $email = $data['email'] ?? '';
    $password = $data['password'] ?? '';
    $name = $data['name'] ?? '';
    $phone = $data['phone'] ?? '';
    
    if (empty($email) || empty($password) || empty($name)) {
        sendResponse(['success' => false, 'error' => 'Nama, Email, dan Password wajib diisi.'], 400);
    }
    
    try {
        // Check if email already registered
        $stmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
        $stmt->execute([$email]);
        if ($stmt->fetch()) {
            sendResponse(['success' => false, 'error' => 'Email sudah terdaftar.'], 400);
        }
        
        // Hash password
        $hashedPassword = password_hash($password, PASSWORD_BCRYPT);
        
        // Insert new user
        $stmt = $pdo->prepare("INSERT INTO users (name, email, password, phone) VALUES (?, ?, ?, ?)");
        $stmt->execute([$name, $email, $hashedPassword, $phone]);
        $userId = $pdo->lastInsertId();
        
        // Prepare user session object
        $userObj = [
            'uid' => $userId,
            'email' => $email,
            'displayName' => $name
        ];
        
        $_SESSION['user'] = $userObj;
        
        sendResponse(['success' => true, 'user' => $userObj]);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Authenticate user credentials
 */
function loginUser($pdo) {
    $data = getRequestData();
    $email = $data['email'] ?? '';
    $password = $data['password'] ?? '';
    
    if (empty($email) || empty($password)) {
        sendResponse(['success' => false, 'error' => 'Email dan Password wajib diisi.'], 400);
    }
    
    try {
        $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();
        
        if (!$user || !password_verify($password, $user['password'])) {
            sendResponse(['success' => false, 'error' => 'Email atau Password salah.'], 401);
        }
        
        $userObj = [
            'uid' => $user['id'],
            'email' => $user['email'],
            'displayName' => $user['name']
        ];
        
        $_SESSION['user'] = $userObj;
        
        // If there was a guest session cart, we can optionally merge it here
        // (Simplified: cart is retrieved by session ID or user ID)
        
        sendResponse(['success' => true, 'user' => $userObj]);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Log out user
 */
function logoutUser() {
    unset($_SESSION['user']);
    sendResponse(['success' => true]);
}

/**
 * Get current session user
 */
function getCurrentUser() {
    if (isset($_SESSION['user'])) {
        sendResponse($_SESSION['user']);
    } else {
        sendResponse(null);
    }
}

/**
 * Retrieve detailed profile
 */
function getUserProfile($pdo) {
    $uid = $_GET['uid'] ?? ($_SESSION['user']['uid'] ?? null);
    
    if (!$uid) {
        sendResponse(['success' => false, 'error' => 'Not authenticated.'], 401);
    }
    
    try {
        $stmt = $pdo->prepare("SELECT name, email, phone, address FROM users WHERE id = ?");
        $stmt->execute([$uid]);
        $profile = $stmt->fetch();
        
        if (!$profile) {
            sendResponse(['success' => false, 'error' => 'Profil tidak ditemukan.'], 404);
        }
        
        sendResponse(['success' => true, 'data' => $profile]);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Update profile attributes
 */
function updateUserProfile($pdo) {
    $uid = $_GET['uid'] ?? ($_SESSION['user']['uid'] ?? null);
    if (!$uid) {
        sendResponse(['success' => false, 'error' => 'Not authenticated.'], 401);
    }
    
    $data = getRequestData();
    $name = $data['name'] ?? '';
    $phone = $data['phone'] ?? '';
    $address = $data['address'] ?? '';
    
    if (empty($name)) {
        sendResponse(['success' => false, 'error' => 'Nama tidak boleh kosong.'], 400);
    }
    
    try {
        $stmt = $pdo->prepare("UPDATE users SET name = ?, phone = ?, address = ? WHERE id = ?");
        $stmt->execute([$name, $phone, $address, $uid]);
        
        // Update display name in session if this is the current user
        if (isset($_SESSION['user']) && $_SESSION['user']['uid'] == $uid) {
            $_SESSION['user']['displayName'] = $name;
        }
        
        sendResponse(['success' => true]);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}
?>
