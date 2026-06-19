import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
interceptor_path = os.path.join(workspace_root, "js", "cart-interceptor.js")

with open(interceptor_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

lines = content.splitlines()
found = False
for idx, line in enumerate(lines):
    if "function buildSectionsHTML" in line:
        print(f"Definition found on line {idx+1}: {line.strip()}")
        # print 80 lines following
        for i in range(idx, min(idx + 120, len(lines))):
            print(f"  Line {i+1}: {lines[i]}")
        found = True
        break
