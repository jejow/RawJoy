import os

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\venison-peas-recipe\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Searching for JS references in index.html:")
for i, line in enumerate(lines):
    if '.js' in line:
        # print line index and content (first 100 chars)
        print(f"Line {i+1}: {line.strip()[:150]}")
