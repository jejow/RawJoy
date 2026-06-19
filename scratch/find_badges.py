import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's search for badge class occurrences
badges = re.findall(r'<[^>]*class="[^"]*badge[^"]*"[^>]*>.*?</[^>]+>', content, re.DOTALL)
print(f"Total badge elements: {len(badges)}")
for b in badges[:20]:
    print(b)
    
# Let's also print all text nodes inside any <product-badge> element
product_badges = re.findall(r'<product-badge[^>]*>(.*?)</product-badge>', content, re.DOTALL)
print(f"\nTotal product-badge elements: {len(product_badges)}")
non_empty = 0
for pb in product_badges:
    text = re.sub(r'<[^>]+>', '', pb).strip()
    if text:
        print(f"Non-empty product-badge text: {text}")
        non_empty += 1
print(f"Non-empty product-badge elements: {non_empty}")
