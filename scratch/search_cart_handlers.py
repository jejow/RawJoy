import os

js_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js"

for file in os.listdir(js_dir):
    if not file.endswith(".js"):
        continue
    file_path = os.path.join(js_dir, file)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    if "cart:add" in content or "CartAddEvent" in content:
        print(f"=== {file} ===")
        # print context around the match
        idx = 0
        while True:
            idx = content.find("cart:add", idx)
            if idx == -1:
                idx = content.find("CartAddEvent", idx)
                if idx == -1:
                    break
            start = max(0, idx - 100)
            end = min(len(content), idx + 200)
            print(f"  Match:\n... {content[start:end]} ...\n")
            idx += 10
