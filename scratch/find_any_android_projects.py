import os

base_path = r"C:\Users\junxi"
print(f"Scanning {base_path} for MainActivity.java...")
found = []

# Top level directories to skip entirely
skip_top_dirs = [
    "appdata", ".antigravity", ".antigravity-ide", ".gemini", ".vscode", 
    ".gradle", ".android", "scikit_learn_data", ".cache", ".config", ".templateengine"
]

for name in os.listdir(base_path):
    if name.lower() in skip_top_dirs:
        continue
    full_path = os.path.join(base_path, name)
    if os.path.isdir(full_path):
        for root, dirs, files in os.walk(full_path):
            # Skip common heavy folders
            for d in list(dirs):
                if d.lower() in ["node_modules", ".git", ".gradle", "build", "bin", "obj", "appdata", "antigravity-ide"]:
                    dirs.remove(d)
            if "MainActivity.java" in files:
                java_path = os.path.join(root, "MainActivity.java")
                if "RawJoy\\android-bridge" not in java_path:
                    found.append(java_path)
                    print(f"  Found: {java_path}")

print("Done! Found files:")
for path in found:
    print(path)
