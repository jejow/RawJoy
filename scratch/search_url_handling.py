import os
import re

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

def check_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    if "window.location.search" in content or ".search" in content or "q=" in content:
        # Check specifically for things related to "q" parameter
        if 'q=' in content or 'URLSearchParams' in content:
            rel_path = os.path.relpath(filepath, workspace_root)
            print(f"File: {rel_path}")
            # Find lines containing search location or search parameters
            lines = content.splitlines()
            for idx, line in enumerate(lines):
                if any(x in line for x in ["search", "URLSearchParams", "getParameterByName", "query"]):
                    if any(y in line for y in ["q", "location", "replace", "href"]):
                        print(f"  Line {idx+1}: {line.strip()}")

for root, dirs, files in os.walk(workspace_root):
    for file in files:
        if file.endswith((".js", ".html")):
            if "node_modules" not in root and ".git" not in root:
                check_file(os.path.join(root, file))
