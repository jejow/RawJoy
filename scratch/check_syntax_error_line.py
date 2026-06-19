import os

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

def check_line(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    print(f"\n=== {os.path.relpath(filepath, root_dir)} ===")
    line_no = 2200
    if len(lines) >= line_no:
        print(f"Line {line_no}: {lines[line_no-1].strip()[:300]}")
        # print surrounding context
        for idx in range(2190, 2240):
            if idx < len(lines):
                print(f"  {idx+1}: {lines[idx].strip()[:200]}")
    else:
        print(f"File only has {len(lines)} lines")

check_line(os.path.join(root_dir, "index.html"))
