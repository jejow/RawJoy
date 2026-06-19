import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
bridge_path = os.path.join(workspace_root, "js", "db-bridge.js")

with open(bridge_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

lines = content.splitlines()
print("Searching for slug in db-bridge.js:")
found = False
for idx, line in enumerate(lines):
    if "slug" in line.lower():
        print(f"  Line {idx+1}: {line.strip()}")
        found = True

if not found:
    print("  No occurrences of 'slug' found.")
