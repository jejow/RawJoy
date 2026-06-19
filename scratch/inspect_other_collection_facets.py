import os
import bs4
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"
collections_to_check = ["puppy-food", "puppy-food-1", "treats", "wet-food", "colostrum", "supplements"]

for name in collections_to_check:
    html_path = os.path.join(collections_dir, name, "index.html")
    if os.path.exists(html_path):
        print(f"\nChecking collection: collections/{name}/index.html")
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = bs4.BeautifulSoup(f.read(), 'html.parser')
            
        # Get actual grid count
        grid = soup.find(class_='product-grid')
        grid_count = len(grid.find_all(class_='product-grid__item')) if grid else 0
        print(f"  Actual grid items count: {grid_count}")
        
        # Check ProductCount elements
        for id_val in ["ProductCount", "ProductCountDesktop"]:
            el = soup.find(id=id_val)
            if el:
                print(f"  {id_val}: {el.text.strip()}")
                
        # Check filter checkboxes
        checkboxes = soup.find_all('input', type='checkbox')
        print(f"  Checkboxes found: {len(checkboxes)}")
        for idx, cb in enumerate(checkboxes[:10]):
            parent_label = cb.find_parent('label')
            parent_text = parent_label.text.strip() if parent_label else ""
            parent_text = re.sub(r'\s+', ' ', parent_text)
            print(f"    [{idx+1}] {cb.get('name')}={cb.get('value')} -> {parent_text}")
