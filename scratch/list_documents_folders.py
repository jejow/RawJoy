import os

doc_path = r"C:\Users\junxi\OneDrive\Documents"
print(f"Listing directories in {doc_path}:")
try:
    for name in os.listdir(doc_path):
        full_path = os.path.join(doc_path, name)
        if os.path.isdir(full_path):
            print(f"  {name}/")
except Exception as e:
    print(e)
