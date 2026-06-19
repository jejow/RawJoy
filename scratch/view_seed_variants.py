import json

with open('firebase/seed-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', [])

for p in products[:5]:
    print(f"Product: {p.get('name')}")
    print("Variants in seed:")
    for v in p.get('variants', []):
        print(f"  {v}")
    print("-" * 50)
