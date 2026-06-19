filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js\cart-interceptor.js"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Rp' in line or 'id-ID' in line or 'Rupiah' in line:
        print(f"Line {i+1}: {line.strip()}")
