import os
import json
import re

products_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\products"
mapping = {}

for name in os.listdir(products_dir):
    subpath = os.path.join(products_dir, name)
    if os.path.isdir(subpath):
        html_path = os.path.join(subpath, "index.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Search for og:image
            match = re.search(r'property="og:image"\s+content="([^"]+)"', content)
            if not match:
                match = re.search(r'content="([^"]+)"\s+property="og:image"', content)
            if not match:
                match = re.search(r'property=\'og:image\'\s+content=\'([^\']+)\'', content)
            if not match:
                match = re.search(r'content=\'([^\']+)\'\s+property=\'og:image\'', content)
                
            if match:
                img_url = match.group(1)
                # If it's a relative path like images/BeefSpinachStew-361_14.jpg, resolve it relative to products/name
                # Usually it has images/xxxx_14.jpg. The base image name is without _14, e.g., BeefSpinachStew-361.jpg
                filename = img_url.split('/')[-1]
                # If it ends with _14.jpg, let's see if the base image exists in images/
                base_filename = filename
                if "_14.jpg" in filename:
                    base_filename = filename.replace("_14.jpg", ".jpg")
                elif "_14.png" in filename:
                    base_filename = filename.replace("_14.png", ".png")
                
                # Check if it exists in the main images folder or local images folder
                # Let's map it to products/name/images/filename or products/name/images/base_filename
                mapping[name] = f"products/{name}/images/{base_filename}"
            else:
                # Fallback to scanning images folder
                mapping[name] = None

print(json.dumps(mapping, indent=2))
