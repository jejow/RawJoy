import os
import json
from bs4 import BeautifulSoup

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
product_path = os.path.join(workspace_root, "products", "chicken-bone-treat", "index.html")

if os.path.exists(product_path):
    with open(product_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    quick_add = soup.find(attrs={"data-quick-add-content": True})
    if quick_add:
        print("Product options/variants in chicken-bone-treat data-quick-add-content:")
        options = quick_add.find_all("option")
        for opt in options:
            print(f"  Option: {opt.text.strip()} -> value: {opt.get('value')}")
            
        inputs = quick_add.find_all("input", type="radio")
        for inp in inputs:
            print(f"  Radio input: name={inp.get('name')}, value={inp.get('value')}")
            
        hidden_ids = quick_add.find_all("input", attrs={"name": "id"})
        for hid in hidden_ids:
            print(f"  Hidden input name=id, value={hid.get('value')}")
            
        # Also print any JSON script tag with variant info if present
        variant_json = quick_add.find("script", type="application/json")
        if variant_json:
            print("  Found variant JSON script tag.")
            try:
                js_data = json.loads(variant_json.text.strip())
                print(json.dumps(js_data[:3] if isinstance(js_data, list) else js_data, indent=2))
            except Exception as e:
                print(variant_json.text.strip()[:300])
    else:
        print("[data-quick-add-content] not found in chicken-bone-treat/index.html")
else:
    print("chicken-bone-treat index.html not found")
