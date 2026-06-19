file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# find line matching id="shopify-section-sections--26013853417762__cart-drawer"
start_idx = -1
for i, line in enumerate(lines):
    if 'id="shopify-section-sections--26013853417762__cart-drawer"' in line:
        start_idx = i
        break

if start_idx != -1:
    print(f"Found at line {start_idx+1}")
    for j in range(max(0, start_idx-5), min(len(lines), start_idx + 60)):
        print(f"{j+1}: {lines[j].strip()}")
else:
    print("Not found")
