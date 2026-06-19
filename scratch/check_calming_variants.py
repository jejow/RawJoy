import json
import re

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\cat-calming-formula\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'<script\s+data-variants-cache=\"\"\s+type=\"application/json\">\s*(.*?)\s*</script>', content, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    for v in data.get('variants', []):
        print(f"ID: {v.get('id')} | Title: {v.get('title')} | Price: {v.get('price')} | Compare: {v.get('compare_at_price')}")
else:
    print("No data-variants-cache found")
