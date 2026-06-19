<?php
// Core Database Connection (PDO) & Session Setup

// Start session if not already started
if (session_status() == PHP_SESSION_NONE) {
    // Set session cookie lifetime to 30 days
    ini_set('session.cookie_lifetime', 60 * 60 * 24 * 30);
    ini_set('session.gc_maxlifetime', 60 * 60 * 24 * 30);
    session_start();
}

// CORS headers to prevent local testing issues
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Credentials: true");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, DELETE");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
header("Content-Type: application/json; charset=UTF-8");

// Handle preflight OPTIONS requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Database Credentials (Default: XAMPP / Laragon)
define('DB_HOST', '127.0.0.1');
define('DB_NAME', 'rawjoy_db');
define('DB_USER', 'root');
define('DB_PASS', '');

$pdo = null;

try {
    $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4";
    $options = [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ];
    $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
} catch (PDOException $e) {
    // If database connection fails, send JSON error (except during setup)
    if (basename($_SERVER['PHP_SELF']) !== 'setup_db.php') {
        sendResponse([
            'success' => false,
            'error' => 'Database connection failed: ' . $e->getMessage()
        ], 500);
    }
}

/**
 * Send JSON response and exit
 */
function sendResponse($data, $status = 200) {
    http_response_code($status);
    echo json_encode($data);
    exit();
}

/**
 * Generate or retrieve a persistent guest session ID
 */
function getSessionId() {
    if (!isset($_SESSION['guest_session_id'])) {
        $_SESSION['guest_session_id'] = bin2hex(random_bytes(16));
    }
    return $_SESSION['guest_session_id'];
}
?>
