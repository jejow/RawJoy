import hashlib

def get_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

for folder in ['colostrum', 'colostrum-1', 'colostrum-2']:
    path = f"collections/{folder}/index.html"
    print(f"Path: {path} | Hash: {get_hash(path)}")
