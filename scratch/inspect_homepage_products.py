import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find product-card components
cards = re.findall(r'<product-card[^>]*>.*?</product-card>', content, re.DOTALL)
print("Total product-card tags:", len(cards))

# Print the first 2 product cards details
for i in range(min(len(cards), 3)):
    print(f"\n--- Card {i} ---")
    print(cards[i][:600])
    print("...")
    print(cards[i][-200:])
