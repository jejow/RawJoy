import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
interceptor_path = os.path.join(workspace_root, "js", "cart-interceptor.js")

with open(interceptor_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

lines = content.splitlines()
found = False
for idx, line in enumerate(lines):
    if "completeLookSection" in line:
        print(f"Line {idx+1}: {line.strip()}")
        found = True

if not found:
    print("No references to completeLookSection found.")
