import json
import re
import os
import sys

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

def verify_variant_obj(variant_obj, default_handle=None, file_path=""):
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
        return True # Not a weight-based variant we care about
        
    base_price = get_base_price(product_handle)
    if base_price is None:
        print(f"[{file_path}] Warning: Cannot find base price for product: {product_handle}")
        return True # Can't verify, skip
        
    if weight == 100:
        expected_price = base_price
    elif weight == 150:
        expected_price = base_price * 1.5
    elif weight == 200:
        expected_price = base_price * 2.0
    else:
        return True
        
    # Check variant_obj['price'] if exists
    if 'price' in variant_obj:
        val = variant_obj['price']
        if isinstance(val, dict):
            amount = val.get('amount')
            if amount != expected_price:
                print(f"[{file_path}] Mismatch: {product_handle} {weight}gr. Expected amount {expected_price}, got {amount}")
                return False
        elif isinstance(val, (int, float)):
            if val > 100:
                expected_val = int(expected_price * 100)
            else:
                expected_val = expected_price
            if val != expected_val:
                print(f"[{file_path}] Mismatch: {product_handle} {weight}gr. Expected int/float price {expected_val}, got {val}")
                return False
        elif isinstance(val, str):
            if '.' in val:
                expected_val = f"{expected_price:.2f}"
            else:
                expected_val = str(int(expected_price * 100))
            if val != expected_val:
                print(f"[{file_path}] Mismatch: {product_handle} {weight}gr. Expected string price {expected_val}, got {val}")
                return False

    # Check offers if exists
    if 'offers' in variant_obj and isinstance(variant_obj['offers'], dict):
        offers = variant_obj['offers']
        if 'price' in offers:
            val = offers['price']
            if isinstance(val, str):
                expected_val = f"{expected_price:.2f}"
                if val != expected_val:
                    print(f"[{file_path}] Mismatch in Schema Offer: {product_handle} {weight}gr. Expected price {expected_val}, got {val}")
                    return False
            elif isinstance(val, (int, float)):
                if val > 100:
                    expected_val = int(expected_price * 100)
                else:
                    expected_val = expected_price
                if val != expected_val:
                    print(f"[{file_path}] Mismatch in Schema Offer: {product_handle} {weight}gr. Expected price {expected_val}, got {val}")
                    return False

    return True

def traverse_and_verify(obj, default_handle=None, file_path=""):
    success = True
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
                        if not verify_variant_obj(item, current_handle, file_path):
                            success = False
                        if not traverse_and_verify(item, current_handle, file_path):
                            success = False
                            
        if not has_variants_list:
            if not verify_variant_obj(obj, default_handle, file_path):
                success = False
                
        for k, v in obj.items():
            if k not in variants_keys:
                if not traverse_and_verify(v, current_handle, file_path):
                    success = False
                    
    elif isinstance(obj, list):
        for item in obj:
            if not traverse_and_verify(item, default_handle, file_path):
                success = False
                
    return success

def verify_seed_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        success = True
        for p in data.get('products', []):
            product_slug = p.get('slug')
            if product_slug and product_slug in price_map:
                variants = p.get('variants', [])
                for v in variants:
                    if not verify_variant_obj(v, product_slug, file_path):
                        success = False
        return success
    except Exception as e:
        print(f"[{file_path}] Error parsing: {e}")
        return False

def verify_html_file(file_path):
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
            
        success = True
        
        # 1. Check <script data-variants-cache> blocks
        for match in re.finditer(r'<script\s+data-variants-cache=""\s+type="application/json">\s*(.*?)\s*</script>', content, re.DOTALL):
            try:
                data = json.loads(match.group(1))
                if not traverse_and_verify(data, default_handle, file_path):
                    success = False
            except Exception:
                pass

        # 2. Check var meta block
        for match in re.finditer(r'var\s+meta\s*=\s*(\{.*?\});', content):
            try:
                data = json.loads(match.group(1))
                if not traverse_and_verify(data, default_handle, file_path):
                    success = False
            except Exception:
                pass

        # 3. Check application/ld+json blocks
        for match in re.finditer(r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>', content, re.DOTALL):
            try:
                data = json.loads(match.group(1))
                if not traverse_and_verify(data, default_handle, file_path):
                    success = False
            except Exception:
                pass

        # 4. Check initData inside wpmLoader
        for match in re.finditer(r'initData:\s*(\{.*?\})\s*,\s*\}\s*,', content):
            try:
                data = json.loads(match.group(1))
                if not traverse_and_verify(data, default_handle, file_path):
                    success = False
            except Exception:
                pass

        # 5. Check generic application/json scripts
        for match in re.finditer(r'<script\s+([^>]*type="application/json"[^>]*)>\s*(.*?)\s*</script>', content, re.DOTALL):
            tag_attrs = match.group(1)
            if 'data-variants-cache' in tag_attrs:
                continue
            try:
                data = json.loads(match.group(2))
                if not traverse_and_verify(data, default_handle, file_path):
                    success = False
            except Exception:
                pass
                
        return success
    except Exception as e:
        print(f"[{file_path}] Error verifying HTML: {e}")
        return False

def main():
    failures = 0
    checked_json = 0
    checked_html = 0
    
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.vscode' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            if file == 'seed-data.json':
                checked_json += 1
                if not verify_seed_json(file_path):
                    failures += 1
            elif file.endswith('.html'):
                checked_html += 1
                if not verify_html_file(file_path):
                    failures += 1
                    
    print(f"\nVerification Results: Checked {checked_json} JSON files, {checked_html} HTML files.")
    if failures == 0:
        print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print(f"FOUND {failures} FILES WITH MISMATCHES!")
        sys.exit(1)

if __name__ == '__main__':
    main()
