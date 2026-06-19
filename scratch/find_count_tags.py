import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\colostrum\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's search for any div or span or p that contains product count, e.g., "products"
matches = re.finditer(r'<[^>]+(?:product-count|product_count|count|results-count)[^>]*>.*?</[^>]+>', content, re.IGNORECASE | re.DOTALL)
for m in list(matches)[:10]:
    print(m.group(0)[:500])
    print("="*50)

# Let's search for "product" in tag text
text_matches = re.finditer(r'>\s*\d+\s+products?\s*<', content, re.IGNORECASE)
for m in text_matches:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 100)
    print("FOUND COUNT TEXT PATTERN:")
    print(content[start:end])
    print("="*50)
