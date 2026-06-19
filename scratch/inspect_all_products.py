import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"
if not os.path.exists(path):
    print("File not found")
    sys.exit(1)

with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's search for <product-card elements
product_cards = re.findall(r'<product-card[^>]*>.*?</product-card>', content, re.DOTALL)
print(f"Total product cards: {len(product_cards)}")

if product_cards:
    # Print the first card
    print("\n=== First Product Card HTML ===")
    print(product_cards[0][:1500])
    
    # Analyze attributes of product cards
    print("\n=== Attributes of first 5 cards ===")
    for idx, card in enumerate(product_cards[:5]):
        attrs = re.findall(r'(\w+(?:-\w+)*)="([^"]*)"', card.split('>')[0])
        print(f"Card {idx}: {dict(attrs)}")
        
        # Let's extract title
        title_match = re.search(r'class="product-card__title[^"]*"[^>]*>\s*<span class="reversed-link__text">(.*?)</span>', card, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Unknown"
        
        # Let's extract price
        price_match = re.search(r'class="price(?: price--sale)?">(.*?)</span>', card)
        price = price_match.group(1).strip() if price_match else "Unknown"
        
        print(f"  Title: {title}, Price: {price}")
else:
    # Maybe product cards are in some other tags? Let's check.
    print("No product-card elements found. Let's find any list items or grid elements.")
    # Search for class product-grid or grid__item
    grid_items = re.findall(r'<li[^>]*class="[^"]*grid__item[^"]*"[^>]*>.*?</li>', content, re.DOTALL)
    print(f"Grid items: {len(grid_items)}")
