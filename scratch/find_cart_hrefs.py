import os
import re

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

for dirpath, _, filenames in os.walk(root_dir):
    for f in filenames:
        if f.endswith(".html"):
            path = os.path.join(dirpath, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
            
            # Find occurrences of href="...cart" or similar
            matches = re.findall(r'href="[^"]*cart"', content)
            if matches:
                # print relative path
                rel = os.path.relpath(path, root_dir)
                print(f"{rel}: {matches}")
