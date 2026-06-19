import os
import re

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
patterns = [
    (re.compile(r'\bRp\b|\bRp\s*[0-9]'), "Rp"),
    (re.compile(r'id-ID'), "id-ID"),
    (re.compile(r'toLocaleString\s*\(\s*[\'"]id-ID[\'"]'), "toLocaleString('id-ID'")
]

ignore_folders = ['.git', '.vscode', 'scratch', 'media', 'node_modules']

for dirpath, dirnames, filenames in os.walk(root_dir):
    # filter out ignored folders
    dirnames[:] = [d for d in dirnames if d not in ignore_folders]
    for filename in filenames:
        if filename.endswith(('.html', '.js', '.json')):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    for regex, name in patterns:
                        if regex.search(line):
                            rel_path = os.path.relpath(filepath, root_dir)
                            print(f"{rel_path}:{i+1} [{name}]: {line.strip()}")
            except Exception as e:
                pass
