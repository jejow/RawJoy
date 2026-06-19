with open(r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for idx in range(2150, 2185):
    if idx < len(lines):
        print(f"{idx+1}: {lines[idx].strip()[:200]}")
