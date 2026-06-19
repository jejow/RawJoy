import os
import re

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
        page_num = int(suffix_num) + 1
        if base not in groups:
            groups[base] = []
        groups[base].append((page_num, d))
    else:
        # Base folder (Page 1)
        if d not in groups:
            groups[d] = []
        groups[d].append((1, d))

# 2. Process each collection group
for base, pages in sorted(groups.items()):
    # Sort pages by page number
    pages.sort(key=lambda x: x[0])
    N = len(pages)
    
    print(f"\nProcessing group '{base}' (pages count: {N}):")
    for page_num, folder in pages:
        print(f"  Page {page_num}: {folder}")
        
    if N == 1:
        # Single page collection: remove or hide pagination block
        folder = pages[0][1]
        path = os.path.join(collections_dir, folder, "index.html")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Find pagination block
            nav_match = re.search(r'<nav aria-label="Pagination"[^>]*>.*?</nav>', content, re.DOTALL)
            if not nav_match:
                nav_match = re.search(r'class="pagination".*?</nav>', content, re.DOTALL)
                
            if nav_match:
                print(f"  -> Removing pagination from single-page collection '{folder}'")
                new_content = content[:nav_match.start()] + content[nav_match.end():]
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
    else:
        # Multi-page collection: generate and replace pagination block
        for idx in range(N):
            _, folder = pages[idx]
            page_num = idx + 1
            path = os.path.join(collections_dir, folder, "index.html")
            if not os.path.exists(path):
                continue
                
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            # Construct new pagination HTML block
            new_nav = ['<nav aria-label="Pagination" class="pagination" role="navigation"><ul class="pagination__list list-unstyled flex items-center flex-wrap justify-center" role="list">']
            
            # Prev button
            if page_num > 1:
                prev_folder = pages[idx-1][1]
                new_nav.append(f'<li class="reversed-link"><a class="pagination__item pagination__item--prev pagination__item-arrow motion-reduce" href="../{prev_folder}/index.html"><span class="icon icon--caret-left icon--small"><svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M0 0H20V20H0V0z" fill="none"></path><path d="M12.5 3.75L6.25 10L12.5 16.25" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="var(--icon-stroke-width, 2)"></path></svg></span><span class="reversed-link__text">Prev</span></a></li>')
                
            # Page numbers
            for p in range(1, N + 1):
                target_folder = pages[p-1][1]
                if p == page_num:
                    new_nav.append(f'<li><a aria-current="page" aria-disabled="true" aria-label="Page {p}" class="pagination__item pagination__item--current background-2" role="link">{p}</a></li>')
                else:
                    new_nav.append(f'<li><a aria-label="Page {p}" class="pagination__item reversed-link" href="../{target_folder}/index.html"><span class="reversed-link__text">{p}</span></a></li>')
                    
            # Next button
            if page_num < N:
                next_folder = pages[idx+1][1]
                new_nav.append(f'<li class="reversed-link"><a class="pagination__item pagination__item--next pagination__item-arrow motion-reduce" href="../{next_folder}/index.html"><span class="reversed-link__text">Next</span><span class="icon icon--caret-right icon--small"><svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M0 0H20V20H0V0z" fill="none"></path><path d="M7.5 3.75L13.75 10L7.5 16.25" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="var(--icon-stroke-width, 2)"></path></svg></span></a></li>')
                
            new_nav.append('</ul></nav>')
            new_nav_html = "\n".join(new_nav)
            
            # Find and replace pagination block
            nav_match = re.search(r'<nav aria-label="Pagination"[^>]*>.*?</nav>', content, re.DOTALL)
            if not nav_match:
                nav_match = re.search(r'class="pagination".*?</nav>', content, re.DOTALL)
                
            if nav_match:
                print(f"  -> Replacing pagination block in '{folder}' (Page {page_num} of {N})")
                new_content = content[:nav_match.start()] + new_nav_html + content[nav_match.end():]
            else:
                # Fallback: Insert immediately after product-grid UL if no pagination exists
                grid_match = re.search(r'<ul[^>]+class="[^"]*product-grid[^"]*".*?</ul>', content, re.DOTALL)
                if grid_match:
                    print(f"  -> Inserting missing pagination block in '{folder}' (Page {page_num} of {N})")
                    insert_idx = grid_match.end()
                    new_content = content[:insert_idx] + "\n" + new_nav_html + content[insert_idx:]
                else:
                    print(f"  [WARNING] Could not find pagination block or product-grid UL in '{folder}'")
                    continue
                    
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)

print("\nDone!")
