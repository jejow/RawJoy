filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\cat-calming-formula\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re
scripts = re.findall(r'<script[^>]*src="([^"]*)"', content)
print("Scripts found on product page:")
for s in scripts:
    print(" -", s)
    
# Check if any inline script references db-bridge or cart
db_occurs = [m.start() for m in re.finditer(r'db-bridge', content)]
print(f"Occurrences of 'db-bridge': {len(db_occurs)}")
for idx in db_occurs[:5]:
    print(f"  Snippet: {content[max(0, idx-50):idx+100]}")
