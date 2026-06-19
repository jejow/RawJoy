with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
matches = re.finditer(r'<product-info[^>]*>|<div[^>]*class="[^"]*product__info-container[^"]*"[^>]*>', content)
for m in matches:
    print(m.group(0))
