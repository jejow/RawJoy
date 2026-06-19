import re
import json

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\cat-calming-formula\index.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for "product" in meta tag
m = re.search(r'var\s+meta\s*=\s*(\{.*?\});', content)
if m:
    data = json.loads(m.group(1))
    print("Meta ID:", data.get("product", {}).get("id"))
else:
    print("Meta not found")
