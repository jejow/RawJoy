import os
from bs4 import BeautifulSoup

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
product_path = os.path.join(workspace_root, "products", "chicken-bone-treat", "index.html")

if os.path.exists(product_path):
    with open(product_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    qa_comp = soup.find("quick-add-component")
    if qa_comp:
        print("Found <quick-add-component>:")
        for attr, val in qa_comp.attrs.items():
            print(f"  {attr}: {val}")
    else:
        print("<quick-add-component> not found.")
else:
    print("chicken-bone-treat/index.html not found")
