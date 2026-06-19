import difflib

path1 = "collections/colostrum/index.html"
path2 = "collections/colostrum-1/index.html"

with open(path1, 'r', encoding='utf-8') as f:
    lines1 = f.readlines()
with open(path2, 'r', encoding='utf-8') as f:
    lines2 = f.readlines()

diff = difflib.unified_diff(lines1, lines2, fromfile=path1, tofile=path2, n=3)
print("Differences:")
for line in list(diff)[:30]:
    print(line.strip())
