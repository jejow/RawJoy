filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js\cart-interceptor.js"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Check for eval, Function, or on:click references
for m in re.finditer(r'eval|Function|on:|on-click|click', content):
    start = m.start()
    line_no = content[:start].count('\n') + 1
    # print context
    print(f"Line {line_no}: {content[max(0, start-40):start+60].strip()}")
