import os

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
db_bridge_paths = []
cart_interceptor_paths = []

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == 'db-bridge.js':
            db_bridge_paths.append(os.path.relpath(os.path.join(dirpath, filename), root_dir))
        elif filename == 'cart-interceptor.js':
            cart_interceptor_paths.append(os.path.relpath(os.path.join(dirpath, filename), root_dir))

print(f"Total db-bridge.js copies: {len(db_bridge_paths)}")
print("First 10 copies:")
for p in db_bridge_paths[:10]:
    print(" -", p)
    
print(f"\nTotal cart-interceptor.js copies: {len(cart_interceptor_paths)}")
print("First 10 copies:")
for p in cart_interceptor_paths[:10]:
    print(" -", p)
