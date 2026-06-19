import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"

# 1. Scan and group all folders
subdirs = [d for d in os.listdir(collections_dir) if os.path.isdir(os.path.join(collections_dir, d))]
exclude_dirs = {"css", "fonts", "images", "js", "firebase", "types"}
subdirs = [d for d in subdirs if d not in exclude_dirs]

groups = {}
for d in subdirs:
    match = re.match(r'^(.*?)-(\d+)$', d)
    if match:
        base, suffix_num = match.groups()
        page_num = int(suffix_num) + 1
        if base not in groups:
            groups[base] = []
        groups[base].append((page_num, d))
    else:
        if d not in groups:
            groups[d] = []
        groups[d].append((1, d))

errors = 0

for base, pages in sorted(groups.items()):
    pages.sort(key=lambda x: x[0])
    N = len(pages)
    
    if N == 1:
        # Check that single-page collection does not have pagination
        folder = pages[0][1]
        path = os.path.join(collections_dir, folder, "index.html")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if re.search(r'class="pagination"', content):
                print(f"[ERROR] Single-page collection '{folder}' still has a pagination block!")
                errors += 1
            else:
                pass
    else:
        # Check each page of the multi-page collection
        for idx in range(N):
            _, folder = pages[idx]
            page_num = idx + 1
            path = os.path.join(collections_dir, folder, "index.html")
            if not os.path.exists(path):
                print(f"[ERROR] Path does not exist: {path}")
                errors += 1
                continue
                
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            # Verify pagination block exists
            nav_match = re.search(r'<nav aria-label="Pagination"[^>]*>.*?</nav>', content, re.DOTALL)
            if not nav_match:
                nav_match = re.search(r'class="pagination".*?</nav>', content, re.DOTALL)
                
            if not nav_match:
                print(f"[ERROR] Multi-page collection '{folder}' (Page {page_num} of {N}) has no pagination block!")
                errors += 1
                continue
                
            nav_html = nav_match.group(0)
            
            # 1. No ?page= should exist in hrefs inside pagination
            if "?page=" in nav_html:
                print(f"[ERROR] '{folder}' pagination block contains '?page=' links: {nav_html}")
                errors += 1
                
            # 2. Check active page highlight
            curr_match = re.search(r'class="[^"]*pagination__item--current[^"]*"[^>]*>(.*?)</a>', nav_html, re.DOTALL)
            if curr_match:
                active_text = curr_match.group(1).strip()
                if active_text != str(page_num):
                    print(f"[ERROR] '{folder}' (Page {page_num}) has wrong active page highlighted: '{active_text}'")
                    errors += 1
            else:
                print(f"[ERROR] '{folder}' (Page {page_num}) has no active page highlighted!")
                errors += 1
                
            # 3. Check all links in pagination block
            links = re.findall(r'<a[^>]+href="([^"]+)"', nav_html)
            for href in links:
                # Relative path from collections/folder/index.html
                # For example, '../colostrum-1/index.html'
                target_rel_path = os.path.normpath(os.path.join(collections_dir, folder, href))
                if not os.path.exists(target_rel_path):
                    print(f"[ERROR] '{folder}' pagination links to non-existent file: '{href}' (resolved to '{target_rel_path}')")
                    errors += 1

if errors == 0:
    print("Verification successful! All checks passed.")
    sys.exit(0)
else:
    print(f"Verification failed with {errors} errors.")
    sys.exit(1)
