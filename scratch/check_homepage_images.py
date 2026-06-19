import os
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_homepage(root_path, label):
    html_path = os.path.join(root_path, "index.html")
    if not os.path.exists(html_path):
        print(f"[{label}] index.html does not exist at {html_path}")
        return
        
    print(f"\nChecking homepage images for [{label}] at {html_path}...")
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
        
    imgs = soup.find_all('img')
    missing_count = 0
    
    for idx, img in enumerate(imgs):
        src = img.get('src')
        if not src:
            continue
            
        if src.startswith('http://') or src.startswith('https://') or src.startswith('//'):
            continue
            
        clean_src = src.split('?')[0]
        abs_path = os.path.normpath(os.path.join(root_path, clean_src))
        
        # We also want to see if there is any product card associated with it
        # Let's find parent product card if possible
        parent_card = img.find_parent(class_=lambda c: c and ('card' in c or 'item' in c))
        card_title = ""
        if parent_card:
            title_el = parent_card.find(class_=lambda c: c and 'title' in c)
            if title_el:
                card_title = title_el.text.strip()
                
        if not os.path.exists(abs_path):
            print(f"  - Missing: {src}")
            if card_title:
                print(f"    Product card title: {card_title}")
            print(f"    Expected path: {abs_path}")
            missing_count += 1
            
    print(f"[{label}] check done. Missing images count: {missing_count}")

src_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
dst_root = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\RawJoy"

check_homepage(src_root, "Source Workspace")
check_homepage(dst_root, "Destination Workspace")
