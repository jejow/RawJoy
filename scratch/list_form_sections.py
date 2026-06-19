import sys
import re

if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

matches = re.finditer(r'<product-form-component([^>]*)>', content)
for idx, m in enumerate(matches):
    attrs = m.group(1)
    # Extract data-product-id and data-section-id
    pid = re.search(r'data-product-id="([^"]*)"', attrs)
    sid = re.search(r'data-section-id="([^"]*)"', attrs)
    pid_val = pid.group(1) if pid else "None"
    sid_val = sid.group(1) if sid else "None"
    print(f"Index {idx+1}: product-id={pid_val}, section-id={sid_val}")
