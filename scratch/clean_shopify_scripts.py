import os
import re
import stat

root_dir = r"c:\laragon\www\op"

# Regex for loader.init-shop-cart-sync script tag
pattern1 = re.compile(r'<script\s+async=""\s+defer="defer"\s+src="[^"]*loader\.init-shop-cart-sync\.en\.esm\.js"\s+type="module"></script>', re.IGNORECASE)

# Regex for the module script block that calls initShopCartSync
pattern2 = re.compile(
    r'<script\s+type="module">\s*await\s+import\("[^"]*loader\.init-shop-cart-sync\.en\.esm\.js"\);\s*window\.Shopify\.SignInWithShop\?\.initShopCartSync\?\.[\s\S]*?;\s*</script>',
    re.IGNORECASE
)

# Regex for trekkie storefront analytics script tag
pattern3 = re.compile(r'<script\s+async=""\s+src="[^"]*trekkie\.storefront\.[a-f0-9]+\.min\.js"\s+type="text/javascript"></script>', re.IGNORECASE)

count = 0
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Skip standard build/development folders
    dirnames[:] = [d for d in dirnames if d not in ['.git', '.vscode', 'scratch', 'media', 'node_modules']]
    
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    html = f.read()
                
                new_html = pattern1.sub('<!-- Removed shop-cart-sync loader -->', html)
                new_html = pattern2.sub('<!-- Removed shop-cart-sync runner -->', new_html)
                new_html = pattern3.sub('<!-- Removed trekkie analytics -->', new_html)
                
                if new_html != html:
                    # Clear read-only attribute if any
                    os.chmod(filepath, stat.S_IWRITE)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_html)
                    count += 1
            except Exception as e:
                print(f"Error cleaning {filepath}: {e}")

print(f"Cleaned {count} HTML files from Shopify tracking scripts.")
