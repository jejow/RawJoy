import os
import re
import shutil
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
collections_dir = os.path.join(root_dir, "collections")

missing_slugs = [
    "pet-meal-time-mix",
    "rawjoy-soft-bar",
    "salmon-broccoli-crunch",
    "salmon-carrot-pate",
    "salmon-rice-formula",
    "salmon-stick",
    "venison-peas-recipe"
]

target_collections = ["all", "shop-all"]

# 1. Find the card and images for each missing product slug in other collections
found_cards = {}  # slug -> (card_soup, source_images_dir)

print("Searching for product cards of missing products...")
for root, dirs, files in os.walk(collections_dir):
    for file in files:
        if file == "index.html":
            path = os.path.join(root, file)
            # Skip target collections
            parts = os.path.relpath(path, collections_dir).split(os.sep)
            if parts[0] in target_collections:
                continue
            
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Check if any missing slug is in this collection
            for slug in missing_slugs:
                if slug in found_cards:
                    continue
                if f"/products/{slug}" in content:
                    # Parse the page
                    soup = bs4.BeautifulSoup(content, 'html.parser')
                    grid = soup.find(class_='product-grid')
                    if grid:
                        cards = grid.find_all(class_='product-grid__item')
                        for card in cards:
                            link = card.find('a', href=lambda h: h and f"/products/{slug}" in h)
                            if link:
                                print(f"Found card for '{slug}' in: {os.path.relpath(path, collections_dir)}")
                                found_cards[slug] = (card, os.path.join(os.path.dirname(path), "images"))
                                break

# 2. Inject missing cards and copy images
for target in target_collections:
    target_path = os.path.join(collections_dir, target, "index.html")
    target_images_dir = os.path.join(collections_dir, target, "images")
    
    if not os.path.exists(target_path):
        print(f"Target file not found: {target_path}")
        continue
    
    with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
        target_soup = bs4.BeautifulSoup(f.read(), 'html.parser')
    
    grid = target_soup.find(class_='product-grid')
    if not grid:
        print(f"Could not find product-grid in: {target_path}")
        continue
    
    # Check if cards are already injected (by looking at data-product-id or href)
    injected_count = 0
    for slug in missing_slugs:
        if slug not in found_cards:
            print(f"ERROR: Could not find card for '{slug}' anywhere!")
            continue
            
        card_soup, src_images_dir = found_cards[slug]
        
        # Check if already present in target
        existing_link = grid.find('a', href=lambda h: h and f"/products/{slug}" in h)
        if existing_link:
            print(f"Product '{slug}' is already present in {target}/index.html. Skipping injection.")
            continue
        
        # Copy images referenced in the card
        img_tags = card_soup.find_all('img')
        for img in img_tags:
            # Check src and srcset
            srcs = []
            if img.get('src'):
                srcs.append(img['src'])
            if img.get('srcset'):
                # Extract image paths from srcset (comma separated, with descriptor like 'images/foo.jpg 165w')
                srcset_parts = img['srcset'].split(',')
                for part in srcset_parts:
                    part = part.strip()
                    if part:
                        img_path = part.split(' ')[0]
                        srcs.append(img_path)
            
            for src in srcs:
                if 'images/' in src:
                    img_name = src.split('images/')[-1].split('?')[0]
                    src_img_file = os.path.join(src_images_dir, img_name)
                    dst_img_file = os.path.join(target_images_dir, img_name)
                    if os.path.exists(src_img_file):
                        shutil.copy2(src_img_file, dst_img_file)
                    else:
                        print(f"  Warning: Source image not found: {src_img_file}")
                        
        # Append the card
        # Make a deep copy
        new_card = bs4.BeautifulSoup(str(card_soup), 'html.parser').find(class_='product-grid__item')
        grid.append(new_card)
        injected_count += 1
        print(f"Injected '{slug}' card into {target}/index.html")
        
    if injected_count > 0:
        # Write back the modified HTML file
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(str(target_soup))
        print(f"Saved: {target_path}")
        
print("Injections complete!")
