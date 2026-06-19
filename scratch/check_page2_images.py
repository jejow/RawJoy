import os
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_page2_images(root_path, label):
    collections_dir = os.path.join(root_path, "collections")
    if not os.path.exists(collections_dir):
        print(f"[{label}] collections directory does not exist at {collections_dir}")
        return
        
    print(f"\nChecking page 2 images for [{label}] under {collections_dir}...")
    total_missing = 0
    
    for dirpath, dirnames, filenames in os.walk(collections_dir):
        if os.path.basename(dirpath) == "page2":
            for filename in filenames:
                if filename == "index.html":
                    html_path = os.path.join(dirpath, filename)
                    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
                        
                    grid = soup.find(class_='product-grid')
                    if not grid:
                        continue
                        
                    cards = grid.find_all(class_='product-grid__item')
                    rel_html_path = os.path.relpath(html_path, collections_dir)
                    
                    for card in cards:
                        title_el = card.find(class_='product-card__title')
                        title = title_el.text.strip() if title_el else "Unknown Title"
                        
                        img_el = card.find('img')
                        if img_el:
                            src = img_el.get('src')
                            if src:
                                clean_src = src.split('?')[0]
                                abs_path = os.path.normpath(os.path.join(dirpath, clean_src))
                                if not os.path.exists(abs_path):
                                    print(f"  - In: collections/{rel_html_path}")
                                    print(f"    Product: {title}")
                                    print(f"    Missing image: {src}")
                                    print(f"    Expected path: {abs_path}")
                                    total_missing += 1
                        else:
                            print(f"  - In: collections/{rel_html_path}")
                            print(f"    Product: {title} - [NO IMG TAG]")
                            total_missing += 1
                            
    print(f"[{label}] check done. Total missing product images on page 2: {total_missing}")

src_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
dst_root = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\RawJoy"

check_page2_images(src_root, "Source Workspace")
check_page2_images(dst_root, "Destination Workspace")
