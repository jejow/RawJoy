import os
import shutil

def propagate_updated_files():
    # Get the project root directory dynamically (one level above this script's directory)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Files to propagate
    files_to_copy = [
        ("js/cart-interceptor.js", "js/cart-interceptor.js"),
        ("js/db-bridge.js", "js/db-bridge.js"),
        ("js/auth-ui.js", "js/auth-ui.js"),
        ("js/section-renderer.js", "js/section-renderer.js"),
        ("js/utilities.js", "js/utilities.js"),
        ("js/quick-add.js", "js/quick-add.js")
    ]
    
    prop_count = 0
    
    # Traverse all directories in the project
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # We look for folders named 'js' that are not the root 'js' folder
        if os.path.basename(dirpath) == 'js' and os.path.abspath(dirpath) != os.path.abspath(os.path.join(root_dir, 'js')):
            # Check if this js folder is inside a product or page subdirectory
            # (we want to propagate to folders like RawJoy/products/chicken-bone-treat/js/)
            for src_rel, dest_rel in files_to_copy:
                src_path = os.path.join(root_dir, src_rel)
                dest_file_name = os.path.basename(dest_rel)
                dest_path = os.path.join(dirpath, dest_file_name)
                
                # Check if the destination file exists before overwriting, or just overwrite it if it's supposed to be there
                # Since we want to make sure it's fully propagated, we copy it.
                try:
                    shutil.copy2(src_path, dest_path)
                    prop_count += 1
                except Exception as e:
                    print(f"Error copying to {dest_path}: {e}")
                    
    print(f"Successfully propagated {prop_count} files across subdirectories.")

if __name__ == "__main__":
    propagate_updated_files()
