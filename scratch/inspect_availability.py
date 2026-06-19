import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

product_cards = re.findall(r'<product-card[^>]*>.*?</product-card>', content, re.DOTALL)
for idx, c in enumerate(product_cards):
    title_match = re.search(r'class="product-card__title[^"]*"[^>]*>\s*<span class="reversed-link__text">(.*?)</span>', c, re.DOTALL)
    title = title_match.group(1).strip() if title_match else f"Card {idx}"
    
    # Check if add to cart button is disabled or has sold out class
    btn_matches = re.findall(r'<button[^>]+ref="addToCartButton"[^>]*>', c)
    disabled = any("disabled" in btn for btn in btn_matches)
    has_badge = "sold-out" in c.lower() and "badge" in c.lower()
    
    # check price container
    price_container = re.search(r'<div class="price-container[^"]*"', c)
    container_class = price_container.group(0) if price_container else ""
    
    if disabled or has_badge or "sold-out" in container_class:
        print(f"Product: {title} is sold out! (disabled={disabled}, has_badge={has_badge}, container={container_class})")
