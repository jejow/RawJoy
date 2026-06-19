import os
import re
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

missing_images = {} # html_file_path -> list of missing image urls

# Find all HTML files in RawJoy (excluding scratch and .git)
ignore_dirs = ['.git', '.vscode', 'scratch', 'node_modules', '__pycache__']

print("Scanning all HTML files for missing images...")
for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
    
    for filename in filenames:
        if filename.endswith(".html"):
            html_path = os.path.join(dirpath, filename)
            
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            soup = bs4.BeautifulSoup(content, 'html.parser')
            imgs = soup.find_all('img')
            
            for img in imgs:
                srcs = []
                if img.get('src'):
                    srcs.append(img['src'])
                if img.get('srcset'):
                    srcset_parts = img['srcset'].split(',')
                    for part in srcset_parts:
                        part = part.strip()
                        if part:
                            srcs.append(part.split(' ')[0])
                            
                for src in srcs:
                    # Resolve relative path
                    # Ignore external urls (http, https, //)
                    if src.startswith('http://') or src.startswith('https://') or src.startswith('//'):
                        continue
                    if not src.strip():
                        continue
                        
                    # Remove query parameters from image path
                    clean_src = src.split('?')[0]
                    
                    # Resolve image path relative to HTML file directory
                    html_dir = os.path.dirname(html_path)
                    img_abs_path = os.path.normpath(os.path.join(html_dir, clean_src))
                    
                    if not os.path.exists(img_abs_path):
                        rel_html = os.path.relpath(html_path, root_dir)
                        if rel_html not in missing_images:
                            missing_images[rel_html] = set()
                        missing_images[rel_html].add((src, img_abs_path))

print("\nScan complete! Results:")
total_issues = 0
for html, missing in sorted(missing_images.items()):
    # Skip checking index.html if we want, or list all
    print(f"\nIn {html}:")
    for src, abs_p in sorted(missing):
        print(f" - Missing: {src}")
        print(f"   Expected path: {os.path.relpath(abs_p, root_dir)}")
        total_issues += 1

print(f"\nTotal missing image references found: {total_issues}")
