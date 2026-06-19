import os
import bs4

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), "html.parser")

# Search for any dialog tags or any elements with id/class containing "search" and "drawer" or "modal"
elements = soup.find_all(lambda tag: tag.name == 'dialog' or (tag.get('id') and 'search' in tag.get('id').lower()) or (tag.get('class') and any('search' in c.lower() for c in tag.get('class'))))
print(f"Found {len(elements)} search/dialog elements:")
for el in elements:
    # check if it's a dialog or has class/id drawer
    classes = " ".join(el.get('class', [])) if isinstance(el.get('class'), list) else str(el.get('class', ''))
    id_str = el.get('id', '')
    if el.name == 'dialog' or 'drawer' in classes.lower() or 'drawer' in id_str.lower() or 'modal' in classes.lower() or 'modal' in id_str.lower():
        print(f"Tag: {el.name} | id: {repr(id_str)} | class: {repr(classes)}")
        # print first 150 chars of outer HTML
        print(str(el)[:200])
        print("=" * 50)
