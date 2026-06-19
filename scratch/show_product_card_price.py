filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("products/cat-calming-formula")
if idx != -1:
    card_html = content[idx:idx+8000]
    price_idx = card_html.find("product-price")
    if price_idx != -1:
        print("Found product-price:")
        print(card_html[price_idx:price_idx+1500])
    else:
        print("product-price tag not found within 8000 chars, showing card_html:")
        print(card_html[:1500])
else:
    print("Not found")
