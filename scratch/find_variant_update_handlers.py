import os
import re

search_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

for root, dirs, files in os.walk(search_path):
    if ".git" in root or ".vscode" in root or "node_modules" in root:
        continue
    for file in files:
        if file.endswith(".js"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if "variantChanged" in content or "variantId" in content or "variant-picker" in content:
                    print(f"File: {file_path}")
                    # Print lines containing the match
                    lines = content.split("\n")
                    for idx, line in enumerate(lines):
                        if "variantId" in line or "variantChanged" in line or 'name="id"' in line or "name = 'id'" in line or 'name=\'id\'' in line:
                            print(f"  Line {idx+1}: {line[:200].strip()}")
            except Exception as e:
                pass
