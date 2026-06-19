import re

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\css\theme.css"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find selectors
classes = set(re.findall(r'\.([a-zA-Z0-9_\-]+)', content))
search_classes = sorted([c for c in classes if "search" in c.lower() or "predictive" in c.lower()])

print(f"Found {len(search_classes)} search/predictive classes:")
for c in search_classes:
    print(c)
