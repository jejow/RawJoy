<?php
require 'api/db.php';
$stmt = $pdo->query('SELECT category, COUNT(*) as count FROM products GROUP BY category');
$rows = $stmt->fetchAll();
foreach ($rows as $row) {
    echo "Category: " . $row['category'] . " -> Count: " . $row['count'] . "\n";
}
?>
