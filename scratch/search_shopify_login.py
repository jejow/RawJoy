import os
import bs4

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

found_links = []

for root, dirs, files in os.walk(workspace_root):
    if any(ignore in root for ignore in ['.git', '.vscode', 'scratch', 'node_modules']):
        continue
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    soup = bs4.BeautifulSoup(file.read(), "html.parser")
                for link in soup.find_all("a"):
                    href = link.get("href", "")
                    if "account/login" in href or "account" in href or "shopify" in href:
                        # Let's see if this is an external shopify link or standard shopify link
                        if "shopify.com" in href or "account/login" in href:
                            found_links.append((path, href, link.text.strip()))
            except Exception as e:
                print(f"Error reading {path}: {e}")

print(f"Found {len(found_links)} Shopify/account login links:")
for path, href, text in found_links[:30]:
    rel = os.path.relpath(path, workspace_root)
    print(f"File: {rel} | Text: {repr(text)} | Href: {repr(href)}")
