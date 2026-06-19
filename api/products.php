<?php
// Products API Controller

require_once __DIR__ . '/db.php';

$action = $_GET['action'] ?? 'all';

switch ($action) {
    case 'all':
        getAllProducts($pdo);
        break;
        
    case 'by_slug':
        getProductBySlug($pdo);
        break;
        
    case 'by_id':
        getProductById($pdo);
        break;
        
    case 'search':
        searchProducts($pdo);
        break;
        
    default:
        sendResponse(['success' => false, 'error' => 'Invalid action.'], 400);
}

/**
 * Fetch all products, optionally filtered by category
 */
function getAllProducts($pdo) {
    try {
        $category = $_GET['category'] ?? null;
        
        if ($category) {
            $stmt = $pdo->prepare("SELECT * FROM products WHERE LOWER(category) = LOWER(?)");
            $stmt->execute([$category]);
        } else {
            $stmt = $pdo->query("SELECT * FROM products");
        }
        
        $products = $stmt->fetchAll();
        $products = attachVariantsAndImages($pdo, $products);
        
        sendResponse($products);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Fetch a single product by its slug
 */
function getProductBySlug($pdo) {
    $slug = $_GET['slug'] ?? '';
    if (empty($slug)) {
        sendResponse(['success' => false, 'error' => 'Slug is required.'], 400);
    }
    
    try {
        $stmt = $pdo->prepare("SELECT * FROM products WHERE slug = ?");
        $stmt->execute([$slug]);
        $product = $stmt->fetch();
        
        if (!$product) {
            sendResponse(null); // Return null to match frontend expectations
        }
        
        $products = attachVariantsAndImages($pdo, [$product]);
        sendResponse($products[0]);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Fetch a single product by its ID
 */
function getProductById($pdo) {
    $id = $_GET['id'] ?? '';
    if (empty($id)) {
        sendResponse(['success' => false, 'error' => 'ID is required.'], 400);
    }
    
    try {
        $stmt = $pdo->prepare("SELECT * FROM products WHERE id = ?");
        $stmt->execute([$id]);
        $product = $stmt->fetch();
        
        if (!$product) {
            sendResponse(null);
        }
        
        $products = attachVariantsAndImages($pdo, [$product]);
        sendResponse($products[0]);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Wildcard search on products
 */
function searchProducts($pdo) {
    $term = $_GET['term'] ?? '';
    if (empty($term)) {
        sendResponse([]);
    }
    
    try {
        $query = "%" . strtolower($term) . "%";
        $stmt = $pdo->prepare("
            SELECT * FROM products 
            WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ? OR LOWER(category) LIKE ?
        ");
        $stmt->execute([$query, $query, $query]);
        $products = $stmt->fetchAll();
        $products = attachVariantsAndImages($pdo, $products);
        
        sendResponse($products);
    } catch (Exception $e) {
        sendResponse(['success' => false, 'error' => $e->getMessage()], 500);
    }
}

/**
 * Helper to fetch variants and decode images for a list of products
 */
function attachVariantsAndImages($pdo, $products) {
    if (empty($products)) return [];
    
    // Fetch all variants in one query to optimize
    $productIds = array_column($products, 'id');
    $placeholders = implode(',', array_fill(0, count($productIds), '?'));
    
    $vStmt = $pdo->prepare("SELECT * FROM product_variants WHERE product_id IN ($placeholders)");
    $vStmt->execute($productIds);
    $allVariants = $vStmt->fetchAll();
    
    // Group variants by product_id
    $variantsByProduct = [];
    foreach ($allVariants as $v) {
        $variantsByProduct[$v['product_id']][] = [
            'name' => $v['name'],
            'price' => floatval($v['price']),
            'compareAtPrice' => $v['compare_at_price'] ? floatval($v['compare_at_price']) : null
        ];
    }
    
    // Map database properties back to original Shopify format
    $formatted = [];
    foreach ($products as $p) {
        $id = $p['id'];
        
        // Decode JSON array of images
        $images = json_decode($p['images'] ?? '[]', true);
        if (empty($images)) {
            $images = [$p['main_image']];
        }
        
        $formatted[] = [
            'id' => $p['id'],
            'name' => $p['name'],
            'slug' => $p['slug'],
            'price' => floatval($p['price']),
            'description' => $p['description'],
            'category' => $p['category'],
            'vendor' => $p['vendor'],
            'images' => $images,
            'mainImage' => $p['main_image'],
            'variants' => $variantsByProduct[$id] ?? [],
            'weight' => floatval($p['weight']),
            'stock' => intval($p['stock']),
            'rating' => floatval($p['rating']),
            'reviewCount' => intval($p['review_count']),
            'compareAtPrice' => $p['compare_at_price'] ? floatval($p['compare_at_price']) : null
        ];
    }
    
    return $formatted;
}
?>
