import os

search_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\full download"
for root, dirs, files in os.walk(search_path):
    for f in files:
        if "suggest" in f or "search" in f:
            print(os.path.join(root, f))
