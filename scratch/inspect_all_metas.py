import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

product_cards = re.findall(r'<product-card[^>]*>.*?</product-card>', content, re.DOTALL)
metas = {}
for c in product_cards:
    title_match = re.search(r'class="product-card__title[^"]*"[^>]*>\s*<span class="reversed-link__text">(.*?)</span>', c, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Unknown"
    
    meta_matches = re.findall(r'<div class="product-card__metas">(.*?)</div>', c, re.DOTALL)
    meta_texts = []
    for mm in meta_matches:
        txt = re.sub(r'<[^>]+>', '', mm).strip()
        if txt:
            meta_texts.append(txt)
            
    metas[title] = meta_texts

print("Product Metas:")
for k, v in sorted(metas.items()):
    print(f"  {k}: {v}")
