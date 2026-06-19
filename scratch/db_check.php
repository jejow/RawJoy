<?php
$host = '127.0.0.1';
$db = 'rawjoy_db';
$user = 'root';
$pass = '';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
try {
    $pdo = new PDO($dsn, $user, $pass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    
    echo "TABLES IN DATABASE:\n";
    $stmt = $pdo->query("SHOW TABLES");
    while ($row = $stmt->fetch(PDO::FETCH_NUM)) {
        echo "  - " . $row[0] . "\n";
    }
    
    echo "\nPRODUCT COUNT BY CATEGORY IN DB:\n";
    $stmt = $pdo->query("SELECT category, COUNT(*) as count FROM products GROUP BY category");
    while ($row = $stmt->fetch()) {
        echo "  - " . $row['category'] . ": " . $row['count'] . "\n";
    }
    
    echo "\nTOTAL PRODUCTS: ";
    echo $pdo->query("SELECT COUNT(*) FROM products")->fetchColumn() . "\n";
    
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage() . "\n";
}
