from bs4 import BeautifulSoup
import re

path = "collections/shop-all/index.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
cards = soup.find_all('product-card')
print(f"Cards count: {len(cards)}")
titles = []
for idx, card in enumerate(cards):
    title_el = card.find(class_=re.compile(r'product-card__title'))
    title = title_el.text.strip() if title_el else 'Unknown'
    titles.append(title)
    print(f"  Card {idx}: {title}")

# Check unique titles
print(f"\nUnique titles count: {len(set(titles))}")
