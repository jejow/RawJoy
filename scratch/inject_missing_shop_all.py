import os
import shutil
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
collections_dir = os.path.join(root_dir, "collections")
products_dir = os.path.join(root_dir, "products")

# Get list of all 25 products
all_slugs = [d for d in os.listdir(products_dir) if os.path.isdir(os.path.join(products_dir, d)) and not d.endswith('__temp')]

# Load shop-all index.html
shop_all_path = os.path.join(collections_dir, "shop-all", "index.html")
with open(shop_all_path, "r", encoding="utf-8", errors="ignore") as f:
    shop_all_soup = bs4.BeautifulSoup(f.read(), 'html.parser')

shop_all_grid = shop_all_soup.find(class_='product-grid')
shop_all_cards = shop_all_grid.find_all(class_='product-grid__item') if shop_all_grid else []

# Extract existing slugs in shop-all
shop_all_slugs = set()
for card in shop_all_cards:
    link = card.find('a', href=lambda h: h and '/products/' in h)
    if link:
        href = link['href']
        slug = href.split('/products/')[-1].split('/')[0].split('?')[0]
        shop_all_slugs.add(slug)

print("Shop-all existing slugs count:", len(shop_all_slugs))

missing_in_shop_all = [slug for slug in all_slugs if slug not in shop_all_slugs]
print("Missing in shop-all count:", len(missing_in_shop_all))
print("Missing slugs:", missing_in_shop_all)

if not missing_in_shop_all:
    print("No missing products in shop-all!")
    sys.exit(0)

# Load all/index.html to find the cards (since all/index.html now has all 25 products)
all_path = os.path.join(collections_dir, "all", "index.html")
with open(all_path, "r", encoding="utf-8", errors="ignore") as f:
    all_soup = bs4.BeautifulSoup(f.read(), 'html.parser')

all_grid = all_soup.find(class_='product-grid')
all_cards = all_grid.find_all(class_='product-grid__item') if all_grid else []

found_cards = {}
for card in all_cards:
    link = card.find('a', href=lambda h: h and '/products/' in h)
    if link:
        href = link['href']
        slug = href.split('/products/')[-1].split('/')[0].split('?')[0]
        if slug in missing_in_shop_all:
            found_cards[slug] = card

# Copy cards and images
target_images_dir = os.path.join(collections_dir, "shop-all", "images")
source_images_dir = os.path.join(collections_dir, "all", "images")

injected_count = 0
for slug in missing_in_shop_all:
    if slug not in found_cards:
        print(f"ERROR: Could not find card for '{slug}' in all/index.html!")
        continue
    
    card_soup = found_cards[slug]
    
    # Copy images referenced in the card
    img_tags = card_soup.find_all('img')
    for img in img_tags:
        srcs = []
        if img.get('src'):
            srcs.append(img['src'])
        if img.get('srcset'):
            srcset_parts = img['srcset'].split(',')
            for part in srcset_parts:
                part = part.strip()
                if part:
                    img_path = part.split(' ')[0]
                    srcs.append(img_path)
        
        for src in srcs:
            if 'images/' in src:
                img_name = src.split('images/')[-1].split('?')[0]
                src_img_file = os.path.join(source_images_dir, img_name)
                dst_img_file = os.path.join(target_images_dir, img_name)
                if os.path.exists(src_img_file):
                    shutil.copy2(src_img_file, dst_img_file)
                else:
                    # Let's also check other collections' images directories
                    # search across collections
                    copied = False
                    for c_dir in os.listdir(collections_dir):
                        src_c_img = os.path.join(collections_dir, c_dir, "images", img_name)
                        if os.path.exists(src_c_img):
                            shutil.copy2(src_c_img, dst_img_file)
                            copied = True
                            break
                    if not copied:
                        print(f"  Warning: Source image not found for {img_name}")

    # Append card to shop-all grid
    new_card = bs4.BeautifulSoup(str(card_soup), 'html.parser').find(class_='product-grid__item')
    shop_all_grid.append(new_card)
    injected_count += 1
    print(f"Injected '{slug}' card into shop-all/index.html")

if injected_count > 0:
    with open(shop_all_path, "w", encoding="utf-8") as f:
        f.write(str(shop_all_soup))
    print(f"Saved: {shop_all_path}")

print("Injections into shop-all complete!")
