import os
from bs4 import BeautifulSoup

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

collections_to_check = [
    ("Raw Foods", "collections/raw-food/index.html"),
    ("Supplements", "collections/organic-food/index.html"), # wait, let's check which file is organic-food or supplements
    ("Bone Broth", "collections/bone-broth/index.html"),
    ("Treats", "collections/treats/index.html"),
    ("Freeze Dried", "collections/freeze-dried/index.html")
]

# Let's list all files in collections/ to find the correct files
for root, dirs, files in os.walk(os.path.join(workspace_root, "collections")):
    for file in files:
        if file.endswith("index.html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            
            # Look for product cards (often have class starting with 'product-card' or inside a grid)
            # Let's see if we can find how many product cards are present
            cards = soup.find_all(class_=lambda x: x and ("product-card" in x or "card-product" in x or "grid__item" in x))
            
            # Let's also check for specific elements to count products
            # In Shopify/RawJoy, product grid items usually have class like "grid__item"
            grid_items = soup.find_all("li", class_=lambda x: x and "grid__item" in x)
            product_links = soup.find_all("a", class_=lambda x: x and "product-card__link" in x)
            
            rel_path = os.path.relpath(path, workspace_root)
            print(f"Collection: {rel_path}")
            print(f"  - grid__item count: {len(grid_items)}")
            print(f"  - product-card__link count: {len(product_links)}")
            print(f"  - generic card count: {len(cards)}")
