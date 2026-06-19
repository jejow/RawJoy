import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"
unmapped_slugs = ["mint-comfort-bowl-series", "pastel-pet-bowl-series", "rawjoy-blue-energy-bar"]

for slug in unmapped_slugs:
    print(f"\n=== Searching for slug: {slug} ===")
    for root, dirs, files in os.walk(collections_dir):
        for file in files:
            if file == "index.html":
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                if slug in content:
                    print(f"Found in: {path}")
                    # Let's extract the product-card containing it
                    cards = re.findall(r'<product-card[^>]*>.*?</product-card>', content, re.DOTALL)
                    for c in cards:
                        if slug in c:
                            print("Card HTML snippet:")
                            print(c[:1000])
                            # Extract variant ID input
                            variant_id_match = re.search(r'name="id"[^>]*value="(\d+)"', c)
                            if variant_id_match:
                                print(f"Default Variant ID: {variant_id_match.group(1)}")
                            else:
                                print("No default Variant ID found in input")
