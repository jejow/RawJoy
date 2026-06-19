import os
import bs4
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"

with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

# Let's search for any forms or elements with "filter" in class name
print("Searching for elements with 'filter' or 'facet' in class name:")
elements = soup.find_all(class_=lambda c: c and ('filter' in c.lower() or 'facet' in c.lower()))
print(f"Found {len(elements)} elements")

# Let's search for checkboxes
print("\nSearching for checkboxes:")
checkboxes = soup.find_all('input', type='checkbox')
print(f"Found {len(checkboxes)} checkboxes")
for idx, cb in enumerate(checkboxes[:15]):
    parent_label = cb.find_parent('label')
    parent_text = parent_label.text.strip() if parent_label else ""
    # Remove excessive newlines
    parent_text = re.sub(r'\s+', ' ', parent_text)
    print(f"[{idx+1}] name: {cb.get('name')} | value: {cb.get('value')} | Text: {parent_text}")

# Let's search for any elements with id="ProductCount"
print("\nProduct counts elements:")
for id_val in ["ProductCount", "ProductCountDesktop"]:
    el = soup.find(id=id_val)
    if el:
        print(f"  - {id_val}: {el.text.strip()}")
