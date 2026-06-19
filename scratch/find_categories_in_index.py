import re
import os
import bs4

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

if not os.path.exists(index_path):
    print("index.html not found!")
    exit(1)

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Search for potential categories in lowercase
keywords = ["raw foods", "supplements", "bone broth", "treats", "freeze dried"]
for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), content, re.IGNORECASE)]
    print(f"Keyword '{kw}' found {len(matches)} times at positions: {matches}")
    for idx, pos in enumerate(matches):
        context = content[max(0, pos-150):min(len(content), pos+150)]
        print(f"  [{idx}] Context: {repr(context)}")
        print("-" * 50)
