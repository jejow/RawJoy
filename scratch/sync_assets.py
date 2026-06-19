import os
import shutil

src_root = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
dst_root = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\RawJoy"

folders_to_sync = ["cart", "js", "css", "firebase", "pages", "collections", "products"]

def sync_folder(folder_name):
    src_dir = os.path.join(src_root, folder_name)
    dst_dir = os.path.join(dst_root, folder_name)
    
    if not os.path.exists(src_dir):
        print(f"Source folder does not exist: {src_dir}")
        return
        
    print(f"Syncing folder: {folder_name}...")
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        target_dir = dst_dir if rel_path == "." else os.path.join(dst_dir, rel_path)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            print(f"  Created directory: {target_dir}")
            
        for f in files:
            src_file = os.path.join(root, f)
            dst_file = os.path.join(target_dir, f)
            
            # Copy file only if it doesn't exist, size differs, or src is newer
            if not os.path.exists(dst_file) or os.path.getsize(src_file) != os.path.getsize(dst_file) or os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                shutil.copy2(src_file, dst_file)
        print(f"  Completed syncing {folder_name}")

for folder in folders_to_sync:
    sync_folder(folder)

# Sync root files (like index.html)
print("Syncing root files...")
for item in os.listdir(src_root):
    src_item = os.path.join(src_root, item)
    if os.path.isfile(src_item) and item.endswith('.html'):
        dst_item = os.path.join(dst_root, item)
        shutil.copy2(src_item, dst_item)
        print(f"  Copied root file: {item}")

print("Synchronization complete!")

