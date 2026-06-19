import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
bridge_path = os.path.join(workspace_root, "js", "db-bridge.js")

with open(bridge_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

lines = content.splitlines()
found = False
for idx, line in enumerate(lines):
    if "async get(" in line or "get: async function" in line or "get: function" in line:
        print(f"Definition found on line {idx+1}: {line.strip()}")
        # print 50 lines following
        for i in range(idx, min(idx + 50, len(lines))):
            print(f"  Line {i+1}: {lines[i]}")
        found = True
        break

if not found:
    # check for cart object methods
    for idx, line in enumerate(lines):
        if "cart = {" in line or "const cart =" in line:
            print(f"Cart object found on line {idx+1}: {line.strip()}")
            for i in range(idx, min(idx + 100, len(lines))):
                print(f"  Line {i+1}: {lines[i]}")
            found = True
            break
