import os
import re

js_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js"
importmap_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"

# Load importmap from index.html
with open(importmap_path, 'r', encoding='utf-8') as f:
    content = f.read()
import re
match = re.search(r'<script\s+type="importmap"\s*>(.*?)</script>', content, re.DOTALL)
import json
importmap = json.loads(match.group(1)) if match else {}
imports = importmap.get("imports", {})

# Check all JS files in js/
count = 0
for root, dirs, files in os.walk(js_dir):
    for file in files:
        if file.endswith('.js'):
            filepath = os.path.join(root, file)
            count += 1
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Find all import statements
            # Find all import statements
            matches = re.findall(r'import\s*.*?\s*from\s*["\'](.*?)["\']', content)
            matches_direct = re.findall(r'import\s*["\'](.*?)["\']', content)
            
            all_imports = set(matches + matches_direct)
            if all_imports:
                print(f"Checking {file} imports: {all_imports}")
            for imp in all_imports:
                # Resolve import
                if imp.startswith('.') or '/' in imp and not imp.startswith('@'):
                    # Relative import, check if file exists
                    imp_path = os.path.normpath(os.path.join(root, imp))
                    if not imp_path.endswith('.js'):
                        imp_path += '.js'
                    if not os.path.exists(imp_path):
                        print(f"FAILED relative import in {file}: {imp} -> {imp_path} (File not found)")
                elif imp in imports:
                    # Mapped import, check if mapped file exists
                    target = imports[imp]
                    target_path = os.path.normpath(os.path.join(js_dir, '..', target))
                    if not os.path.exists(target_path):
                        print(f"FAILED mapped import in {file}: {imp} -> {target_path} (Mapped file not found)")
                else:
                    # Not in importmap and not relative!
                    print(f"FAILED unmapped import in {file}: {imp} (Not in importmap)")

print(f"Total files checked: {count}")
