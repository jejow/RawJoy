import os

html_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"

with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print(f"File length: {len(content)} characters")

slugs_to_check = [
    "pet-meal-time-mix",
    "rawjoy-soft-bar",
    "salmon-broccoli-crunch",
    "salmon-carrot-pate",
    "salmon-rice-formula",
    "salmon-stick",
    "venison-peas-recipe",
    "beef-spinach-stew"
]

for slug in slugs_to_check:
    count = content.count(slug)
    print(f"Slug '{slug}': count = {count}")
