import re
import json
import os

price_map = {
    'beef-spinach-stew': 12.0,
    'cat-calming-formula': 22.0,
    'cat-wellness-mix': 23.0,
    'chicken-bone-treat': 22.0,
    'chicken-herb-stick': 22.0,
    'chicken-pumpkin-pate': 23.0,
    'crunchy-bone-treat': 23.0,
    'doggy-dental-mix': 15.0,
    'duck-soft-chews': 22.0,
    'fish-bone-treat': 22.0,
    'juicy-turkey-crunch': 15.0,
    'juicy-turkey-stick': 22.0,
    'lamb-quinoa-blend': 22.0,
    'mackerel-salmon-kibble': 23.0,
    'mint-comfort-bowl-series': 22.0,
    'pet-meal-time-mix': 22.0,
    'rawjoy-blue-energy-bar': 22.0,
    'rawjoy-green-bar': 22.0,
    'rawjoy-soft-bar': 12.0,
    'salmon-broccoli-crunch': 15.0,
    'salmon-carrot-pate': 23.0,
    'salmon-rice-formula': 23.0,
    'salmon-stick': 22.0,
    'venison-peas-recipe': 12.0
}

name_to_slug = {
    'Beef Spinach': 'beef-spinach-stew',
    'Cat Calming': 'cat-calming-formula',
    'Cat Wellness': 'cat-wellness-mix',
    'Chicken Bone': 'chicken-bone-treat',
    'Chicken Herb': 'chicken-herb-stick',
    'Chicken Pa\u0302te\u0301': 'chicken-pumpkin-pate',
    'Chicken P\u00e2t\u00e9': 'chicken-pumpkin-pate',
    'Chicken P\u00e2te': 'chicken-pumpkin-pate',
    'Chicken Pate': 'chicken-pumpkin-pate',
    'Chicken Pa\u0302te': 'chicken-pumpkin-pate',
    'Crunchy Bone': 'crunchy-bone-treat',
    'Chicken & Carrots': 'doggy-dental-mix',
    'Duck Soft Chews': 'duck-soft-chews',
    'Fish Bone': 'fish-bone-treat',
    'Juicy Turkey Crunch': 'juicy-turkey-crunch',
    'Juicy Turkey': 'juicy-turkey-stick',
    'Lamb Quinoa': 'lamb-quinoa-blend',
    'Mackerel Salmon': 'mackerel-salmon-kibble',
    'Mint Bowl': 'mint-comfort-bowl-series',
    'Pet Meal Mix': 'pet-meal-time-mix',
    'Blue Bowl': 'rawjoy-blue-energy-bar',
    'Doggy Dental Biscuit': 'rawjoy-green-bar',
    'RawJoy Soft Bar': 'rawjoy-soft-bar',
    'Salmon Broccoli': 'salmon-broccoli-crunch',
    'Salmon Carrot': 'salmon-carrot-pate',
    'Salmon Rice': 'salmon-rice-formula',
    'Salmon Stick': 'salmon-stick',
    'Venison Peas': 'venison-peas-recipe'
}

def get_base_price(identifier):
    if not identifier:
        return None
    if identifier in price_map:
        return price_map[identifier]
    clean_id = identifier.split('/')[-1].split('?')[0].split('#')[0]
    if clean_id in price_map:
        return price_map[clean_id]
    if identifier in name_to_slug:
        slug = name_to_slug[identifier]
        return price_map[slug]
    for name, slug in name_to_slug.items():
        if name in identifier or identifier in name:
            return price_map[slug]
    for slug in price_map:
        if slug in clean_id or clean_id in slug:
            return price_map[slug]
    return None

mapping = {}

def extract_variants_from_obj(obj, default_handle=None):
    if isinstance(obj, dict):
        current_handle = default_handle
        for key in ['handle', 'slug', 'url', 'id']:
            val = obj.get(key)
            if isinstance(val, (str, int)):
                val_str = str(val)
                if get_base_price(val_str) is not None:
                    current_handle = val_str
                    break
        
        # Check if this object itself is a variant
        variant_id = obj.get('id')
        if variant_id and (isinstance(variant_id, int) or (isinstance(variant_id, str) and variant_id.isdigit())):
            # Determine weight name
            weight_name = None
            for key in ['title', 'public_title', 'option1', 'name']:
                val = obj.get(key)
                if isinstance(val, str):
                    if '100gr' in val:
                        weight_name = '100gr'
                        break
                    elif '150gr' in val:
                        weight_name = '150gr'
                        break
                    elif '200gr' in val:
                        weight_name = '200gr'
                        break
            
            if not weight_name:
                options = obj.get('options')
                if isinstance(options, list):
                    for opt in options:
                        if isinstance(opt, str):
                            if '100gr' in opt:
                                weight_name = '100gr'
                            elif '150gr' in opt:
                                weight_name = '150gr'
                            elif '200gr' in opt:
                                weight_name = '200gr'
            
            # If we found a weight name and we have a valid slug, map it
            if weight_name and current_handle:
                # Resolve slug
                slug = current_handle.split('/')[-1].split('?')[0].split('#')[0]
                if slug in name_to_slug:
                    slug = name_to_slug[slug]
                if slug in price_map:
                    mapping[str(variant_id)] = {
                        "slug": slug,
                        "variantName": weight_name
                    }
        
        # Recursively search children
        for k, v in obj.items():
            extract_variants_from_obj(v, current_handle)
            
    elif isinstance(obj, list):
        for item in obj:
            extract_variants_from_obj(item, default_handle)

def process_html_file(file_path):
    default_handle = None
    parts = file_path.replace('\\', '/').split('/')
    if 'products' in parts:
        prod_idx = parts.index('products')
        if prod_idx + 1 < len(parts):
            default_handle = parts[prod_idx + 1]
            if default_handle.endswith('__temp'):
                default_handle = default_handle[:-6]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Parse <script data-variants-cache> blocks
        for match in re.finditer(r'<script\s+data-variants-cache=""\s+type="application/json">\s*(.*?)\s*</script>', content, re.DOTALL):
            try:
                data = json.loads(match.group(1))
                extract_variants_from_obj(data, default_handle)
            except Exception:
                pass

        # 2. Parse var meta block
        for match in re.finditer(r'var\s+meta\s*=\s*(\{.*?\});', content):
            try:
                data = json.loads(match.group(1))
                extract_variants_from_obj(data, default_handle)
            except Exception:
                pass

        # 3. Parse application/ld+json blocks
        for match in re.finditer(r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>', content, re.DOTALL):
            try:
                data = json.loads(match.group(1))
                extract_variants_from_obj(data, default_handle)
            except Exception:
                pass

        # 4. Parse initData inside wpmLoader
        for match in re.finditer(r'initData:\s*(\{.*?\})\s*,\s*\}\s*,', content):
            try:
                data = json.loads(match.group(1))
                extract_variants_from_obj(data, default_handle)
            except Exception:
                pass

        # 5. Parse generic application/json scripts
        for match in re.finditer(r'<script\s+([^>]*type="application/json"[^>]*)>\s*(.*?)\s*</script>', content, re.DOTALL):
            tag_attrs = match.group(1)
            if 'data-variants-cache' in tag_attrs:
                continue
            try:
                data = json.loads(match.group(2))
                extract_variants_from_obj(data, default_handle)
            except Exception:
                pass
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # Scan all HTML files
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.vscode' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                process_html_file(os.path.join(root, file))
                
    print(f"Found {len(mapping)} variants in total.")
    
    # Save the mapping to a temporary JSON file so we can read/inspect it
    with open('scratch/variant_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)
    print("Saved to scratch/variant_mapping.json")

if __name__ == '__main__':
    main()
