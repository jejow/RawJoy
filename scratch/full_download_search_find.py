import os
import re

search_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\full download"
query = "PredictiveSearchResults"

matches = []
for root, dirs, files in os.walk(search_path):
    for f in files:
        if f.endswith(".html") or f.endswith(".js"):
            full_path = os.path.join(root, f)
            try:
                with open(full_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    if query in content:
                        matches.append(full_path)
            except Exception as e:
                pass

print(f"Found matches in {len(matches)} files:")
for m in matches[:10]:
    print(m)
