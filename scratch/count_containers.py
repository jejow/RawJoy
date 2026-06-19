with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re

# Find position of product-information__details
container_match = re.search(r'class="[^"]*product-information__details[^"]*"', content)
if container_match:
    container_start = container_match.start()
    # Let's find all product-form-component tags on the page
    form_matches = list(re.finditer(r'<product-form-component([^>]*)>', content))
    print(f"Total product-form-component: {len(form_matches)}")
    for idx, m in enumerate(form_matches):
        attrs = m.group(1)
        pid = re.search(r'data-product-id="([^"]*)"', attrs)
        sid = re.search(r'data-section-id="([^"]*)"', attrs)
        pid_val = pid.group(1) if pid else "None"
        sid_val = sid.group(1) if sid else "None"
        
        pos = m.start()
        # Find if it is before or after container_start
        rel_pos = "Inside / After container" if pos > container_start else "Before container"
        print(f"Index {idx+1}: pos={pos} ({rel_pos}), product-id={pid_val}, section-id={sid_val}")
else:
    print("Container not found")
