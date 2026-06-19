import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\colostrum\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Find pagination block
nav_match = re.search(r'<nav aria-label="Pagination"[^>]*>.*?</nav>', content, re.DOTALL)
if not nav_match:
    nav_match = re.search(r'class="pagination".*?</nav>', content, re.DOTALL)
    
if nav_match:
    print("=== Pagination HTML Block ===")
    print(nav_match.group(0))
else:
    print("Pagination block not found")
