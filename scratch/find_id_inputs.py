with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
matches = re.finditer(r'<input[^>]*name="id"[^>]*>|<select[^>]*name="id"[^>]*>.*?</select>', content, re.IGNORECASE | re.DOTALL)
for m in matches:
    print(m.group(0))
