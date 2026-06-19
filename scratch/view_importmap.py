import re

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\rawjoy-blue-energy-bar\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all script blocks
matches = re.finditer(r'<script.*?>.*?</script>', content, re.DOTALL)
for m in matches:
    tag = m.group(0)
    # Print first 200 chars of script tag
    if 'importmap' in tag or 'src=' in tag:
        print("MATCHED TAG:")
        print(tag[:500])
        print("-" * 40)
