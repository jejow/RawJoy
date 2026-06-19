import re
import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's search for links containing "login", "account", "register", or "signup"
links = re.findall(r'<a\s+[^>]*href=["\'][^"\']*(?:login|account|register|signup|myshopify)[^"\']*["\'][^>]*>.*?</\s*a\s*>', content, re.IGNORECASE | re.DOTALL)
print(f"Found {len(links)} matching links:")
for i, l in enumerate(links[:20]):
    print(f"[{i}]: {repr(l[:300])}")
    print("-" * 50)
