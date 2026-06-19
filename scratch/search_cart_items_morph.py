import os

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js\cart-items.js"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's search for "morph" in cart-items.js
idx = 0
while True:
    idx = content.find("morph", idx)
    if idx == -1:
        break
    start = max(0, idx - 100)
    end = min(len(content), idx + 200)
    print(f"Found at {idx}:\n... {content[start:end]} ...\n")
    idx += 5
