import re

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\venison-peas-recipe\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for the garbled script tag
pattern = r'<script\s+[^>]*?3b3c7daf.*?></script>'
new_content, count = re.subn(pattern, '', content, flags=re.DOTALL)

print(f"Removed {count} garbled script tags.")

if count > 0:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("File saved successfully.")
else:
    print("No matches found. Let's try matching a smaller part.")
