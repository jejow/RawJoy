import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"

# 1. Scan and group all folders
subdirs = [d for d in os.listdir(collections_dir) if os.path.isdir(os.path.join(collections_dir, d))]

# Exclude common asset directories that are not collections
exclude_dirs = {"css", "fonts", "images", "js", "firebase", "types"}
subdirs = [d for d in subdirs if d not in exclude_dirs]

# Group by base collection name
groups = {}
for d in subdirs:
    match = re.match(r'^(.*?)-(\d+)$', d)
    if match:
        base, suffix_num = match.groups()
        if base not in groups:
            groups[base] = []
        groups[base].append(d)
    else:
        # Base folder (Page 1)
        if d not in groups:
            groups[d] = []
        groups[d].append(d)

print("Grouping complete. Found collection groups:")
for base, folders in sorted(groups.items()):
    # Ensure the base folder itself is included if it exists
    if base in subdirs and base not in folders:
        folders.append(base)
    folders = list(set(folders))
    groups[base] = sorted(folders)
    print(f"  Group '{base}': {groups[base]}")

# 2. Merge images for each group
for base, folders in sorted(groups.items()):
    if len(folders) <= 1:
        # Single page collection, no need to merge with other pages
        continue
        
    print(f"\nMerging images for group '{base}'...")
    
    # Collect all image files from all folders in the group
    all_images = {} # filename -> source_abs_path
    for folder in folders:
        img_dir = os.path.join(collections_dir, folder, "images")
        if os.path.exists(img_dir):
            for filename in os.listdir(img_dir):
                filepath = os.path.join(img_dir, filename)
                if os.path.isfile(filepath):
                    all_images[filename] = filepath
                    
    print(f"  Total unique images in group '{base}': {len(all_images)}")
    
    # Copy all collected images to every folder's images directory
    for folder in folders:
        target_img_dir = os.path.join(collections_dir, folder, "images")
        if not os.path.exists(target_img_dir):
            os.makedirs(target_img_dir)
            print(f"  Created directory: {target_img_dir}")
            
        copied_count = 0
        for filename, src_path in all_images.items():
            dst_path = os.path.join(target_img_dir, filename)
            # Only copy if it doesn't exist or is different size
            if not os.path.exists(dst_path) or os.path.getsize(src_path) != os.path.getsize(dst_path):
                shutil.copy2(src_path, dst_path)
                copied_count += 1
                
        print(f"  Copied {copied_count} new/updated images to collections/{folder}/images")

print("\nImage merging complete!")
