import os
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

all_html_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"
products_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products"

product_slugs = [d for d in os.listdir(products_dir) if os.path.isdir(os.path.join(products_dir, d)) and not d.endswith('__temp')]

with open(all_html_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

grid = soup.find(class_='product-grid')
cards = grid.find_all(class_='product-grid__item') if grid else []

grid_slugs = set()
for card in cards:
    link = card.find('a', href=lambda h: h and '/products/' in h)
    if link:
        href = link['href']
        # Extract slug
        slug = href.split('/products/')[-1].split('/')[0].split('?')[0]
        grid_slugs.add(slug)

print("Slugs in collections/all/index.html grid:")
for slug in sorted(grid_slugs):
    print(f"  - {slug}")

missing = [s for s in product_slugs if s not in grid_slugs]
print(f"\nMissing product slugs from collections/all/index.html grid ({len(missing)}):")
for s in missing:
    print(f"  - {s}")
