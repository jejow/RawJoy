import os
import bs4

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), "html.parser")

cards = soup.find_all(class_="collection-card__inner")
print(f"Found {len(cards)} collection cards:")
for idx, card in enumerate(cards):
    title_el = card.find(class_="collection-card__title")
    title_text = title_el.text.strip() if title_el else "No title"
    # Print the outer HTML of title_el
    title_html = str(title_el) if title_el else ""
    print(f"Card {idx}: Title text: {repr(title_text)}, HTML: {repr(title_html)}")
