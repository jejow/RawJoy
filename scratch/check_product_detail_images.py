import os
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_product_details(root_path, label):
    products_dir = os.path.join(root_path, "products")
    if not os.path.exists(products_dir):
        print(f"[{label}] products directory does not exist at {products_dir}")
        return
        
    print(f"\nChecking product detail images for [{label}] under {products_dir}...")
    missing_count = 0
    
    for item in os.listdir(products_dir):
        subpath = os.path.join(products_dir, item)
        if os.path.isdir(subpath):
            html_path = os.path.join(subpath, "index.html")
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                    soup = bs4.BeautifulSoup(f.read(), 'html.parser')
                    
                imgs = soup.find_all('img')
                for img in imgs:
                    src = img.get('src')
                    if not src:
                        continue
                    if src.startswith('http://') or src.startswith('https://') or src.startswith('//'):
                        continue
                        
                    clean_src = src.split('?')[0]
                    abs_path = os.path.normpath(os.path.join(subpath, clean_src))
                    
                    if not os.path.exists(abs_path):
                        print(f"  - In product: products/{item}/index.html")
                        print(f"    Missing image: {src}")
                        print(f"    Expected path: {abs_path}")
                        missing_count += 1
                        
    print(f"[{label}] check done. Missing images count: {missing_count}")

src_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
dst_root = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\RawJoy"

check_product_details(src_root, "Source Workspace")
check_product_details(dst_root, "Destination Workspace")
