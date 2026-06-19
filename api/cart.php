<?php
// Shopping Cart API Controller

require_once __DIR__ . '/db.php';

$action = $_GET['action'] ?? '';

// Helper to decode JSON input payloads
function getRequestData() {
    $raw = file_get_contents('php://input');
    $decoded = json_decode($raw, true);
    return is_array($decoded) ? $decoded : $_POST;
}

// Determine query condition based on user login state
$userId = $_SESSION['user']['uid'] ?? null;
$sessionId = getSessionId();

switch ($action) {
    case 'get':
        getCart($pdo, $userId, $sessionId);
        break;
        
    case 'add':
        addToCart($pdo, $userId, $sessionId);
        break;
        
    case 'update':
        updateCart($pdo, $userId, $sessionId);
        break;
        
    case 'clear':
        clearCart($pdo, $userId, $sessionId);
        break;
        
    default:
        sendResponse(['success' => false, 'error' => 'Invalid cart action.'], 400);
}

/**
 * Merge guest cart items into user cart when user logs in
 */
function mergeCart($pdo, $userId, $sessionId) {
    try {
        // Find guest items
        $stmt = $pdo->prepare("SELECT * FROM cart_items WHERE session_id = ? AND user_id IS NULL");
        $stmt->execute([$sessionId]);
        $guestItems = $stmt->fetchAll();
        
        if (empty($guestItems)) return;
        
        foreach ($guestItems as $guestItem) {
            // Check if user already has this item
            $stmt = $pdo->prepare("
                SELECT id, quantity FROM cart_items 
                WHERE user_id = ? AND product_id = ? AND (variant = ? OR (variant IS NULL AND ? IS NULL))
            ");
            $stmt->execute([$userId, $guestItem['product_id'], $guestItem['variant'], $guestItem['variant']]);
            $userItem = $stmt->fetch();
            
            if ($userItem) {
                // Update quantity and delete guest item
                $newQty = $userItem['quantity'] + $guestItem['quantity'];
                $stmt = $pdo->prepare("UPDATE cart_items SET quantity = ? WHERE id = ?");
                $stmt->execute([$newQty, $userItem['id']]);
                
                $stmt = $pdo->prepare("DELETE FROM cart_items WHERE id = ?");
                $stmt->execute([$guestItem['id']]);
            } else {
                // Update guest item to belong to user
                $stmt = $pdo->prepare("UPDATE cart_items SET user_id = ?, session_id = ? WHERE id = ?");
                $stmt->execute([$userId, $sessionId, $guestItem['id']]);
            }
        }
    } catch (Exception $e) {
        // Log error but don't fail response
        error_log("Cart merge failed: " . $e->getMessage());
    }
}

/**
 * Fetch cart items
 */
function getCart($pdo, $userId, $sessionId) {
    try {
        if ($userId) {
            // Automatically merge any guest items first
            mergeCart($pdo, $userId, $sessionId);
            
            $stmt = $pdo->prepare("
                SELECT ci.id AS item_id, ci.product_id AS productId, ci.variant, ci.quantity, 
                       p.name, p.slug, p.main_image AS image, p.price AS base_price
                FROM cart_items ci
                JOIN products p ON ci.product_id = p.id
                WHERE ci.user_id = ?
            ");
            $stmt->execute([$userId]);
        } else {
            $stmt = $pdo->prepare("
                SELECT ci.id AS item_id, ci.product_id AS productId, ci.variant, ci.quantity, 
                       p.name, p.slug, p.main_image AS image, p.price AS base_price
                FROM cart_items ci
                JOIN products p ON ci.product_id = p.id
                WHERE ci.session_id = ? AND ci.user_id IS NULL
            ");
            $stmt->execute([$sessionId]);
        }
        
        $dbItems = $stmt->fetchAll();
        $formattedItems = [];
        $total = 0;
        
        foreach ($dbItems as $item) {
            // Find variant price if variant exists
            $price = floatval($item['base_price']);
            if ($item['variant']) {
                $vStmt = $pdo->prepare("SELECT price FROM product_variants WHERE product_id = ? AND name = ?");
                $vStmt->execute([$item['productId'], $item['variant']]);
                $vPrice = $vStmt->fetchColumn();
                if ($vPrice !== false) {
                    $price = floatval($vPrice);
                }
            }
            
            $qty = intval($item['quantity']);
            $itemTotal = $price * $qty;
            $total += $itemTotal;
            
            $formattedItems[] = [
                'productId' => $item['productId'],
                'name' => $item['name'],
                'price' => $price,
                'quantity' => $qty,
                'image' => $item['image'],
                'variant' => $item['variant'],
                'slug' => $item['slug']
            ];
        }
        
        sendResponse([
            'items' => $formattedItems,
            'total' => round($total, 2)
        ]);
        
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Add item to cart
 */
function addToCart($pdo, $userId, $sessionId) {
    $data = getRequestData();
    $productId = $data['product_id'] ?? $data['productId'] ?? '';
    $quantity = intval($data['quantity'] ?? 1);
    $variant = $data['variant'] ?? null;
    
    if (empty($productId)) {
        sendResponse(['success' => false, 'error' => 'Product ID is required.'], 400);
    }
    
    try {
        // Verify product exists
        $stmt = $pdo->prepare("SELECT id FROM products WHERE id = ?");
        $stmt->execute([$productId]);
        if (!$stmt->fetch()) {
            sendResponse(['success' => false, 'error' => 'Product not found.'], 404);
        }
        
        // Check if item already exists in cart
        if ($userId) {
            $stmt = $pdo->prepare("
                SELECT id, quantity FROM cart_items 
                WHERE user_id = ? AND product_id = ? AND (variant = ? OR (variant IS NULL AND ? IS NULL))
            ");
            $stmt->execute([$userId, $productId, $variant, $variant]);
        } else {
            $stmt = $pdo->prepare("
                SELECT id, quantity FROM cart_items 
                WHERE session_id = ? AND user_id IS NULL AND product_id = ? AND (variant = ? OR (variant IS NULL AND ? IS NULL))
            ");
            $stmt->execute([$sessionId, $productId, $variant, $variant]);
        }
        
        $existing = $stmt->fetch();
        
        if ($existing) {
            $newQty = $existing['quantity'] + $quantity;
            $stmt = $pdo->prepare("UPDATE cart_items SET quantity = ? WHERE id = ?");
            $stmt->execute([$newQty, $existing['id']]);
        } else {
            $stmt = $pdo->prepare("
                INSERT INTO cart_items (user_id, session_id, product_id, variant, quantity) 
                VALUES (?, ?, ?, ?, ?)
            ");
            $stmt->execute([$userId, $sessionId, $productId, $variant, $quantity]);
        }
        
        // Return total item count
        if ($userId) {
            $countStmt = $pdo->prepare("SELECT SUM(quantity) FROM cart_items WHERE user_id = ?");
            $countStmt->execute([$userId]);
        } else {
            $countStmt = $pdo->prepare("SELECT SUM(quantity) FROM cart_items WHERE session_id = ? AND user_id IS NULL");
            $countStmt->execute([$sessionId]);
        }
        $totalItems = intval($countStmt->fetchColumn());
        
        sendResponse(['success' => true, 'itemCount' => $totalItems]);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Update cart item quantity
 */
function updateCart($pdo, $userId, $sessionId) {
    $data = getRequestData();
    $productId = $data['product_id'] ?? $data['productId'] ?? '';
    $quantity = intval($data['quantity'] ?? 0);
    $variant = $data['variant'] ?? null;
    
    if (empty($productId)) {
        sendResponse(['success' => false, 'error' => 'Product ID is required.'], 400);
    }
    
    try {
        if ($userId) {
            if ($quantity <= 0) {
                $stmt = $pdo->prepare("
                    DELETE FROM cart_items 
                    WHERE user_id = ? AND product_id = ? AND (variant = ? OR (variant IS NULL AND ? IS NULL))
                ");
                $stmt->execute([$userId, $productId, $variant, $variant]);
            } else {
                // Check if exists
                $stmt = $pdo->prepare("
                    SELECT id FROM cart_items 
                    WHERE user_id = ? AND product_id = ? AND (variant = ? OR (variant IS NULL AND ? IS NULL))
                ");
                $stmt->execute([$userId, $productId, $variant, $variant]);
                $item = $stmt->fetch();
                
                if ($item) {
                    $stmt = $pdo->prepare("UPDATE cart_items SET quantity = ? WHERE id = ?");
                    $stmt->execute([$quantity, $item['id']]);
                } else {
                    $stmt = $pdo->prepare("
                        INSERT INTO cart_items (user_id, session_id, product_id, variant, quantity) 
                        VALUES (?, ?, ?, ?, ?)
                    ");
                    $stmt->execute([$userId, $sessionId, $productId, $variant, $quantity]);
                }
            }
        } else {
            if ($quantity <= 0) {
                $stmt = $pdo->prepare("
                    DELETE FROM cart_items 
                    WHERE session_id = ? AND user_id IS NULL AND product_id = ? AND (variant = ? OR (variant IS NULL AND ? IS NULL))
                ");
                $stmt->execute([$sessionId, $productId, $variant, $variant]);
            } else {
                $stmt = $pdo->prepare("
                    SELECT id FROM cart_items 
                    WHERE session_id = ? AND user_id IS NULL AND product_id = ? AND (variant = ? OR (variant IS NULL AND ? IS NULL))
                ");
                $stmt->execute([$sessionId, $productId, $variant, $variant]);
                $item = $stmt->fetch();
                
                if ($item) {
                    $stmt = $pdo->prepare("UPDATE cart_items SET quantity = ? WHERE id = ?");
                    $stmt->execute([$quantity, $item['id']]);
                } else {
                    $stmt = $pdo->prepare("
                        INSERT INTO cart_items (user_id, session_id, product_id, variant, quantity) 
                        VALUES (NULL, ?, ?, ?, ?)
                    ");
                    $stmt->execute([$sessionId, $productId, $variant, $quantity]);
                }
            }
        }
        
        sendResponse(['success' => true]);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Clear all cart items
 */
function clearCart($pdo, $userId, $sessionId) {
    try {
        if ($userId) {
            $stmt = $pdo->prepare("DELETE FROM cart_items WHERE user_id = ?");
            $stmt->execute([$userId]);
        } else {
            $stmt = $pdo->prepare("DELETE FROM cart_items WHERE session_id = ? AND user_id IS NULL");
            $stmt->execute([$sessionId]);
        }
        sendResponse(['success' => true]);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}
?>
