import re
import os

css_dir = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\css"
print("Searching in CSS files for summary/checkout:")
for filename in os.listdir(css_dir):
    if filename.endswith('.css'):
        filepath = os.path.join(css_dir, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        matches = re.findall(r'\.[a-zA-Z0-9_-]*(?:summary|checkout)[a-zA-Z0-9_-]*', content, re.IGNORECASE)
        if matches:
            print(f"\nFile: {filename}")
            print(set(matches))
