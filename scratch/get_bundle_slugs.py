import re
import os

file_path = 'index.html'
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Search for all product-bundle-selection elements
    matches = re.findall(r'data-product-url="products/([^"]+)"', html)
    print("Unique slugs found:", list(set(matches)))
else:
    print("index.html not found")
