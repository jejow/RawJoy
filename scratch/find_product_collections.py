import os
import re
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"
products_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products"

# List all actual product slugs from the products folder
product_slugs = [d for d in os.listdir(products_dir) if os.path.isdir(os.path.join(products_dir, d)) and not d.endswith('__temp')]
print("Total actual products in folder:", len(product_slugs))

# Find which collection index.html files contain each product slug
product_locations = {slug: [] for slug in product_slugs}

for root, dirs, files in os.walk(collections_dir):
    for file in files:
        if file == "index.html":
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, collections_dir)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            for slug in product_slugs:
                # Check if the product link or quick add contains this slug
                if f"/products/{slug}" in content:
                    product_locations[slug].append(rel_path)

# Print mapping
print("\nProduct slug -> Collection locations:")
for slug, locs in sorted(product_locations.items()):
    print(f" - {slug}: found in {len(locs)} collections")
    if not locs:
        print("   WARNING: NOT FOUND IN ANY COLLECTION!")
