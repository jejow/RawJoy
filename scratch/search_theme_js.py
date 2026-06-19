import re

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js\theme.js"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js\theme.js"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print("Length of theme.js:", len(content))

# Look for HTML-like tags (e.g., <div, </script, etc.)
html_tags = re.findall(r'<\s*/?\s*[a-zA-Z]+(?:\s+[^>]*?)?>', content)
print(f"Found {len(html_tags)} HTML-like tags in theme.js.")
for tag in html_tags[:10]:
    print("  Tag:", tag)

