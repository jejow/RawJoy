from bs4 import BeautifulSoup

filepath = "index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
pp = soup.find_all('product-price')[26]
print(str(pp)[:1500])
# Let's print parent card structure
card = pp.find_parent('product-card')
if card:
    print("\nParent Card HTML:")
    print(str(card)[:1500])
