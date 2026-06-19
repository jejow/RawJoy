import os
import filecmp

dir_workspace = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
dir_android = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\RawJoy"

def compare_dirs(w_dir, a_dir):
    missing_in_android = []
    mismatched_files = []
    
    for root, dirs, files in os.walk(w_dir):
        # Skip .git, .vscode, .gradle, and android-bridge folders
        if any(p in root for p in [".git", ".vscode", ".gradle", "android-bridge", "scratch"]):
            continue
            
        rel_path = os.path.relpath(root, w_dir)
        target_dir = a_dir if rel_path == "." else os.path.join(a_dir, rel_path)
        
        if not os.path.exists(target_dir):
            missing_in_android.append(os.path.join("RawJoy", rel_path) + " (directory)")
            continue
            
        for f in files:
            w_file = os.path.join(root, f)
            a_file = os.path.join(target_dir, f)
            
            if not os.path.exists(a_file):
                missing_in_android.append(os.path.join(rel_path, f))
            else:
                try:
                    if not filecmp.cmp(w_file, a_file, shallow=False):
                        mismatched_files.append(os.path.join(rel_path, f))
                except Exception as e:
                    mismatched_files.append(os.path.join(rel_path, f) + f" (error: {e})")
                    
    return missing_in_android, mismatched_files

missing, mismatched = compare_dirs(dir_workspace, dir_android)

print("--- MISSING IN ANDROID RAWJOY ---")
for m in sorted(missing):
    print(m)
    
print("\n--- MISMATCHED FILES ---")
for m in sorted(mismatched):
    print(m)
