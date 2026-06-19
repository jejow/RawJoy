import os
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"

exclude_dirs = {"css", "fonts", "images", "js", "firebase", "types"}
subdirs = [d for d in os.listdir(collections_dir) if os.path.isdir(os.path.join(collections_dir, d)) and d not in exclude_dirs]

for d in sorted(subdirs):
    html_path = os.path.join(collections_dir, d, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = bs4.BeautifulSoup(f.read(), 'html.parser')
            
        # Find count elements
        count_text = ""
        count_el = soup.find(id="ProductCount")
        if count_el:
            count_text = count_el.text.strip()
            
        count_desktop_el = soup.find(id="ProductCountDesktop")
        count_desktop_text = ""
        if count_desktop_el:
            count_desktop_text = count_desktop_el.text.strip()
            
        grid = soup.find(class_='product-grid')
        grid_items_count = len(grid.find_all(class_='product-grid__item')) if grid else 0
        
        # Check if they match
        print(f"Collection: collections/{d}/index.html")
        print(f"  - Actual grid items count: {grid_items_count}")
        if count_text:
            print(f"  - ProductCount: {count_text}")
        if count_desktop_text:
            print(f"  - ProductCountDesktop: {count_desktop_text}")
            
        # Check parent category counts (facets count)
        # Search for facet counts
        facet_counts = []
        for facet_val in soup.find_all(class_="facets__value"):
            count_span = facet_val.find(class_="facets__count")
            if count_span:
                facet_counts.append(f"{facet_val.text.strip()}")
        if facet_counts:
            print(f"  - Facets list counts: {facet_counts[:5]}...")
