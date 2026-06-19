import os
import filecmp

dir1 = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
dir2 = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\RawJoy"

def compare_dirs(d1, d2):
    dcmp = filecmp.dircmp(d1, d2)
    
    # Files only in workspace (newly added files/folders)
    if dcmp.left_only:
        print(f"Only in Workspace ({d1}): {dcmp.left_only}")
    
    # Files only in Android copy
    if dcmp.right_only:
        print(f"Only in Android copy ({d2}): {dcmp.right_only}")
        
    # Files that differ
    if dcmp.diff_files:
        print(f"Different files: {dcmp.diff_files} under {d1}")
        
    for sub in dcmp.common_dirs:
        compare_dirs(os.path.join(d1, sub), os.path.join(d2, sub))

compare_dirs(dir1, dir2)
