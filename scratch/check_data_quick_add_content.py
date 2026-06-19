import os
from bs4 import BeautifulSoup

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
product_path = os.path.join(workspace_root, "products", "chicken-bone-treat", "index.html")

if os.path.exists(product_path):
    with open(product_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    el = soup.find(attrs={"data-quick-add-content": True})
    if el:
        print(f"Element tag name: <{el.name}>")
        print("Attributes:")
        for attr, val in el.attrs.items():
            print(f"  {attr}: {val}")
        
        # Check parents
        parent = el.parent
        print(f"Parent tag name: <{parent.name}>")
        if parent.name == "quick-add-component":
            print("Parent is quick-add-component. Attributes:")
            for attr, val in parent.attrs.items():
                print(f"  {attr}: {val}")
    else:
        print("data-quick-add-content not found")
else:
    print("chicken-bone-treat/index.html not found")
