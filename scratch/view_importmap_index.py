with open(r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html", "r", encoding="utf-8") as f:
    content = f.read()
    
import re
match = re.search(r'<script\s+type="importmap"\s*>(.*?)</script>', content, re.DOTALL)
if match:
    print(match.group(1))
else:
    print("No importmap found in index.html")
