import json

with open("firebase/seed-data.json", "r") as f:
    data = json.load(f)

products = data.get("products", [])
print(f"Total products: {len(products)}")

category_counts = {}
for p in products:
    cat = p.get("category", "Unknown")
    category_counts[cat] = category_counts.get(cat, 0) + 1

for cat, count in category_counts.items():
    print(f"Category: {cat} -> {count}")
