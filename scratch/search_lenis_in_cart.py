filepath = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\cart\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'lenis', content, re.IGNORECASE))
print(f"Total matches for 'lenis': {len(matches)}")
for m in matches[:5]:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 100)
    print(f"Context: {content[start:end]}\n---")
