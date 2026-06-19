import os
import re
import json
from bs4 import BeautifulSoup

SALMON_STICK_ID = "9958927434018"
CAT_CALMING_ID = "9958900760866"

def verify_seed():
    print("--- Verifying Database Seeds ---")
    seed_path = "firebase/seed-data.json"
    if not os.path.exists(seed_path):
        print(f"Seed file not found: {seed_path}")
        return False
        
    with open(seed_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    success = True
    for p in data.get('products', []):
        if p.get('slug') in ['salmon-stick', 'cat-calming-formula']:
            slug = p.get('slug')
            print(f"Product: {slug}")
            if p.get('compareAtPrice') != 32.0:
                print(f"  Error: Top-level compareAtPrice is {p.get('compareAtPrice')}, expected 32.0")
                success = False
            else:
                print("  Top-level compareAtPrice: OK")
                
            for v in p.get('variants', []):
                name = v.get('name')
                expected = None
                if '100gr' in name:
                    expected = 32.0
                elif '150gr' in name:
                    expected = 48.0
                elif '200gr' in name:
                    expected = 64.0
                    
                if expected:
                    if v.get('compareAtPrice') != expected:
                        print(f"  Error: Variant {name} compareAtPrice is {v.get('compareAtPrice')}, expected {expected}")
                        success = False
                    else:
                        print(f"  Variant {name} compareAtPrice: OK ({v.get('compareAtPrice')})")
    return success

def verify_html_files():
    print("\n--- Verifying HTML Files ---")
    success = True
    html_count = 0
    checked_count = 0
    
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.vscode' in root or 'scratch' in root or 'node_modules' in root or 'firebase' in root:
            continue
        for file in files:
            if file.endswith('.html') and 'seed.html' not in file:
                file_path = os.path.join(root, file)
                checked_count += 1
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                soup = BeautifulSoup(content, 'html.parser')
                
                # Check target pricing elements
                for pp in soup.find_all('product-price'):
                    # Check if this pp matches salmon-stick or cat-calming
                    is_target = False
                    
                    if pp.get('data-product-id') in [SALMON_STICK_ID, CAT_CALMING_ID]:
                        is_target = True
                    else:
                        card = pp.find_parent('product-card')
                        if card:
                            card_str = str(card).lower()
                            if 'salmon-stick' in card_str or 'cat-calming' in card_str:
                                is_target = True
                        else:
                            pp_str = str(pp).lower()
                            if 'salmon-stick' in pp_str or 'cat-calming' in pp_str:
                                is_target = True
                                
                    # If this page itself is salmon-stick or cat-calming and this is the main price
                    parts = file_path.replace('\\', '/').split('/')
                    if 'products' in parts:
                        prod_idx = parts.index('products')
                        if prod_idx + 1 < len(parts):
                            handle = parts[prod_idx + 1]
                            if handle in ['salmon-stick', 'cat-calming-formula'] and not pp.find_parent('product-card'):
                                is_target = True
                                
                    if is_target:
                        container = pp.find(ref="priceContainer")
                        if not container:
                            print(f"[{file_path}] Error: No priceContainer found inside target product-price")
                            success = False
                            continue
                            
                        classes = container.get('class', [])
                        if 'price--on-sale' not in classes:
                            print(f"[{file_path}] Error: target priceContainer is missing 'price--on-sale' class: {classes}")
                            success = False
                        
                        compare_span = container.find(class_="compare-at-price")
                        if not compare_span:
                            print(f"[{file_path}] Error: compare-at-price span not found inside target product-price")
                            success = False
                        elif compare_span.text != '$32.00' and compare_span.string != '$32.00':
                            print(f"[{file_path}] Error: compare-at-price span text is '{compare_span.text}', expected '$32.00'")
                            success = False
                
                # Check data-variants-cache in target product pages
                parts = file_path.replace('\\', '/').split('/')
                if 'products' in parts and len(parts) > parts.index('products') + 1:
                    handle = parts[parts.index('products') + 1]
                    if handle in ['salmon-stick', 'cat-calming-formula']:
                        m = re.search(r'<script\s+data-variants-cache=\"\"\s+type=\"application/json\">\s*(.*?)\s*</script>', content, re.DOTALL)
                        if m:
                            data = json.loads(m.group(1))
                            for v in data.get('variants', []):
                                title = v.get('title')
                                expected = None
                                if '100gr' in title:
                                    expected = 3200
                                elif '150gr' in title:
                                    expected = 4800
                                elif '200gr' in title:
                                    expected = 6400
                                    
                                if expected and v.get('compare_at_price') != expected:
                                    print(f"[{file_path}] Error: Variant {title} compare_at_price is {v.get('compare_at_price')}, expected {expected}")
                                    success = False
                        else:
                            print(f"[{file_path}] Error: No data-variants-cache found on target product page")
                            success = False
                            
    print(f"Checked {checked_count} HTML files.")
    return success

def main():
    s_seed = verify_seed()
    s_html = verify_html_files()
    if s_seed and s_html:
        print("\nSUCCESS: All checks passed!")
    else:
        print("\nFAILURE: Some verification checks failed.")

if __name__ == '__main__':
    main()
