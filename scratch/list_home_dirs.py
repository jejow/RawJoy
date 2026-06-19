import os

home = r"C:\Users\junxi"
print(f"Listing directories in {home}:")
try:
    for name in os.listdir(home):
        full_path = os.path.join(home, name)
        if os.path.isdir(full_path):
            print(f"  {name}/")
except Exception as e:
    print(e)
