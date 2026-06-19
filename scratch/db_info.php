<?php
require 'api/db.php';

echo "--- TABLES ---\n";
$stmt = $pdo->query('SHOW TABLES');
while ($row = $stmt->fetch(PDO::FETCH_NUM)) {
    echo $row[0] . "\n";
}

echo "\n--- PRODUCTS TABLE COLUMNS ---\n";
$stmt = $pdo->query('DESCRIBE products');
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    echo $row['Field'] . " - " . $row['Type'] . "\n";
}

echo "\n--- PRODUCT COUNT BY CATEGORY IN DB ---\n";
$stmt = $pdo->query('SELECT category, COUNT(*) as cnt FROM products GROUP BY category');
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    echo $row['category'] . ": " . $row['cnt'] . "\n";
}

echo "\n--- DOES WE HAVE A COLLECTIONS OR RELATION TABLE? ---\n";
// Let's see if there is a collections table or tags or anything
try {
    $stmt = $pdo->query('SELECT * FROM collections');
    echo "Collections table exists! Rows:\n";
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        print_r($row);
    }
} catch (Exception $e) {
    echo "No collections table: " . $e->getMessage() . "\n";
}
?>
