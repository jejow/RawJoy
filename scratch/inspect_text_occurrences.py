import os
import bs4
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\puppy-food\index.html"

with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

# Find all occurrences of "Puppy Food" in the text of the page
print("Occurrences of 'Puppy Food' text in elements:")
for el in soup.find_all(text=re.compile("Puppy Food", re.IGNORECASE)):
    parent = el.parent
    if parent:
        snippet = re.sub(r'\s+', ' ', parent.text.strip())[:150]
        print(f"  - Tag: <{parent.name}> | Text: {snippet}")

print("\nOccurrences of 'Product title' in elements:")
for el in soup.find_all(text=re.compile("Product title", re.IGNORECASE)):
    parent = el.parent
    if parent:
        snippet = re.sub(r'\s+', ' ', parent.text.strip())[:150]
        print(f"  - Tag: <{parent.name}> | Text: {snippet}")
