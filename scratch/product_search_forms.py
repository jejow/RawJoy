import os
import re

search_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products"
actions = set()

for root, dirs, files in os.walk(search_path):
    for f in files:
        if f.endswith(".html"):
            full_path = os.path.join(root, f)
            try:
                with open(full_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    matches = re.findall(r'<form[^>]*action="([^"]*search[^"]*)"', content)
                    for m in matches:
                        actions.add(m)
            except Exception as e:
                pass

print("Form actions found in product pages:")
for a in actions:
    print(a)
