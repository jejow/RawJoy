import os
import json

def update_seed_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated = False
        for p in data.get('products', []):
            product_slug = p.get('slug')
            if product_slug in ['salmon-stick', 'cat-calming-formula']:
                # Set top-level compareAtPrice
                if p.get('compareAtPrice') != 32.0:
                    p['compareAtPrice'] = 32.0
                    updated = True
                
                # Set variant-level compareAtPrice
                variants = p.get('variants', [])
                for v in variants:
                    name = v.get('name', '')
                    if '100gr' in name:
                        expected_compare = 32.0
                    elif '150gr' in name:
                        expected_compare = 48.0
                    elif '200gr' in name:
                        expected_compare = 64.0
                    else:
                        continue
                    
                    if v.get('compareAtPrice') != expected_compare:
                        v['compareAtPrice'] = expected_compare
                        updated = True
                        
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Updated: {file_path}")
            return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
    return False

def main():
    count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.vscode' in root:
            continue
        for file in files:
            if file == 'seed-data.json':
                file_path = os.path.join(root, file)
                if update_seed_json(file_path):
                    count += 1
    print(f"Finished. Updated {count} seed-data.json files.")

if __name__ == '__main__':
    main()
