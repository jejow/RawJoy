import re

path = 'products/venison-peas-recipe/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for variant select or fieldset options
matches = re.findall(r'<option[^>]*>.*?</option>', content)
print("Option tags:")
for m in matches[:15]:
    print(m)

# Find variant picker code
picker = re.findall(r'<variant-picker.*?</variant-picker>', content, re.DOTALL)
print("\nVariant picker tag found:", len(picker) > 0)
if picker:
    print(picker[0][:500])

# Check json script with id containing 'ProductJSON' or similar
json_scripts = re.findall(r'<script[^>]*type="application/json"[^>]*>.*?</script>', content, re.DOTALL)
print("\nJSON script tags count:", len(json_scripts))
for js in json_scripts:
    if '100g' in js or '150g' in js or '200g' in js or '12.0' in js:
        print(js[:300])
