import re

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\css\theme.css"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for rules containing search__result-list
matches = re.finditer(r'(\.[a-zA-Z0-9_\-\[\]\:\*\s\>\.\+]+search__result-list[^}]*\})', content)
results = []
for m in matches:
    results.append(m.group(1))

print(f"Found {len(results)} matching rules:")
for r in results:
    print(r)
    print("=" * 60)
