import os
from bs4 import BeautifulSoup

for folder in ['colostrum', 'colostrum-1', 'colostrum-2']:
    path = f"collections/{folder}/index.html"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        cards = soup.find_all('product-card')
        print(f"Folder: {folder} | Cards count: {len(cards)}")
        for idx, card in enumerate(cards[:5]):
            link = card.find('a', href=True)
            title_el = card.find(class_='reversed-link__text')
            print(f"  Card {idx}: title='{title_el.text.strip() if title_el else 'None'}' href='{link.get('href') if link else 'None'}'")
        print("-" * 50)
