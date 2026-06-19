import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"
src_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\scratch\facets_custom.js"

if not os.path.exists(src_path):
    print(f"[ERROR] Source file not found: {src_path}")
    sys.exit(1)

count = 0
for root, dirs, files in os.walk(collections_dir):
    for file in files:
        if file == "facets.js":
            dest_path = os.path.join(root, file)
            print(f"Syncing to: {dest_path}")
            shutil.copy(src_path, dest_path)
            count += 1

print(f"\nSuccessfully synced {count} facets.js files!")
