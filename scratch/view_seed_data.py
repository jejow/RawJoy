import json

with open('firebase/seed-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', [])
print(f"Total products in seed: {len(products)}")

# Print details of first 10 products
for p in products[:10]:
    print(f"Slug: {p.get('slug')}")
    print(f"  Name: {p.get('name')}")
    # Show price and weight/variants info
    print(f"  Price: {p.get('price')}")
    print(f"  Compare Price: {p.get('compareAtPrice')}")
    print(f"  Weight/Gram/Variants: {p.get('variants') or p.get('weight') or p.get('grams')}")
    print(f"  Keys: {list(p.keys())}")
    print("-" * 40)
