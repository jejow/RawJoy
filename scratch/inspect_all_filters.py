import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\all\index.html"
if not os.path.exists(path):
    print("File not found")
    sys.exit(1)

with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print("=== Checkboxes/Inputs in collections/all ===")
inputs = re.findall(r'<input[^>]+(?:name|id)="[^"]*(?:filter|facet)[^"]*"[^>]*>', content, re.IGNORECASE)
for inp in inputs[:30]:
    print(inp)

print("\n=== Select / Sort dropdown in collections/all ===")
selects = re.findall(r'<select[^>]*>.*?</select>', content, re.DOTALL)
for sel in selects:
    options = re.findall(r'<option[^>]*>.*?</option>', sel, re.DOTALL)
    print(sel[:120] + " ... " + str(options))
