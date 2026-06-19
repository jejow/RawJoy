import json
import sys

if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
matches = re.finditer(r'<product-form-component[^>]*>.*?</product-form-component>', content, re.DOTALL)
for idx, m in enumerate(matches):
    print(f"Product Form Component {idx+1}:")
    print(m.group(0)[:3000])
    print("=" * 60)
