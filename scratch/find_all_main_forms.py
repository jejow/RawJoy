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
    if "template--26013853253922__main" in attrs:
        pos = m.start()
        # Find closing tag of this form component
        end_idx = content.find('</product-form-component>', pos)
        form_content = content[pos:end_idx + len('</product-form-component>')]
        
        # Extract ID of the nested form
        form_id_match = re.search(r'<form[^>]*id="([^"]*)"', form_content)
        form_id = form_id_match.group(1) if form_id_match else "None"
        
        print(f"Index {idx+1}: pos={pos}, form_id={form_id}")
        # Print first 500 chars of form_content
        print(form_content[:500])
        print("-" * 50)
