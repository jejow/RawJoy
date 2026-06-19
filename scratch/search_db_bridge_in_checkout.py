filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\pages\checkout\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re
scripts = re.findall(r'<script[^>]*src="([^"]*)"', content)
print("Scripts found in checkout/index.html:")
for s in scripts:
    print(" -", s)
