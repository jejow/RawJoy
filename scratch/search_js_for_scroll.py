import re
import os

js_dir = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\cart\js"
print("Searching in JS files for scroll or sticky:")
for filename in os.listdir(js_dir):
    if filename.endswith('.js'):
        filepath = os.path.join(js_dir, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        matches = re.findall(r'scroll|sticky-element|stickyElement', content, re.IGNORECASE)
        if matches:
            print(f"File: {filename} matches count: {len(matches)}")
            # print some contexts
            for m in re.finditer(r'scroll|sticky-element|stickyElement', content, re.IGNORECASE):
                start = max(0, m.start() - 60)
                end = min(len(content), m.end() + 60)
                print(f"  Context: {content[start:end].strip()}")
                print("  ---")
