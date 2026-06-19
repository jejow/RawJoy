import os
import re

def fix_interceptor_paths():
    root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
    count = 0
    errors = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip git or vscode
        if ".git" in dirpath or ".vscode" in dirpath:
            continue
            
        for filename in filenames:
            if filename.endswith(".html"):
                filepath = os.path.join(dirpath, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    
                    # Calculate depth
                    rel_dir = os.path.relpath(dirpath, root_dir)
                    if rel_dir == ".":
                        prefix = ""
                    else:
                        parts = rel_dir.split(os.sep)
                        prefix = "../" * len(parts)
                    
                    # Replace <script src="js/cart-interceptor.js"></script>
                    # with <script src="[prefix]js/cart-interceptor.js"></script>
                    target_tag = '<script src="js/cart-interceptor.js"></script>'
                    correct_tag = f'<script src="{prefix}js/cart-interceptor.js"></script>'
                    
                    # Also handle variations (like single quotes or leading whitespace)
                    # We can use regex to find any <script src="js/cart-interceptor.js"></script>
                    # and replace its src with the correct prefix path.
                    pattern = r'<script\s+src="js/cart-interceptor\.js"\s*>\s*</script>'
                    
                    # But since the previous script injected exactly '<script src="js/cart-interceptor.js"></script>'
                    # a simple string replace is very safe and clean.
                    if target_tag in content:
                        new_content = content.replace(target_tag, correct_tag)
                        if new_content != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            count += 1
                            print(f"Fixed interceptor path in: {os.path.relpath(filepath, root_dir)} -> {correct_tag}")
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
                    errors += 1
                    
    print(f"Finished fixing interceptor paths in {count} HTML files ({errors} errors).")

if __name__ == "__main__":
    fix_interceptor_paths()
