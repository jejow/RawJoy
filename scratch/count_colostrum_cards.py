import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

colostrum_pages = [
    r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\colostrum\index.html",
    r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\colostrum-1\index.html",
    r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\colostrum-2\index.html"
]

for idx, p in enumerate(colostrum_pages):
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        cards = re.findall(r'<product-card[^>]*>', content)
        print(f"Page {idx+1} ({os.path.basename(os.path.dirname(p))}): {len(cards)} product cards")
    else:
        print(f"Page {idx+1} does not exist: {p}")
