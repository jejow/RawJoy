import os

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\salmon-stick\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

found = False
for i, line in enumerate(lines):
    if '<product-price' in line:
        print(f"Line {i+1}:")
        for j in range(max(0, i-5), min(len(lines), i+15)):
            print(f"  {j+1}: {lines[j].strip()}")
        found = True
        # Let's print all occurrences of <product-price
        print("-" * 40)

if not found:
    print("No <product-price tag found in the HTML.")
