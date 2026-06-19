import re
import json

path = 'products/venison-peas-recipe/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all scripts with data-variants-cache
matches = re.findall(r'<script\s+data-variants-cache=""\s+type="application/json">\s*(.*?)\s*</script>', content, re.DOTALL)
print(f"Found {len(matches)} cache scripts")
for idx, m in enumerate(matches):
    try:
        data = json.loads(m)
        print(f"Script {idx+1}:")
        for v in data.get('variants', []):
            print(f"  ID: {v.get('id')}, Title: {v.get('title')}, Price: {v.get('price')}")
    except Exception as e:
        print(f"Error parsing script {idx+1}: {e}")
