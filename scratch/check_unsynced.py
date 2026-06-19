import os
import filecmp

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
src_db = os.path.join(root_dir, 'js', 'db-bridge.js')
src_interceptor = os.path.join(root_dir, 'js', 'cart-interceptor.js')

ignore_folders = ['.git', '.vscode', 'scratch', 'media', 'node_modules']

unsynced_db = []
unsynced_int = []

for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if d not in ignore_folders]
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        if filename == 'db-bridge.js' and filepath != src_db:
            if not filecmp.cmp(src_db, filepath, shallow=False):
                unsynced_db.append(os.path.relpath(filepath, root_dir))
        elif filename == 'cart-interceptor.js' and filepath != src_interceptor:
            if not filecmp.cmp(src_interceptor, filepath, shallow=False):
                unsynced_int.append(os.path.relpath(filepath, root_dir))

print(f"Unsynced db-bridge.js copies ({len(unsynced_db)}):")
for p in unsynced_db:
    print(" -", p)
    
print(f"Unsynced cart-interceptor.js copies ({len(unsynced_int)}):")
for p in unsynced_int:
    print(" -", p)
