import os
import re

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

def check_file(filepath):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Pattern to find category name and count
    pattern = re.compile(
        r'<span class="reversed-link__text">\s*([^<]+?)\s*</span>\s*</span>\s*<sup class="collection-card__count paragraph">\s*(\d+)\s*</sup>',
        re.IGNORECASE | re.DOTALL
    )
    
    matches = pattern.findall(content)
    if matches:
        rel_path = os.path.relpath(filepath, workspace_root)
        print(f"File: {rel_path}")
        for cat, val in matches:
            print(f"  - {cat.strip()}: {val}")

def scan_dir(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                check_file(os.path.join(root, file))

scan_dir(workspace_root)
