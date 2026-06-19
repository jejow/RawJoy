import re

original_path = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\full download\cart\index.html"
with open(original_path, 'r', encoding='utf-8') as f:
    content = f.read()

# search for where "Summary" or "Checkout" is mentioned
print("Matches for 'Summary':")
for m in re.finditer(r'class="[^"]*summary[^"]*"|class="[^"]*checkout[^"]*"', content, re.IGNORECASE):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 100)
    print(f"Context: {content[start:end]}\n---")
