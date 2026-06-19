<?php
// Database Installer and Seeder Script

// We don't include db.php immediately because the database itself might not exist yet
// We will build a temporary connection to create the database if needed

define('DB_HOST', '127.0.0.1');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'rawjoy_db');

header("Content-Type: application/json; charset=UTF-8");

try {
    // 1. Connect to MySQL Server (without database)
    $dsn = "mysql:host=" . DB_HOST . ";charset=utf8mb4";
    $tempPdo = new PDO($dsn, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);

    // 2. Create database if not exists
    $tempPdo->exec("CREATE DATABASE IF NOT EXISTS " . DB_NAME . " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    
    // 3. Connect to the newly created database
    $pdo = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);

    // 4. Read and execute the SQL schema file
    $schemaPath = __DIR__ . '/setup_db.sql';
    if (!file_exists($schemaPath)) {
        throw new Exception("Schema SQL file 'setup_db.sql' not found.");
    }
    
    $sql = file_get_contents($schemaPath);
    $pdo->exec($sql);
    
    // 5. Seed Products from seed-data.json if tables are empty
    $productsSeeded = 0;
    $variantsSeeded = 0;
    
    // Check if products table is empty
    $stmt = $pdo->query("SELECT COUNT(*) FROM products");
    $productCount = $stmt->fetchColumn();
    
    if ($productCount == 0) {
        $seedDataPath = __DIR__ . '/../js/seed-data.json';
        if (!file_exists($seedDataPath)) {
            throw new Exception("Seed data file 'seed-data.json' not found in js/ folder.");
        }
        
        $jsonContent = file_get_contents($seedDataPath);
        $seedData = json_decode($jsonContent, true);
        
        if (!$seedData || !isset($seedData['products'])) {
            throw new Exception("Invalid seed-data.json format.");
        }
        
        // Disable foreign key checks for clean insert
        $pdo->exec("SET FOREIGN_KEY_CHECKS = 0");
        $pdo->exec("TRUNCATE TABLE product_variants");
        $pdo->exec("TRUNCATE TABLE products");
        $pdo->exec("SET FOREIGN_KEY_CHECKS = 1");
        
        $productStmt = $pdo->prepare("
            INSERT INTO products (
                id, name, slug, price, description, category, vendor, 
                main_image, images, weight, stock, rating, review_count, compare_at_price
            ) VALUES (
                :id, :name, :slug, :price, :description, :category, :vendor, 
                :main_image, :images, :weight, :stock, :rating, :review_count, :compare_at_price
            )
        ");
        
        $variantStmt = $pdo->prepare("
            INSERT INTO product_variants (
                product_id, name, price, compare_at_price
            ) VALUES (
                :product_id, :name, :price, :compare_at_price
            )
        ");
        
        foreach ($seedData['products'] as $p) {
            // Encode images list as JSON string
            $imagesJson = json_encode($p['images'] ?? []);
            
            // Insert product
            $productStmt->execute([
                ':id'               => $p['id'],
                ':name'             => $p['name'],
                ':slug'             => $p['slug'],
                ':price'            => $p['price'] ?? 0,
                ':description'      => $p['description'] ?? '',
                ':category'         => $p['category'] ?? 'General',
                ':vendor'           => $p['vendor'] ?? 'RawJoy',
                ':main_image'       => $p['mainImage'] ?? ($p['images'][0] ?? ''),
                ':images'           => $imagesJson,
                ':weight'           => $p['weight'] ?? 0,
                ':stock'            => $p['stock'] ?? 50,
                ':rating'           => $p['rating'] ?? 0,
                ':review_count'     => $p['reviewCount'] ?? 0,
                ':compare_at_price' => $p['compareAtPrice'] ?? null
            ]);
            $productsSeeded++;
            
            // Insert variants if present
            if (isset($p['variants']) && is_array($p['variants'])) {
                foreach ($p['variants'] as $v) {
                    $variantStmt->execute([
                        ':product_id'        => $p['id'],
                        ':name'              => $v['name'],
                        ':price'             => $v['price'],
                        ':compare_at_price'  => $v['compareAtPrice'] ?? null
                    ]);
                    $variantsSeeded++;
                }
            }
        }
    }
    
    echo json_encode([
        'success' => true,
        'message' => 'Database initialized successfully!',
        'details' => [
            'products_seeded' => $productsSeeded,
            'variants_seeded' => $variantsSeeded,
            'status' => $productCount > 0 ? 'Already seeded' : 'Freshly seeded'
        ]
    ]);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}
?>
