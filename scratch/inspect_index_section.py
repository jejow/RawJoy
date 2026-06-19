filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(3380, 4200):
    if idx < len(lines):
        line = lines[idx]
        if '<script' in line or '</script>' in line or 'theme.js' in line:
            print(f"Line {idx+1}: {line.strip()[:200]}")
