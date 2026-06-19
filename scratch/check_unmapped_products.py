import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"
mapping_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\scratch\variant_mapping.json"

with open(mapping_path, "r", encoding="utf-8") as f:
    mapping = json.load(f)

mapped_slugs = set(item["slug"] for item in mapping.values())

unmapped = set()
all_slugs = set()

# Scan all index.html files under collections
for root, dirs, files in os.walk(collections_dir):
    for file in files:
        if file == "index.html":
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Find all product cards or quick-add urls
            urls = re.findall(r'data-product-url="([^"]+)"', content)
            hrefs = re.findall(r'href="[^"]*/products/([^"?\s]+)', content)
            
            for url in urls:
                slug = url.split('/')[-1]
                all_slugs.add(slug)
                if slug not in mapped_slugs:
                    unmapped.add(slug)
                    
            for href in hrefs:
                all_slugs.add(href)
                if href not in mapped_slugs:
                    unmapped.add(href)

print(f"Total distinct slugs found in HTML files: {len(all_slugs)}")
print(f"Total unmapped slugs: {len(unmapped)}")
if unmapped:
    print("Unmapped slugs:")
    for slug in sorted(unmapped):
        print(f"  - {slug}")
else:
    print("All slugs are successfully mapped in variant_mapping.json!")
