import os
import re

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
pattern = r'<script\s+[^>]*?3b3c7daf.*?></script>'

count = 0
ignore_folders = ['.git', '.vscode', 'scratch', 'media', 'node_modules']

for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if d not in ignore_folders]
    
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            new_content, n = re.subn(pattern, '', content, flags=re.DOTALL)
            if n > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {n} garbled script tags in {os.path.relpath(filepath, root_dir)}")
                count += 1

print(f"Successfully cleaned syntax errors in {count} HTML files.")
