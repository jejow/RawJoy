import os
import shutil

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
src_file = os.path.join(root_dir, 'js', 'variant-picker.js')

print("Source variant-picker.js exists:", os.path.exists(src_file))

count = 0
ignore_folders = ['.git', '.vscode', 'scratch', 'media', 'node_modules']

for dirpath, dirnames, filenames in os.walk(root_dir):
    # filter out ignored folders
    dirnames[:] = [d for d in dirnames if d not in ignore_folders]
    
    for filename in filenames:
        dest_file = os.path.join(dirpath, filename)
        if filename == 'variant-picker.js' and dest_file != src_file:
            shutil.copy2(src_file, dest_file)
            count += 1

print(f"Successfully copied variant-picker.js to {count} directories.")
