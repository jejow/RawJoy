import os
import re
from bs4 import BeautifulSoup

for folder in ['colostrum', 'colostrum-1', 'colostrum-2']:
    path = f"collections/{folder}/index.html"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        cards = soup.find_all('product-card')
        print(f"Folder: {folder} | Cards count: {len(cards)}")
        titles = []
        for card in cards:
            title_el = card.find(class_=re.compile(r'product-card__title'))
            if title_el:
                titles.append(title_el.text.strip())
        print(f"  First 5 product titles: {titles[:5]}")
        print(f"  Last 5 product titles: {titles[-5:]}")
        print("-" * 50)
