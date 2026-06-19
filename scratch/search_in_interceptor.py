import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
interceptor_path = os.path.join(workspace_root, "js", "cart-interceptor.js")

with open(interceptor_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

search_queries = ["addRecommendedToCart", "resolveUrl", "showDialog", "DOMContentLoaded", "Complete the look", "recommended"]

print(f"Searching in cart-interceptor.js ({len(lines)} lines):")
for query in search_queries:
    print(f"\nQuery: '{query}'")
    found = False
    for idx, line in enumerate(lines):
        if query.lower() in line.lower():
            print(f"  Line {idx+1}: {line.strip()}")
            found = True
    if not found:
        print("  Not found.")
