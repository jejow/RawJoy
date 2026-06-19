import os

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

def inspect_line(filepath, line_no):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    print(f"\n=== {os.path.relpath(filepath, root_dir)} ===")
    if len(lines) >= line_no:
        line = lines[line_no-1]
        print(f"Line {line_no} length: {len(line)}")
        print(f"Snippet: {line[:500]}")
        # Print around char 1214 if long enough
        if len(line) > 1200:
            print(f"Around 1214: ... {line[1150:1280]} ...")
    else:
        print(f"File only has {len(lines)} lines")

inspect_line(os.path.join(root_dir, "products", "venison-peas-recipe", "index.html"), 2178)
inspect_line(os.path.join(root_dir, "index.html"), 2174)
