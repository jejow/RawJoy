import os
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\RawJoy"
collections_dir = os.path.join(root_dir, "collections")

print("Scanning all collections for missing product images...")

total_missing = 0

for item in os.listdir(collections_dir):
    subpath = os.path.join(collections_dir, item)
    if os.path.isdir(subpath):
        html_path = os.path.join(subpath, "index.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                soup = bs4.BeautifulSoup(f.read(), 'html.parser')
                
            grid = soup.find(class_='product-grid')
            if not grid:
                continue
                
            cards = grid.find_all(class_='product-grid__item')
            missing_in_collection = []
            
            for card in cards:
                title_el = card.find(class_='product-card__title')
                title = title_el.text.strip() if title_el else "Unknown Title"
                
                img_el = card.find('img')
                if img_el:
                    src = img_el.get('src')
                    if src:
                        clean_src = src.split('?')[0]
                        abs_src_path = os.path.normpath(os.path.join(subpath, clean_src))
                        if not os.path.exists(abs_src_path):
                            missing_in_collection.append((title, src, abs_src_path))
                            total_missing += 1
                else:
                    missing_in_collection.append((title, "NO IMG TAG", ""))
                    total_missing += 1
            
            if missing_in_collection:
                print(f"\nIn Collection: collections/{item}/index.html")
                for title, src, path in missing_in_collection:
                    print(f"  - Product: {title}")
                    print(f"    Image: {src}")
                    if path:
                        print(f"    Expected absolute path: {path}")

print(f"\nScan complete. Total missing image references in source collections: {total_missing}")
