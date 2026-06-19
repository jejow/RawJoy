import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\colostrum\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's search for lists or grids that hold product cards
# Find all <ul> tags with class containing product-grid or similar
ul_matches = re.finditer(r'<ul[^>]*class="[^"]*grid[^"]*"[^>]*>', content)
for m in ul_matches:
    start = m.start()
    snippet = content[start:start+300]
    print(f"UL Match:\n{snippet}\n" + "="*50)
    
# Let's see how many product-cards are children of a grid
# Let's parse with a simple nested search or regex
# Let's find the section containing the product grid
grid_section_match = re.search(r'<ul[^>]*id="product-grid"[^>]*>(.*?)</ul>', content, re.DOTALL)
if grid_section_match:
    grid_content = grid_section_match.group(1)
    cards = re.findall(r'<product-card[^>]*>', grid_content)
    print(f"Found product-grid with id='product-grid'. It contains {len(cards)} product-cards.")
else:
    print("No product-grid with id='product-grid' found.")
    
# Let's check for any UL with product-grid class
grid_class_match = re.search(r'<ul[^>]*class="[^"]*product-grid[^"]*"[^>]*>(.*?)</ul>', content, re.DOTALL)
if grid_class_match:
    grid_content = grid_class_match.group(1)
    cards = re.findall(r'<product-card[^>]*>', grid_content)
    print(f"Found product-grid with class='product-grid'. It contains {len(cards)} product-cards.")
else:
    print("No product-grid with class='product-grid' found.")
