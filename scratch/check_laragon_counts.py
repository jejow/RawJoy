import os
import re

laragon_root = r"c:\laragon\www\RawJoy"

def check_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    found = False
    for match in re.finditer(r'Bone\s+Broth', content, re.IGNORECASE):
        start = match.start()
        chunk = content[start:start+150]
        if "18" in chunk:
            print(f"Laragon File {filepath} has 'Bone Broth' near '18':\n{repr(chunk)}\n")
            found = True
            
    for match in re.finditer(r'Treats', content, re.IGNORECASE):
        start = match.start()
        chunk = content[start:start+150]
        if "17" in chunk:
            print(f"Laragon File {filepath} has 'Treats' near '17':\n{repr(chunk)}\n")
            found = True
            
    return found

count = 0
for root, dirs, files in os.walk(laragon_root):
    for file in files:
        if file.endswith(".html"):
            if check_file(os.path.join(root, file)):
                count += 1

print(f"Laragon Scan complete. Found {count} files with old count indicators.")
