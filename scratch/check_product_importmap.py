import re

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\venison-peas-recipe\index.html"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

importmap_match = re.search(r'<script\s+type="importmap".*?</script>', content, re.DOTALL)
if importmap_match:
    print(importmap_match.group(0)[:800])
else:
    print("No importmap found on product page")
