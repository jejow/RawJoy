import os
import shutil
import stat

# Root paths
workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
laragon_root = r"c:\laragon\www\RawJoy"

files_to_sync = [
    ('js/auth-ui.js', 'js/auth-ui.js'),
    ('css/db-ui.css', 'css/db-ui.css'),
    ('js/cart-interceptor.js', 'js/cart-interceptor.js'),
    ('js/db-bridge.js', 'js/db-bridge.js'),
    ('js/quick-add.js', 'js/quick-add.js'),
    ('js/variant-picker.js', 'js/variant-picker.js'),
    ('pages/checkout/index.html', 'pages/checkout/index.html')
]

# 1. Copy files between roots
for rel_src, rel_dest in files_to_sync:
    src_path = os.path.join(workspace_root, rel_src)
    dest_path = os.path.join(laragon_root, rel_dest)
    
    try:
        if os.path.exists(src_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            # Make destination writeable if it exists
            if os.path.exists(dest_path):
                os.chmod(dest_path, stat.S_IWRITE)
            shutil.copy2(src_path, dest_path)
            print(f"Copied root {rel_src} from Workspace to Laragon.")
        else:
            print(f"WARNING: Source {src_path} not found!")
    except Exception as e:
        print(f"Error copying root {rel_src}: {e}")

ignore_folders = ['.git', '.vscode', 'scratch', 'media', 'node_modules']

def sync_asset_globally(root, filename, src_rel_path):
    count = 0
    src_full = os.path.join(root, src_rel_path)
    
    for dirpath, dirnames, filenames in os.walk(root):
        # filter out ignored folders
        dirnames[:] = [d for d in dirnames if d not in ignore_folders]
        
        for fn in filenames:
            dest_file = os.path.join(dirpath, fn)
            # check if file name matches and it's not the source itself
            if fn == filename and dest_file != src_full:
                try:
                    # Clear read-only attributes if present
                    if os.path.exists(dest_file):
                        os.chmod(dest_file, stat.S_IWRITE)
                    shutil.copy2(src_full, dest_file)
                    count += 1
                except PermissionError:
                    # Fallback to copyfile which might bypass some WinError 32 locks
                    try:
                        shutil.copyfile(src_full, dest_file)
                        count += 1
                    except Exception as e:
                        print(f"Skipped (locked): {dest_file} due to permission error: {e}")
                except Exception as e:
                    print(f"Skipped {dest_file} due to error: {e}")
    return count

for fn_name, rel_path in [
    ('auth-ui.js', 'js/auth-ui.js'),
    ('db-ui.css', 'css/db-ui.css'),
    ('cart-interceptor.js', 'js/cart-interceptor.js'),
    ('db-bridge.js', 'js/db-bridge.js'),
    ('quick-add.js', 'js/quick-add.js'),
    ('variant-picker.js', 'js/variant-picker.js')
]:
    # Sync in Workspace
    ws_c = sync_asset_globally(workspace_root, fn_name, rel_path)
    print(f"Synced {ws_c} copies of {fn_name} in Workspace.")
    
    # Sync in Laragon
    lg_c = sync_asset_globally(laragon_root, fn_name, rel_path)
    print(f"Synced {lg_c} copies of {fn_name} in Laragon.")
