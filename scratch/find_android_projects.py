import os

search_paths = [
    r"C:\Users\junxi\source",
    r"C:\Users\junxi\OneDrive",
    r"C:\Users\junxi\Documents"
]

print("Searching for Android projects containing AndroidManifest.xml...")
found = []
for base_path in search_paths:
    if not os.path.exists(base_path):
        continue
    print(f"Scanning {base_path}...")
    for root, dirs, files in os.walk(base_path):
        # Skip directories to keep it fast
        for d in list(dirs):
            if d in ["node_modules", ".git", ".gradle", "build", "appMod", "AppData", "antigravity-ide"]:
                dirs.remove(d)
                
        if "AndroidManifest.xml" in files:
            manifest_path = os.path.join(root, "AndroidManifest.xml")
            if "RawJoy\\android-bridge" not in manifest_path:
                found.append(manifest_path)
                print(f"  Found: {manifest_path}")

print("Done! Found manifest files:")
for path in found:
    print(path)
