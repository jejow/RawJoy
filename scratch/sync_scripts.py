import os
import shutil

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
src_db = os.path.join(root_dir, 'js', 'db-bridge.js')
src_interceptor = os.path.join(root_dir, 'js', 'cart-interceptor.js')

print("Source db-bridge.js exists:", os.path.exists(src_db))
print("Source cart-interceptor.js exists:", os.path.exists(src_interceptor))

db_count = 0
interceptor_count = 0

ignore_folders = ['.git', '.vscode', 'scratch', 'media', 'node_modules']

for dirpath, dirnames, filenames in os.walk(root_dir):
    # filter out ignored folders
    dirnames[:] = [d for d in dirnames if d not in ignore_folders]
    
    for filename in filenames:
        dest_file = os.path.join(dirpath, filename)
        if filename == 'db-bridge.js' and dest_file != src_db:
            shutil.copy2(src_db, dest_file)
            db_count += 1
        elif filename == 'cart-interceptor.js' and dest_file != src_interceptor:
            shutil.copy2(src_interceptor, dest_file)
            interceptor_count += 1

print(f"Successfully copied db-bridge.js to {db_count} directories.")
print(f"Successfully copied cart-interceptor.js to {interceptor_count} directories.")
