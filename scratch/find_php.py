import os

laragon_php_dir = r"C:\laragon\bin\php"
if os.path.exists(laragon_php_dir):
    for root, dirs, files in os.walk(laragon_php_dir):
        if "php.exe" in files:
            print(os.path.join(root, "php.exe"))
            break
else:
    print("Laragon PHP directory not found.")
