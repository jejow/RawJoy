import os
import re

affected_files = []
good_files = []
missing_files = []

for root, dirs, files in os.walk('.'):
    # Skip .git, .vscode, node_modules etc.
    if any(p in root for p in ['.git', '.vscode', 'node_modules']):
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if 'id="captcha-bootstrap"' in content:
                # Find the script tag
                match = re.search(r'(<script id="captcha-bootstrap">.*?</script>)', content, re.DOTALL)
                if match:
                    script_content = match.group(1)
                    if 'shopify.loadfeatures' in script_content:
                        affected_files.append((filepath, len(script_content)))
                    else:
                        good_files.append((filepath, len(script_content)))
                else:
                    # It might be truncated and closed by a different script tag's closing tag or unclosed
                    # Let's search for the opening tag and see what follows
                    opening_idx = content.find('<script id="captcha-bootstrap">')
                    snippet = content[opening_idx:opening_idx+500]
                    affected_files.append((filepath, -1))
            else:
                missing_files.append(filepath)

print("AFFECTED FILES (broken captcha):", len(affected_files))
for f, l in affected_files:
    print(f" - {f} (length: {l})")

print("\nGOOD FILES (correct captcha):", len(good_files))
for f, l in good_files:
    print(f" - {f} (length: {l})")

print("\nMISSING CAPTCHA-BOOTSTRAP:", len(missing_files))
