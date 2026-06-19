import os
import re

js_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js"
terms = ["CartAddEvent", "CartUpdateEvent", "CartErrorEvent", "sections", "morph", "replaceChildren"]

for file in os.listdir(js_dir):
    if not file.endswith(".js"):
        continue
    file_path = os.path.join(js_dir, file)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    found = []
    for term in terms:
        if term in content:
            found.append(term)
    if found:
        print(f"{file}: contains {', '.join(found)}")
