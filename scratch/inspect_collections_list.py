import os
import bs4
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\index.html"

if os.path.exists(html_path):
    print("Inspecting collections/index.html:")
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
        
    items = soup.find_all(class_=lambda c: c and ('collection-card' in c or 'card' in c or 'grid__item' in c))
    print(f"Found {len(items)} items/cards")
    
    for idx, item in enumerate(items[:20]):
        title_el = item.find(class_=lambda c: c and 'title' in c)
        count_el = item.find(class_=lambda c: c and 'count' in c)
        
        title = title_el.text.strip() if title_el else "No Title"
        count = count_el.text.strip() if count_el else "No Count"
        
        title = re.sub(r'\s+', ' ', title)
        count = re.sub(r'\s+', ' ', count)
        
        # Link
        link_el = item.find('a')
        href = link_el.get('href') if link_el else ""
        
        print(f"[{idx+1}] Category: {title} | Count shown: {count} | Link: {href}")
else:
    print("collections/index.html does not exist!")
