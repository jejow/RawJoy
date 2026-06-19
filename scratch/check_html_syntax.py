with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

line = lines[2225]
idx = line.find("initData:")
if idx != -1:
    print(line[idx:idx + 3000])
