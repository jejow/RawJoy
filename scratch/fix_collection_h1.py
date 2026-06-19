import os
import bs4
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"

exclude_dirs = {"css", "fonts", "images", "js", "firebase", "types"}
subdirs = [d for d in os.listdir(collections_dir) if os.path.isdir(os.path.join(collections_dir, d)) and d not in exclude_dirs]

def get_collection_title(folder_name):
    # Remove page suffixes (-1, -2, etc.)
    base = re.sub(r'-\d+$', '', folder_name)
    
    # Custom overrides
    if base == "all":
        return "Products"
    if base == "shop-all":
        return "Shop All"
    if base == "air-dried-food":
        return "Air-Dried Food"
    if base == "the-new":
        return "The New"
    if base == "best-sellers":
        return "Best Sellers"
    if base == "new-arrivals":
        return "New Arrivals"
    if base == "seasonal-products":
        return "Seasonal Products"
    if base == "senior-dog-food":
        return "Senior Dog Food"
    if base == "sensitive-stomach":
        return "Sensitive Stomach"
    if base == "sockete-salmon":
        return "Sockete Salmon"
    if base == "doggy-dental-mix":
        return "Doggy Dental Mix"
    
    # General title case replacement
    return base.replace("-", " ").title()

print("Fixing collection heading titles (h1) in workspace...")

fixed_count = 0
for folder in subdirs:
    html_path = os.path.join(collections_dir, folder, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        soup = bs4.BeautifulSoup(content, 'html.parser')
        h1 = soup.find('h1')
        if h1:
            title = get_collection_title(folder)
            # Only update if it is "Product title" or generic
            if h1.text.strip() == "Product title" or h1.text.strip() == "Products" or h1.text.strip() == "":
                h1.string = title
                fixed_count += 1
                print(f"  Fixed h1 in collections/{folder}/index.html -> '{title}'")
                
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(str(soup))

print(f"\nDone! Updated h1 heading in {fixed_count} collection pages.")
