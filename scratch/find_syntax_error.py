import re

with open(r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Find all script blocks
scripts = re.findall(r'<script(.*?)>(.*?)</script>', content, re.DOTALL)
print(f"Found {len(scripts)} script blocks.")

for idx, (attrs, code) in enumerate(scripts):
    if len(code) > 0:
        # Check if code contains non-ascii or weird characters
        non_ascii = re.findall(r'[^\x00-\x7F]', code)
        if non_ascii:
            print(f"Script {idx} (attrs: {attrs.strip()}) contains non-ASCII characters: {set(non_ascii)}")
            # print surrounding snippet of the first non-ascii char
            pos = re.search(r'[^\x00-\x7F]', code).start()
            print(f"  Snippet: ... {code[max(0, pos-50):pos+50]} ...")
