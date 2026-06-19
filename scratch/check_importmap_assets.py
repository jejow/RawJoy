import json
import urllib.request
import re

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<script\s+type="importmap"\s*>(.*?)</script>', content, re.DOTALL)
if not match:
    print("No importmap found")
    exit(1)

importmap = json.loads(match.group(1))
imports = importmap.get("imports", {})

print(f"Checking {len(imports)} imports...")
for name, rel_path in imports.items():
    url = f"http://localhost:8000/{rel_path.lstrip('./')}"
    try:
        req = urllib.request.urlopen(url)
        status = req.status
        content_type = req.headers.get("Content-Type", "")
        # read first 50 bytes
        preview = req.read(50)
        print(f"OK: {name} -> {url} [status {status}] Content-Type: {content_type} | Preview: {preview}")
    except Exception as e:
        print(f"FAILED: {name} -> {url} | Error: {e}")
