import os
import re

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
patterns = [
    (re.compile(r'\bRp\b|\bRp\s*[0-9]'), "Rp"),
    (re.compile(r'id-ID'), "id-ID"),
    (re.compile(r'Keranjang|Kembali|Belanja|Pengiriman|Penerima|Selesai'), "Indonesian Text")
]

ignore_folders = ['.git', '.vscode', 'scratch', 'media', 'node_modules']
# We also want to skip the duplicated js files for this search to find unique HTML/JSON files
ignore_js_copies = True

results = []

for dirpath, dirnames, filenames in os.walk(root_dir):
    # filter out ignored folders
    dirnames[:] = [d for d in dirnames if d not in ignore_folders]
    
    # Skip if we are inside a js folder nested under products/collections/blogs
    rel_dir = os.path.relpath(dirpath, root_dir)
    if ignore_js_copies and ('products' in rel_dir or 'collections' in rel_dir or 'blogs' in rel_dir) and 'js' in rel_dir.split(os.sep):
        continue
        
    for filename in filenames:
        if filename.endswith(('.html', '.json')) or (filename.endswith('.js') and dirpath == os.path.join(root_dir, 'js')):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check patterns
                matched = []
                for regex, name in patterns:
                    if regex.search(content):
                        matched.append(name)
                
                if matched:
                    results.append((os.path.relpath(filepath, root_dir), matched))
            except Exception as e:
                pass

print(f"Found {len(results)} matching files:")
for path, pats in results:
    print(f" - {path}: {pats}")
