import os
import re

collections_dir = "collections"
for root, dirs, files in os.walk(collections_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            matches = re.finditer(r'<product-card.*?</product-card>', content, re.DOTALL)
            for i, m in enumerate(matches):
                card_html = m.group(0)
                if 'salmon-stick' in card_html or 'cat-calming' in card_html or 'Salmon Stick' in card_html or 'Cat Calming' in card_html:
                    price_match = re.search(r'<product-price.*?</product-price>', card_html, re.DOTALL)
                    price_str = price_match.group(0) if price_match else "No price tag"
                    
                    title_match = re.search(r'class="[^"]*product-card__title[^"]*".*?</a>', card_html, re.DOTALL)
                    title_str = title_match.group(0) if title_match else "No title"
                    
                    print(f"File: {filepath} | Card {i}:")
                    print(f"  Title: {title_str.strip()}")
                    print(f"  Price: {price_str.strip()}")
                    print("-" * 60)
