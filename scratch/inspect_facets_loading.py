import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\colostrum\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Search for any script tag containing facets
matches = re.finditer(r'<script[^>]*src="[^"]*facets[^"]*"[^>]*>', content)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 100)
    print(f"Match:\n{content[start:end]}\n" + "="*50)
    
# Let's search if facets is imported inside another js file, e.g. theme.js
# Or let's search for facets in the whole index.html
print("\n=== Search for 'facets' in the whole file ===")
matches2 = re.finditer(r'facets', content, re.IGNORECASE)
count = 0
for m in matches2:
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 50)
    print(f"Match {count}: {content[start:end].strip()}")
    count += 1
    if count >= 15:
        break
