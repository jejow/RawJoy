import os
import bs4

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), "html.parser")

print("--- ALL LINKS ---")
links = soup.find_all("a")
print(f"Total links: {len(links)}")

# Search for any link containing account, login, register, sign, or having those classes
found = 0
for link in links:
    href = link.get("href", "")
    cls = link.get("class", [])
    classes_str = " ".join(cls) if isinstance(cls, list) else str(cls)
    text = link.text.strip().replace("\n", " ")
    
    if any(k in href.lower() or k in classes_str.lower() or k in text.lower() for k in ["account", "login", "register", "sign", "masuk", "daftar"]):
        found += 1
        print(f"Link: Text: {repr(text[:50])} | Href: {repr(href)} | Classes: {repr(classes_str)}")
        if found >= 50:
            break
