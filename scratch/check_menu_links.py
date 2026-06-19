import os
from bs4 import BeautifulSoup

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

# Find all links starting with collections/ in the header or menu-drawer
menu = soup.find(id="HeaderMenu-Navigation") or soup.find(class_="header__inline-menu")
links = []
if menu:
    for a in menu.find_all("a", href=True):
        if "collections" in a["href"]:
            links.append((a.text.strip(), a["href"]))
else:
    # fallback to all collections links in page
    for a in soup.find_all("a", href=True):
        if "collections" in a["href"]:
            links.append((a.text.strip(), a["href"]))

print(f"Found {len(links)} collection links in header menu/page:")
for title, href in set(links):
    print(f"  - {title or 'Empty Title'} -> {href}")
