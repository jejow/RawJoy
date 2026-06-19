import os
from bs4 import BeautifulSoup

for folder in ['colostrum', 'colostrum-1', 'colostrum-2']:
    path = f"collections/{folder}/index.html"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find('title')
        print(f"Folder: {folder} | Title: {title.text.strip() if title else 'None'}")
        # Let's count number of product cards
        cards = soup.find_all('product-card')
        print(f"  Product Cards: {len(cards)}")
        # Let's check pagination block
        nav = soup.find('nav', class_='pagination')
        if nav:
            print("  Pagination Links:")
            for link in nav.find_all('a'):
                print(f"    {link.get('aria-label') or link.text.strip()}: {link.get('href')}")
        else:
            print("  No pagination found")
        print("-" * 50)
    else:
        print(f"Folder {folder} does not exist at {path}")
