import os

print("Searching for folders containing 'rawjoy' (case-insensitive) on C: drive...")
found = []
skip_roots = ["$recycle.bin", "$sysreset", "windows", "program files", "program files (x86)", "programdata", "appdata"]

for root_dir in ["C:\\"]:
    try:
        for name in os.listdir(root_dir):
            if name.lower() in skip_roots:
                continue
            full_path = os.path.join(root_dir, name)
            if os.path.isdir(full_path):
                # Scan recursively
                for r, dirs, files in os.walk(full_path):
                    for d in list(dirs):
                        if d.lower() in ["node_modules", ".git", ".gradle", "build", "appdata", "antigravity-ide"]:
                            dirs.remove(d)
                        elif "rawjoy" in d.lower():
                            found_dir = os.path.join(r, d)
                            found.append(found_dir)
                            print(f"  Found: {found_dir}")
    except Exception as e:
        print(f"Error reading root: {e}")

print("Done! Found directories:")
for d in found:
    print(d)
