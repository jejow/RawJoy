import os
import bs4

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), "html.parser")

ps_elements = soup.find_all(lambda tag: 'predictive' in tag.name.lower() or (tag.get('id') and 'predictive' in tag.get('id').lower()))
print(f"Found {len(ps_elements)} predictive elements:")
for el in ps_elements[:10]:
    print(f"Tag: {el.name} | id: {el.get('id')} | class: {el.get('class')}")
    print(str(el)[:400])
    print("-" * 50)
