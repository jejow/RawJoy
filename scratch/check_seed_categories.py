import json

with open("firebase/seed-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", [])
categories = set()
for p in products:
    cat = p.get("category")
    if cat:
        categories.add(cat)
print("Categories in seed-data.json:")
print(categories)
