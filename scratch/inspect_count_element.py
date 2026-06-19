import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\colostrum\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's search for elements containing "product" and a number or count
# Search for class names containing count
matches = re.finditer(r'class="[^"]*(?:count|product-count|summary)[^"]*"', content, re.IGNORECASE)
for m in matches:
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 150)
    print(f"Match: {content[start:end].strip()}\n" + "="*50)
    
# Let's search for the text showing how many products there are
# e.g., "products" or "items"
print("\n=== Searching for products or items text ===")
text_matches = re.finditer(r'(?:products|items|product)', content, re.IGNORECASE)
count = 0
for tm in text_matches:
    start = max(0, tm.start() - 50)
    end = min(len(content), tm.end() + 50)
    print(f"Match {count}: {content[start:end].strip()}")
    count += 1
    if count >= 15:
        break
