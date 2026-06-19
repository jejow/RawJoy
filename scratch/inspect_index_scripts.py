import re

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find all script tags with their start line, end line, and attributes
matches = re.finditer(r'<script([^>]*)>(.*?)</script>', content, re.DOTALL)
for m in matches:
    attrs = m.group(1)
    code = m.group(2)
    start_pos = m.start()
    # Find line number of start_pos
    line_no = content[:start_pos].count('\n') + 1
    
    # Check if this script is executed as JS
    is_js = True
    if 'type=' in attrs:
        # Check type
        type_match = re.search(r'type=["\'](.*?)["\']', attrs)
        if type_match:
            t = type_match.group(1)
            if 'json' in t or 'importmap' in t:
                is_js = False
    
    if is_js:
        print(f"JS Script at line {line_no}: attributes={attrs[:100]} | Code length={len(code)}")
        # Check if the code has syntax errors or contains '<' (which might indicate HTML leaked in)
        # Note: sometimes '<' is used for comparison (e.g. i < len), but usually not '<a' or '<span'
        if '<' in code and not re.search(r'<\s*[a-zA-Z/]', code):
            # Probably a comparison operator
            pass
        elif re.search(r'<\s*[a-zA-Z/]', code):
            print(f"  WARNING: Contains HTML-like tag inside JS script: {code[:300]}")
