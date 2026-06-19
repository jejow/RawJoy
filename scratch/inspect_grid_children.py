import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\colostrum\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Find the product-grid UL
grid_match = re.search(r'<ul[^>]*class="[^"]*product-grid[^"]*"[^>]*>(.*?)</ul>', content, re.DOTALL)
if grid_match:
    grid_content = grid_match.group(1)
    # Print first 2000 characters of children inside the grid
    print("=== Start of Grid Content ===")
    print(grid_content[:2000])
    
    # Check what the first child tag is
    child_match = re.match(r'^\s*<(\w+)', grid_content)
    if child_match:
        print(f"\nFirst child tag: {child_match.group(1)}")
else:
    print("Product grid not found")
