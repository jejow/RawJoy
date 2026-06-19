import os
import re

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
ignore_dirs = ['.git', '.vscode', 'scratch', 'media', 'node_modules']
broken_count = 0

for dirpath, dirnames, filenames in os.walk(workspace_root):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
    for fn in filenames:
        if fn.endswith('.html'):
            html_path = os.path.join(dirpath, fn)
            try:
                with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception as e:
                print(f"Failed to read {html_path}: {e}")
                continue
                
            # Check script tags
            scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', content, re.IGNORECASE)
            
            for src in scripts:
                if 'cart-interceptor' in src or 'db-bridge' in src or 'auth-ui' in src:
                    rel_dir = os.path.dirname(html_path)
                    target_path = os.path.normpath(os.path.join(rel_dir, src))
                    exists = os.path.exists(target_path)
                    if not exists:
                        print(f"BROKEN SCRIPT: In {os.path.relpath(html_path, workspace_root)}, src='{src}' -> does not exist!")
                        broken_count += 1

print(f"Diagnostic complete. Total broken imports found: {broken_count}")
