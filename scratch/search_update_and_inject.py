import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
interceptor_path = os.path.join(workspace_root, "js", "cart-interceptor.js")

with open(interceptor_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

lines = content.splitlines()
found = False
for idx, line in enumerate(lines):
    if "function updateAndInjectCart" in line or "updateAndInjectCart = function" in line:
        print(f"Definition found on line {idx+1}: {line.strip()}")
        # print 50 lines following
        for i in range(idx, min(idx + 60, len(lines))):
            print(f"  Line {i+1}: {lines[i]}")
        found = True
        break

if not found:
    # check for any usage or reference
    for idx, line in enumerate(lines):
        if "updateAndInjectCart" in line:
            print(f"Reference on line {idx+1}: {line.strip()}")
