import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\RawJoy"

missing_images = {}

img_tag_regex = re.compile(r'<img[^>]+>', re.IGNORECASE)
src_regex = re.compile(r'src="([^"]+)"', re.IGNORECASE)
srcset_regex = re.compile(r'srcset="([^"]+)"', re.IGNORECASE)

ignore_dirs = ['.git', '.vscode', 'scratch', 'node_modules', '__pycache__']

for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
    
    for filename in filenames:
        if filename.endswith(".html"):
            html_path = os.path.join(dirpath, filename)
            
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            img_tags = img_tag_regex.findall(content)
            for tag in img_tags:
                srcs = []
                m_src = src_regex.search(tag)
                if m_src:
                    srcs.append(m_src.group(1))
                m_srcset = srcset_regex.search(tag)
                if m_srcset:
                    srcset_parts = m_srcset.group(1).split(',')
                    for part in srcset_parts:
                        part = part.strip()
                        if part:
                            srcs.append(part.split(' ')[0])
                            
                for src in srcs:
                    if src.startswith('http://') or src.startswith('https://') or src.startswith('//'):
                        continue
                    if not src.strip() or src.startswith('${'):
                        continue
                        
                    clean_src = src.split('?')[0]
                    html_dir = os.path.dirname(html_path)
                    img_abs_path = os.path.normpath(os.path.join(html_dir, clean_src))
                    
                    if not os.path.exists(img_abs_path):
                        rel_html = os.path.relpath(html_path, root_dir)
                        if rel_html not in missing_images:
                            missing_images[rel_html] = set()
                        missing_images[rel_html].add((src, img_abs_path))

print("\nMissing images in destination directory:")
total = 0
for html, missing in sorted(missing_images.items()):
    print(f"\nIn {html}:")
    for src, abs_p in sorted(missing):
        print(f" - Missing: {src}")
        print(f"   Expected absolute path: {abs_p}")
        total += 1
print(f"\nTotal missing in destination: {total}")
