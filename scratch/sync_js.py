import os
import shutil

src_interceptor = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js\cart-interceptor.js"
src_bridge = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js\db-bridge.js"
products_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products"

count = 0
for name in os.listdir(products_dir):
    subpath = os.path.join(products_dir, name)
    if os.path.isdir(subpath):
        js_dir = os.path.join(subpath, "js")
        if os.path.exists(js_dir):
            dest_interceptor = os.path.join(js_dir, "cart-interceptor.js")
            dest_bridge = os.path.join(js_dir, "db-bridge.js")
            
            # Copy file if it exists
            if os.path.exists(dest_interceptor):
                shutil.copy2(src_interceptor, dest_interceptor)
            if os.path.exists(dest_bridge):
                shutil.copy2(src_bridge, dest_bridge)
            count += 1

print(f"Successfully synced JS files to {count} product subdirectories.")
