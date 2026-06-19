import json
import re
import os
import subprocess

def main():
    # Load the new variant mapping
    with open('scratch/variant_mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    # Format mapping as JS object string
    mapping_lines = []
    for var_id, data in sorted(mapping.items()):
        mapping_lines.append(f'    "{var_id}": {{ "slug": "{data["slug"]}", "variantName": "{data["variantName"]}" }}')
    mapping_js = 'var variantMapping = {\n' + ',\n'.join(mapping_lines) + '\n  };'
    
    # Read cart-interceptor.js
    file_path = 'js/cart-interceptor.js'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace variantMapping definition
    pattern_mapping = r'var variantMapping = \{.*?\};'
    content, count = re.subn(pattern_mapping, mapping_js, content, flags=re.DOTALL)
    print(f"Replaced variantMapping: {count} matches")
    
    # 2. Update radio extraction to only run if !variantName
    old_radio_logic = (
        '        // Try extracting variant name from radio buttons\n'
        '        var container = dialog || card || section || document;\n'
        '        var radio = container.querySelector(\'input[type="radio"]:checked\');\n'
        '        if (radio) variantName = radio.value || null;'
    )
    new_radio_logic = (
        '        // Try extracting variant name from radio buttons\n'
        '        if (!variantName) {\n'
        '          var container = dialog || card || section || document;\n'
        '          var radio = container.querySelector(\'input[type="radio"]:checked\');\n'
        '          if (radio) variantName = radio.value || null;\n'
        '        }'
    )
    content, count = re.subn(re.escape(old_radio_logic), new_radio_logic, content)
    print(f"Updated radio button extraction logic: {count} matches")
    
    # 3. Add final override logic before the return statement
    old_return_logic = (
        "    console.log('[Cart] Extracted:', name, slug, '$' + price);\n"
        "    return { id: slug || String(variantId), name: name || slug, slug: slug, price: price, image: image, variant: variantName };"
    )
    new_return_logic = (
        "    // Final variant price resolution using the resolved variantName\n"
        "    if (cachedProduct && variantName && cachedProduct.variants) {\n"
        "      for (var v = 0; v < cachedProduct.variants.length; v++) {\n"
        "        if (cachedProduct.variants[v].name === variantName) {\n"
        "          price = cachedProduct.variants[v].price;\n"
        "          break;\n"
        "        }\n"
        "      }\n"
        "    }\n\n"
        "    console.log('[Cart] Extracted:', name, slug, '$' + price);\n"
        "    return { id: slug || String(variantId), name: name || slug, slug: slug, price: price, image: image, variant: variantName };"
    )
    content, count = re.subn(re.escape(old_return_logic), new_return_logic, content)
    print(f"Updated final price lookup logic: {count} matches")
    
    # Write updated content back to js/cart-interceptor.js
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully updated {file_path}")
    
    # Run the propagation script
    print("Running scratch/propagate_interceptor.py...")
    result = subprocess.run(['python', 'scratch/propagate_interceptor.py'], capture_output=True, text=True)
    print("Stdout:", result.stdout)
    print("Stderr:", result.stderr)

if __name__ == '__main__':
    main()
