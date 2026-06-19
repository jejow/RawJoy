import re

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Search for CartDrawer
matches = [m.start() for m in re.finditer(r"CartDrawer", content)]
print(f"Found {len(matches)} occurrences of 'CartDrawer':")
for idx, pos in enumerate(matches):
    # Find line number
    line_no = content[:pos].count('\n') + 1
    # Print surrounding context
    start = max(0, pos - 150)
    end = min(len(content), pos + 150)
    snippet = content[start:end].replace('\n', ' ')
    print(f"Match {idx+1} at line {line_no}: ... {snippet} ...")
