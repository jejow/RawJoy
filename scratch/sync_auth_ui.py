import os
import shutil

# Root paths
workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
laragon_root = r"c:\laragon\www\RawJoy"

src_auth_ui = os.path.join(workspace_root, 'js', 'auth-ui.js')
dest_laragon_auth_ui = os.path.join(laragon_root, 'js', 'auth-ui.js')

print(f"Source auth-ui.js exists: {os.path.exists(src_auth_ui)}")

# 1. Copy root auth-ui.js to Laragon root js folder
if os.path.exists(src_auth_ui):
    os.makedirs(os.path.dirname(dest_laragon_auth_ui), exist_ok=True)
    shutil.copy2(src_auth_ui, dest_laragon_auth_ui)
    print("Successfully copied auth-ui.js from Workspace to Laragon root.")
else:
    print("ERROR: Source auth-ui.js not found in workspace!")
    exit(1)

ignore_folders = ['.git', '.vscode', 'scratch', 'media', 'node_modules']

def sync_auth_ui_in_root(root):
    count = 0
    root_src = os.path.join(root, 'js', 'auth-ui.js')
    
    for dirpath, dirnames, filenames in os.walk(root):
        # filter out ignored folders
        dirnames[:] = [d for d in dirnames if d not in ignore_folders]
        
        for filename in filenames:
            dest_file = os.path.join(dirpath, filename)
            if filename == 'auth-ui.js' and dest_file != root_src:
                shutil.copy2(root_src, dest_file)
                count += 1
    return count

# 2. Sync all copies in Workspace
workspace_count = sync_auth_ui_in_root(workspace_root)
print(f"Synced {workspace_count} duplicate auth-ui.js files in Workspace.")

# 3. Sync all copies in Laragon
laragon_count = sync_auth_ui_in_root(laragon_root)
print(f"Synced {laragon_count} duplicate auth-ui.js files in Laragon.")
