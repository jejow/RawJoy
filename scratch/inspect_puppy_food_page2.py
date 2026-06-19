import os
import bs4

html_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\puppy-food-1\index.html"
html_dir = os.path.dirname(html_path)

with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

grid = soup.find(class_='product-grid')
if not grid:
    print("No product-grid found!")
    exit(1)

cards = grid.find_all(class_='product-grid__item')
print(f"Total cards on Puppy Food page 2: {len(cards)}")

for idx, card in enumerate(cards):
    title_el = card.find(class_='product-card__title')
    title = title_el.text.strip() if title_el else "Unknown Title"
    
    img_el = card.find('img')
    if img_el:
        src = img_el.get('src')
        srcset = img_el.get('srcset')
        
        clean_src = src.split('?')[0] if src else ""
        abs_src_path = os.path.normpath(os.path.join(html_dir, clean_src))
        src_exists = os.path.exists(abs_src_path)
        
        print(f"\n[{idx+1}] Product: {title}")
        print(f"  - src: {src}")
        print(f"    File exists on disk: {src_exists} ({abs_src_path})")
        if srcset:
            srcset_parts = srcset.split(',')
            for part in srcset_parts[:2]: # print first 2
                part = part.strip()
                if part:
                    path = part.split(' ')[0].split('?')[0]
                    abs_path = os.path.normpath(os.path.join(html_dir, path))
                    print(f"  - srcset path: {path} (exists: {os.path.exists(abs_path)})")
    else:
        print(f"\n[{idx+1}] Product: {title} - [NO IMG TAG]")
