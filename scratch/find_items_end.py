import re

path = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\downloaded_site\pebble-rawjoy.myshopify.com\cart\index.html"
content = open(path, encoding="utf-8").read()

# Let's find '<div class="cart-page__items'
idx = content.find('class="cart-page__items')
if idx != -1:
    start = content.rfind('<div', 0, idx)
    print("Found cart-page__items starting at:", start)
    # Print the next 6000 characters
    print(content[start:start+6000])
else:
    print("cart-page__items not found")
