import json

with open('firebase/seed-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', [])

variant_names = set()
for p in products:
    for v in p.get('variants', []):
        variant_names.add(v.get('name'))

print("All distinct variant names in seed-data.json:")
print(variant_names)
