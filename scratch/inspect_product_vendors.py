import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

products_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products"
vendors = ["Aura Interiors", "Casa Curate", "Haven & Hearth", "Modern Oak", "Nest & Nook", "Timeless Haven"]

found_vendors = {}

for d in os.listdir(products_dir):
    p_dir = os.path.join(products_dir, d)
    if os.path.isdir(p_dir) and not d.endswith("__temp"):
        html_path = os.path.join(p_dir, "index.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Search for vendor names in the HTML content
            matched_vendors = []
            for v in vendors:
                # Search case-insensitively or exactly
                if v in content:
                    matched_vendors.append(v)
            
            # Also search for any meta/json vendor tag
            vendor_tag = re.search(r'"vendor"\s*:\s*"([^"]+)"', content, re.IGNORECASE)
            tag_val = vendor_tag.group(1) if vendor_tag else None
            
            found_vendors[d] = {
                "matched": matched_vendors,
                "json_vendor": tag_val
            }

print("Product Vendors found on product pages:")
for p, info in sorted(found_vendors.items()):
    print(f"  {p}: matched={info['matched']}, json={info['json_vendor']}")
