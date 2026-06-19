import re

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\css\theme.css"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for rules containing search__
matches = re.finditer(r'(\.[a-zA-Z0-9_\-\[\]\:\*]+\s*\{[^}]*\})', content)
results = []
for m in matches:
    rule = m.group(1)
    if "search__result" in rule or "search__item" in rule or "search__no-results" in rule:
        results.append(rule)

print(f"Found {len(results)} matching rules:")
for r in results:
    print(r)
    print("=" * 60)
