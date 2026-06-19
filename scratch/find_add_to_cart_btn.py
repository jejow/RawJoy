file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\venison-peas-recipe\index.html"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
# Find buttons with "add to cart" in text or class
matches = re.finditer(r'<button[^>]*>.*?</button>', content, re.IGNORECASE | re.DOTALL)
count = 0
for m in matches:
    btn = m.group(0)
    if "add-to-cart" in btn.lower() or "add to cart" in btn.lower() or "submit" in btn.lower():
        print(f"Match: {btn[:300]}")
        count += 1
print(f"Total matches: {count}")
