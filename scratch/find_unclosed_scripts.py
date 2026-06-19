filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Find all <script and </script> positions and print any mismatch
opens = [m.start() for m in re.finditer(r'<script', content, re.IGNORECASE)]
closes = [m.start() for m in re.finditer(r'</script>', content, re.IGNORECASE)]

print(f"Total opens: {len(opens)}, Total closes: {len(closes)}")

# Let's trace them in order
all_tags = []
for o in opens:
    all_tags.append((o, 'open'))
for c in closes:
    all_tags.append((c, 'close'))
all_tags.sort()

stack = []
for pos, tag_type in all_tags:
    # Get line number
    line_no = content[:pos].count('\n') + 1
    if tag_type == 'open':
        stack.append(line_no)
    else:
        if len(stack) == 0:
            print(f"ERROR: Close tag at line {line_no} without an open tag!")
        else:
            stack.pop()

if stack:
    print(f"ERROR: Unclosed script tags opened at lines: {stack}")
else:
    print("All script tags are properly matched!")
