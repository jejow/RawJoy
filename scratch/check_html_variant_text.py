with open('products/venison-peas-recipe/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if '150gr' in line or '50657212498210' in line:
        print(f"Line {idx+1}: {line.strip()[:140]}")
