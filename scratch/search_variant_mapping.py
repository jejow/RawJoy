import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
interceptor_path = os.path.join(workspace_root, "js", "cart-interceptor.js")

with open(interceptor_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Search for the ID in the file
lines = content.splitlines()
found = False
for idx, line in enumerate(lines):
    if "50657359560994" in line or "chicken-bone-treat" in line:
        print(f"Line {idx+1}: {line.strip()}")
        found = True

if not found:
    print("Neither 50657359560994 nor chicken-bone-treat found in variantMapping keys.")
