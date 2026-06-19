file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\venison-peas-recipe\index.html"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "cart-interceptor.js" in line or "db-bridge.js" in line or "cart-drawer.js" in line:
        print(f"Line {i+1}: {line.strip()}")
