import os
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"

with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

print("Checking Facets Filter counts on collections/all/index.html:")

facet_items = soup.find_all(class_="facets__item")
print(f"Total facet items found: {len(facet_items)}")

for idx, item in enumerate(facet_items):
    label = item.find(class_="facet-checkbox__text")
    count_el = item.find(class_="facets__count")
    
    label_text = label.text.strip() if label else "Unknown"
    count_text = count_el.text.strip() if count_el else "No count"
    
    # Check input value or name
    inp = item.find('input')
    inp_name = inp.get('name') if inp else ""
    inp_val = inp.get('value') if inp else ""
    
    print(f"[{idx+1}] Filter: {label_text} | Count in HTML: {count_text} | Input: {inp_name}={inp_val}")
