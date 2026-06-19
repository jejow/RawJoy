import os
import stat
import re

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
laragon_root = r"c:\laragon\www\RawJoy"

def fix_file(filepath):
    if not os.path.exists(filepath):
        return False
        
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Pattern for Bone Broth count (change 18 to 12)
    p_bone_broth = re.compile(
        r'(<span class="reversed-link__text">Bone Broth</span>\s*</span>\s*<sup class="collection-card__count paragraph">\s*)18(\s*</sup>)',
        re.IGNORECASE
    )
    
    # Pattern for Treats count (change 17 to 12)
    p_treats = re.compile(
        r'(<span class="reversed-link__text">Treats</span>\s*</span>\s*<sup class="collection-card__count paragraph">\s*)17(\s*</sup>)',
        re.IGNORECASE
    )
    
    new_content, count1 = p_bone_broth.subn(r'\g<1>12\g<2>', content)
    new_content, count2 = p_treats.subn(r'\g<1>12\g<2>', new_content)
    
    if count1 > 0 or count2 > 0:
        # Clear read-only attribute if any
        os.chmod(filepath, stat.S_IWRITE)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed {filepath}: replaced Bone Broth counts ({count1} times) and Treats counts ({count2} times).")
        return True
    return False

# List of HTML files we found
files_to_check = [
    "index.html",
    "collections/sockete-salmon-2/index.html",
    "collections/shop-all/index.html",
    "collections/raw-food/index.html",
    "collections/organic-food/index.html",
    "collections/freeze-dried/index.html",
    "collections/doggy-dental-mix/index.html",
    "collections/all/index.html",
    "collections/air-dried-food/index.html"
]

for rel_path in files_to_check:
    fix_file(os.path.join(workspace_root, rel_path))
    fix_file(os.path.join(laragon_root, rel_path))

print("Done fixing counts.")
