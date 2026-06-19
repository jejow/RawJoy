import re

filepath = "index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find all product-cards
matches = re.finditer(r'<product-card.*?</product-card>', content, re.DOTALL)
for i, m in enumerate(matches):
    card_html = m.group(0)
    if 'salmon-stick' in card_html or 'cat-calming' in card_html or 'Salmon Stick' in card_html or 'Cat Calming' in card_html:
        # Let's search for the price block inside this product card
        price_match = re.search(r'<product-price.*?</product-price>', card_html, re.DOTALL)
        price_str = price_match.group(0) if price_match else "No price tag"
        
        # Let's search for the title
        title_match = re.search(r'class="[^"]*product-card__title[^"]*".*?</a>', card_html, re.DOTALL)
        title_str = title_match.group(0) if title_match else "No title"
        
        print(f"Card {i} (Char {m.start()}):")
        print(f"  Title: {title_str.strip()}")
        print(f"  Price tag: {price_str.strip()}")
        print("-" * 60)
