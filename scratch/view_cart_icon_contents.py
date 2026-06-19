file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
matches = re.finditer(r'<a\s+[^>]*class="[^"]*cart-icon[^"]*".*?</a>', content, re.DOTALL)
for m in matches:
    print(m.group(0))
