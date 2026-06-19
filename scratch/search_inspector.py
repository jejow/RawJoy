import re

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
search_matches = []
for idx, line in enumerate(lines):
    if "search" in line.lower():
        search_matches.append((idx + 1, line.strip()))

print(f"Matches count: {len(search_matches)}")
for num, content in search_matches[:50]:
    print(f"Line {num}: {content[:100]}")
