with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
matches = list(re.finditer(r'BuyButtons-ProductSubmitButton-AdWhwTml0SnM5NHZJM__add-to-cart', content))
if matches:
    idx = matches[0].start()
    preceding = content[max(0, idx - 30000):idx]
    
    tags = re.findall(r'<(div|section|product-info|product-form)\s+[^>]*class="([^"]*)"[^>]*>', preceding)
    print("Nearest parent tags containing 'product' (in reverse order):")
    for t in reversed(tags):
        cl = t[1]
        if 'product' in cl or 'section' in cl:
            print(f"  <{t[0]} class='{cl}'>")
else:
    print("Main button not found")
