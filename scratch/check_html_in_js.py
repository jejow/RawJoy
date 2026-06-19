import os

js_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js"

for root, dirs, files in os.walk(js_dir):
    for file in files:
        if file.endswith('.js'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
            if content.startswith('<'):
                print(f"ERROR: JS file {os.path.relpath(filepath, js_dir)} starts with '<'!")
                print(content[:200])
                print("-" * 50)
