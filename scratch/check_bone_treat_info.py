import json
import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
seed_path = os.path.join(workspace_root, "firebase", "seed-data.json")

if os.path.exists(seed_path):
    with open(seed_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for p in data.get("products", []):
        if "bone" in p.get("id", "").lower() or "bone" in p.get("name", "").lower():
            print(f"Product ID: {p.get('id')}")
            print(f"  Name: {p.get('name')}")
            print(f"  Slug: {p.get('slug')}")
            print(f"  Category: {p.get('category')}")
            print(f"  Variants count: {len(p.get('variants', []))}")
            print("-" * 30)
else:
    print("seed-data.json not found!")
