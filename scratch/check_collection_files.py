import os
import bs4

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
collections = ["raw-foods", "supplements", "bone-broth", "treats", "freeze-dried"]

for col in collections:
    path = os.path.join(workspace_root, "collections", col, "index.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            soup = bs4.BeautifulSoup(f.read(), "html.parser")
            
        # Find grid items count
        grid = soup.find(class_="product-grid")
        grid_items = grid.find_all(class_="product-grid__item") if grid else []
        grid_count = len(grid_items)
        
        # Find ProductCount text
        p_count = soup.find(id="ProductCount")
        p_count_text = p_count.text.strip() if p_count else "Not found"
        
        # Find ProductCountDesktop text
        p_count_d = soup.find(id="ProductCountDesktop")
        p_count_d_text = p_count_d.text.strip() if p_count_d else "Not found"
        
        print(f"Collection '{col}':")
        print(f"  - Actual grid items count: {grid_count}")
        print(f"  - id='ProductCount': {p_count_text}")
        print(f"  - id='ProductCountDesktop': {p_count_d_text}")
    else:
        print(f"Collection '{col}': index.html NOT found at {path}")
