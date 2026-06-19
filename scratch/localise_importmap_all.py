import os
import json
import re
import shutil

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
js_src_dir = os.path.join(root_dir, "js")

def copy_all_js_to_subdirs():
    print("Propagating all JS files from root js/ to nested js/ folders...")
    # Get all files in root js/
    js_files = [f for f in os.listdir(js_src_dir) if os.path.isfile(os.path.join(js_src_dir, f))]
    
    dir_count = 0
    file_copy_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # We look for folders named 'js' that are not the root 'js' folder
        if os.path.basename(dirpath) == 'js' and os.path.abspath(dirpath) != os.path.abspath(js_src_dir):
            dir_count += 1
            for filename in js_files:
                src_path = os.path.join(js_src_dir, filename)
                dest_path = os.path.join(dirpath, filename)
                try:
                    shutil.copy2(src_path, dest_path)
                    file_copy_count += 1
                except Exception as e:
                    print(f"Error copying {filename} to {dirpath}: {e}")
                    
    print(f"Successfully copied files to {dir_count} subdirectories (total {file_copy_count} file copies).")

def localise_html_importmaps():
    print("\nLocalising import maps in all HTML files with './js/' prefix...")
    html_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if ".git" in dirpath or ".vscode" in dirpath:
            continue
            
        for filename in filenames:
            if filename.endswith(".html"):
                filepath = os.path.join(dirpath, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    
                    # Find the importmap script block
                    importmap_match = re.search(r'(<script\s+type="importmap"\s*>)(.*?)(</script>)', content, re.DOTALL)
                    if not importmap_match:
                        continue
                        
                    start_tag, json_text, end_tag = importmap_match.groups()
                    
                    try:
                        importmap_json = json.loads(json_text)
                    except Exception as e:
                        print(f"Error parsing JSON in {filepath}: {e}")
                        continue
                        
                    imports = importmap_json.get("imports", {})
                    modified = False
                    
                    for key, url in list(imports.items()):
                        # Match CDN URLs or previously localized "js/..." bare paths
                        if "pebble-rawjoy.myshopify.com/cdn" in url or url.startswith("//") or url.startswith("http"):
                            base_filename = url.split('/')[-1].split('?')[0]
                            local_path = f"./js/{base_filename}"
                            if imports[key] != local_path:
                                imports[key] = local_path
                                modified = True
                        elif url.startswith("js/"):
                            local_path = f"./{url}"
                            if imports[key] != local_path:
                                imports[key] = local_path
                                modified = True
                                
                    if modified:
                        importmap_json["imports"] = imports
                        new_json_text = "\n" + json.dumps(importmap_json, indent=2) + "\n"
                        new_block = start_tag + new_json_text + end_tag
                        
                        new_content = content[:importmap_match.start()] + new_block + content[importmap_match.end():]
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                            
                        html_count += 1
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
                    
    print(f"Finished localising import maps in {html_count} HTML files.")

if __name__ == "__main__":
    copy_all_js_to_subdirs()
    localise_html_importmaps()
