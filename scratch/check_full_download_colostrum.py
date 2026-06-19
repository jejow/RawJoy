import os
import re
from bs4 import BeautifulSoup

fd_path = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\full download"
for folder in ['collections_colostrum', 'collections_colostrum-1', 'collections_colostrum-2']:
    path = os.path.join(fd_path, folder, "index.html")
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
        # Let's check pagination links in this file
        nav = soup.find('nav', class_='pagination')
        if nav:
            print("  Pagination Links:")
            for link in nav.find_all('a'):
                print(f"    {link.get('aria-label') or link.text.strip()}: {link.get('href')}")
        print("-" * 50)
    else:
        print(f"Path not found: {path}")
