import os
import bs4

html_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"

with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

print("Script tags in collections/all/index.html:")
for idx, script in enumerate(soup.find_all('script')):
    src = script.get('src')
    type_attr = script.get('type')
    if src:
        print(f"[{idx+1}] src: {src} | type: {type_attr}")
    else:
        # Inline script: print first 100 chars
        content = script.string
        if content:
            snippet = content.strip().replace('\n', ' ')[:100]
            print(f"[{idx+1}] inline: {snippet}... | type: {type_attr}")
        else:
            print(f"[{idx+1}] empty script | type: {type_attr}")

# Let's also check for importmap
importmap = soup.find('script', type='importmap')
if importmap:
    print("\nImportmap found!")
    try:
        import json
        data = json.loads(importmap.string)
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error parsing importmap: {e}")
