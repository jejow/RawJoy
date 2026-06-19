import os
import re

def fix_preloads(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'preloads.js':
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace scripts array
                    new_content = re.sub(
                        r'var\s+scripts\s*=\s*\[[^\]]*\];',
                        'var scripts = [];',
                        content
                    )
                    
                    # Replace styles array
                    new_content = re.sub(
                        r'var\s+styles\s*=\s*\[[^\]]*\];',
                        'var styles = [];',
                        new_content
                    )
                    
                    # Replace preconnectOrigins array
                    new_content = re.sub(
                        r'var\s+preconnectOrigins\s*=\s*\[[^\]]*\];',
                        'var preconnectOrigins = [];',
                        new_content
                    )
                    
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed: {path}")
                        count += 1
                except Exception as e:
                    print(f"Error processing {path}: {e}")
    print(f"Total files fixed: {count}")

if __name__ == '__main__':
    project_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
    fix_preloads(project_dir)
