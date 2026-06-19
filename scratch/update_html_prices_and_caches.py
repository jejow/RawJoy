import os
import re
import json
from bs4 import BeautifulSoup

# Variant ID to compare-at price in cents
CENTS_MAP = {
    50657320403234: 3200, # Salmon Stick 100gr
    50657320436002: 4800, # Salmon Stick 150gr
    50657320468770: 6400, # Salmon Stick 200gr
    50657166557474: 3200, # Cat Calming 100gr
    50657166590242: 4800, # Cat Calming 150gr
    50657166623010: 6400, # Cat Calming 200gr
}

# String representation mapping
STR_MAP = {
    "50657320403234": 3200,
    "50657320436002": 4800,
    "50657320468770": 6400,
    "50657166557474": 3200,
    "50657166590242": 4800,
    "50657166623010": 6400,
}

SALMON_STICK_ID = "9958927434018"
CAT_CALMING_ID = "9958900760866"

def update_variant_dict(v, product_handle=None):
    updated = False
    vid = v.get('id')
    # Match by ID
    if vid and int(vid) in CENTS_MAP:
        cents = CENTS_MAP[int(vid)]
        if v.get('compare_at_price') != cents:
            v['compare_at_price'] = cents
            updated = True
        return updated
    
    # Match by product handle and name/title/option
    title = v.get('title') or v.get('name') or v.get('public_title') or v.get('option1')
    if title and isinstance(title, str):
        # Determine product
        is_salmon = (product_handle == 'salmon-stick')
        is_calming = (product_handle == 'cat-calming-formula')
        
        # Or try variant name match
        name_lower = title.lower()
        if 'salmon stick' in name_lower:
            is_salmon = True
        elif 'cat calming' in name_lower:
            is_calming = True
            
        if is_salmon:
            if '100gr' in title:
                val = 3200
            elif '150gr' in title:
                val = 4800
            elif '200gr' in title:
                val = 6400
            else:
                return False
            if v.get('compare_at_price') != val:
                v['compare_at_price'] = val
                updated = True
        elif is_calming:
            if '100gr' in title:
                val = 3200
            elif '150gr' in title:
                val = 4800
            elif '200gr' in title:
                val = 6400
            else:
                return False
            if v.get('compare_at_price') != val:
                v['compare_at_price'] = val
                updated = True
    return updated

def update_json_data(obj, default_handle=None):
    updated = False
    if isinstance(obj, dict):
        current_handle = default_handle
        for key in ['handle', 'slug', 'url']:
            val = obj.get(key)
            if isinstance(val, str):
                if 'salmon-stick' in val:
                    current_handle = 'salmon-stick'
                elif 'cat-calming' in val:
                    current_handle = 'cat-calming-formula'
        
        # If it's a variant dictionary itself
        if 'id' in obj and (str(obj['id']) in STR_MAP or (isinstance(obj['id'], int) and obj['id'] in CENTS_MAP)):
            if update_variant_dict(obj, current_handle):
                updated = True
        
        # Traverse list of variants
        for vk in ['variants', 'hasVariant', 'productvariants', 'productVariants']:
            v_list = obj.get(vk)
            if isinstance(v_list, list):
                for item in v_list:
                    if isinstance(item, dict):
                        if update_variant_dict(item, current_handle):
                            updated = True
                        if update_json_data(item, current_handle):
                            updated = True
                            
        for k, v in obj.items():
            if k not in ['variants', 'hasVariant', 'productvariants', 'productVariants']:
                if update_json_data(v, current_handle):
                    updated = True
    elif isinstance(obj, list):
        for item in obj:
            if update_json_data(item, default_handle):
                updated = True
    return updated

def update_html_file(file_path):
    # Infer default handle from directory name
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
                if update_json_data(data, default_handle):
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
                if update_json_data(data, default_handle):
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
                if update_json_data(data, default_handle):
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
                if update_json_data(data, default_handle):
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

        # 5. Update generic application/json scripts
        def replace_generic_json(match):
            nonlocal updated
            tag_attrs = match.group(1)
            json_str = match.group(2)
            if 'data-variants-cache' in tag_attrs:
                return match.group(0)
            try:
                data = json.loads(json_str)
                if update_json_data(data, default_handle):
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
        
        # 6. Parse and update HTML price tags using BeautifulSoup
        soup = BeautifulSoup(new_content, 'html.parser')
        html_modified = False
        
        # Helper to check if a product-card or product-price tag is for salmon-stick or cat-calming
        def is_target_element(el):
            # Check data-product-id
            pid = el.get('data-product-id')
            if pid in [SALMON_STICK_ID, CAT_CALMING_ID]:
                return pid
            
            # Check if this element is inside a product-card, or contains a link to salmon-stick or cat-calming
            text = str(el).lower()
            if 'salmon-stick' in text or 'salmon stick' in text:
                return SALMON_STICK_ID
            if 'cat-calming' in text or 'cat calming' in text:
                return CAT_CALMING_ID
            return None

        # Find all product cards or product-price elements
        # Note: we can find all <product-price> elements and check if they belong to target products
        for pp in soup.find_all('product-price'):
            # Check if this pp element or its ancestors match Salmon Stick or Cat Calming Formula
            target_id = None
            
            # 1. Check pp data-product-id
            if pp.get('data-product-id') == SALMON_STICK_ID:
                target_id = SALMON_STICK_ID
            elif pp.get('data-product-id') == CAT_CALMING_ID:
                target_id = CAT_CALMING_ID
                
            # 2. Check parent product-card
            if not target_id:
                card = pp.find_parent('product-card')
                if card:
                    target_id = is_target_element(card)
                    
            # 3. Check containing elements or hrefs inside card or pp
            if not target_id:
                target_id = is_target_element(pp)
                
            # 4. If this is the main product page
            if not target_id and default_handle in ['salmon-stick', 'cat-calming-formula']:
                # Any product-price on the salmon-stick page that doesn't belong to another card
                if not pp.find_parent('product-card') and pp.get('data-product-id') not in [c for c in [SALMON_STICK_ID, CAT_CALMING_ID] if c != target_id]:
                    if default_handle == 'salmon-stick':
                        target_id = SALMON_STICK_ID
                    else:
                        target_id = CAT_CALMING_ID

            if target_id:
                # Update price Container
                container = pp.find(ref="priceContainer")
                if container:
                    classes = container.get('class', [])
                    if 'price--on-sale' not in classes:
                        if isinstance(classes, str):
                            container['class'] = classes + ' price--on-sale'
                        else:
                            classes.append('price--on-sale')
                            container['class'] = classes
                        html_modified = True
                    
                    # Update compare-at-price
                    compare_span = container.find(class_="compare-at-price")
                    if compare_span:
                        if compare_span.text != '$32.00':
                            compare_span.string = '$32.00'
                            html_modified = True
                    else:
                        # If compare-at-price span doesn't exist, let's inject it into price__sale
                        sale_div = container.find(class_="price__sale")
                        if sale_div:
                            new_span = soup.new_tag('span', **{'class': 'compare-at-price'})
                            new_span.string = '$32.00'
                            # Also inject Regular price visually hidden span if missing
                            reg_hidden = soup.new_tag('span', **{'class': 'visually-hidden'})
                            reg_hidden.string = 'Regular price'
                            sale_div.append(reg_hidden)
                            sale_div.append(new_span)
                            html_modified = True

        if html_modified or updated:
            final_content = str(soup) if html_modified else new_content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            print(f"Updated HTML: {file_path} (JS/JSON updated: {updated}, HTML updated: {html_modified})")
            return True
            
    except Exception as e:
        print(f"Error updating HTML {file_path}: {e}")
    return False

def main():
    count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.vscode' in root or 'scratch' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if update_html_file(file_path):
                    count += 1
    print(f"Finished. Updated {count} HTML files.")

if __name__ == '__main__':
    main()
