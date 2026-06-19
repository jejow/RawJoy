with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
match = re.search(r'class="variant-option variant-option--fieldset variant-option--buttons"', content)
if match:
    start = match.start()
    print(content[start:start+3000])
else:
    print("Not found")
