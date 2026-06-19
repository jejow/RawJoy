with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
# Find script tags containing "variant" or "option" or "Size"
matches = re.finditer(r'<script[^>]*>.*?</script>', content, re.IGNORECASE | re.DOTALL)
count = 0
for m in matches:
    script = m.group(0)
    if "variant" in script or "option" in script or "Size" in script or "change" in script:
        if len(script) < 3000:
            print(f"Match {count+1} (small script):")
            print(script)
        else:
            print(f"Match {count+1} (large script, showing first 500 chars):")
            print(script[:500])
        count += 1
