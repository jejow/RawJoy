import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

mapping_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\scratch\variant_mapping.json"
products_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products"

with open(mapping_path, "r", encoding="utf-8") as f:
    var_map = json.load(f)

# Group variant names by slug
slug_to_variants = {}
for var_id, info in var_map.items():
    slug = info["slug"]
    var_name = info["variantName"]
    if slug not in slug_to_variants:
        slug_to_variants[slug] = []
    if var_name not in slug_to_variants[slug]:
        slug_to_variants[slug].append(var_name)

# Scan product files for vendor names
slug_to_vendor = {}
vendors = ["Aura Interiors", "Casa Curate", "Haven & Hearth", "Modern Oak", "Nest & Nook", "Timeless Haven"]

for d in os.listdir(products_dir):
    p_dir = os.path.join(products_dir, d)
    if os.path.isdir(p_dir) and not d.endswith("__temp"):
        html_path = os.path.join(p_dir, "index.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Find vendor in JSON metadata first
            vendor_match = re.search(r'"vendor"\s*:\s*"([^"]+)"', content, re.IGNORECASE)
            if vendor_match:
                vendor = vendor_match.group(1).replace("\\u0026", "&")
                slug_to_vendor[d] = vendor
            else:
                # Fallback to search
                for v in vendors:
                    if v in content:
                        slug_to_vendor[d] = v
                        break

# Let's combine them into a single product metadata dictionary
product_metadata = {}
all_slugs = set(slug_to_variants.keys()).union(slug_to_vendor.keys())

for slug in all_slugs:
    product_metadata[slug] = {
        "variants": slug_to_variants.get(slug, []),
        "vendor": slug_to_vendor.get(slug, "Nest & Nook") # Fallback to Nest & Nook if none matches
    }

# Print the resulting JavaScript object
js_code = "const PRODUCT_METADATA = " + json.dumps(product_metadata, indent=2) + ";"
print(js_code)

# Write it to a temporary file
with open(r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\scratch\js_mappings.js", "w", encoding="utf-8") as f:
    f.write(js_code)
