import os

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
interceptor_path = os.path.join(workspace_root, "js", "cart-interceptor.js")

with open(interceptor_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

lines = content.splitlines()
search_queries = ["renderCartDrawer", "/cart/add", "updateCartDrawer", "redraw", "cart-drawer", "DB.cart.add"]

print("Searching cart interceptor for cart drawer render updates:")
for query in search_queries:
    print(f"\nQuery: '{query}'")
    for idx, line in enumerate(lines):
        if query in line:
            print(f"  Line {idx+1}: {line.strip()}")
