filepath = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'<script[^>]*src="[^"]*lenis[^"]*"', content, re.IGNORECASE))
print(f"Script tags loading lenis in index.html: {len(matches)}")
for m in matches:
    print(m.group(0))
