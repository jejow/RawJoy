import re

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\css\theme.css"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find selectors containing search or predictive
matches = re.findall(r'(\.[a-zA-Z0-9_\-\[\]\:\*]+\s*\{[^}]*\})', content)
print(f"Total selectors: {len(matches)}")
search_selectors = []
for m in matches:
    if "search__" in m or "predictive-" in m or "predictive_search" in m:
        search_selectors.append(m)

print(f"Search selectors count: {len(search_selectors)}")
for s in search_selectors[:40]:
    print(s[:200])
    print("-" * 50)
