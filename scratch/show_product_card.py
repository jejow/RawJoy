filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("products/cat-calming-formula")
if idx != -1:
    print("Found product card:")
    print(content[idx:idx+2000])
else:
    print("Not found")
