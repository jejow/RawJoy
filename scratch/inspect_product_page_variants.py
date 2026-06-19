import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\mint-comfort-bowl-series\index.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's search for json scripts
scripts = re.findall(r'<script[^>]*type="application/json"[^>]*>.*?</script>', content, re.DOTALL)
print(f"Total JSON scripts: {len(scripts)}")
for idx, s in enumerate(scripts):
    print(f"\nScript {idx}: {s[:500]} ... len={len(s)}")

# Let's search for variant-picker elements
variant_pickers = re.findall(r'<variant-picker[^>]*>.*?</variant-picker>', content, re.DOTALL)
print(f"\nTotal variant-picker elements: {len(variant_pickers)}")
for idx, vp in enumerate(variant_pickers):
    print(f"\nVariant picker {idx}: {vp[:1000]} ... len={len(vp)}")
