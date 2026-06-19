with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re
# Find product-information__details start
container_match = re.search(r'<div[^>]*class="[^"]*product-information__details[^"]*"[^>]*>', content)
if container_match:
    start_pos = container_match.start()
    # Let's find the closing tag for this div. Since it could be nested, we can find the next few product-form-components
    # and also look for variant-picker tags.
    # Let's print the next 25000 characters from start_pos
    snippet = content[start_pos:start_pos + 25000]
    
    # Count how many <product-form-component and <variant-picker are inside this snippet
    picker_matches = list(re.finditer(r'<variant-picker', snippet))
    form_matches = list(re.finditer(r'<product-form-component', snippet))
    print(f"Inside snippet of length 25000:")
    print(f"  Variant Pickers: {len(picker_matches)}")
    print(f"  Product Form Components: {len(form_matches)}")
    
    # Print the attributes of the variant pickers and forms found in the snippet
    for i, m in enumerate(picker_matches):
        p_idx = start_pos + m.start()
        tag_end = content[p_idx:p_idx+300].split('>')[0] + '>'
        print(f"    Picker {i+1}: {tag_end}")
    for i, m in enumerate(form_matches):
        f_idx = start_pos + m.start()
        tag_end = content[f_idx:f_idx+300].split('>')[0] + '>'
        print(f"    Form {i+1}: {tag_end}")
else:
    print("Container not found")
