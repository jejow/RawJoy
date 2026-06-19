<?php
// Orders API Controller

require_once __DIR__ . '/db.php';

$action = $_GET['action'] ?? '';

// Helper to decode JSON input payloads
function getRequestData() {
    $raw = file_get_contents('php://input');
    $decoded = json_decode($raw, true);
    return is_array($decoded) ? $decoded : $_POST;
}

$userId = $_SESSION['user']['uid'] ?? null;
$sessionId = getSessionId();

switch ($action) {
    case 'create':
        createOrder($pdo, $userId, $sessionId);
        break;
        
    case 'user_orders':
        getUserOrders($pdo, $userId);
        break;
        
    default:
        sendResponse(['success' => false, 'error' => 'Invalid orders action.'], 400);
}

/**
 * Place a new order
 */
function createOrder($pdo, $userId, $sessionId) {
    $data = getRequestData();
    
    $items = $data['items'] ?? [];
    $subtotal = floatval($data['subtotal'] ?? 0);
    $shipping = floatval($data['shipping'] ?? 0);
    $total = floatval($data['total'] ?? 0);
    $shippingAddress = $data['shippingAddress'] ?? $data['address'] ?? '';
    $paymentMethod = $data['paymentMethod'] ?? 'COD';
    $notes = $data['notes'] ?? '';
    
    // Fallback names/emails if not logged in
    $userName = $_SESSION['user']['displayName'] ?? $data['userName'] ?? $data['name'] ?? 'Guest';
    $userEmail = $_SESSION['user']['email'] ?? $data['userEmail'] ?? $data['email'] ?? 'guest@rawjoy.com';
    
    if (empty($items)) {
        sendResponse(['success' => false, 'error' => 'Keranjang belanja kosong.'], 400);
    }
    
    if (empty($shippingAddress)) {
        sendResponse(['success' => false, 'error' => 'Alamat pengiriman wajib diisi.'], 400);
    }
    
    try {
        $pdo->beginTransaction();
        
        // Generate string ID like 'local_1718000000000' to maintain backward compatibility
        $orderId = 'local_' . round(microtime(true) * 1000);
        
        // Insert order header
        $stmt = $pdo->prepare("
            INSERT INTO orders (
                id, user_id, user_name, user_email, subtotal, shipping, 
                total, shipping_address, payment_method, status, notes
            ) VALUES (
                ?, ?, ?, ?, ?, ?, 
                ?, ?, ?, 'pending', ?
            )
        ");
        
        $stmt->execute([
            $orderId, $userId, $userName, $userEmail, $subtotal, $shipping,
            $total, $shippingAddress, $paymentMethod, $notes
        ]);
        
        // Insert order items
        $itemStmt = $pdo->prepare("
            INSERT INTO order_items (
                order_id, product_id, name, price, quantity, image, variant
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?
            )
        ");
        
        foreach ($items as $item) {
            $prodId = $item['productId'] ?? $item['product_id'] ?? '';
            $name = $item['name'] ?? 'Product';
            $price = floatval($item['price'] ?? 0);
            $quantity = intval($item['quantity'] ?? 1);
            $image = $item['image'] ?? '';
            $variant = $item['variant'] ?? null;
            
            $itemStmt->execute([
                $orderId, $prodId, $name, $price, $quantity, $image, $variant
            ]);
        }
        
        // Clear cart for this session/user
        if ($userId) {
            $clearStmt = $pdo->prepare("DELETE FROM cart_items WHERE user_id = ?");
            $clearStmt->execute([$userId]);
        } else {
            $clearStmt = $pdo->prepare("DELETE FROM cart_items WHERE session_id = ? AND user_id IS NULL");
            $clearStmt->execute([$sessionId]);
        }
        
        $pdo->commit();
        
        sendResponse(['success' => true, 'orderId' => $orderId]);
    } catch (Exception $e) {
        if ($pdo->inTransaction()) {
            $pdo->rollBack();
        }
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Retrieve current user's order history
 */
function getUserOrders($pdo, $userId) {
    if (!$userId) {
        sendResponse([]); // Return empty list if not logged in
    }
    
    try {
        // Fetch order headers
        $stmt = $pdo->prepare("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC");
        $stmt->execute([$userId]);
        $orders = $stmt->fetchAll();
        
        $formattedOrders = [];
        
        foreach ($orders as $order) {
            // Fetch items for this order
            $itemStmt = $pdo->prepare("SELECT * FROM order_items WHERE order_id = ?");
            $itemStmt->execute([$order['id']]);
            $items = $itemStmt->fetchAll();
            
            $formattedItems = [];
            foreach ($items as $item) {
                $formattedItems[] = [
                    'productId' => $item['product_id'],
                    'name' => $item['name'],
                    'price' => floatval($item['price']),
                    'quantity' => intval($item['quantity']),
                    'image' => $item['image'],
                    'variant' => $item['variant']
                ];
            }
            
            $formattedOrders[] = [
                'id' => $order['id'],
                'userId' => $order['user_id'],
                'userName' => $order['user_name'],
                'userEmail' => $order['user_email'],
                'items' => $formattedItems,
                'subtotal' => floatval($order['subtotal']),
                'shipping' => floatval($order['shipping']),
                'total' => floatval($order['total']),
                'shippingAddress' => $order['shipping_address'],
                'paymentMethod' => $order['payment_method'],
                'status' => $order['status'],
                'notes' => $order['notes'],
                'createdAt' => $order['created_at']
            ];
        }
        
        sendResponse($formattedOrders);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}
?>
