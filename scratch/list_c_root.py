import os

root = r"C:\\"
print(f"Listing directories in {root}:")
try:
    for name in os.listdir(root):
        full_path = os.path.join(root, name)
        if os.path.isdir(full_path):
            print(f"  {name}/")
except Exception as e:
    print(e)
