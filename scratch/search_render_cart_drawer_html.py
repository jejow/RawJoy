import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
bridge_path = os.path.join(workspace_root, "js", "db-bridge.js")

with open(bridge_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

lines = content.splitlines()
print("Searching for renderCartDrawerHTML in db-bridge.js:")
for idx, line in enumerate(lines):
    if "renderCartDrawerHTML" in line:
        print(f"  Line {idx+1}: {line.strip()}")
