import os
from bs4 import BeautifulSoup

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
product_path = os.path.join(workspace_root, "products", "chicken-bone-treat", "index.html")

if os.path.exists(product_path):
    with open(product_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    quick_add = soup.find(attrs={"data-quick-add-content": True})
    if quick_add:
        print("Found [data-quick-add-content] in chicken-bone-treat/index.html:")
        imgs = quick_add.find_all("img")
        for idx, img in enumerate(imgs):
            print(f"  Img [{idx}]:")
            print(f"    src: {img.get('src')}")
            print(f"    srcset: {img.get('srcset')}")
    else:
        print("[data-quick-add-content] not found in chicken-bone-treat/index.html")
else:
    print("chicken-bone-treat/index.html not found!")
