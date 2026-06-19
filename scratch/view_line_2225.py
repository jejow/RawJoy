with open("products/venison-peas-recipe/index.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

print(lines[2225]) # Line 2226 (0-indexed is 2225)
