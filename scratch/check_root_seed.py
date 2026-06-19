import json
import sys

# Safely output encoding
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

with open("firebase/seed-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", [])
print(f"Total products: {len(products)}")
for p in products:
    print(f"  Slug: {p.get('slug')}, Name: {p.get('name')}")
