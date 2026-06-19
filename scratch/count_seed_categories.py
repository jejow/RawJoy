import json
import os
from collections import Counter

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
seed_path = os.path.join(workspace_root, "firebase", "seed-data.json")

if os.path.exists(seed_path):
    with open(seed_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    categories = [p.get("category") for p in data.get("products", [])]
    counter = Counter(categories)
    print("Database Seed Categories:")
    for cat, count in counter.items():
        print(f"  - {cat}: {count}")
else:
    print("seed-data.json not found!")
