with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
# Look for custom scripts or inline event listeners
matches = re.finditer(r'<script[^>]*>.*?</script>', content, re.IGNORECASE | re.DOTALL)
for m in matches:
    script = m.group(0)
    if "addEventListener" in script or "click" in script or "change" in script:
        if "google-analytics" not in script and "trekkie" not in script and "Shopify" not in script:
            print("Found potential custom script:")
            print(script[:1000])
            print("-" * 50)
