import re

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\chicken-bone-treat\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# find any occurrence of 418_4 or 419_7 or 420_8
for term in ["418_4", "419_7", "420_8", "418"]:
    matches = [m.start() for m in re.finditer(term, content)]
    print(f"Term '{term}': {len(matches)} matches")
    for idx in matches[:5]:
        start = max(0, idx - 100)
        end = min(len(content), idx + 100)
        print(f"Match at {idx}: {content[start:end].strip()}")
