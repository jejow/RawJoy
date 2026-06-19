import json
import os
import urllib.request
import re

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(root_dir, "index.html")
js_dir = os.path.join(root_dir, "js")

if not os.path.exists(js_dir):
    os.makedirs(js_dir)

# Read index.html to extract the importmap JSON
with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

importmap_match = re.search(r'<script\s+type="importmap"\s*>\s*({.*?})\s*</script>', content, re.DOTALL)
if not importmap_match:
    print("No importmap found in index.html")
    exit(1)

importmap_json = json.loads(importmap_match.group(1))
imports = importmap_json.get("imports", {})

print(f"Found {len(imports)} imports in importmap.")

downloaded = 0
skipped = 0

for key, url in imports.items():
    if url.startswith("//") or url.startswith("http"):
        # Normalize URL to http
        full_url = url if url.startswith("http") else "http:" + url
        
        # Get filename
        # e.g. //pebble-rawjoy.myshopify.com/cdn/shop/t/2/assets/component.js?v=123
        filename = url.split('/')[-1].split('?')[0]
        
        dest_path = os.path.join(js_dir, filename)
        
        if os.path.exists(dest_path):
            print(f"Local file already exists: js/{filename} (skipped)")
            skipped += 1
            continue
            
        try:
            print(f"Downloading {key} from {full_url} to js/{filename}...")
            urllib.request.urlretrieve(full_url, dest_path)
            print(f"Downloaded: js/{filename} ({os.path.getsize(dest_path)} bytes)")
            downloaded += 1
        except Exception as e:
            print(f"Error downloading {key}: {e}")

print(f"\nDone! Downloaded {downloaded} new files, skipped {skipped} existing files.")
