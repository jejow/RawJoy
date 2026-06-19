import json

with open('firebase/seed-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', [])

with open('scratch/seed_products.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(f"Total products in seed: {len(products)}\n\n")
    for idx, p in enumerate(products):
        f_out.write(f"Product {idx+1}:\n")
        f_out.write(f"  ID: {p.get('id')}\n")
        f_out.write(f"  Name: {p.get('name')}\n")
        f_out.write(f"  Slug: {p.get('slug')}\n")
        f_out.write(f"  Base Price: {p.get('price')}\n")
        f_out.write(f"  Category: {p.get('category')}\n")
        f_out.write(f"  Variants: {p.get('variants')}\n")
        f_out.write("-" * 50 + "\n")

print("Dumped successfully to scratch/seed_products.txt")
