import os
import re

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

# Look for 'Bone Broth' or 'Treats' near 18 or 17
# e.g., "Bone Broth" followed by whitespace or tags and then "18" (or "17" for Treats)
p_bone_broth = re.compile(r'Bone\s+Broth.*?(18|17|12)', re.IGNORECASE | re.DOTALL)
p_treats = re.compile(r'Treats.*?(18|17|12)', re.IGNORECASE | re.DOTALL)

def check_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # We want to find any occurrences of "Bone Broth" followed by "18" within 100 characters
    # and "Treats" followed by "17" within 100 characters.
    found = False
    for match in re.finditer(r'Bone\s+Broth', content, re.IGNORECASE):
        start = match.start()
        chunk = content[start:start+150]
        if "18" in chunk:
            print(f"File {filepath} has 'Bone Broth' near '18':\n{repr(chunk)}\n")
            found = True
            
    for match in re.finditer(r'Treats', content, re.IGNORECASE):
        start = match.start()
        chunk = content[start:start+150]
        if "17" in chunk:
            print(f"File {filepath} has 'Treats' near '17':\n{repr(chunk)}\n")
            found = True
            
    return found

count = 0
for root, dirs, files in os.walk(workspace_root):
    for file in files:
        if file.endswith(".html"):
            if check_file(os.path.join(root, file)):
                count += 1

print(f"Scan complete. Found {count} files with old count indicators.")
