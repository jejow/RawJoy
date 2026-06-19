import os
import bs4
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"

def inspect_header(folder):
    html_path = os.path.join(collections_dir, folder, "index.html")
    if not os.path.exists(html_path):
        print(f"{folder} does not exist!")
        return
        
    print(f"\nHeader for collections/{folder}/index.html:")
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
        
    # Find h1
    h1 = soup.find('h1')
    if h1:
        print(f"  h1 text: {h1.text.strip()}")
        
    # Find ProductCount elements
    for id_val in ["ProductCount", "ProductCountDesktop"]:
        el = soup.find(id=id_val)
        if el:
            print(f"  {id_val}: {el.text.strip()}")
            
    # Find main pagination list
    pag = soup.find(class_="pagination")
    if pag:
        links = pag.find_all('a')
        print(f"  Pagination has {len(links)} links:")
        for a in links:
            print(f"    href={a.get('href')} | text={a.text.strip()}")

inspect_header("puppy-food")
inspect_header("puppy-food-1")
