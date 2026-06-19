import os

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products\salmon-stick\index.html"
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's search for "price" or "compare" or "regular"
    import re
    # Find all occurrences of class containing price
    matches = re.findall(r'<[^>]*class="[^"]*price[^"]*"[^>]*>.*?<\/[^>]+>', content, re.IGNORECASE)
    print("Matches containing 'price' in class:")
    for m in matches[:15]:
        print(m[:120])
else:
    print("File not found")
