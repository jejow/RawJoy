with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
# Find where BuyButtons-ProductSubmitButton- is and search backwards for tags
matches = list(re.finditer(r'BuyButtons-ProductSubmitButton-[A-Za-z0-9_]+__add-to-cart', content))
if matches:
    first_match_idx = matches[0].start()
    # print preceding 1000 characters
    print("Preceding content:")
    print(content[max(0, first_match_idx - 1000):first_match_idx])
else:
    print("No submit buttons found")
