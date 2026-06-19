import re

path = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\downloaded_site\pebble-rawjoy.myshopify.com\cart\index.html"
content = open(path, encoding="utf-8").read()

# Let's find the cart-page div and everything inside it
# We can find where '<div\nclass="cart-page' starts and trace its content
start_idx = content.find('class="cart-page')
if start_idx != -1:
    # Go back to the '<div' tag
    start_tag_idx = content.rfind('<div', 0, start_idx)
    # Print the next 15000 characters
    print("Found cart-page container starting at:", start_tag_idx)
    # Let's extract child elements
    segment = content[start_tag_idx:start_tag_idx+20000]
    print(segment[:1500])
    print("...\n\n...")
    print(segment[-1500:])
else:
    print("cart-page class not found!")
