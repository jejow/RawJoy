import os

js_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\js"

def search_terms(file_name, terms):
    file_path = os.path.join(js_dir, file_name)
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    print(f"\n=== {file_name} ===")
    for term in terms:
        start_idx = 0
        while True:
            idx = content.find(term, start_idx)
            if idx == -1:
                break
            start = max(0, idx - 100)
            end = min(len(content), idx + 200)
            print(f"[{term}] at {idx}:\n... {content[start:end]} ...\n")
            start_idx = idx + len(term)

search_terms("theme.js", ["CartAddEvent", "CartUpdateEvent", "cart:add", "cart:update"])
search_terms("events.js", ["CartAddEvent", "CartUpdateEvent", "cart:add", "cart:update"])
