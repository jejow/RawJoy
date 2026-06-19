import os

def search_in_file(file_name, terms):
    file_path = os.path.join(r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js", file_name)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    print(f"\n=== {file_name} (length: {len(content)}) ===")
    # Print occurrences and 200 chars around them
    for term in terms:
        idx = 0
        while True:
            idx = content.find(term, idx)
            if idx == -1:
                break
            start = max(0, idx - 100)
            end = min(len(content), idx + 200)
            print(f"[{term}] at {idx}:\n... {content[start:end]} ...\n")
            idx += len(term)

search_in_file("cart-items.js", ["morph", "CartUpdateEvent", "sections"])
search_in_file("theme.js", ["morph", "CartUpdateEvent", "sections"])
