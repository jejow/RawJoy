import json
import re
import os

# Define the price map
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

# Add name mappings
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

def update_variant_dict(variant_obj, default_handle=None):
    product_handle = default_handle
    product_info = variant_obj.get('product')
    if isinstance(product_info, dict):
        url = product_info.get('url') or product_info.get('handle') or product_info.get('title')
        if url:
            product_handle = url

    weight = None
    for key in ['title', 'public_title', 'option1', 'name']:
        val = variant_obj.get(key)
        if isinstance(val, str):
            if '100gr' in val:
                weight = 100
                break
            elif '150gr' in val:
                weight = 150
                break
            elif '200gr' in val:
                weight = 200
                break
    
    if not weight:
        options = variant_obj.get('options')
        if isinstance(options, list):
            for opt in options:
                if isinstance(opt, str):
                    if '100gr' in opt:
                        weight = 100
                    elif '150gr' in opt:
                        weight = 150
                    elif '200gr' in opt:
                        weight = 200
    
    if not weight:
        return False
        
    base_price = get_base_price(product_handle)
    if base_price is None:
        return False
        
    if weight == 100:
        new_price = base_price
    elif weight == 150:
        new_price = base_price * 1.5
    elif weight == 200:
        new_price = base_price * 2.0
    else:
        return False
        
    updated = False
    
    # 1. Price as dict: {"price": {"amount": 12.0, "currencyCode": "USD"}}
    if 'price' in variant_obj and isinstance(variant_obj['price'], dict):
        old_val = variant_obj['price'].get('amount')
        if old_val != new_price:
            variant_obj['price']['amount'] = new_price
            updated = True
        
    # 2. Price as float/int
    elif 'price' in variant_obj:
        old_val = variant_obj['price']
        if isinstance(old_val, (int, float)):
            if old_val > 100:
                expected = int(new_price * 100)
            else:
                expected = new_price
            if old_val != expected:
                variant_obj['price'] = expected
                updated = True
        elif isinstance(old_val, str):
            if '.' in old_val:
                expected = f"{new_price:.2f}"
            else:
                expected = str(int(new_price * 100))
            if old_val != expected:
                variant_obj['price'] = expected
                updated = True

    # 3. Schema offers: "offers": {"price": "12.00", ...}
    if 'offers' in variant_obj and isinstance(variant_obj['offers'], dict):
        offers = variant_obj['offers']
        if 'price' in offers:
            old_val = offers['price']
            if isinstance(old_val, str):
                expected = f"{new_price:.2f}"
                if old_val != expected:
                    offers['price'] = expected
                    updated = True
            elif isinstance(old_val, (int, float)):
                if old_val > 100:
                    expected = int(new_price * 100)
                else:
                    expected = new_price
                if old_val != expected:
                    offers['price'] = expected
                    updated = True
                
    return updated

def traverse_and_update(obj, default_handle=None):
    updated = False
    if isinstance(obj, dict):
        current_handle = default_handle
        for key in ['handle', 'slug', 'url', 'id']:
            val = obj.get(key)
            if isinstance(val, (str, int)):
                val_str = str(val)
                if get_base_price(val_str) is not None:
                    current_handle = val_str
                    break
        
        variants_keys = ['variants', 'hasVariant', 'productvariants', 'productVariants']
        has_variants_list = False
        for vk in variants_keys:
            v_list = obj.get(vk)
            if isinstance(v_list, list):
                has_variants_list = True
                for item in v_list:
                    if isinstance(item, dict):
                        if update_variant_dict(item, current_handle):
                            updated = True
                        if traverse_and_update(item, current_handle):
                            updated = True
                            
        if not has_variants_list:
            if update_variant_dict(obj, default_handle):
                updated = True
                
        for k, v in obj.items():
            if k not in variants_keys:
                if traverse_and_update(v, current_handle):
                    updated = True
                    
    elif isinstance(obj, list):
        for item in obj:
            if traverse_and_update(item, default_handle):
                updated = True
                
    return updated

def update_seed_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated = False
        for p in data.get('products', []):
            product_slug = p.get('slug')
            if product_slug and product_slug in price_map:
                variants = p.get('variants', [])
                for v in variants:
                    if update_variant_dict(v, product_slug):
                        updated = True
                        
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Updated JSON seed: {file_path}")
            return True
    except Exception as e:
        print(f"Error updating JSON seed {file_path}: {e}")
    return False

def update_html_file(file_path):
    # Infer default handle from directory name if it's under products/
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
            
        updated = False
        new_content = content
        
        # 1. Update <script data-variants-cache> blocks
        def replace_variants_cache(match):
            nonlocal updated
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                if traverse_and_update(data, default_handle):
                    updated = True
                    return f'<script data-variants-cache="" type="application/json">\n      {json.dumps(data, indent=2)}\n    </script>'
            except Exception as e:
                pass
            return match.group(0)

        new_content = re.sub(
            r'<script\s+data-variants-cache=""\s+type="application/json">\s*(.*?)\s*</script>',
            replace_variants_cache,
            new_content,
            flags=re.DOTALL
        )

        # 2. Update var meta block
        def replace_meta(match):
            nonlocal updated
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                if traverse_and_update(data, default_handle):
                    updated = True
                    return f'var meta = {json.dumps(data, separators=(",", ":"))};'
            except Exception as e:
                pass
            return match.group(0)

        new_content = re.sub(
            r'var\s+meta\s*=\s*(\{.*?\});',
            replace_meta,
            new_content
        )

        # 3. Update application/ld+json blocks
        def replace_ld_json(match):
            nonlocal updated
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                if traverse_and_update(data, default_handle):
                    updated = True
                    return f'<script type="application/ld+json">{json.dumps(data, separators=(",", ":"))}</script>'
            except Exception as e:
                pass
            return match.group(0)

        new_content = re.sub(
            r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
            replace_ld_json,
            new_content,
            flags=re.DOTALL
        )

        # 4. Update initData inside wpmLoader
        def replace_init_data(match):
            nonlocal updated
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                if traverse_and_update(data, default_handle):
                    updated = True
                    return f'initData: {json.dumps(data, separators=(",", ":"))},'
            except Exception as e:
                pass
            return match.group(0)

        new_content = re.sub(
            r'initData:\s*(\{.*?\})\s*,\s*\}\s*,',
            replace_init_data,
            new_content
        )

        # 5. Update generic application/json scripts (other than variants cache)
        def replace_generic_json(match):
            nonlocal updated
            tag_attrs = match.group(1)
            json_str = match.group(2)
            if 'data-variants-cache' in tag_attrs:
                return match.group(0)
            try:
                data = json.loads(json_str)
                if traverse_and_update(data, default_handle):
                    updated = True
                    return f'<script {tag_attrs}>{json.dumps(data, separators=(",", ":"))}</script>'
            except Exception as e:
                pass
            return match.group(0)

        new_content = re.sub(
            r'<script\s+([^>]*type="application/json"[^>]*)>\s*(.*?)\s*</script>',
            replace_generic_json,
            new_content,
            flags=re.DOTALL
        )
        
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated HTML file: {file_path}")
            return True
    except Exception as e:
        print(f"Error updating HTML {file_path}: {e}")
    return False

def main():
    json_count = 0
    html_count = 0
    
    # Recursively find and update all seed-data.json and html files
    for root, dirs, files in os.walk('.'):
        # Skip git and vscode
        if '.git' in root or '.vscode' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            if file == 'seed-data.json':
                if update_seed_json(file_path):
                    json_count += 1
            elif file.endswith('.html'):
                if update_html_file(file_path):
                    html_count += 1
                    
    print(f"\nDone. Updated {json_count} JSON seed files and {html_count} HTML files.")

if __name__ == '__main__':
    main()
