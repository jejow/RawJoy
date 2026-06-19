import json

with open('firebase/seed-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', [])
print("Total products in seed-data.json:", len(products))

for p in products:
    print(f"ID: {p.get('id')} | Name: {p.get('name')} | Slug: {p.get('slug')} | MainImage: {p.get('mainImage')}")
