import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\mint-comfort-bowl-series\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print("=== Select tags ===")
selects = re.findall(r'<select[^>]*>.*?</select>', content, re.DOTALL)
for sel in selects[:5]:
    print(sel[:300] + " ... len=" + str(len(sel)))

print("\n=== Radio/Checkbox inputs for variants ===")
variant_inputs = re.findall(r'<input[^>]+(?:variant|option|name="id")[^>]*>', content, re.IGNORECASE)
for inp in variant_inputs[:10]:
    print(inp)
    
print("\n=== Swatches or custom options ===")
swatches = re.findall(r'<div[^>]*class="[^"]*swatch[^"]*"[^>]*>.*?</div>', content, re.DOTALL)
print(f"Total swatches divs: {len(swatches)}")
for sw in swatches[:5]:
    print(sw[:300])
