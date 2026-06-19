import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

product_cards = re.findall(r'<product-card[^>]*>.*?</product-card>', content, re.DOTALL)
if product_cards:
    card = product_cards[0]
    print("=== Complete First Product Card ===")
    print(card)
    
    # Check other cards for vendor or sold out text
    print("\n=== Checking for sold out or vendor in all cards ===")
    for i, c in enumerate(product_cards):
        sold_out = "sold-out" in c or "Sold out" in c or "sold out" in c.lower() or "price--sold-out" in c
        vendor_match = re.search(r'vendor', c, re.IGNORECASE)
        print(f"Card {i} ({re.search(r'class=\"product-card__title.*?<span class=\"reversed-link__text\">(.*?)</span>', c, re.DOTALL).group(1).strip()}): Sold out={sold_out}, Vendor exists={vendor_match is not None}")
