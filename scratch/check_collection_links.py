import os
from bs4 import BeautifulSoup

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

# Find the category list section
# We can find category cards, typically with class reversed-link and count sup
cards = soup.find_all(class_=lambda x: x and "collection-card" in x)
print(f"Found {len(cards)} collection cards:")
for idx, card in enumerate(cards):
    link = card.find("a", class_="collection-card__link")
    href = link["href"] if link else "No link"
    
    title_el = card.find("span", class_="reversed-link__text")
    title = title_el.text.strip() if title_el else "No title"
    
    count_el = card.find("sup", class_="collection-card__count")
    count = count_el.text.strip() if count_el else "No count"
    
    print(f"Card [{idx}]:")
    print(f"  Title: {title}")
    print(f"  Link: {href}")
    print(f"  Count: {count}")
