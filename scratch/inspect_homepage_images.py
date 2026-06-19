import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's find some product cards or img tags that are products
img_tags = re.findall(r'<img[^>]*>', content)
print("Total img tags:", len(img_tags))

# Print some images containing "products" or specific names
for img in img_tags:
    if 'Beef' in img or 'Salmon' in img or 'Chicken' in img or 'doggy' in img or 'cat' in img:
        print(img)
